"""
Cena de Introdução — história narrada em texto pixel art com fade.
Baseada na história descrita no documento do jogo.
"""
import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, UI_BG, UI_TEXT, UI_TITLE,
    SCENE_GAME, SCENE_SELECT
)
from src.utils.assets import FontManager, draw_text, sprite
from src.constants import PIXEL_SCALE


class IntroScene:
    """
    Sequência de telas de texto que conta a história de introdução:
    1. Tela preta → "Você estava dormindo…"
    2. "…mas acabou entrando em um pesadelo."
    3. "Você não consegue sair."
    4. Aparece o quarto em pixel art
    5. O amigo imaginário aparece
    6. "Não se preocupe, estou aqui para ajudar"
    7. "Encontre a saída."
    """

    SLIDES = [
        {"text": "Você estava dormindo…",          "sub": "",                                    "duration": 2800, "bg": (0, 0, 0)},
        {"text": "…mas acabou entrando em",         "sub": "um pesadelo.",                        "duration": 2800, "bg": (5, 0, 10)},
        {"text": "Você não consegue sair.",         "sub": "",                                    "duration": 2800, "bg": (10, 0, 20)},
        {"text": "",                                "sub": "",                                    "duration": 2000, "bg": (15, 10, 30), "show_room": True},
        {"text": "Uma luz surge no escuro…",        "sub": "",                                    "duration": 2200, "bg": (15, 10, 30), "show_room": True, "show_friend": True},
        {"text": "\"Não se preocupe,\"",            "sub": "\"estou aqui para ajudar.\"",         "duration": 3000, "bg": (15, 10, 30), "show_friend": True},
        {"text": "OBJETIVO:",                       "sub": "Encontre a saída.",                   "duration": 3000, "bg": (10, 5, 25), "highlight": True},
    ]

    def __init__(self, game):
        self.game        = game
        self.font_main   = FontManager.pixel(28)
        self.font_sub    = FontManager.pixel(20)
        self.font_small  = FontManager.pixel(13)
        self.font_title  = FontManager.pixel(36)

        self.slide_idx   = 0
        self.slide_timer = 0
        self.fade_alpha  = 255   # 255 = preto, 0 = visível
        self.fading_in   = True
        self.fading_out  = False
        self.FADE_SPEED  = 5

        self._fade_surf  = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._fade_surf.fill(BLACK)

        # Carrega sprites
        try:
            self._friend_img = sprite("imaginary_friend.png", scale=PIXEL_SCALE * 3)
        except:
            self._friend_img = None

        # Sprites dos jogadores para mostrar no quarto
        genders = getattr(game, "player_genders", ["boy", "girl"])
        try:
            self._p1_img = sprite(f"{genders[0]}_down_0.png", scale=PIXEL_SCALE * 2)
            self._p2_img = sprite(f"{genders[1]}_down_0.png", scale=PIXEL_SCALE * 2)
        except:
            self._p1_img = None
            self._p2_img = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                self._next_slide()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene(SCENE_SELECT)

    def _next_slide(self):
        if self.slide_idx < len(self.SLIDES) - 1:
            self.fading_out = True
        else:
            self._start_game()

    def _start_game(self):
        self.game.change_scene(SCENE_GAME)

    def update(self, dt_ms):
        self.slide_timer += dt_ms

        # Fade in
        if self.fading_in:
            self.fade_alpha = max(0, self.fade_alpha - self.FADE_SPEED * 2)
            if self.fade_alpha == 0:
                self.fading_in = False

        # Fade out (para trocar slide)
        elif self.fading_out:
            self.fade_alpha = min(255, self.fade_alpha + self.FADE_SPEED * 2)
            if self.fade_alpha == 255:
                self.fading_out = False
                self.slide_idx += 1
                if self.slide_idx >= len(self.SLIDES):
                    self._start_game()
                    return
                self.slide_timer = 0
                self.fading_in   = True

        # Avanço automático
        elif not self.fading_in and not self.fading_out:
            duration = self.SLIDES[self.slide_idx].get("duration", 3000)
            if self.slide_timer >= duration:
                if self.slide_idx < len(self.SLIDES) - 1:
                    self.fading_out = True
                else:
                    self._start_game()

    def draw(self, surface):
        slide = self.SLIDES[self.slide_idx]
        bg    = slide.get("bg", (0, 0, 0))
        surface.fill(bg)

        # Quarto pixel art simples
        if slide.get("show_room"):
            self._draw_room(surface)

        # Amigo imaginário
        if slide.get("show_friend") and self._friend_img:
            fx = SCREEN_WIDTH // 2 + 80
            fy = SCREEN_HEIGHT // 2 - self._friend_img.get_height() // 2
            surface.blit(self._friend_img, (fx, fy))

        # Texto principal
        text = slide.get("text", "")
        sub  = slide.get("sub", "")

        if slide.get("highlight"):
            self._draw_highlight_slide(surface, text, sub)
        else:
            self._draw_text_slide(surface, text, sub)

        # Hint de avançar
        if not self.fading_in and not self.fading_out:
            hint = self.font_small.render("Pressione ENTER ou E para continuar", False, (80, 70, 100))
            surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 28))

        # Overlay de fade
        if self.fade_alpha > 0:
            self._fade_surf.set_alpha(self.fade_alpha)
            surface.blit(self._fade_surf, (0, 0))

    def _draw_text_slide(self, surface, text, sub):
        cy = SCREEN_HEIGHT // 2 - 30
        if text:
            rendered = self.font_main.render(text, False, UI_TEXT)
            rx = SCREEN_WIDTH // 2 - rendered.get_width() // 2
            shadow  = self.font_main.render(text, False, BLACK)
            surface.blit(shadow,   (rx + 2, cy + 2))
            surface.blit(rendered, (rx, cy))
        if sub:
            rendered_sub = self.font_sub.render(sub, False, (180, 160, 220))
            sx = SCREEN_WIDTH // 2 - rendered_sub.get_width() // 2
            surface.blit(rendered_sub, (sx, cy + 38))

    def _draw_highlight_slide(self, surface, text, sub):
        # Painel central
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50, 400, 100)
        panel = pygame.Surface((400, 100), pygame.SRCALPHA)
        panel.fill((30, 20, 60, 200))
        surface.blit(panel, panel_rect.topleft)
        pygame.draw.rect(surface, (120, 80, 200), panel_rect, 2)

        title_r = self.font_title.render(text, False, UI_TITLE)
        surface.blit(title_r, (SCREEN_WIDTH // 2 - title_r.get_width() // 2,
                                SCREEN_HEIGHT // 2 - 40))
        sub_r = self.font_sub.render(sub, False, (200, 220, 255))
        surface.blit(sub_r, (SCREEN_WIDTH // 2 - sub_r.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 10))

    def _draw_room(self, surface):
        """Quarto simples em pixel art."""
        # Piso
        floor_color = (80, 60, 100)
        pygame.draw.rect(surface, floor_color,
                         (0, SCREEN_HEIGHT // 2 + 60, SCREEN_WIDTH, SCREEN_HEIGHT // 2 - 60))
        # Parede
        wall_color = (40, 30, 60)
        pygame.draw.rect(surface, wall_color,
                         (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2 + 60))
        # Linha parede/piso
        pygame.draw.line(surface, (100, 80, 140),
                         (0, SCREEN_HEIGHT // 2 + 60),
                         (SCREEN_WIDTH, SCREEN_HEIGHT // 2 + 60), 2)
        # Cama
        bed_rect = pygame.Rect(80, SCREEN_HEIGHT // 2 + 20, 140, 80)
        pygame.draw.rect(surface, (120, 80, 40), bed_rect)
        pygame.draw.rect(surface, (200, 200, 220), (90, SCREEN_HEIGHT // 2 + 30, 120, 50))
        pygame.draw.rect(surface, (240, 240, 255), (92, SCREEN_HEIGHT // 2 + 32, 40, 20))
        # Janela
        pygame.draw.rect(surface, (60, 80, 120), (SCREEN_WIDTH - 160, 60, 100, 80))
        pygame.draw.rect(surface, (100, 140, 200), (SCREEN_WIDTH - 155, 65, 90, 70))
        pygame.draw.line(surface, (60, 80, 120), (SCREEN_WIDTH - 110, 65), (SCREEN_WIDTH - 110, 135), 2)
        pygame.draw.line(surface, (60, 80, 120), (SCREEN_WIDTH - 155, 100), (SCREEN_WIDTH - 65, 100), 2)
        # Porta trancada
        pygame.draw.rect(surface, (100, 70, 30), (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 10, 40, 60))
        pygame.draw.rect(surface, (80, 50, 20), (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 10, 40, 60), 2)
        # Cadeado na porta
        pygame.draw.rect(surface, (200, 180, 50), (SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2 + 35, 10, 8))
        # Jogadores
        if self._p1_img:
            surface.blit(self._p1_img, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 40))
        if self._p2_img:
            surface.blit(self._p2_img, (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 40))
