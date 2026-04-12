#!/usr/bin/env python3
"""Main renderer for the Radio Scale Peppy display.

Release 1.8.0 keeps the proven runtime contract intact and focuses on a safer
visual extension layer:
- theme.json driven fonts, colors and layout
- dimmed station logo rendering
- configurable station label offsets
- configurable VU meter drawing scaffold

The renderer intentionally reads only JSON state/settings files. Volumio control
logic remains in the plugin's index.js so that UI extensions do not destabilise
playback handling.

Release 1.10.2 keeps the resident renderer path but hardens it for
shared-overlay appliance use. Hidden standby becomes true deep idle with no
draw loop, visible mode is capped to a Pi-friendly frame rate, and the
renderer honours `/tmp/mediastreamer_active_overlay.json` so other overlays
(such as fun_linea) can force Scale FM into deep idle without changing any
existing public call methods or service paths.
"""

from __future__ import annotations

import io
import json
import math
import os
import random
import signal
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

import pygame

from layered_theme import LayeredTheme
from theme_config import ThemeConfig

PLUGIN_DIR = Path(os.environ.get('RADIO_SCALE_PLUGIN_DIR', '/data/plugins/user_interface/radio_scale_peppy'))
RUNTIME_DIR = PLUGIN_DIR / 'runtime'
SETTINGS_PATH = RUNTIME_DIR / 'settings.json'
STATE_PATH = RUNTIME_DIR / 'state.json'
READY_PATH = RUNTIME_DIR / 'renderer_ready.json'
PID_PATH = RUNTIME_DIR / 'renderer.pid'
OWNER_PATH = Path('/tmp/mediastreamer_active_overlay.json')
THEMES_DIR = PLUGIN_DIR / 'renderer' / 'themes'

RUNNING = True


def handle_signal(signum, frame):
    """Allow SIGTERM / SIGINT to stop the renderer loop cleanly."""
    global RUNNING
    RUNNING = False


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


DEFAULT_SETTINGS = {
    'fullscreen': True,
    'screen_width': 1920,
    'screen_height': 550,
    'fps': 24,
    'visible_fps_cap': 24,
    'hidden_standby_fps': 12,
    'hidden_state_reload_ms': 2000,
    'deep_idle_reload_ms': 5000,
    'hidden_standby_sleep_ms': 250,
    'deep_idle_sleep_ms': 1000,
    'info_panel_width': 430,
    'fallback_frequency': 98.3,
    'scale_start': 87.5,
    'scale_end': 108.0,
    'show_clock': True,
    'show_technical': True,
    'shared_overlay_owner_path': str(OWNER_PATH),
    'stations': [],
    'tuning_step_mhz': 0.02,
    'snap_window_mhz': 0.045,
    'release_window_mhz': 0.09,
    'noise_window_mhz': 0.32,
    'auto_play_on_lock': True,
    'pause_on_unlock': False,
    'magnetic_lock_enabled': True,
    'magnetic_radius_mhz': 0.04,
    'magnetic_strength': 0.02,
    'scale_vertical_offset': 78,
    'station_label_levels': 3,
    'use_layer_theme': True,
    'theme_name': 'braun_hd',
    'pointer_visual_follow_gain': 0.38,
    'pointer_visual_locked_gain': 0.48,
    'pointer_jitter_enabled': False,
    'lock_visual_snap_enabled': False,
    'pointer_idle_lock_ms': 220,
    'pointer_startup_settle_ms': 900,
    'pointer_settle_epsilon_mhz': 0.004,
    'pointer_visual_deadband_mhz': 0.006,
    'pointer_pixel_snap_deadband_px': 1.0,
}

DEFAULT_STATE = {
    'status': 'stop',
    'source_type': 'idle',
    'ui_mode': 'normal',
    'service': '',
    'title': '',
    'artist': '',
    'album': '',
    'volume': 0,
    'mute': False,
    'samplerate': '',
    'bitdepth': '',
    'track_type': '',
    'uri': '',
    'albumart': '',
    'active_frequency': 98.3,
    'matched_station': None,
    'tuning_position': 98.3,
    'tuning_locked': False,
    'tuning_mode': 'auto',
    'tuning_noise': 1.0,
    'tuning_station': None,
    'tuning_nearest_station': None,
    'tuning_distance': None,
    'vu_left': 0.0,
    'vu_right': 0.0,
}


def load_json(path: Path, fallback):
    """Read one JSON file with a safe fallback on any failure."""
    try:
        with path.open('r', encoding='utf-8') as handle:
            return json.load(handle)
    except Exception:
        return fallback


