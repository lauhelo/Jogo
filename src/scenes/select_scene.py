"""
Cena de Seleção de Personagem.
Cada jogador escolhe: Menino ou Menina.
P1 usa WASD + E para confirmar.
P2 usa Setas + Enter para confirmar.
"""
import pygame
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    UI_BG, UI_PANEL, UI_BORDER, UI_TITLE, UI_TEXT,
    UI_HIGHLIGHT, UI_SELECTED, UI_HOVER,
    BOY_COLOR, GIRL_COLOR, WHITE,
    SCENE_INTRO, SCENE_TITLE,
    PIXEL_SCALE
)
from src.utils.assets import (
    FontManager, draw_text, draw_panel,
    draw_pixel_border, sprite, ui_img
)


class SelectScene:
    """
    Tela de seleção de personagem para 2 jogadores.

    Layout:
    ┌─────────────────────────────────────────────┐
    │         ESCOLHA SEU PERSONAGEM              │
    │                                             │
    │  ┌──── JOGADOR 1 ────┐  ┌──── JOGADOR 2 ──┐│
    │  │  [MENINO] [MENINA]│  │ [MENINO] [MENINA]││
    │  │   WASD + E        │  │  Setas + Enter   ││
    │  └───────────────────┘  └──────────────────┘│
    │                                             │
    │         [INICIAR quando ambos ok]           │
    └─────────────────────────────────────────────┘
    """

    OPTIONS = ["boy", "girl"]
    LABELS  = {"boy": "MENINO", "girl": "MENINA"}
    COLORS  = {"boy": BOY_COLOR, "girl": GIRL_COLOR}

    def __init__(self, game):
        self.game = game

        self.font_title  = FontManager.pixel(34)
        self.font_sub    = FontManager.pixel(20)
        self.font_label  = FontManager.pixel(16)
        self.font_small  = FontManager.pixel(12)
        self.font_hint   = FontManager.pixel(13)

        # Estado de seleção por jogador: cursor e confirmação
        self._cursor    = [0, 0]    # índice em OPTIONS para cada jogador
        self._confirmed = [False, False]
        self._timer     = 0

        # Carrega sprites grandes para preview
        self._previews = {
            "boy":  sprite("boy_down_0.png",  scale=PIXEL_SCALE * 4),
            "girl": sprite("girl_down_0.png", scale=PIXEL_SCALE * 4),
        }

        # Animação de "bounce" nos ícones selecionados
        self._bounce = [0.0, 0.0]

        # Mensagem de feedback
        self._msg       = ""
        self._msg_timer = 0

    # ─── Eventos ─────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        # Voltar para título
        if event.key == pygame.K_ESCAPE:
            self.game.change_scene(SCENE_TITLE)
            return

        # ── Jogador 1 (WASD + E) ──────────────────────────────────────────
        if not self._confirmed[0]:
            if event.key == pygame.K_a:
                self._cursor[0] = (self._cursor[0] - 1) % len(self.OPTIONS)
            elif event.key == pygame.K_d:
                self._cursor[0] = (self._cursor[0] + 1) % len(self.OPTIONS)
            elif event.key == pygame.K_e:
                self._confirmed[0] = True
                self._show_msg(f"Jogador 1: {self.LABELS[self.OPTIONS[self._cursor[0]]]} confirmado!")
        else:
            # Permite desfazer com A ou D
            if event.key in (pygame.K_a, pygame.K_d):
                self._confirmed[0] = False

        # ── Jogador 2 (Setas + Enter) ─────────────────────────────────────
        if not self._confirmed[1]:
            if event.key == pygame.K_LEFT:
                self._cursor[1] = (self._cursor[1] - 1) % len(self.OPTIONS)
            elif event.key == pygame.K_RIGHT:
                self._cursor[1] = (self._cursor[1] + 1) % len(self.OPTIONS)
            elif event.key == pygame.K_RETURN:
                self._confirmed[1] = True
                self._show_msg(f"Jogador 2: {self.LABELS[self.OPTIONS[self._cursor[1]]]} confirmado!")
        else:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self._confirmed[1] = False

        # Ambos confirmados → iniciar jogo
        if self._confirmed[0] and self._confirmed[1]:
            self._start_game()

    def _show_msg(self, msg):
        self._msg       = msg
        self._msg_timer = 2000

    def _start_game(self):
        p1_gender = self.OPTIONS[self._cursor[0]]
        p2_gender = self.OPTIONS[self._cursor[1]]
        self.game.player_genders = [p1_gender, p2_gender]
        self.game.change_scene(SCENE_INTRO)

    # ─── Update ──────────────────────────────────────────────────────────────
    def update(self, dt_ms):
        self._timer     += dt_ms
        self._msg_timer  = max(0, self._msg_timer - dt_ms)
        for i in range(2):
            self._bounce[i] = math.sin(self._timer / 300 + i * math.pi) * 4

    # ─── Draw ─────────────────────────────────────────────────────────────────
    def draw(self, surface):
        surface.fill(UI_BG)
        self._draw_bg_pattern(surface)
        self._draw_title(surface)
        self._draw_player_panel(surface, 0, SCREEN_WIDTH // 4)
        self._draw_player_panel(surface, 1, 3 * SCREEN_WIDTH // 4)
        self._draw_divider(surface)
        self._draw_bottom(surface)

    def _draw_bg_pattern(self, surface):
        """Grade de pontos decorativa."""
        for x in range(0, SCREEN_WIDTH, 24):
            for y in range(0, SCREEN_HEIGHT, 24):
                pygame.draw.rect(surface, (25, 20, 45), (x, y, 2, 2))

    def _draw_title(self, surface):
        title = self.font_title.render("ESCOLHA SEU PERSONAGEM", False, UI_TITLE)
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        # Sombra
        shadow = self.font_title.render("ESCOLHA SEU PERSONAGEM", False, (40, 20, 60))
        surface.blit(shadow, (tx + 2, 32))
        surface.blit(title, (tx, 30))

        # Linha decorativa
        pygame.draw.line(surface, UI_BORDER,
                         (SCREEN_WIDTH // 2 - 280, 72),
                         (SCREEN_WIDTH // 2 + 280, 72), 1)

    def _draw_divider(self, surface):
        """Linha vertical central."""
        pygame.draw.line(surface, UI_BORDER,
                         (SCREEN_WIDTH // 2, 90),
                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80), 1)

    def _draw_player_panel(self, surface, player_idx, cx):
        """Desenha painel de seleção para um jogador."""
        confirmed = self._confirmed[player_idx]
        cursor    = self._cursor[player_idx]
        p_num     = player_idx + 1
        p_color   = BOY_COLOR if player_idx == 0 else GIRL_COLOR

        # ── Cabeçalho do jogador ─────────────────────────────────────────
        header_y = 90
        label    = f"JOGADOR {p_num}"
        header   = self.font_sub.render(label, False, p_color)
        surface.blit(header, (cx - header.get_width() // 2, header_y))

        if confirmed:
            ok = self.font_small.render("✓ CONFIRMADO", False, (100, 220, 100))
            surface.blit(ok, (cx - ok.get_width() // 2, header_y + 26))
        else:
            hint_text = "A/D + E" if player_idx == 0 else "◄/► + Enter"
            hint = self.font_small.render(hint_text, False, (140, 120, 180))
            surface.blit(hint, (cx - hint.get_width() // 2, header_y + 26))

        # ── Preview do personagem selecionado ────────────────────────────
        sel_gender  = self.OPTIONS[cursor]
        preview_img = self._previews[sel_gender]
        bounce_off  = int(self._bounce[player_idx]) if not confirmed else 0
        pw, ph      = preview_img.get_size()
        preview_x   = cx - pw // 2
        preview_y   = 150 + bounce_off

        # Sombra do personagem
        shadow_surf = pygame.Surface((pw, 8), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 60))
        surface.blit(shadow_surf, (preview_x, preview_y + ph + 2))

        surface.blit(preview_img, (preview_x, preview_y))

        # ── Opções (Menino / Menina) ──────────────────────────────────────
        opt_y = 310
        opt_w = 100
        opt_h = 36
        gap   = 20
        total_w = len(self.OPTIONS) * opt_w + (len(self.OPTIONS) - 1) * gap
        start_x = cx - total_w // 2

        for i, opt in enumerate(self.OPTIONS):
            ox = start_x + i * (opt_w + gap)
            oy = opt_y
            rect = pygame.Rect(ox, oy, opt_w, opt_h)

            is_selected = (i == cursor)
            is_confirmed_opt = confirmed and is_selected

            # Cor do painel
            if is_confirmed_opt:
                bg_col  = (30, 80, 30)
                bd_col  = (80, 200, 80)
            elif is_selected:
                bg_col  = self.COLORS[opt]
                bd_col  = UI_SELECTED
            else:
                bg_col  = UI_PANEL
                bd_col  = UI_BORDER

            draw_panel(surface, rect, bg_col, bd_col, alpha=200)
            if is_selected:
                draw_pixel_border(surface, rect, bd_col, 2)

            # Label
            lbl_color = WHITE if is_selected else (140, 130, 160)
            lbl = self.font_label.render(self.LABELS[opt], False, lbl_color)
            surface.blit(lbl, (ox + opt_w // 2 - lbl.get_width() // 2,
                                oy + opt_h // 2 - lbl.get_height() // 2))

            # Mini sprite dentro da opção
            mini = sprite(f"{opt}_down_0.png", scale=PIXEL_SCALE)
            mini_x = ox + opt_w // 2 - mini.get_width() // 2
            surface.blit(mini, (mini_x, oy - mini.get_height() - 4))

        # ── Nome do personagem selecionado ───────────────────────────────
        name_y = opt_y + opt_h + 16
        name_color = self.COLORS[sel_gender]
        name_lbl = self.font_sub.render(self.LABELS[sel_gender], False, name_color)
        surface.blit(name_lbl, (cx - name_lbl.get_width() // 2, name_y))

    def _draw_bottom(self, surface):
        """Rodapé com instrução de início."""
        both_confirmed = all(self._confirmed)
        y = SCREEN_HEIGHT - 65

        if both_confirmed:
            # Pulsação
            pulse = abs(math.sin(self._timer / 300))
            r, g, b = 100, 220, 100
            color = (int(r * pulse + 60), int(g * pulse + 60), int(b * pulse + 60))
            msg = self.font_sub.render("INICIANDO...", False, color)
            surface.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, y))
        else:
            remaining = []
            if not self._confirmed[0]:
                remaining.append("P1: pressione E")
            if not self._confirmed[1]:
                remaining.append("P2: pressione Enter")
            hint_text = "  |  ".join(remaining) + " para confirmar"
            hint = self.font_hint.render(hint_text, False, (140, 120, 180))
            surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, y))

        # Mensagem de feedback
        if self._msg_timer > 0:
            alpha = min(255, self._msg_timer // 4)
            msg_surf = self.font_small.render(self._msg, False, (180, 220, 180))
            surface.blit(msg_surf, (SCREEN_WIDTH // 2 - msg_surf.get_width() // 2,
                                    y + 22))

        # ESC para voltar
        esc = self.font_small.render("ESC: Voltar ao Menu", False, (80, 70, 100))
        surface.blit(esc, (SCREEN_WIDTH // 2 - esc.get_width() // 2,
                           SCREEN_HEIGHT - 20))
