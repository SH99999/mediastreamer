#!/usr/bin/env python3
"""Theme configuration helpers for the radio scale renderer.

This module keeps all JSON-theme handling in one place so the renderer can stay
focused on drawing. The JSON format is intentionally forgiving:
- unknown keys are ignored
- missing keys fall back to safe defaults
- theme.json is optional

The defaults below are also used as the in-file developer reference for what a
custom theme may override.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


DEFAULT_THEME_CONFIG: Dict[str, Any] = {
    "_dev_info": {
        "summary": "Theme overrides for renderer layout, fonts, colors, layers, logos and future VU meter placement.",
        "notes": [
            "PNG layer filenames stay simple and stable. Theme JSON only changes behavior and positioning.",
            "All coordinates are pixels. Colors accept either #RRGGBB, #RRGGBBAA or [r, g, b] / [r, g, b, a].",
            "Station entries may optionally add label_dx, label_dy, marker_dx, marker_dy and label_lines.",
            "VU meter rendering is scaffolded here; audio-driven stereo metering is the next release step."
        ]
    },
    "fonts": {
        "ui_family": "DejaVu Sans",
        "scale_family": "DejaVu Sans",
        "mono_family": "DejaVu Sans Mono",
        "ui_file": "",
        "scale_file": "",
        "mono_file": "",
        "size_adjust": {
            "tiny": -2,
            "small": 0,
            "medium": 8,
            "large": 20,
            "huge": 44,
            "mono": 0
        }
    },
    "layers": {
        "background_stack": ["background", "backlight", "scale_bed"],
        "overlay_stack": ["glass", "vignette", "noise"],
        "fullscreen_alpha": {},
        "pointer": {
            "marker_name": "marker",
            "shadow_name": "marker_shadow",
            "marker_alpha_locked": 255,
            "marker_alpha_unlocked_min": 150,
            "marker_alpha_unlocked_base": 215,
            "marker_alpha_unlocked_noise_boost": 24,
            "shadow_alpha_locked": 145,
            "shadow_alpha_unlocked_base": 110,
            "shadow_alpha_unlocked_noise_boost": 45,
            "shadow_dx": 2,
            "shadow_dy": 22,
            "marker_dx": 0,
            "marker_dy": 18
        }
    },
    "draw_flags": {
        "scale_ticks": True,
        "scale_numbers": True,
        "station_labels": True,
        "station_markers": True,
        "noise_band": True,
        "dimmed_logo": True,
        "vu_meter": False
    },
    "layout": {
        "header": {
            "title_x": 26,
            "title_y": 10,
            "meta_x": 280,
            "meta_y": 15,
            "service_x": 470,
            "service_y": 15,
            "clock_right_margin": 24,
            "clock_y": 10
        },
        "scale": {
            "left": 40,
            "top": 78,
            "right_margin": 60,
            "bottom_margin": 60,
            "baseline_ratio": 0.64,
            "baseline_min_y": 180,
            "baseline_max_bottom_margin": 72,
            "label_y_offset": 46,
            "major_tick_top_delta": 42,
            "mid_tick_top_delta": 26,
            "minor_tick_top_delta": 18,
            "pointer_line_extension": 14,
            "noise_band_y_offset": 30
        },
        "station_labels": {
            "levels": 3,
            "lane_gap": 56,
            "lane_top_offset": 6,
            "marker_size": 12,
            "text_gap": 14,
            "left_margin": 8,
            "right_margin": 14
        },
        "info_panel": {
            "width": 430,
            "left_inset": 18,
            "top": 62,
            "bottom_margin": 22,
            "x_padding": 34,
            "radius": 16,
            "border_width": 2,
            "headline_y": 88,
            "subline_y": 126,
            "body_y": 170,
            "body_gap_title": 88,
            "body_gap_artist": 64,
            "bottom_offset": 150,
            "bottom_line_2_gap": 34,
            "bottom_line_3_gap": 72
        },
        "logo": {
            "enabled": True,
            "coordinate_space": "panel",
            "x": 0,
            "y": 114,
            "x_padding": 28,
            "y_padding": 0,
            "anchor": "right",
            "max_width": 140,
            "max_height": 140,
            "alpha": 76
        },
        "vu_meter": {
            "enabled": False,
            "coordinate_space": "panel",
            "x": 18,
            "y": 18,
            "width": 90,
            "height": 140,
            "channel_gap": 12,
            "orientation": "vertical",
            "style": "bar",
            "alpha": 255,
            "label_enabled": True,
            "label_y_gap": 10
        }
    },
    "colors": {
        "header_title": "#ceb176",
        "header_meta": "#e6dcbe",
        "header_service": "#a8a8b0",
        "baseline": "#ceb174",
        "tick_major": "#e4c37e",
        "tick_mid": "#c4a76a",
        "tick_minor": "#847653",
        "scale_label": "#d8ceb2",
        "station_label": "#d6ccb6",
        "station_marker_locked": "#ffe9a5",
        "station_marker_unlocked": "#e6782e",
        "station_marker_border": "#1c313a",
        "pointer_glow_locked": "#ffdc82",
        "pointer_glow_unlocked": "#e6b46e",
        "pointer_beam_locked": "#fff5d2",
        "pointer_beam_unlocked": "#f2dcaa",
        "pointer_jitter": "#6e5a3a",
        "noise_bg": "#222226",
        "noise_fill": "#aa8c5a",
        "noise_text": "#c4b896",
        "panel_bg": "#101012",
        "panel_border": "#766138",
        "panel_headline": "#e7cb96",
        "panel_subline": "#b4aea4",
        "panel_primary": "#f4f0e8",
        "panel_secondary": "#bcbcc2",
        "panel_tertiary": "#9a9aa4",
        "panel_accent": "#c6b896",
        "vu_bg": "#1b1b20",
        "vu_border": "#5c4a26",
        "vu_fill_left": "#d0b172",
        "vu_fill_right": "#ead09a",
        "vu_label": "#d6ccb6"
    }
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge override into base without mutating either input dictionary."""
    result = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