class RadioScaleRenderer:
    """Drive the full-screen retro radio UI from runtime JSON files."""

    def __init__(self):
        """Initialise runtime caches, theme state and pygame-facing members."""
        self.settings = DEFAULT_SETTINGS.copy()
        self.state = DEFAULT_STATE.copy()
        self.settings_mtime = None
        self.state_mtime = None
        self.screen = None
        self.clock = None
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.size = (0, 0)
        self.last_pointer_freq = self.settings['fallback_frequency']
        self.last_pointer_x = None
        self.pointer_bootstrap_done = False
        self.random = random.Random()
        self.layered_theme: Optional[LayeredTheme] = None
        self.theme_config: Optional[ThemeConfig] = None
        self.albumart_cache: Dict[str, Dict[str, Any]] = {}
        self.albumart_cache_ttl = 20.0
        self.first_frame_presented = False
        self.ready_marker_written = False
        self.resident_mode = str(os.environ.get('RADIO_SCALE_RESIDENT', '0')).strip().lower() in ('1', 'true', 'yes', 'on')
        self.window_visible = False
        self.last_ui_mode = 'normal'
        self.overlay_owner = 'none'
        self.overlay_owner_mtime = None
        self.hidden_reload_due_at = 0.0

    def reload_settings(self, force=False):
        """Reload runtime settings when the JSON file changes on disk."""
        try:
            mtime = SETTINGS_PATH.stat().st_mtime
        except FileNotFoundError:
            return
        if force or mtime != self.settings_mtime:
            self.settings = DEFAULT_SETTINGS.copy()
            self.settings.update(load_json(SETTINGS_PATH, {}))
            self.settings_mtime = mtime
            self.init_display(force=True)

    def reload_state(self, force=False):
        """Reload runtime state when the JSON file changes on disk."""
        try:
            mtime = STATE_PATH.stat().st_mtime
        except FileNotFoundError:
            return
        if force or mtime != self.state_mtime:
            self.state = DEFAULT_STATE.copy()
            self.state.update(load_json(STATE_PATH, {}))
            self.state_mtime = mtime


    def reload_overlay_owner(self, force=False):
        """Reload the shared overlay owner marker with a cheap mtime gate.

        The marker lets multiple resident overlays coordinate ownership of the
        visible appliance surface without changing any legacy Volumio call
        methods. Scale FM renders actively only while owner=scale_fm.
        """
        owner_path = Path(str(self.settings.get('shared_overlay_owner_path') or OWNER_PATH))
        try:
            mtime = owner_path.stat().st_mtime
        except FileNotFoundError:
            self.overlay_owner = 'none'
            self.overlay_owner_mtime = None
            return
        if force or mtime != self.overlay_owner_mtime:
            payload = load_json(owner_path, {'owner': 'none'})
            self.overlay_owner = str(payload.get('owner') or 'none').strip().lower() or 'none'
            self.overlay_owner_mtime = mtime

    def determine_power_mode(self) -> str:
        """Return active / idle / deep_idle for the current owner and ui state."""
        if not self.resident_mode:
            return 'active'
        if self.overlay_owner == 'fun_linea':
            return 'deep_idle'
        if str(self.state.get('ui_mode') or 'normal').lower() == 'scale' and self.overlay_owner == 'scale_fm':
            return 'active'
        return 'idle'

    def clear_ready_marker(self):
        """Remove any stale renderer-ready marker before a fresh overlay open."""
        try:
            if READY_PATH.exists():
                READY_PATH.unlink()
        except Exception:
            pass

    def write_ready_marker(self, stage: str = 'ready'):
        """Write one small JSON marker so Node.js knows the first frame is visible."""
        try:
            READY_PATH.write_text(json.dumps({'ready': True, 'stage': stage, 'ts': time.time()}), encoding='utf-8')
            self.ready_marker_written = True
        except Exception:
            pass

    def write_pid_marker(self):
        """Persist the resident renderer PID so Node.js can detect service-backed instances."""
        try:
            PID_PATH.write_text(str(os.getpid()), encoding='utf-8')
        except Exception:
            pass

    def clear_pid_marker(self):
        """Remove the PID marker on clean shutdown."""
        try:
            if PID_PATH.exists():
                PID_PATH.unlink()
        except Exception:
            pass

    def present_startup_splash(self):
        """Present a dark first frame immediately to hide the white X11 gap."""
        if self.screen is None:
            return
        width, height = self.size
        self.screen.fill((10, 10, 12))
        pygame.draw.rect(self.screen, (16, 16, 20), (0, 0, width, height))
        pygame.draw.line(self.screen, (88, 71, 38), (0, 42), (width, 42), 2)
        splash_font = pygame.font.SysFont('DejaVu Sans', max(18, int(height * 0.05)))
        meta_font = pygame.font.SysFont('DejaVu Sans', max(12, int(height * 0.03)))
        title = splash_font.render('SCALE FM', True, (214, 188, 134))
        meta = meta_font.render('overlay start …', True, (186, 176, 154))
        self.screen.blit(title, (26, max(12, int(height * 0.08))))
        self.screen.blit(meta, (28, max(48, int(height * 0.17))))
        pygame.display.flip()

    def build_display_flags(self, visible: bool) -> int:
        """Build pygame display flags for visible and hidden standby modes."""
        flags = pygame.NOFRAME
        fullscreen = bool(self.settings.get('fullscreen', True))
        if visible:
            flags |= pygame.DOUBLEBUF
        if visible and fullscreen:
            flags |= pygame.FULLSCREEN
        if not visible:
            flags |= getattr(pygame, 'HIDDEN', 0)
        return flags

    def init_display(self, force=False, visible: Optional[bool] = None):
        """Create or recreate the pygame screen when geometry or visibility changes."""
        width = int(self.settings.get('screen_width', 1920))
        height = int(self.settings.get('screen_height', 550))
        requested_visible = self.window_visible if visible is None else bool(visible)
        target_size = (width, height)

        if not force and self.screen is not None and target_size == self.size and requested_visible == self.window_visible:
            return

        flags = self.build_display_flags(requested_visible)
        self.screen = pygame.display.set_mode(target_size, flags)
        pygame.display.set_caption('Scale FM Overlay')
        self.clock = self.clock or pygame.time.Clock()
        self.size = target_size
        self.window_visible = requested_visible
        self.first_frame_presented = False
        self.ready_marker_written = False
        self.clear_ready_marker()
        self.init_theme()
        self.init_fonts()
        self.pointer_bootstrap_done = False
        if self.window_visible and not self.resident_mode:
            # Non-resident cold starts still paint a dark splash immediately.
            # In resident mode we stay hidden in standby and reveal only the real
            # first content frame when ui_mode switches to `scale`.
            self.present_startup_splash()

    def sync_window_visibility(self):
        """Keep the SDL window visible only while the overlay is in scale mode.

        1.10.2 forces a fresh state reload *before* the window becomes visible
        and resets pointer bootstrap on every show transition. This prevents the
        first post-boot open from briefly drawing the pointer at an old fallback
        frequency before the latest locked station state is applied.
        """
        desired_visible = True
        if self.resident_mode:
            desired_visible = (
                str(self.state.get('ui_mode') or 'normal').lower() == 'scale'
                and str(self.overlay_owner or 'none').lower() == 'scale_fm'
            )

        if self.screen is None:
            self.init_display(force=True, visible=desired_visible)
            self.last_ui_mode = str(self.state.get('ui_mode') or 'normal').lower()
            return

        if desired_visible == self.window_visible:
            self.last_ui_mode = str(self.state.get('ui_mode') or 'normal').lower()
            return

        # Always reload the state one more time right before the visibility flip.
        self.reload_state(force=True)
        self.window_visible = desired_visible
        self.first_frame_presented = False
        self.ready_marker_written = False
        self.clear_ready_marker()
        if desired_visible:
            self.pointer_bootstrap_done = False
            preferred_freq = self.state.get('tuning_last_locked_freq')
            if preferred_freq is None:
                station = self.state.get('tuning_station') or self.state.get('matched_station') or {}
                preferred_freq = station.get('freq') if isinstance(station, dict) else None
            try:
                if preferred_freq is not None:
                    self.last_pointer_freq = float(preferred_freq)
                    self.last_pointer_x = None
            except Exception:
                pass
        flags = self.build_display_flags(desired_visible)
        self.screen = pygame.display.set_mode(self.size, flags)
        pygame.display.set_caption('Scale FM Overlay')
        self.last_ui_mode = str(self.state.get('ui_mode') or 'normal').lower()

    def init_theme(self):
        """Load theme.json and the optional PNG layer stack for the active theme."""
        self.layered_theme = None
        self.theme_config = None
        if not bool(self.settings.get('use_layer_theme', True)):
            return

        theme_name = str(self.settings.get('theme_name', 'braun_hd') or 'braun_hd').strip()
        theme_root = THEMES_DIR / theme_name
        try:
            self.theme_config = ThemeConfig(theme_root)
            theme = LayeredTheme(theme_root, self.size, self.theme_config)
            if theme.available:
                self.layered_theme = theme
        except Exception:
            self.theme_config = ThemeConfig(theme_root)
            self.layered_theme = None

    def init_fonts(self):
        """Build all renderer fonts from theme-configured families or font files."""
        height = self.size[1]
        base = max(14, int(height * 0.035))
        size_adjust = self.theme_value('fonts.size_adjust', {}) or {}
        self.fonts = {
            'tiny': self.load_font('ui', base + int(size_adjust.get('tiny', -2)), 'DejaVu Sans'),
            'small': self.load_font('scale', base + int(size_adjust.get('small', 0)), 'DejaVu Sans'),
            'medium': self.load_font('ui', base + int(size_adjust.get('medium', 8)), 'DejaVu Sans'),
            'large': self.load_font('ui', base + int(size_adjust.get('large', 20)), 'DejaVu Sans'),
            'huge': self.load_font('ui', base + int(size_adjust.get('huge', 44)), 'DejaVu Sans'),
            'mono': self.load_font('mono', base + int(size_adjust.get('mono', 0)), 'DejaVu Sans Mono'),
        }

    def load_font(self, group: str, size: int, fallback_family: str) -> pygame.font.Font:
        """Resolve one themed font by group name with file and family fallback."""
        size = max(8, int(size))
        file_path = None
        family = fallback_family
        if self.theme_config is not None:
            file_path = self.theme_config.resolve_asset(str(self.theme_value(f'fonts.{group}_file', '') or ''))
            family = str(self.theme_value(f'fonts.{group}_family', fallback_family) or fallback_family)
        if file_path is not None:
            try:
                return pygame.font.Font(str(file_path), size)
            except Exception:
                pass
        return pygame.font.SysFont(family, size)

    def theme_value(self, dotted_path: str, default=None):
        """Read one theme.json value with a renderer-local default."""
        if self.theme_config is None:
            return default
        return self.theme_config.get_path(dotted_path, default)

    def theme_flag(self, dotted_path: str, default: bool) -> bool:
        """Read a boolean-like theme flag safely."""
        return bool(self.theme_value(dotted_path, default))

    def theme_color(self, dotted_path: str, default):
        """Resolve one theme color from hex / array / tuple into an RGB(A) tuple."""
        value = self.theme_value(dotted_path, default)
        return self.parse_color(value, default)

    def parse_color(self, value, fallback):
        """Convert a theme color into a pygame-friendly tuple."""
        if isinstance(value, (list, tuple)) and len(value) in (3, 4):
            return tuple(int(max(0, min(255, channel))) for channel in value)
        if isinstance(value, str):
            raw = value.strip().lstrip('#')
            if len(raw) in (6, 8):
                try:
                    numbers = [int(raw[index:index + 2], 16) for index in range(0, len(raw), 2)]
                    return tuple(numbers)
                except Exception:
                    pass
        if isinstance(fallback, (list, tuple)):
            return tuple(fallback)
        return tuple(fallback)


    def run(self):
        """Run the renderer with active, idle and deep-idle power states.

        1.10.2 intentionally stops all draw activity while hidden. In resident
        mode the loop only reloads runtime JSON files on a coarse cadence and
        sleeps in between, which keeps hidden CPU usage close to zero.
        """
        pygame.display.init()
        pygame.font.init()
        self.write_pid_marker()
        self.clear_ready_marker()
        self.reload_settings(force=True)
        self.reload_state(force=True)
        self.reload_overlay_owner(force=True)
        initial_visible = True if not self.resident_mode else (
            str(self.state.get('ui_mode') or 'normal').lower() == 'scale'
            and self.overlay_owner == 'scale_fm'
        )
        self.init_display(force=True, visible=initial_visible)
        self.hidden_reload_due_at = 0.0

        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.clear_ready_marker()
                    self.clear_pid_marker()
                    pygame.quit()
                    return

            power_mode = self.determine_power_mode()
            if power_mode == 'active':
                self.reload_settings()
                self.reload_state()
                self.reload_overlay_owner()
                self.sync_window_visibility()

                if self.window_visible:
                    self.draw()
                    pygame.display.flip()
                    if not self.first_frame_presented:
                        self.first_frame_presented = True
                        self.write_ready_marker('first-paint')
                    visible_cap = max(10, int(self.settings.get('visible_fps_cap', 24)))
                    requested_fps = max(10, int(self.settings.get('fps', 24)))
                    self.clock.tick(min(requested_fps, visible_cap))
                    continue

            # Hidden standby / deep idle path: no draw, no flip, coarse reload cadence only.
            now = time.monotonic()
            if power_mode == 'deep_idle':
                reload_ms = max(1000, int(self.settings.get('deep_idle_reload_ms', 5000)))
                sleep_ms = max(250, int(self.settings.get('deep_idle_sleep_ms', 1000)))
            else:
                reload_ms = max(250, int(self.settings.get('hidden_state_reload_ms', 2000)))
                sleep_ms = max(50, int(self.settings.get('hidden_standby_sleep_ms', 250)))

            if now >= self.hidden_reload_due_at:
                self.reload_settings(force=True)
                self.reload_state(force=True)
                self.reload_overlay_owner(force=True)
                self.sync_window_visibility()
                self.hidden_reload_due_at = now + (reload_ms / 1000.0)
                if self.window_visible:
                    continue

            time.sleep(sleep_ms / 1000.0)

        self.clear_ready_marker()
        self.clear_pid_marker()
        pygame.quit()

    def compute_geometry(self):
        """Calculate the major screen regions using settings and theme overrides."""
        width, height = self.size
        info_width = int(self.theme_value('layout.info_panel.width', self.settings.get('info_panel_width', 430)))
        info_width = min(info_width, max(260, width - 400))
        scale_left = int(self.theme_value('layout.scale.left', 40))
        scale_top = int(self.theme_value('layout.scale.top', 78))
        scale_right_margin = int(self.theme_value('layout.scale.right_margin', 60))
        scale_bottom_margin = int(self.theme_value('layout.scale.bottom_margin', 60))
        scale_width = max(260, width - info_width - scale_left - scale_right_margin)
        scale_height = max(180, height - scale_top - scale_bottom_margin)
        info_left = width - info_width
        return {
            'width': width,
            'height': height,
            'info_width': info_width,
            'info_left': info_left,
            'scale_left': scale_left,
            'scale_top': scale_top,
            'scale_width': scale_width,
            'scale_height': scale_height,
        }

    def draw(self):
        """Draw one full frame using the current state and active theme."""
        geometry = self.compute_geometry()
        width = geometry['width']
        height = geometry['height']
        info_left = geometry['info_left']

        if self.layered_theme and self.layered_theme.available:
            self.screen.fill((8, 8, 10))
            self.layered_theme.draw_background_stack(self.screen)
        else:
            self.screen.fill((14, 14, 16))
            pygame.draw.rect(self.screen, (20, 20, 24), (0, 0, width, height))
            pygame.draw.line(self.screen, (88, 71, 38), (0, 42), (width, 42), 2)
            pygame.draw.line(self.screen, (88, 71, 38), (info_left, 50), (info_left, height - 24), 2)

        self.draw_header(width)
        self.draw_scale(
            geometry['scale_left'],
            geometry['scale_top'],
            geometry['scale_width'],
            geometry['scale_height']
        )
        self.draw_info_panel(info_left, 0, geometry['info_width'], height)

        if self.layered_theme and self.layered_theme.available and self.first_frame_presented:
            self.layered_theme.draw_overlay_stack(self.screen)

    def draw_header(self, width):
        """Draw the top status strip for title, mode, service and clock."""
        title = 'RADIO SCALE'
        ui_mode = (self.state.get('ui_mode') or 'normal').upper()
        tuning_mode = (self.state.get('tuning_mode') or 'auto').upper()
        locked = bool(self.state.get('tuning_locked'))
        lock_label = 'LOCK' if locked else 'SCAN'
        service = (self.state.get('service') or self.state.get('source_type') or '').upper()

        self.blit_text(
            title,
            self.fonts['medium'],
            self.theme_color('colors.header_title', (206, 176, 118)),
            int(self.theme_value('layout.header.title_x', 26)),
            int(self.theme_value('layout.header.title_y', 10))
        )
        self.blit_text(
            f'{ui_mode}  {lock_label}  {tuning_mode}',
            self.fonts['small'],
            self.theme_color('colors.header_meta', (230, 220, 190)),
            int(self.theme_value('layout.header.meta_x', 280)),
            int(self.theme_value('layout.header.meta_y', 15))
        )

        if service:
            self.blit_text(
                service,
                self.fonts['small'],
                self.theme_color('colors.header_service', (168, 168, 176)),
                int(self.theme_value('layout.header.service_x', 470)),
                int(self.theme_value('layout.header.service_y', 15))
            )

        if self.settings.get('show_clock', True):
            clock_text = datetime.now().strftime('%H:%M')
            clock_surface = self.fonts['medium'].render(clock_text, True, self.theme_color('colors.header_meta', (230, 220, 190)))
            clock_x = width - clock_surface.get_width() - int(self.theme_value('layout.header.clock_right_margin', 24))
            clock_y = int(self.theme_value('layout.header.clock_y', 10))
            self.screen.blit(clock_surface, (clock_x, clock_y))

    def draw_scale(self, x, y, width, height):
        """Draw the main radio scale, ticks, labels, pointer and hiss band."""
        start = float(self.settings.get('scale_start', 87.5))
        end = float(self.settings.get('scale_end', 108.0))
        baseline_ratio = float(self.theme_value('layout.scale.baseline_ratio', 0.64))
        baseline_min_y = int(self.theme_value('layout.scale.baseline_min_y', 180))
        baseline_bottom_margin = int(self.theme_value('layout.scale.baseline_max_bottom_margin', 72))
        baseline_y = y + int(height * baseline_ratio) + max(0, int(self.settings.get('scale_vertical_offset', 78)))
        baseline_y = min(y + height - baseline_bottom_margin, max(y + baseline_min_y, baseline_y))
        label_y = baseline_y + int(self.theme_value('layout.scale.label_y_offset', 46))
        minor_top = baseline_y - int(self.theme_value('layout.scale.minor_tick_top_delta', 18))
        mid_top = baseline_y - int(self.theme_value('layout.scale.mid_tick_top_delta', 26))
        major_top = baseline_y - int(self.theme_value('layout.scale.major_tick_top_delta', 42))

        pygame.draw.line(self.screen, self.theme_color('colors.baseline', (206, 177, 116)), (x, baseline_y), (x + width, baseline_y), 3)

        if self.theme_flag('draw_flags.scale_ticks', True):
            current = start
            while current <= end + 0.0001:
                pos_x = self.freq_to_x(current, x, width, start, end)
                rounded = round(current * 10) % 10
                if rounded == 0:
                    pygame.draw.line(self.screen, self.theme_color('colors.tick_major', (228, 195, 126)), (pos_x, major_top), (pos_x, baseline_y + 6), 3)
                    if self.theme_flag('draw_flags.scale_numbers', True):
                        label = f'{int(round(current))}'
                        self.blit_centered(label, self.fonts['small'], self.theme_color('colors.scale_label', (216, 206, 178)), pos_x, label_y)
                elif rounded == 5:
                    pygame.draw.line(self.screen, self.theme_color('colors.tick_mid', (196, 167, 106)), (pos_x, mid_top), (pos_x, baseline_y + 4), 2)
                else:
                    pygame.draw.line(self.screen, self.theme_color('colors.tick_minor', (132, 118, 83)), (pos_x, minor_top), (pos_x, baseline_y + 2), 1)
                current = round(current + 0.1, 1)

        stations = self.settings.get('stations', []) or []
        layouts = self.compute_station_label_layouts(stations, x, width, start, end, y, baseline_y)
        if self.theme_flag('draw_flags.station_markers', True):
            for station in stations:
                station_key = station.get('key') or station.get('name') or station.get('title') or ''
                self.draw_station_marker(station, x, width, start, end, baseline_y, layouts.get(station_key))

        self.draw_pointer(x, y, width, start, end, baseline_y)
        if self.theme_flag('draw_flags.noise_band', True):
            self.draw_noise_band(x, baseline_y + int(self.theme_value('layout.scale.noise_band_y_offset', 30)), width)

    def compute_station_label_layouts(self, stations, x, width, start, end, top_y, baseline_y):
        """Compute non-overlapping label positions with optional per-station offsets."""
        lane_count = max(1, min(6, int(self.theme_value('layout.station_labels.levels', self.settings.get('station_label_levels', 3)))))
        lane_gap = max(28, int(self.theme_value('layout.station_labels.lane_gap', 56)))
        lane_top = top_y + int(self.theme_value('layout.station_labels.lane_top_offset', 6))
        lane_ys = [lane_top + i * lane_gap for i in range(lane_count)]
        lane_right_edges = [x + int(self.theme_value('layout.station_labels.left_margin', 8)) for _ in range(lane_count)]
        layouts = {}

        ordered = sorted(stations, key=lambda item: float(item.get('freq', 0) or 0))
        marker_size = int(self.theme_value('layout.station_labels.marker_size', 12))
        text_gap = int(self.theme_value('layout.station_labels.text_gap', 14))
        left_margin = x + int(self.theme_value('layout.station_labels.left_margin', 8))
        right_margin = x + width - int(self.theme_value('layout.station_labels.right_margin', 14))
        marker_half = marker_size // 2

        for index, station in enumerate(ordered):
            freq = float(station.get('freq', 0) or 0)
            if freq < start or freq > end:
                continue

            pos_x = self.freq_to_x(freq, x, width, start, end)
            lines = self.station_label_lines(station)
            text_width = max((self.fonts['tiny'].size(line)[0] for line in lines), default=0)
            preferred_lane = index % lane_count
            base_text_x = pos_x + marker_half + text_gap

            best_lane = None
            best_text_x = None
            best_score = None
            lane_candidates = [((preferred_lane + offset) % lane_count) for offset in range(lane_count)]
            for lane_index in lane_candidates:
                candidate_x = max(base_text_x, lane_right_edges[lane_index] + 18)
                overflow = max(0, (candidate_x + text_width) - right_margin)
                score = (overflow, candidate_x)
                if best_score is None or score < best_score:
                    best_score = score
                    best_lane = lane_index
                    best_text_x = candidate_x
                if overflow == 0:
                    break

            chosen_lane = best_lane if best_lane is not None else 0
            text_x = int(best_text_x if best_text_x is not None else base_text_x)
            text_x = min(text_x, max(left_margin, int(right_margin - text_width)))

            marker_x = pos_x - marker_half
            marker_x = max(left_margin, min(int(right_margin - marker_size), marker_x))
            min_text_x = marker_x + marker_size + text_gap
            if text_x < min_text_x:
                text_x = min_text_x

            label_dx = int(station.get('label_dx', 0) or 0)
            label_dy = int(station.get('label_dy', 0) or 0)
            marker_dx = int(station.get('marker_dx', 0) or 0)
            marker_dy = int(station.get('marker_dy', 0) or 0)
            text_y = lane_ys[chosen_lane] + label_dy
            text_x += label_dx
            marker_x += marker_dx
            marker_y = text_y + max(2, (self.fonts['tiny'].get_height() - marker_size) // 2) + marker_dy
            lane_right_edges[chosen_lane] = max(lane_right_edges[chosen_lane], text_x + text_width)
            station_key = station.get('key') or station.get('name') or station.get('title') or ''
            layouts[station_key] = {
                'parts': lines,
                'text_y': text_y,
                'text_x': text_x,
                'marker_x': marker_x,
                'marker_y': marker_y,
                'marker_size': marker_size,
                'pos_x': pos_x,
                'lane': chosen_lane,
            }

        return layouts

    def station_label_lines(self, station: Dict[str, Any]) -> List[str]:
        """Return custom label lines or a simple fallback station label."""
        explicit = station.get('label_lines')
        if isinstance(explicit, list) and explicit:
            return [str(line) for line in explicit[:3]]
        return self.split_station_name(str(station.get('name', '') or ''))

    def draw_station_marker(self, station, x, width, start, end, baseline_y, layout=None):
        """Draw one station square marker and its label text block."""
        freq = float(station.get('freq', 0) or 0)
        if freq < start or freq > end:
            return
        pos_x = self.freq_to_x(freq, x, width, start, end)
        if layout is None:
            text = str(station.get('name', '') or '')
            layout = {
                'parts': [text],
                'text_y': baseline_y - 160,
                'text_x': pos_x + 18,
                'marker_x': pos_x - 6,
                'marker_y': baseline_y - 156,
                'marker_size': 12,
                'pos_x': pos_x,
            }

        is_locked = bool(self.state.get('tuning_station') and self.state.get('tuning_station', {}).get('name') == station.get('name'))
        color = self.theme_color('colors.station_marker_locked', (255, 233, 165)) if is_locked else self.theme_color('colors.station_marker_unlocked', (230, 120, 46))
        border_color = self.theme_color('colors.station_marker_border', (28, 49, 58))

        marker_x = int(round(layout.get('marker_x', pos_x - 6)))
        marker_y = int(layout.get('marker_y', baseline_y - 90))
        marker_size = int(layout.get('marker_size', 12))
        if is_locked:
            glow_rect = pygame.Rect(marker_x - 4, marker_y - 4, marker_size + 8, marker_size + 8)
            pygame.draw.rect(self.screen, (255, 240, 190), glow_rect, border_radius=4)
        pygame.draw.rect(self.screen, color, (marker_x, marker_y, marker_size, marker_size))
        pygame.draw.rect(self.screen, border_color, (marker_x, marker_y, marker_size, marker_size), 2 if marker_size >= 6 else 1)

        if not self.theme_flag('draw_flags.station_labels', True):
            return

        text_y = int(layout.get('text_y', marker_y - 2))
        text_x = int(layout.get('text_x', marker_x + marker_size + 10))
        parts = layout.get('parts') or self.station_label_lines(station)
        for line in parts:
            text_surface = self.fonts['tiny'].render(line, True, self.theme_color('colors.station_label', (214, 204, 182)))
            self.screen.blit(text_surface, (text_x, text_y))
            text_y += self.fonts['tiny'].get_linesize() - 2

    def draw_pointer(self, x, y, width, start, end, baseline_y):
        """Draw the tuning marker, preferring the themed PNG pointer when present.

        1.10.2 keeps the post-1.9 tuning feel but adds two extra stabilisers:
        - a small MHz deadband so micro target updates no longer shimmer
        - a pixel snap deadband so the displayed x position stays steady unless
          the movement is visually meaningful on the scale
        """
        target_freq = float(self.state.get('tuning_position') or self.state.get('active_frequency') or self.settings.get('fallback_frequency', 98.3))
        locked_station = self.state.get('tuning_station') or {}
        visual_lock_snap_enabled = bool(self.settings.get('lock_visual_snap_enabled', False))
        tuning_locked = bool(self.state.get('tuning_locked'))
        now_ms = int(time.time() * 1000)
        last_interaction_ts = int(self.state.get('tuning_last_interaction_ts') or 0)
        last_locked_freq = self.state.get('tuning_last_locked_freq')
        last_stable_position = self.state.get('tuning_last_stable_position')
        overlay_opened_at = int(self.state.get('overlay_opened_at') or 0)
        idle_lock_ms = max(80, int(self.settings.get('pointer_idle_lock_ms', 220) or 220))
        startup_settle_ms = max(0, int(self.settings.get('pointer_startup_settle_ms', 900) or 900))
        settle_epsilon = max(0.001, float(self.settings.get('pointer_settle_epsilon_mhz', 0.004) or 0.004))
        visual_deadband = max(settle_epsilon, float(self.settings.get('pointer_visual_deadband_mhz', 0.006) or 0.006))
        pixel_deadband = max(0.0, float(self.settings.get('pointer_pixel_snap_deadband_px', 1.0) or 1.0))

        if visual_lock_snap_enabled and tuning_locked and isinstance(locked_station, dict) and locked_station.get('freq') is not None:
            try:
                target_freq = float(locked_station.get('freq'))
            except Exception:
                pass

        if tuning_locked and last_locked_freq is not None:
            try:
                last_locked_freq = float(last_locked_freq)
                opened_recently = bool(overlay_opened_at) and (now_ms - overlay_opened_at) <= startup_settle_ms
                idle_locked = bool(last_interaction_ts) and (now_ms - last_interaction_ts) >= idle_lock_ms
                if opened_recently or idle_locked:
                    target_freq = last_locked_freq
            except Exception:
                pass
        elif last_stable_position is not None and last_interaction_ts and (now_ms - last_interaction_ts) >= idle_lock_ms:
            try:
                stable_freq = float(last_stable_position)
                if abs(float(target_freq) - stable_freq) <= 0.015:
                    target_freq = stable_freq
            except Exception:
                pass

        target_freq = max(start, min(end, target_freq))

        unlocked_gain = max(0.18, min(1.0, float(self.settings.get('pointer_visual_follow_gain', 0.38) or 0.38)))
        locked_gain = max(unlocked_gain, min(1.0, float(self.settings.get('pointer_visual_locked_gain', 0.48) or 0.48)))
        gain = locked_gain if tuning_locked else unlocked_gain

        if (not isinstance(self.last_pointer_freq, (int, float))) or (not self.pointer_bootstrap_done):
            self.last_pointer_freq = target_freq
            self.pointer_bootstrap_done = True
        else:
            if abs(target_freq - self.last_pointer_freq) <= visual_deadband:
                target_freq = self.last_pointer_freq
            self.last_pointer_freq = self.last_pointer_freq + ((target_freq - self.last_pointer_freq) * gain)
            if abs(self.last_pointer_freq - target_freq) < settle_epsilon:
                self.last_pointer_freq = target_freq

        candidate_x = self.freq_to_x(self.last_pointer_freq, x, width, start, end)
        if self.last_pointer_x is None or abs(candidate_x - self.last_pointer_x) > pixel_deadband:
            self.last_pointer_x = candidate_x
        pos_x = int(self.last_pointer_x)

        locked = bool(self.state.get('tuning_locked'))
        noise = float(self.state.get('tuning_noise') or 0.0)

        if self.layered_theme and self.layered_theme.available:
            if self.layered_theme.draw_pointer(self.screen, pos_x, baseline_y, locked, noise):
                return

        if locked:
            glow_color = self.theme_color('colors.pointer_glow_locked', (255, 220, 130))
            beam_color = self.theme_color('colors.pointer_beam_locked', (255, 245, 210))
        else:
            glow_color = self.theme_color('colors.pointer_glow_unlocked', (230, 180, 110))
            beam_color = self.theme_color('colors.pointer_beam_unlocked', (242, 220, 170))

        if not locked and bool(self.settings.get('pointer_jitter_enabled', False)):
            jitter_count = max(1, int(1 + (noise * 3)))
            for _ in range(jitter_count):
                jitter = self.random.randint(-2, 2)
                alpha_x = pos_x + jitter
                pygame.draw.rect(self.screen, self.theme_color('colors.pointer_jitter', (110, 90, 58)), (alpha_x - 1, y + 24, 2, baseline_y - y + 40), border_radius=1)

        glow_rect = pygame.Rect(pos_x - 6, y + 34, 12, baseline_y - y + 30)
        pygame.draw.rect(self.screen, glow_color, glow_rect, border_radius=6)
        pygame.draw.rect(self.screen, beam_color, (pos_x - 6, y + 18, 12, baseline_y - y + 54), border_radius=4)
        extension = int(self.theme_value('layout.scale.pointer_line_extension', 14))
        pygame.draw.line(self.screen, beam_color, (pos_x - 16, baseline_y + extension), (pos_x + 16, baseline_y + extension), 2)

    def draw_noise_band(self, x, y, width):
        """Draw the visual hiss indicator under the scale."""
        noise = float(self.state.get('tuning_noise') or 0.0)
        bar_width = max(100, int(width * 0.18))
        pygame.draw.rect(self.screen, self.theme_color('colors.noise_bg', (34, 34, 38)), (x, y, bar_width, 12), border_radius=6)
        fill = int(bar_width * max(0.0, min(1.0, noise)))
        if fill > 0:
            pygame.draw.rect(self.screen, self.theme_color('colors.noise_fill', (170, 140, 90)), (x, y, fill, 12), border_radius=6)
        self.blit_text('HISS', self.fonts['tiny'], self.theme_color('colors.noise_text', (196, 184, 150)), x + bar_width + 12, y - 5)

    def draw_info_panel(self, x, y, width, height):
        """Draw the right-side information panel, logo and optional VU meter."""
        inset = int(self.theme_value('layout.info_panel.left_inset', 18))
        panel_top = int(self.theme_value('layout.info_panel.top', 62))
        panel_bottom_margin = int(self.theme_value('layout.info_panel.bottom_margin', 22))
        radius = int(self.theme_value('layout.info_panel.radius', 16))
        border_width = int(self.theme_value('layout.info_panel.border_width', 2))
        padding_x = int(self.theme_value('layout.info_panel.x_padding', 34))
        panel_rect = pygame.Rect(x + inset, panel_top, width - (inset * 2), height - panel_top - panel_bottom_margin)

        pygame.draw.rect(self.screen, self.theme_color('colors.panel_bg', (16, 16, 18)), panel_rect, border_radius=radius)
        pygame.draw.rect(self.screen, self.theme_color('colors.panel_border', (118, 97, 56)), panel_rect, border_width, border_radius=radius)

        self.draw_dimmed_logo(panel_rect)
        self.draw_vu_meter(panel_rect)

        locked_station = self.state.get('tuning_station') or {}
        nearest_station = self.state.get('tuning_nearest_station') or {}
        is_locked = bool(self.state.get('tuning_locked'))
        station_name = (locked_station.get('name') if is_locked else nearest_station.get('name')) or (self.state.get('service') or self.state.get('source_type') or 'READY')
        title = self.state.get('title') or ''
        artist = self.state.get('artist') or ''
        album = self.state.get('album') or ''
        noise = float(self.state.get('tuning_noise') or 0.0)
        distance = self.state.get('tuning_distance')

        content_x = panel_rect.x + padding_x
        body_width = panel_rect.width - (padding_x * 2)
        headline = station_name.upper() if is_locked else 'SEARCHING'
        self.blit_text(headline, self.fonts['medium'], self.theme_color('colors.panel_headline', (231, 203, 150)), content_x, int(self.theme_value('layout.info_panel.headline_y', 88)))

        subline = station_name if not is_locked and station_name else ('Locked' if is_locked else 'Between stations')
        self.blit_text(subline, self.fonts['small'], self.theme_color('colors.panel_subline', (180, 174, 164)), content_x, int(self.theme_value('layout.info_panel.subline_y', 126)))

        info_y = int(self.theme_value('layout.info_panel.body_y', 170))
        if is_locked:
            self.blit_wrapped(title or 'No title', self.fonts['large'], self.theme_color('colors.panel_primary', (244, 240, 232)), content_x, info_y, body_width, max_lines=2)
            info_y += int(self.theme_value('layout.info_panel.body_gap_title', 88))
            self.blit_wrapped(artist or '', self.fonts['medium'], self.theme_color('colors.panel_secondary', (188, 188, 194)), content_x, info_y, body_width, max_lines=2)
            info_y += int(self.theme_value('layout.info_panel.body_gap_artist', 64))
            self.blit_wrapped(album or '', self.fonts['small'], self.theme_color('colors.panel_tertiary', (154, 154, 164)), content_x, info_y, body_width, max_lines=2)
        else:
            self.blit_wrapped('Rauschen / scan', self.fonts['large'], self.theme_color('colors.panel_primary', (220, 214, 200)), content_x, info_y, body_width, max_lines=2)
            info_y += int(self.theme_value('layout.info_panel.body_gap_title', 88))
            strength = int((1.0 - max(0.0, min(1.0, noise))) * 100)
            self.blit_text(f'Signal {strength:>3}%', self.fonts['medium'], self.theme_color('colors.panel_secondary', (188, 188, 194)), content_x, info_y)
            info_y += 44
            if distance is not None:
                self.blit_text(f'Δ {float(distance):.2f} MHz', self.fonts['small'], self.theme_color('colors.panel_tertiary', (154, 154, 164)), content_x, info_y)

        bottom_y = y + height - int(self.theme_value('layout.info_panel.bottom_offset', 150))
        volume = int(self.state.get('volume') or 0)
        mute = ' MUTE' if self.state.get('mute') else ''
        self.blit_text(f'VOL {volume:>3}{mute}', self.fonts['mono'], self.theme_color('colors.panel_accent', (214, 204, 182)), content_x, bottom_y)

        if self.settings.get('show_technical', True):
            samplerate = self.state.get('samplerate') or ''
            bitdepth = self.state.get('bitdepth') or ''
            tech = ' '.join([part for part in [samplerate, bitdepth] if part]).strip()
            if not tech:
                tech = self.state.get('track_type') or self.state.get('source_type') or ''
            self.blit_text(tech.upper(), self.fonts['mono'], self.theme_color('colors.panel_tertiary', (164, 156, 140)), content_x, bottom_y + int(self.theme_value('layout.info_panel.bottom_line_2_gap', 34)))

        status = (self.state.get('status') or 'stop').upper()
        pointer = float(self.state.get('tuning_position') or self.settings.get('fallback_frequency', 98.3))
        mode = (self.state.get('tuning_mode') or 'auto').upper()
        line3_y = bottom_y + int(self.theme_value('layout.info_panel.bottom_line_3_gap', 72))
        self.blit_text(status, self.fonts['small'], self.theme_color('colors.panel_accent', (198, 184, 150)), content_x, line3_y)
        self.blit_text(f'{pointer:.1f} MHz', self.fonts['small'], self.theme_color('colors.panel_accent', (198, 184, 150)), content_x + 106, line3_y)
        self.blit_text(mode, self.fonts['small'], self.theme_color('colors.panel_accent', (198, 184, 150)), content_x + 246, line3_y)

    def draw_dimmed_logo(self, panel_rect: pygame.Rect):
        """Draw a softly dimmed station logo when albumart can be resolved."""
        if not self.theme_flag('draw_flags.dimmed_logo', True):
            return
        if not bool(self.theme_value('layout.logo.enabled', True)):
            return

        source = str(self.state.get('albumart') or '').strip()
        surface = self.load_albumart_surface(source)
        if surface is None:
            return

        max_width = int(self.theme_value('layout.logo.max_width', 140))
        max_height = int(self.theme_value('layout.logo.max_height', 140))
        scaled = self.scale_surface(surface, max_width, max_height)
        if scaled is None:
            return

        logo = scaled.copy()
        logo.set_alpha(max(0, min(255, int(self.theme_value('layout.logo.alpha', 76)))))
        coordinate_space = str(self.theme_value('layout.logo.coordinate_space', 'panel')).lower()
        anchor = str(self.theme_value('layout.logo.anchor', 'right')).lower()
        base_x = int(self.theme_value('layout.logo.x', 0))
        base_y = int(self.theme_value('layout.logo.y', 114))
        x_padding = int(self.theme_value('layout.logo.x_padding', 28))
        y_padding = int(self.theme_value('layout.logo.y_padding', 0))

        if coordinate_space == 'panel':
            if anchor == 'right':
                draw_x = panel_rect.right - logo.get_width() - x_padding + base_x
            else:
                draw_x = panel_rect.x + x_padding + base_x
            draw_y = panel_rect.y + base_y + y_padding
        else:
            draw_x = base_x
            draw_y = base_y
        self.screen.blit(logo, (draw_x, draw_y))

    def draw_vu_meter(self, panel_rect: pygame.Rect):
        """Draw a configurable VU meter scaffold fed by vu_left / vu_right state keys."""
        enabled = self.theme_flag('draw_flags.vu_meter', False) and bool(self.theme_value('layout.vu_meter.enabled', False))
        if not enabled:
            return

        coordinate_space = str(self.theme_value('layout.vu_meter.coordinate_space', 'panel')).lower()
        meter_x = int(self.theme_value('layout.vu_meter.x', 18))
        meter_y = int(self.theme_value('layout.vu_meter.y', 18))
        meter_width = max(24, int(self.theme_value('layout.vu_meter.width', 90)))
        meter_height = max(60, int(self.theme_value('layout.vu_meter.height', 140)))
        channel_gap = max(4, int(self.theme_value('layout.vu_meter.channel_gap', 12)))
        if coordinate_space == 'panel':
            origin_x = panel_rect.x + meter_x
            origin_y = panel_rect.y + meter_y
        else:
            origin_x = meter_x
            origin_y = meter_y

        channel_width = max(8, int((meter_width - channel_gap) / 2))
        left_rect = pygame.Rect(origin_x, origin_y, channel_width, meter_height)
        right_rect = pygame.Rect(origin_x + channel_width + channel_gap, origin_y, channel_width, meter_height)

        pygame.draw.rect(self.screen, self.theme_color('colors.vu_bg', (27, 27, 32)), left_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme_color('colors.vu_bg', (27, 27, 32)), right_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme_color('colors.vu_border', (92, 74, 38)), left_rect, 2, border_radius=8)
        pygame.draw.rect(self.screen, self.theme_color('colors.vu_border', (92, 74, 38)), right_rect, 2, border_radius=8)

        vu_left = max(0.0, min(1.0, float(self.state.get('vu_left') or 0.0)))
        vu_right = max(0.0, min(1.0, float(self.state.get('vu_right') or 0.0)))
        self.fill_vu_channel(left_rect, vu_left, self.theme_color('colors.vu_fill_left', (208, 177, 114)))
        self.fill_vu_channel(right_rect, vu_right, self.theme_color('colors.vu_fill_right', (234, 208, 154)))

        if bool(self.theme_value('layout.vu_meter.label_enabled', True)):
            label_y = origin_y + meter_height + int(self.theme_value('layout.vu_meter.label_y_gap', 10))
            self.blit_text('L', self.fonts['tiny'], self.theme_color('colors.vu_label', (214, 204, 182)), left_rect.centerx - 4, label_y)
            self.blit_text('R', self.fonts['tiny'], self.theme_color('colors.vu_label', (214, 204, 182)), right_rect.centerx - 4, label_y)

    def fill_vu_channel(self, rect: pygame.Rect, level: float, color):
        """Fill one VU channel from the bottom upwards."""
        inner = rect.inflate(-8, -8)
        fill_height = max(0, int(inner.height * level))
        if fill_height <= 0:
            return
        fill_rect = pygame.Rect(inner.x, inner.bottom - fill_height, inner.width, fill_height)
        pygame.draw.rect(self.screen, color, fill_rect, border_radius=6)

    def load_albumart_surface(self, source: str) -> Optional[pygame.Surface]:
        """Load and cache one albumart or logo image from Volumio or an HTTP URL."""
        source = str(source or '').strip()
        if not source:
            return None
        normalized = source
        if source.startswith('/'):
            normalized = 'http://127.0.0.1:3000' + source

        cached = self.albumart_cache.get(normalized)
        now = time.time()
        if cached and (now - cached['ts']) < self.albumart_cache_ttl:
            return cached['surface']

        try:
            if normalized.startswith('http://') or normalized.startswith('https://'):
                request = urllib.request.Request(normalized, headers={'User-Agent': 'radio-scale-peppy/1.8.0'})
                with urllib.request.urlopen(request, timeout=2.0) as response:
                    payload = response.read()
                surface = pygame.image.load(io.BytesIO(payload)).convert_alpha()
            else:
                file_path = Path(normalized)
                if not file_path.is_absolute():
                    file_path = (PLUGIN_DIR / normalized).resolve()
                surface = pygame.image.load(str(file_path)).convert_alpha()
            self.albumart_cache[normalized] = {'ts': now, 'surface': surface}
            return surface
        except Exception:
            return cached['surface'] if cached else None

    def scale_surface(self, surface: pygame.Surface, max_width: int, max_height: int) -> Optional[pygame.Surface]:
        """Scale an image to fit inside a bounding box while keeping aspect ratio."""
        if surface is None:
            return None
        width, height = surface.get_size()
        if width <= 0 or height <= 0:
            return None
        ratio = min(max_width / float(width), max_height / float(height))
        ratio = min(ratio, 1.0)
        new_size = (max(1, int(width * ratio)), max(1, int(height * ratio)))
        if new_size == surface.get_size():
            return surface
        return pygame.transform.smoothscale(surface, new_size)

    def split_station_name(self, value):
        """Split a station name into simple line blocks for label rendering."""
        value = value.strip()
        if not value:
            return ['']
        return [value]

    def freq_to_x(self, freq, x, width, start, end):
        """Map a frequency value onto the visible scale width."""
        ratio = (freq - start) / (end - start)
        ratio = max(0.0, min(1.0, ratio))
        return int(x + (width * ratio))

    def blit_text(self, text, font, color, x, y):
        """Render one line of text at a fixed screen position."""
        if not text:
            return
        surface = font.render(str(text), True, color)
        self.screen.blit(surface, (x, y))

    def blit_centered(self, text, font, color, center_x, y):
        """Render one line of text centered on the given x coordinate."""
        if not text:
            return
        surface = font.render(str(text), True, color)
        self.screen.blit(surface, (center_x - surface.get_width() // 2, y))

    def blit_wrapped(self, text, font, color, x, y, max_width, max_lines=2):
        """Render wrapped text with ellipsis once the allowed line count is hit."""
        if not text:
            return y
        words = str(text).split()
        lines = []
        current = ''
        for word in words:
            trial = word if not current else current + ' ' + word
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
            if len(lines) >= max_lines:
                break
        if current and len(lines) < max_lines:
            lines.append(current)

        if len(lines) == max_lines and len(words) > 0:
            total_words = ' '.join(lines).split()
            if len(total_words) < len(words):
                last = lines[-1]
                while font.size(last + '…')[0] > max_width and len(last) > 1:
                    last = last[:-1]
                lines[-1] = last + '…'

        line_y = y
        for line in lines:
            self.blit_text(line, font, color, x, line_y)
            line_y += font.get_linesize() + 4
        return line_y


if __name__ == '__main__':
    os.environ.setdefault('SDL_VIDEO_CENTERED', '0')
    renderer = RadioScaleRenderer()
    renderer.run()
