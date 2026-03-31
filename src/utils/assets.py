"""
Utilitários de carregamento e gerenciamento de assets.
"""
import pygame
import os
from src.constants import SPRITES_DIR, TILES_DIR, UI_DIR, PIXEL_SCALE

_cache = {}

def load_image(path, scale=1, colorkey=None):
    """Carrega imagem com cache. scale multiplica o tamanho."""
    key = (path, scale)
    if key in _cache:
        return _cache[key]
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale != 1:
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
        if colorkey is not None:
            img.set_colorkey(colorkey)
        _cache[key] = img
        return img
    except Exception as e:
        print(f"[WARN] Não foi possível carregar {path}: {e}")
        # Retorna superfície placeholder
        surf = pygame.Surface((16 * scale, 16 * scale), pygame.SRCALPHA)
        surf.fill((255, 0, 255, 180))
        _cache[key] = surf
        return surf

def sprite(name, scale=PIXEL_SCALE):
    return load_image(os.path.join(SPRITES_DIR, name), scale)

def tile(name, scale=PIXEL_SCALE):
    return load_image(os.path.join(TILES_DIR, name), scale)

def ui_img(name, scale=1):
    return load_image(os.path.join(UI_DIR, name), scale)

def clear_cache():
    _cache.clear()


class FontManager:
    """Gerencia fontes pixel art do jogo."""
    _fonts = {}

    @classmethod
    def get(cls, size, bold=False):
        key = (size, bold)
        if key not in cls._fonts:
            # Tenta usar fonte monospace embutida; fallback para SysFont
            try:
                cls._fonts[key] = pygame.font.SysFont("monospace", size, bold=bold)
            except:
                cls._fonts[key] = pygame.font.Font(None, size)
        return cls._fonts[key]

    @classmethod
    def pixel(cls, size):
        """Fonte estilo pixel art."""
        key = ("pixel", size)
        if key not in cls._fonts:
            try:
                cls._fonts[key] = pygame.font.SysFont("courier", size, bold=True)
            except:
                cls._fonts[key] = pygame.font.Font(None, size)
        return cls._fonts[key]


def draw_text(surface, text, x, y, font, color=(255, 255, 255), shadow=True, center=False):
    """Desenha texto com sombra opcional."""
    rendered = font.render(text, False, color)
    if center:
        x = x - rendered.get_width() // 2
    if shadow:
        shadow_surf = font.render(text, False, (0, 0, 0))
        surface.blit(shadow_surf, (x + 1, y + 1))
    surface.blit(rendered, (x, y))
    return rendered.get_width()


def draw_text_wrapped(surface, text, x, y, font, color, max_width, line_height=None):
    """Desenha texto com quebra de linha automática."""
    if line_height is None:
        line_height = font.get_height() + 2
    words = text.split(' ')
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for i, line in enumerate(lines):
        draw_text(surface, line, x, y + i * line_height, font, color)
    return len(lines) * line_height


def draw_panel(surface, rect, bg_color, border_color, border_width=2, alpha=220):
    """Desenha painel semi-transparente com borda."""
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((*bg_color, alpha))
    surface.blit(panel, rect.topleft)
    pygame.draw.rect(surface, border_color, rect, border_width)


def draw_pixel_border(surface, rect, color, thickness=2):
    """Borda estilo pixel art (sem anti-aliasing)."""
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x, y, w, thickness))
    pygame.draw.rect(surface, color, (x, y + h - thickness, w, thickness))
    pygame.draw.rect(surface, color, (x, y, thickness, h))
    pygame.draw.rect(surface, color, (x + w - thickness, y, thickness, h))
