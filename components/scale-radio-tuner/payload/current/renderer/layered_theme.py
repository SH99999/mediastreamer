#!/usr/bin/env python3
"""Layered theme helper for radio_scale_peppy.

This module is intentionally narrow: it only knows how to load PNG layers and
pointer sprites. All Volumio state interpretation stays in the main renderer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple

import pygame

from theme_config import ThemeConfig


class LayeredTheme:
    """Load and draw PNG layers based on theme.json conventions.

    Expected theme folder contents still default to the stable filenames used by
    earlier releases, but the draw order, alpha and pointer sprite names are now
    configurable through theme.json.
    """

    FALLBACK_FULLSCREEN_LAYERS = (
        'background',
        'backlight',
        'scale_bed',
        'glass',
        'vignette',
        'noise',
    )

    def __init__(self, theme_root: Path, screen_size: Tuple[int, int], theme_config: ThemeConfig):
        """Initialise the theme loader for one screen resolution."""
        self.theme_root = Path(theme_root)
        self.screen_size = tuple(screen_size)
        self.theme_config = theme_config
        self.fullscreen_assets: Dict[str, pygame.Surface] = {}
        self.sprite_assets: Dict[str, pygame.Surface] = {}
        self.pointer_noise_visual = 0.0
        self.deferred_overlay_names = list(self.theme_config.get_stack('layers.overlay_stack', ['glass', 'vignette', 'noise']))
        self.overlay_assets_loaded = False
        self._load()

    @property
    def available(self) -> bool:
        """Report whether at least one background layer was loaded successfully."""
        background_stack = list(self.theme_config.get_stack('layers.background_stack', ['background']))
        return any(name in self.fullscreen_assets for name in background_stack)

    def _load(self) -> None:
        """Load all fullscreen and pointer sprite assets referenced by theme.json."""
        layer_names = set(self.FALLBACK_FULLSCREEN_LAYERS)
        layer_names.update(self.theme_config.get_stack('layers.background_stack', []))

        # 1.9.7-safe defers pure overlay/glass layers until after the first
        # visible frame. This keeps startup focused on getting *something* on
        # screen quickly instead of finishing every decorative PNG first.
        for name in layer_names:
            surface = self._load_layer(name, scale_to_screen=True)
            if surface is not None:
                alpha = self.theme_config.get_path(f'layers.fullscreen_alpha.{name}', None)
                if alpha is not None:
                    surface = surface.copy()
                    surface.set_alpha(max(0, min(255, int(alpha))))
                self.fullscreen_assets[name] = surface

        for sprite_name in self._pointer_sprite_names():
            surface = self._load_layer(sprite_name, scale_to_screen=False)
            if surface is not None:
                self.sprite_assets[sprite_name] = surface

    def _pointer_sprite_names(self):
        """Return the configured marker and marker-shadow sprite names."""
        marker_name = str(self.theme_config.get_path('layers.pointer.marker_name', 'marker') or 'marker')
        shadow_name = str(self.theme_config.get_path('layers.pointer.shadow_name', 'marker_shadow') or 'marker_shadow')
        return {marker_name, shadow_name}

    def _load_layer(self, name: str, scale_to_screen: bool) -> Optional[pygame.Surface]:
        """Load one PNG layer by its logical theme name."""
        path = self.theme_root / f'{name}.png'
        if not path.is_file():
            return None

        surface = pygame.image.load(str(path)).convert_alpha()
        if scale_to_screen and surface.get_size() != self.screen_size:
            # Startup on the Pi is dominated by loading and scaling large PNGs.
            # Regular scale is intentionally the default in 1.9.3 because it is
            # much faster than smoothscale and visually sufficient for the
            # appliance-style layered artwork. Themes can opt back into smoother
            # scaling through theme.json if needed.
            use_smoothscale = bool(self.theme_config.get_path('rendering.use_smoothscale_assets', False))
            surface = pygame.transform.smoothscale(surface, self.screen_size) if use_smoothscale else pygame.transform.scale(surface, self.screen_size)
        return surface

    def draw_background_stack(self, screen: pygame.Surface) -> None:
        """Draw the configured background stack before dynamic renderer content."""
        for name in self.theme_config.get_stack('layers.background_stack', ['background', 'backlight', 'scale_bed']):
            surface = self.fullscreen_assets.get(name)
            if surface is not None:
                screen.blit(surface, (0, 0))

    def ensure_overlay_assets_loaded(self) -> None:
        """Load deferred overlay layers on demand after the first frame."""
        if self.overlay_assets_loaded:
            return
        for name in self.deferred_overlay_names:
            if name in self.fullscreen_assets:
                continue
            surface = self._load_layer(name, scale_to_screen=True)
            if surface is not None:
                alpha = self.theme_config.get_path(f'layers.fullscreen_alpha.{name}', None)
                if alpha is not None:
                    surface = surface.copy()
                    surface.set_alpha(max(0, min(255, int(alpha))))
                self.fullscreen_assets[name] = surface
        self.overlay_assets_loaded = True

    def draw_overlay_stack(self, screen: pygame.Surface) -> None:
        """Draw the configured overlay stack after dynamic renderer content."""
        self.ensure_overlay_assets_loaded()
        for name in self.theme_config.get_stack('layers.overlay_stack', ['glass', 'vignette', 'noise']):
            surface = self.fullscreen_assets.get(name)
            if surface is not None:
                screen.blit(surface, (0, 0))

    def draw_pointer(
        self,
        screen: pygame.Surface,
        center_x: int,
        baseline_y: int,
        locked: bool,
        noise_level: float,
    ) -> bool:
        """Draw themed pointer sprites.

        Returns True when a themed marker was drawn successfully. The caller can
        then skip the primitive fallback pointer.
        """
        marker_name = str(self.theme_config.get_path('layers.pointer.marker_name', 'marker') or 'marker')
        shadow_name = str(self.theme_config.get_path('layers.pointer.shadow_name', 'marker_shadow') or 'marker_shadow')
        marker = self.sprite_assets.get(marker_name)
        if marker is None:
            return False

        shadow = self.sprite_assets.get(shadow_name)
        noise_level = max(0.0, min(1.0, float(noise_level or 0.0)))
        smoothing = max(0.05, min(1.0, float(self.theme_config.get_path('layers.pointer.noise_alpha_smoothing', 0.18) or 0.18)))
        self.pointer_noise_visual = self.pointer_noise_visual + ((noise_level - self.pointer_noise_visual) * smoothing)
        noise_level = self.pointer_noise_visual

        if shadow is not None:
            shadow_surface = shadow.copy()
            shadow_alpha = int(self.theme_config.get_path('layers.pointer.shadow_alpha_locked', 145)) if locked else int(
                self.theme_config.get_path('layers.pointer.shadow_alpha_unlocked_base', 110)
                + (noise_level * float(self.theme_config.get_path('layers.pointer.shadow_alpha_unlocked_noise_boost', 45)))
            )
            shadow_surface.set_alpha(max(50, min(220, shadow_alpha)))
            shadow_rect = shadow_surface.get_rect()
            shadow_rect.midbottom = (
                int(center_x + int(self.theme_config.get_path('layers.pointer.shadow_dx', 2))),
                int(baseline_y + int(self.theme_config.get_path('layers.pointer.shadow_dy', 22))),
            )
            screen.blit(shadow_surface, shadow_rect)

        marker_surface = marker.copy()
        marker_alpha = int(self.theme_config.get_path('layers.pointer.marker_alpha_locked', 255)) if locked else int(
            self.theme_config.get_path('layers.pointer.marker_alpha_unlocked_base', 215)
            + (noise_level * float(self.theme_config.get_path('layers.pointer.marker_alpha_unlocked_noise_boost', 24)))
        )
        marker_surface.set_alpha(max(
            int(self.theme_config.get_path('layers.pointer.marker_alpha_unlocked_min', 150)),
            min(255, marker_alpha)
        ))
        marker_rect = marker_surface.get_rect()
        marker_rect.midbottom = (
            int(center_x + int(self.theme_config.get_path('layers.pointer.marker_dx', 0))),
            int(baseline_y + int(self.theme_config.get_path('layers.pointer.marker_dy', 18))),
        )
        screen.blit(marker_surface, marker_rect)
        return True
