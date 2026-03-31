"""
Constantes e configurações globais do jogo Escape Room.
Otimizado para Raspberry Pi com resolução 800x600.
"""

# ─── Tela ────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 30
TITLE         = "Escape Room"

# ─── Tile ────────────────────────────────────────────────────────────────────
TILE_SIZE     = 32   # pixels por tile no mundo
PIXEL_SCALE   = 2    # escala dos sprites (16px * 2 = 32px)

# ─── Cores ───────────────────────────────────────────────────────────────────
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
DARK_GRAY   = (30,  30,  30)
GRAY        = (100, 100, 100)
LIGHT_GRAY  = (180, 180, 180)
RED         = (200,  50,  50)
GREEN       = (50,  180,  50)
BLUE        = (50,  100, 200)
YELLOW      = (255, 220,  50)
PURPLE      = (150,  50, 200)
ORANGE      = (230, 120,  30)
PINK        = (220,  80, 140)
CYAN        = (50,  200, 200)
DARK_BLUE   = (20,  20,  80)
CREAM       = (240, 230, 200)

# Cores de UI
UI_BG           = (15,  12,  30)
UI_PANEL        = (30,  25,  50)
UI_BORDER       = (80,  60, 120)
UI_TITLE        = (255, 220,  80)
UI_TEXT         = (220, 220, 240)
UI_HIGHLIGHT    = (100, 180, 255)
UI_SELECTED     = (255, 200,  50)
UI_HOVER        = (60,  50,  90)

# Cores de personagem
BOY_COLOR       = (60,  100, 200)
GIRL_COLOR      = (220,  80, 120)

# ─── Jogadores ───────────────────────────────────────────────────────────────
PLAYER1_KEYS = {
    "up":      "w",
    "down":    "s",
    "left":    "a",
    "right":   "d",
    "action":  "e",
}
PLAYER2_KEYS = {
    "up":      "up",
    "down":    "down",
    "left":    "left",
    "right":   "right",
    "action":  "return",
}

# Mapeamento pygame key names → pygame.K_*
import pygame
KEY_MAP = {
    "w":      pygame.K_w,
    "s":      pygame.K_s,
    "a":      pygame.K_a,
    "d":      pygame.K_d,
    "e":      pygame.K_e,
    "up":     pygame.K_UP,
    "down":   pygame.K_DOWN,
    "left":   pygame.K_LEFT,
    "right":  pygame.K_RIGHT,
    "return": pygame.K_RETURN,
    "space":  pygame.K_SPACE,
    "escape": pygame.K_ESCAPE,
}

# ─── Sistema de vida ─────────────────────────────────────────────────────────
MAX_HEARTS          = 3
INVULNERABILITY_MS  = 1500   # ms de invulnerabilidade após levar dano

# ─── Fases ───────────────────────────────────────────────────────────────────
SCENE_TITLE         = "title"
SCENE_SELECT        = "select"
SCENE_INTRO         = "intro"
SCENE_GAME          = "game"
SCENE_GAMEOVER      = "gameover"
SCENE_WIN           = "win"
SCENE_CREDITS       = "credits"

PHASE_GARDEN        = "garden"
PHASE_OFFICE        = "office"
PHASE_KITCHEN       = "kitchen"
PHASE_BEDROOM1      = "bedroom1"
PHASE_ATTIC         = "attic"
PHASE_BEDROOM2      = "bedroom2"
PHASE_BASEMENT      = "basement"
PHASE_GARAGE        = "garage"

PHASE_ORDER = [
    PHASE_GARDEN,
    PHASE_OFFICE,
    PHASE_KITCHEN,
    PHASE_BEDROOM1,
    PHASE_ATTIC,
    PHASE_BEDROOM2,
    PHASE_BASEMENT,
    PHASE_GARAGE,
]

PHASE_NAMES = {
    PHASE_GARDEN:   "Jardim",
    PHASE_OFFICE:   "Escritório",
    PHASE_KITCHEN:  "Cozinha",
    PHASE_BEDROOM1: "Quarto 1",
    PHASE_ATTIC:    "Sótão",
    PHASE_BEDROOM2: "Quarto 2 (Suíte)",
    PHASE_BASEMENT: "Porão",
    PHASE_GARAGE:   "Garagem",
}

# ─── Velocidades ─────────────────────────────────────────────────────────────
PLAYER_SPEED    = 2
MOB_SPEED_SLOW  = 0.6
MOB_SPEED_MED   = 1.0
MOB_SPEED_FAST  = 1.6
MOB_SPEED_VFAST = 2.2

# ─── Paths ───────────────────────────────────────────────────────────────────
import os
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR  = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
TILES_DIR   = os.path.join(ASSETS_DIR, "tiles")
UI_DIR      = os.path.join(ASSETS_DIR, "ui")
