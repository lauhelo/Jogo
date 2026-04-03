"""
Cena de Pausa — Menu visível durante o jogo.
"""
import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, UI_BG, UI_PANEL, UI_BORDER,
    UI_TEXT, UI_SELECTED, WHITE, YELLOW, GREEN, RED
)
from src.utils.assets import FontManager, draw_text, draw_panel, draw_pixel_border

class PauseScene:
    def __init__(self, game, parent_phase):
        self.game = game
        self.parent_phase = parent_phase
        
        self.font_title = FontManager.pixel(32)
        self.font_menu  = FontManager.pixel(20)
        self.font_hint  = FontManager.pixel(12)
        
        self.options = ["CONTINUAR", "REINICIAR FASE", "SAIR PARA O MENU"]
        self.cursor = 0
        
        # Overlay semi-transparente
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.cursor = (self.cursor - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.cursor = (self.cursor + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_e, pygame.K_SPACE):
                self._select_option()
            elif event.key == pygame.K_ESCAPE:
                self.parent_phase._paused = False
                self.game._scene = self.parent_phase

    def _select_option(self):
        if self.cursor == 0: # CONTINUAR
            self.parent_phase._paused = False
            self.game._scene = self.parent_phase
        elif self.cursor == 1: # REINICIAR
            self.game.retry_phase()
        elif self.cursor == 2: # SAIR
            self.game.change_scene("title")

    def update(self, dt_ms):
        pass

    def draw(self, surface):
        # Desenha a fase por baixo
        self.parent_phase.draw(surface)
        
        # Desenha o overlay
        surface.blit(self.overlay, (0, 0))
        
        # Painel do menu
        menu_w, menu_h = 300, 250
        menu_x = (SCREEN_WIDTH - menu_w) // 2
        menu_y = (SCREEN_HEIGHT - menu_h) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_w, menu_h)
        
        draw_panel(surface, menu_rect, UI_PANEL, UI_BORDER, alpha=230)
        draw_pixel_border(surface, menu_rect, UI_BORDER, 2)
        
        # Título
        title_lbl = self.font_title.render("PAUSA", False, YELLOW)
        surface.blit(title_lbl, (SCREEN_WIDTH // 2 - title_lbl.get_width() // 2, menu_y + 20))
        
        # Opções
        for i, opt in enumerate(self.options):
            is_sel = (i == self.cursor)
            color = UI_SELECTED if is_sel else UI_TEXT
            
            if is_sel:
                # Indicador de seleção
                pygame.draw.rect(surface, (60, 50, 80), (menu_x + 10, menu_y + 80 + i * 45, menu_w - 20, 35))
                draw_pixel_border(surface, pygame.Rect(menu_x + 10, menu_y + 80 + i * 45, menu_w - 20, 35), UI_SELECTED, 1)
            
            lbl = self.font_menu.render(opt, False, color)
            surface.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, menu_y + 85 + i * 45))
            
        # Dica
        hint = self.font_hint.render("WASD/Setas para mover • Enter/E para selecionar", False, (140, 130, 160))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, menu_y + menu_h - 30))