class ThemeConfig:
    """Load a theme.json file and provide safe nested accessors for the renderer."""

    def __init__(self, theme_root: Path):
        self.theme_root = Path(theme_root)
        self.path = self.theme_root / 'theme.json'
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        """Read theme.json and deep-merge it onto the default config."""
        if not self.path.is_file():
            return copy.deepcopy(DEFAULT_THEME_CONFIG)
        try:
            with self.path.open('r', encoding='utf-8') as handle:
                raw = json.load(handle)
            if not isinstance(raw, dict):
                return copy.deepcopy(DEFAULT_THEME_CONFIG)
            return _deep_merge(DEFAULT_THEME_CONFIG, raw)
        except Exception:
            return copy.deepcopy(DEFAULT_THEME_CONFIG)

    def get_path(self, dotted_path: str, default: Any = None) -> Any:
        """Return a nested value like `layout.scale.left` with a fallback."""
        current: Any = self.data
        for part in dotted_path.split('.'):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        return current

    def resolve_asset(self, relative_path: str) -> Optional[Path]:
        """Resolve a font or asset path relative to the theme root when possible."""
        relative_path = str(relative_path or '').strip()
        if not relative_path:
            return None
        candidate = (self.theme_root / relative_path).resolve()
        if candidate.is_file():
            return candidate
        return None

    def get_color(self, dotted_path: str, default: Any) -> Any:
        """Return a raw color value. Parsing is intentionally handled by the renderer."""
        return self.get_path(dotted_path, default)

    def get_stack(self, dotted_path: str, fallback: Iterable[str]) -> Iterable[str]:
        """Return a list-like layer stack with a safe iterable fallback."""
        value = self.get_path(dotted_path, None)
        if isinstance(value, list):
            return value
        return list(fallback)
