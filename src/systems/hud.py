"""
HUD — exibe corações, inventário e informações de fase.
"""
import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MAX_HEARTS, UI_BG, UI_PANEL, UI_BORDER,
    UI_TEXT, UI_TITLE, UI_SELECTED,
    BOY_COLOR, GIRL_COLOR,
    PIXEL_SCALE, PHASE_NAMES
)
from src.utils.assets import FontManager, draw_text, draw_panel, ui_img


class HUD:
    """
    HUD do jogo exibindo:
    - Corações de cada jogador
    - Inventário (itens coletados)
    - Nome da fase atual
    - Chaves coletadas / necessárias
    """

    def __init__(self):
        self.font_small = FontManager.pixel(12)
        self.font_med   = FontManager.pixel(14)
        self.font_phase = FontManager.pixel(16)

        # Carrega imagens de coração
        try:
            self._heart_full  = ui_img("heart_full.png",  scale=2)
            self._heart_empty = ui_img("heart_empty.png", scale=2)
        except:
            self._heart_full  = self._make_heart(True)
            self._heart_empty = self._make_heart(False)

        # Notificações temporárias
        self._notifications = []  # [(text, color, timer_ms)]

    def _make_heart(self, full):
        s = pygame.Surface((16, 16), pygame.SRCALPHA)
        color = (220, 50, 50) if full else (60, 60, 60)
        pixels = [(3,1),(4,1),(6,1),(7,1),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),
                  (2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(3,4),(4,4),(5,4),(6,4),(7,4),
                  (4,5),(5,5),(6,5),(5,6)]
        for px, py in pixels:
            s.set_at((px, py), color)
        return s

    def add_notification(self, text, color=(255, 220, 80), duration=2500):
        self._notifications.append({"text": text, "color": color, "timer": duration})

    def update(self, dt_ms):
        for n in self._notifications[:]:
            n["timer"] -= dt_ms
            if n["timer"] <= 0:
                self._notifications.remove(n)

    def draw(self, surface, players, phase_key, keys_collected, keys_needed):
        self._draw_phase_info(surface, phase_key, keys_collected, keys_needed)
        self._draw_player_hud(surface, players)
        self._draw_notifications(surface)

    def _draw_phase_info(self, surface, phase_key, keys_collected, keys_needed):
        """Barra superior com nome da fase e chaves."""
        bar_h = 28
        bar   = pygame.Surface((SCREEN_WIDTH, bar_h), pygame.SRCALPHA)
        bar.fill((10, 8, 20, 200))
        surface.blit(bar, (0, 0))
        pygame.draw.line(surface, UI_BORDER, (0, bar_h), (SCREEN_WIDTH, bar_h), 1)

        phase_name = PHASE_NAMES.get(phase_key, phase_key)
        draw_text(surface, phase_name,
                  SCREEN_WIDTH // 2, 6,
                  self.font_phase, UI_TITLE,
                  shadow=True, center=True)

        # Chaves
        key_text = f"Chaves: {keys_collected}/{keys_needed}"
        draw_text(surface, key_text,
                  SCREEN_WIDTH - 10, 7,
                  self.font_med, UI_SELECTED,
                  shadow=True, center=False)
        # Ajusta posição à direita
        rendered = self.font_med.render(key_text, False, UI_SELECTED)
        surface.blit(rendered, (SCREEN_WIDTH - rendered.get_width() - 8, 7))

    def _draw_player_hud(self, surface, players):
        """Painéis de vida e inventário de cada jogador."""
        for i, player in enumerate(players):
            if i == 0:
                x_start = 8
            else:
                x_start = SCREEN_WIDTH - 8 - 160

            y_start = SCREEN_HEIGHT - 56

            # Painel de fundo
            panel_rect = pygame.Rect(x_start, y_start, 160, 50)
            draw_panel(surface, panel_rect, (10, 8, 20), UI_BORDER, alpha=180)

            # Nome do jogador
            p_color = BOY_COLOR if player.gender == "boy" else GIRL_COLOR
            gender_label = "Menino" if player.gender == "boy" else "Menina"
            label = f"P{player.player_id} ({gender_label})"
            draw_text(surface, label, x_start + 6, y_start + 4,
                      self.font_small, p_color, shadow=True)

            # Corações
            hx = x_start + 6
            hy = y_start + 20
            for h in range(MAX_HEARTS):
                img = self._heart_full if h < player.hearts else self._heart_empty
                surface.blit(img, (hx + h * 20, hy))

            # Inventário (itens como texto pequeno)
            if player.inventory:
                inv_text = " ".join(player.inventory[:4])
                draw_text(surface, inv_text, x_start + 6, y_start + 38,
                          self.font_small, (180, 180, 140), shadow=False)

    def _draw_notifications(self, surface):
        """Notificações flutuantes no centro da tela."""
        ny = SCREEN_HEIGHT // 2 - 60
        for i, n in enumerate(self._notifications[-3:]):
            alpha = min(255, n["timer"] // 4)
            text  = n["text"]
            color = n["color"]
            rendered = self.font_med.render(text, False, color)
            rendered.set_alpha(alpha)
            nx = SCREEN_WIDTH // 2 - rendered.get_width() // 2
            surface.blit(rendered, (nx, ny + i * 22))
