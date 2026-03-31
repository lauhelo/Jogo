"""
Cenas de Game Over e Vitória.
"""
import pygame
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, RED, UI_BG, UI_TITLE, UI_TEXT,
    SCENE_TITLE, SCENE_GAME,
    PIXEL_SCALE
)
from src.utils.assets import FontManager, draw_text, sprite


class GameOverScene:
    """Tela de Game Over — volta para a fase anterior."""

    def __init__(self, game):
        self.game       = game
        self.font_title = FontManager.pixel(48)
        self.font_sub   = FontManager.pixel(20)
        self.font_small = FontManager.pixel(14)
        self.timer      = 0
        self._alpha     = 0
        self._fading_in = True

        self._fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._fade_surf.fill(BLACK)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                self.game.retry_phase()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene(SCENE_TITLE)

    def update(self, dt_ms):
        self.timer += dt_ms
        if self._fading_in:
            self._alpha = max(0, self._alpha - 4)
            if self._alpha == 0:
                self._fading_in = False

    def draw(self, surface):
        surface.fill((20, 5, 10))

        # Partículas de fundo
        t = self.timer / 1000
        for i in range(20):
            x = (i * 67 + int(t * 30)) % SCREEN_WIDTH
            y = (i * 43 + int(t * 20)) % SCREEN_HEIGHT
            pygame.draw.rect(surface, (80, 20, 20), (x, y, 2, 2))

        # Título
        pulse = abs(math.sin(self.timer / 500))
        r = int(180 + 75 * pulse)
        title_color = (r, 30, 30)
        title = self.font_title.render("GAME OVER", False, title_color)
        shadow = self.font_title.render("GAME OVER", False, (40, 0, 0))
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        surface.blit(shadow, (tx + 3, SCREEN_HEIGHT // 2 - 70 + 3))
        surface.blit(title,  (tx,     SCREEN_HEIGHT // 2 - 70))

        # Subtítulo
        sub = self.font_sub.render("Você perdeu todos os corações...", False, (180, 120, 120))
        surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2))

        sub2 = self.font_sub.render("Voltando para a fase anterior.", False, (160, 100, 100))
        surface.blit(sub2, (SCREEN_WIDTH // 2 - sub2.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

        # Instruções
        hint = self.font_small.render("ENTER / E: Tentar novamente   |   ESC: Menu", False, (100, 80, 80))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))

        # Fade
        if self._alpha > 0:
            self._fade_surf.set_alpha(self._alpha)
            surface.blit(self._fade_surf, (0, 0))


class WinScene:
    """
    Cena de vitória final — sequência de texto como descrita na história.
    """

    SLIDES = [
        {"text": "Você conseguiu…",       "sub": "",                    "duration": 3000, "distort": True},
        {"text": "Você acordou.",          "sub": "",                    "duration": 3000, "distort": False, "show_room": True},
        {"text": "O amigo imaginário",     "sub": "não está mais lá.",   "duration": 3000, "show_room": True},
        {"text": "Era só um sonho…?",      "sub": "",                    "duration": 3500},
        {"text": "FIM",                    "sub": "Obrigado por jogar!", "duration": 0,    "is_end": True},
    ]

    def __init__(self, game):
        self.game        = game
        self.font_title  = FontManager.pixel(52)
        self.font_main   = FontManager.pixel(28)
        self.font_sub    = FontManager.pixel(20)
        self.font_small  = FontManager.pixel(14)
        self.slide_idx   = 0
        self.slide_timer = 0
        self.timer       = 0
        self.fade_alpha  = 255
        self.fading_in   = True
        self.fading_out  = False
        self.FADE_SPEED  = 4

        self._fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._fade_surf.fill(BLACK)

        genders = getattr(game, "player_genders", ["boy", "girl"])
        try:
            self._p1_img = sprite(f"{genders[0]}_down_0.png", scale=PIXEL_SCALE * 2)
        except:
            self._p1_img = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                self._next_slide()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene(SCENE_TITLE)

    def _next_slide(self):
        slide = self.SLIDES[self.slide_idx]
        if slide.get("is_end"):
            self.game.change_scene(SCENE_TITLE)
        elif self.slide_idx < len(self.SLIDES) - 1:
            self.fading_out = True

    def update(self, dt_ms):
        self.timer       += dt_ms
        self.slide_timer += dt_ms

        if self.fading_in:
            self.fade_alpha = max(0, self.fade_alpha - self.FADE_SPEED)
            if self.fade_alpha == 0:
                self.fading_in = False

        elif self.fading_out:
            self.fade_alpha = min(255, self.fade_alpha + self.FADE_SPEED)
            if self.fade_alpha == 255:
                self.fading_out = False
                self.slide_idx += 1
                if self.slide_idx >= len(self.SLIDES):
                    self.game.change_scene(SCENE_TITLE)
                    return
                self.slide_timer = 0
                self.fading_in   = True

        elif not self.fading_in and not self.fading_out:
            duration = self.SLIDES[self.slide_idx].get("duration", 3000)
            if duration > 0 and self.slide_timer >= duration:
                if self.slide_idx < len(self.SLIDES) - 1:
                    self.fading_out = True

    def draw(self, surface):
        slide = self.SLIDES[self.slide_idx]

        # Fundo
        if slide.get("distort"):
            self._draw_distorted_bg(surface)
        elif slide.get("show_room"):
            self._draw_peaceful_room(surface)
        else:
            surface.fill((5, 5, 15))

        # Texto
        text = slide.get("text", "")
        sub  = slide.get("sub", "")

        if slide.get("is_end"):
            self._draw_end(surface, text, sub)
        else:
            cy = SCREEN_HEIGHT // 2 - 30
            if text:
                rendered = self.font_main.render(text, False, (220, 220, 240))
                surface.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, cy))
            if sub:
                rendered_sub = self.font_sub.render(sub, False, (160, 140, 200))
                surface.blit(rendered_sub, (SCREEN_WIDTH // 2 - rendered_sub.get_width() // 2, cy + 40))

        if not slide.get("is_end"):
            hint = self.font_small.render("ENTER / E para continuar", False, (60, 50, 80))
            surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 28))

        # Fade
        if self.fade_alpha > 0:
            self._fade_surf.set_alpha(self.fade_alpha)
            surface.blit(self._fade_surf, (0, 0))

    def _draw_distorted_bg(self, surface):
        """Efeito de sonho quebrando."""
        t = self.timer / 200
        surface.fill((10, 5, 20))
        for i in range(0, SCREEN_HEIGHT, 8):
            offset = int(math.sin(t + i * 0.1) * 12)
            color  = (int(40 + 20 * math.sin(t + i * 0.05)), 10, int(60 + 20 * math.cos(t + i * 0.03)))
            pygame.draw.line(surface, color, (offset, i), (SCREEN_WIDTH + offset, i), 2)

    def _draw_peaceful_room(self, surface):
        """Quarto normal, sem distorções."""
        surface.fill((180, 160, 200))
        pygame.draw.rect(surface, (140, 120, 160),
                         (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.line(surface, (160, 140, 180),
                         (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
        # Cama
        pygame.draw.rect(surface, (120, 80, 40),
                         (80, SCREEN_HEIGHT // 2 + 20, 140, 80))
        pygame.draw.rect(surface, (220, 220, 240),
                         (90, SCREEN_HEIGHT // 2 + 30, 120, 50))
        # Personagem acordado
        if self._p1_img:
            surface.blit(self._p1_img,
                         (SCREEN_WIDTH // 2 - self._p1_img.get_width() // 2,
                          SCREEN_HEIGHT // 2 + 30))

    def _draw_end(self, surface, text, sub):
        title = self.font_title.render(text, False, (255, 220, 80))
        shadow = self.font_title.render(text, False, (60, 40, 0))
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        surface.blit(shadow, (tx + 3, SCREEN_HEIGHT // 2 - 60 + 3))
        surface.blit(title,  (tx,     SCREEN_HEIGHT // 2 - 60))

        sub_r = self.font_sub.render(sub, False, (200, 180, 140))
        surface.blit(sub_r, (SCREEN_WIDTH // 2 - sub_r.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 20))

        hint = self.font_small.render("ENTER / E: Voltar ao Menu", False, (120, 100, 80))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
