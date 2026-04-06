"""
Cena de Título — tela inicial do jogo com animação e menu.
"""
import pygame
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, DARK_GRAY, UI_BG, UI_PANEL, UI_BORDER,
    UI_TITLE, UI_TEXT, UI_HIGHLIGHT, UI_SELECTED, UI_HOVER,
    SCENE_SELECT, SCENE_CREDITS,
    PIXEL_SCALE
)
from src.utils.assets import FontManager, draw_text, draw_panel, draw_pixel_border, sprite


class TitleScene:
    """
    Tela de título com:
    - Logo animado "ESCAPE ROOM"
    - Subtítulo em pixel art
    - Menu: Jogar / Créditos / Sair
    - Estrelas piscando no fundo
    """

    def __init__(self, game):
        self.game       = game
        self.font_title = FontManager.pixel(52)
        self.font_sub   = FontManager.pixel(18)
        self.font_menu  = FontManager.pixel(22)
        self.font_small = FontManager.pixel(13)

        self.menu_items = ["JOGAR", "CRÉDITOS", "SAIR"]
        self.selected   = 0
        self.timer      = 0

        # Estrelas de fundo
        import random
        self.stars = [
            (random.randint(0, SCREEN_WIDTH),
             random.randint(0, SCREEN_HEIGHT),
             random.uniform(0.3, 1.0))
            for _ in range(120)
        ]

        # Animação do título
        self._title_y_offset = 0
        self._flash_timer    = 0
        self._flash_on       = True

        # Carrega ícones de personagem para decoração
        try:
            self._boy_img  = sprite("boy_down_0.png",  scale=PIXEL_SCALE * 2)
            self._girl_img = sprite("girl_down_0.png", scale=PIXEL_SCALE * 2)
        except:
            self._boy_img  = None
            self._girl_img = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.menu_items)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.menu_items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                self._confirm()

    def _confirm(self):
        choice = self.menu_items[self.selected]
        if choice == "JOGAR":
            self.game.change_scene(SCENE_SELECT)
        elif choice == "CRÉDITOS":
            self.game.change_scene(SCENE_CREDITS)
        elif choice == "SAIR":
            self.game.running = False

    def update(self, dt_ms):
        self.timer       += dt_ms
        self._flash_timer += dt_ms
        if self._flash_timer > 600:
            self._flash_timer = 0
            self._flash_on = not self._flash_on

        self._title_y_offset = math.sin(self.timer / 800) * 6

    def draw(self, surface):
        # Fundo gradiente escuro
        surface.fill(UI_BG)
        self._draw_stars(surface)
        self._draw_decorations(surface)
        self._draw_title(surface)
        self._draw_menu(surface)
        self._draw_footer(surface)

    def _draw_stars(self, surface):
        t = self.timer / 1000
        for sx, sy, brightness in self.stars:
            flicker = 0.5 + 0.5 * math.sin(t * brightness * 3 + sx)
            alpha   = int(255 * brightness * flicker)
            size    = 1 if brightness < 0.6 else 2
            color   = (alpha, alpha, min(255, alpha + 30))
            if size == 1:
                surface.set_at((sx, sy), color)
            else:
                pygame.draw.rect(surface, color, (sx, sy, size, size))

    def _draw_decorations(self, surface):
        """Desenha personagens decorativos nas laterais."""
        if self._boy_img:
            surface.blit(self._boy_img,  (60,  SCREEN_HEIGHT // 2 - 40))
        if self._girl_img:
            surface.blit(self._girl_img, (SCREEN_WIDTH - 60 - self._girl_img.get_width(),
                                          SCREEN_HEIGHT // 2 - 40))

    def _draw_title(self, surface):
        cy = 140 + int(self._title_y_offset)

        # Sombra do título
        shadow = self.font_title.render("ESCAPE ROOM", False, (40, 20, 60))
        sx = SCREEN_WIDTH // 2 - shadow.get_width() // 2
        surface.blit(shadow, (sx + 3, cy + 3))

        # Título principal
        title = self.font_title.render("ESCAPE ROOM", False, UI_TITLE)
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        surface.blit(title, (tx, cy))

        # Subtítulo
        sub = self.font_sub.render("~ Um Sonho do Qual Você Não Pode Sair ~", False, (180, 160, 220))
        subx = SCREEN_WIDTH // 2 - sub.get_width() // 2
        surface.blit(sub, (subx, cy + 60))

        # Linha decorativa
        line_y = cy + 85
        pygame.draw.line(surface, UI_BORDER,
                         (SCREEN_WIDTH // 2 - 200, line_y),
                         (SCREEN_WIDTH // 2 + 200, line_y), 1)

    def _draw_menu(self, surface):
        menu_y = SCREEN_HEIGHT // 2 + 30
        item_h = 42

        for i, item in enumerate(self.menu_items):
            is_sel = (i == self.selected)
            y = menu_y + i * item_h

            if is_sel:
                # Painel de seleção
                panel_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 120, y - 6,
                    240, 34
                )
                draw_panel(surface, panel_rect, UI_HOVER, UI_BORDER, alpha=200)
                draw_pixel_border(surface, panel_rect, UI_SELECTED, 2)

                # Setas indicadoras
                arrow_color = UI_SELECTED
                draw_text(surface, ">", SCREEN_WIDTH // 2 - 110, y,
                          self.font_menu, arrow_color, shadow=True)
                draw_text(surface, "<", SCREEN_WIDTH // 2 + 92, y,
                          self.font_menu, arrow_color, shadow=True)

                color = UI_SELECTED
            else:
                color = UI_TEXT

            draw_text(surface, item,
                      SCREEN_WIDTH // 2, y,
                      self.font_menu, color,
                      shadow=True, center=True)

    def _draw_footer(self, surface):
        if self._flash_on:
            hint = self.font_small.render(
                "P1: WASD + E   |   P2: Setas + Enter", False, (120, 100, 160))
            surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2,
                                SCREEN_HEIGHT - 30))
