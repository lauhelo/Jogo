"""
Cena de Créditos.
"""
import pygame
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_TITLE, UI_TEXT, UI_BORDER,
    SCENE_TITLE
)
from src.utils.assets import FontManager, draw_text


class CreditsScene:

    def __init__(self, game):
        self.game       = game
        self.font_title = FontManager.pixel(32)
        self.font_text  = FontManager.pixel(16)
        self.font_small = FontManager.pixel(13)
        self.timer      = 0
        self.scroll_y   = SCREEN_HEIGHT

        self.lines = [
            ("ESCAPE ROOM", "title"),
            ("", ""),
            ("Um jogo de Escape Room em Pixel Art", "text"),
            ("para 2 jogadores no Raspberry Pi", "text"),
            ("", ""),
            ("HISTÓRIA", "subtitle"),
            ("Escrita por Alicia", "text"),
            ("", ""),
            ("DESIGN & PROGRAMAÇÃO", "subtitle"),
            ("Desenvolvido com Python + Pygame", "text"),
            ("", ""),
            ("FASES", "subtitle"),
            ("Jardim • Escritório • Cozinha", "text"),
            ("Quarto 1 • Sótão • Quarto 2", "text"),
            ("Porão • Garagem", "text"),
            ("", ""),
            ("CONTROLES", "subtitle"),
            ("Jogador 1: WASD + E", "text"),
            ("Jogador 2: Setas + Enter", "text"),
            ("", ""),
            ("Obrigado por jogar!", "title"),
            ("", ""),
            ("Pressione ESC para voltar ao menu", "small"),
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene(SCENE_TITLE)

    def update(self, dt_ms):
        self.timer    += dt_ms
        self.scroll_y -= 0.5
        if self.scroll_y < -len(self.lines) * 28 - 100:
            self.scroll_y = SCREEN_HEIGHT

    def draw(self, surface):
        surface.fill(UI_BG)

        # Estrelas
        t = self.timer / 1000
        for i in range(60):
            sx = (i * 137) % SCREEN_WIDTH
            sy = (i * 97 + int(t * 20)) % SCREEN_HEIGHT
            alpha = int(128 + 127 * math.sin(t + i))
            pygame.draw.rect(surface, (alpha, alpha, min(255, alpha + 30)), (sx, sy, 1, 1))

        y = int(self.scroll_y)
        for text, style in self.lines:
            if not text:
                y += 20
                continue
            if style == "title":
                font  = self.font_title
                color = UI_TITLE
            elif style == "subtitle":
                font  = self.font_text
                color = (180, 160, 220)
                pygame.draw.line(surface, UI_BORDER,
                                 (SCREEN_WIDTH // 2 - 150, y + font.get_height()),
                                 (SCREEN_WIDTH // 2 + 150, y + font.get_height()), 1)
            elif style == "small":
                font  = self.font_small
                color = (100, 90, 130)
            else:
                font  = self.font_text
                color = UI_TEXT

            rendered = font.render(text, False, color)
            surface.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, y))
            y += rendered.get_height() + 8
