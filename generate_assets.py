"""
Gerador de assets de pixel art para o jogo Escape Room.
Cria todos os sprites, tiles e elementos de UI usando pygame + numpy.
"""
import pygame
import numpy as np
import os

pygame.init()

ASSETS_DIR = "/home/ubuntu/escape_room/assets"

def save_surface(surface, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pygame.image.save(surface, path)
    print(f"Salvo: {path}")

def make_surface(w, h):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    return s

# ─────────────────────────────────────────────
# PALETAS
# ─────────────────────────────────────────────
SKIN_LIGHT  = (255, 213, 170)
SKIN_DARK   = (200, 150, 100)
HAIR_BOY    = (80, 50, 20)
HAIR_GIRL   = (200, 100, 50)
SHIRT_BOY   = (60, 100, 200)
SHIRT_GIRL  = (220, 80, 120)
PANTS_BOY   = (50, 50, 120)
SKIRT_GIRL  = (240, 140, 180)
SHOES       = (60, 40, 20)
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

# ─────────────────────────────────────────────
# SPRITE MENINO (16x24 px)
# ─────────────────────────────────────────────
def draw_boy_sprite(direction="down", frame=0):
    """Desenha sprite do menino 16x24"""
    s = make_surface(16, 24)
    # Cabeça
    for x in range(4, 12):
        for y in range(0, 8):
            s.set_at((x, y), SKIN_LIGHT)
    # Cabelo
    for x in range(4, 12):
        s.set_at((x, 0), HAIR_BOY)
        s.set_at((x, 1), HAIR_BOY)
    for y in range(0, 4):
        s.set_at((4, y), HAIR_BOY)
        s.set_at((11, y), HAIR_BOY)
    # Olhos (dependendo da direção)
    if direction == "down":
        s.set_at((6, 4), BLACK)
        s.set_at((9, 4), BLACK)
    elif direction == "up":
        pass  # sem olhos visíveis
    elif direction == "left":
        s.set_at((5, 4), BLACK)
    elif direction == "right":
        s.set_at((10, 4), BLACK)
    # Corpo (camisa)
    for x in range(3, 13):
        for y in range(8, 16):
            s.set_at((x, y), SHIRT_BOY)
    # Braços
    for y in range(8, 15):
        s.set_at((2, y), SKIN_LIGHT)
        s.set_at((13, y), SKIN_LIGHT)
    # Calças
    for x in range(3, 8):
        for y in range(16, 22):
            s.set_at((x, y), PANTS_BOY)
    for x in range(8, 13):
        for y in range(16, 22):
            s.set_at((x, y), PANTS_BOY)
    # Separação das pernas
    s.set_at((7, 17), TRANSPARENT)
    s.set_at((8, 17), TRANSPARENT)
    # Sapatos
    for x in range(3, 8):
        for y in range(22, 24):
            s.set_at((x, y), SHOES)
    for x in range(8, 13):
        for y in range(22, 24):
            s.set_at((x, y), SHOES)
    # Animação de caminhada (frame 1 = pernas abertas)
    if frame == 1:
        for x in range(3, 7):
            for y in range(17, 22):
                s.set_at((x, y), PANTS_BOY)
        for x in range(9, 13):
            for y in range(17, 22):
                s.set_at((x, y), PANTS_BOY)
    return s

# ─────────────────────────────────────────────
# SPRITE MENINA (16x24 px)
# ─────────────────────────────────────────────
def draw_girl_sprite(direction="down", frame=0):
    """Desenha sprite da menina 16x24"""
    s = make_surface(16, 24)
    # Cabeça
    for x in range(4, 12):
        for y in range(0, 8):
            s.set_at((x, y), SKIN_LIGHT)
    # Cabelo longo
    for x in range(3, 13):
        s.set_at((x, 0), HAIR_GIRL)
        s.set_at((x, 1), HAIR_GIRL)
    for y in range(0, 10):
        s.set_at((3, y), HAIR_GIRL)
        s.set_at((12, y), HAIR_GIRL)
    for y in range(0, 3):
        s.set_at((4, y), HAIR_GIRL)
        s.set_at((11, y), HAIR_GIRL)
    # Olhos
    if direction == "down":
        s.set_at((6, 4), BLACK)
        s.set_at((9, 4), BLACK)
        # Cílios
        s.set_at((6, 3), BLACK)
        s.set_at((9, 3), BLACK)
    elif direction == "left":
        s.set_at((5, 4), BLACK)
    elif direction == "right":
        s.set_at((10, 4), BLACK)
    # Blusa
    for x in range(3, 13):
        for y in range(8, 15):
            s.set_at((x, y), SHIRT_GIRL)
    # Braços
    for y in range(8, 15):
        s.set_at((2, y), SKIN_LIGHT)
        s.set_at((13, y), SKIN_LIGHT)
    # Saia
    for x in range(2, 14):
        for y in range(15, 21):
            s.set_at((x, y), SKIRT_GIRL)
    # Pernas
    for x in range(4, 7):
        for y in range(21, 24):
            s.set_at((x, y), SKIN_LIGHT)
    for x in range(9, 12):
        for y in range(21, 24):
            s.set_at((x, y), SKIN_LIGHT)
    # Sapatos
    for x in range(4, 7):
        s.set_at((x, 23), SHOES)
    for x in range(9, 12):
        s.set_at((x, 23), SHOES)
    return s

# ─────────────────────────────────────────────
# SPRITE AMIGO IMAGINÁRIO (fantasminha luminoso 16x24)
# ─────────────────────────────────────────────
def draw_imaginary_friend():
    s = make_surface(16, 24)
    GLOW = (180, 220, 255, 200)
    GLOW2 = (140, 190, 255, 150)
    GLOW_EYE = (50, 100, 200)
    # Corpo oval
    for x in range(4, 12):
        for y in range(2, 18):
            s.set_at((x, y), GLOW)
    for x in range(3, 13):
        for y in range(4, 16):
            s.set_at((x, y), GLOW)
    for x in range(2, 14):
        for y in range(6, 14):
            s.set_at((x, y), GLOW)
    # Cauda ondulada
    for x in range(3, 13):
        for y in range(16, 20):
            s.set_at((x, y), GLOW2)
    for x in range(4, 6):
        s.set_at((x, 20), GLOW2)
    for x in range(7, 9):
        s.set_at((x, 21), GLOW2)
    for x in range(10, 12):
        s.set_at((x, 20), GLOW2)
    # Olhos
    s.set_at((6, 8), GLOW_EYE)
    s.set_at((9, 8), GLOW_EYE)
    s.set_at((6, 9), GLOW_EYE)
    s.set_at((9, 9), GLOW_EYE)
    return s

# ─────────────────────────────────────────────
# MOB GENÉRICO (slime 12x10)
# ─────────────────────────────────────────────
def draw_mob_slime(color=(100, 200, 80)):
    s = make_surface(16, 16)
    # Corpo
    for x in range(2, 14):
        for y in range(4, 12):
            s.set_at((x, y), color)
    for x in range(4, 12):
        for y in range(2, 14):
            s.set_at((x, y), color)
    for x in range(3, 13):
        for y in range(3, 13):
            s.set_at((x, y), color)
    # Olhos
    s.set_at((5, 6), BLACK)
    s.set_at((10, 6), BLACK)
    s.set_at((5, 7), BLACK)
    s.set_at((10, 7), BLACK)
    # Boca
    for x in range(6, 10):
        s.set_at((x, 9), BLACK)
    return s

def draw_mob_ghost():
    s = make_surface(16, 20)
    GHOST_C = (180, 180, 220, 200)
    GHOST_D = (140, 140, 180, 150)
    for x in range(3, 13):
        for y in range(0, 14):
            s.set_at((x, y), GHOST_C)
    for x in range(2, 14):
        for y in range(4, 12):
            s.set_at((x, y), GHOST_C)
    # Cauda
    for x in range(3, 6):
        for y in range(14, 18):
            s.set_at((x, y), GHOST_D)
    for x in range(6, 10):
        for y in range(14, 19):
            s.set_at((x, y), GHOST_D)
    for x in range(10, 13):
        for y in range(14, 18):
            s.set_at((x, y), GHOST_D)
    # Olhos
    s.set_at((5, 6), (50, 50, 150))
    s.set_at((6, 6), (50, 50, 150))
    s.set_at((9, 6), (50, 50, 150))
    s.set_at((10, 6), (50, 50, 150))
    return s

def draw_mob_spider():
    s = make_surface(20, 16)
    BODY = (40, 20, 60)
    # Corpo
    for x in range(6, 14):
        for y in range(3, 11):
            s.set_at((x, y), BODY)
    for x in range(7, 13):
        for y in range(2, 12):
            s.set_at((x, y), BODY)
    # Pernas
    for i in range(4):
        y = 4 + i * 2
        s.set_at((3, y), BODY)
        s.set_at((4, y), BODY)
        s.set_at((5, y+1), BODY)
        s.set_at((15, y), BODY)
        s.set_at((16, y), BODY)
        s.set_at((14, y+1), BODY)
    # Olhos
    s.set_at((8, 5), (255, 50, 50))
    s.set_at((11, 5), (255, 50, 50))
    return s

# ─────────────────────────────────────────────
# TILES DE CENÁRIO
# ─────────────────────────────────────────────
def draw_tile_grass():
    s = make_surface(16, 16)
    s.fill((60, 160, 60))
    # Detalhes de grama
    for x in [2, 5, 8, 11, 14]:
        s.set_at((x, 2), (80, 200, 80))
        s.set_at((x, 1), (80, 200, 80))
    for x in [1, 4, 7, 10, 13]:
        s.set_at((x, 4), (50, 140, 50))
    return s

def draw_tile_grass_special():
    """Grama com pixels diferentes (local para cavar)"""
    s = draw_tile_grass()
    for x in range(4, 12):
        for y in range(6, 12):
            s.set_at((x, y), (80, 120, 40))
    return s

def draw_tile_floor_wood():
    s = make_surface(16, 16)
    s.fill((160, 100, 50))
    for y in [4, 8, 12]:
        for x in range(16):
            s.set_at((x, y), (130, 80, 30))
    for x in [0, 8]:
        for y in range(16):
            s.set_at((x, y), (140, 90, 40))
    return s

def draw_tile_floor_kitchen():
    s = make_surface(16, 16)
    s.fill((220, 220, 200))
    for x in range(0, 16, 8):
        for y in range(0, 16, 8):
            for i in range(8):
                for j in range(8):
                    if (x // 8 + y // 8) % 2 == 0:
                        s.set_at((x + i, y + j), (200, 200, 180))
    for x in range(0, 16, 8):
        for y in range(0, 16, 8):
            pygame.draw.rect(s, (180, 180, 160), (x, y, 8, 8), 1)
    return s

def draw_tile_floor_bedroom():
    s = make_surface(16, 16)
    s.fill((180, 140, 180))
    for x in range(0, 16, 4):
        for y in range(16):
            s.set_at((x, y), (160, 120, 160))
    return s

def draw_tile_wall():
    s = make_surface(16, 16)
    s.fill((120, 100, 80))
    for y in [0, 8]:
        for x in range(16):
            s.set_at((x, y), (100, 80, 60))
    for x in [0, 8]:
        for y in range(16):
            s.set_at((x, y), (100, 80, 60))
    return s

def draw_tile_wall_office():
    s = make_surface(16, 16)
    s.fill((180, 170, 160))
    for y in [0, 8]:
        for x in range(16):
            s.set_at((x, y), (160, 150, 140))
    return s

def draw_tile_stone():
    s = make_surface(16, 16)
    s.fill((140, 140, 140))
    for x in range(0, 16, 4):
        for y in range(0, 16, 4):
            s.set_at((x, y), (120, 120, 120))
    return s

def draw_tile_dark_floor():
    """Piso escuro para sótão/porão"""
    s = make_surface(16, 16)
    s.fill((60, 50, 40))
    for x in range(0, 16, 4):
        for y in range(16):
            s.set_at((x, y), (50, 40, 30))
    return s

# ─────────────────────────────────────────────
# OBJETOS INTERATIVOS
# ─────────────────────────────────────────────
def draw_key(color=(255, 215, 0)):
    s = make_surface(12, 12)
    # Cabeça da chave
    for x in range(2, 7):
        for y in range(2, 7):
            s.set_at((x, y), color)
    s.set_at((4, 4), BLACK)  # buraco
    # Cabo
    for y in range(7, 11):
        s.set_at((4, y), color)
    s.set_at((5, 8), color)
    s.set_at((6, 9), color)
    return s

def draw_heart(full=True):
    s = make_surface(12, 12)
    RED = (220, 50, 50)
    DARK_RED = (160, 30, 30)
    color = RED if full else (80, 80, 80)
    # Forma de coração
    pixels = [
        (2,1),(3,1),(5,1),(6,1),
        (1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),
        (1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),
        (2,4),(3,4),(4,4),(5,4),(6,4),
        (3,5),(4,5),(5,5),
        (4,6),
    ]
    for px, py in pixels:
        s.set_at((px, py), color)
    if full:
        s.set_at((2, 2), DARK_RED)
        s.set_at((3, 2), DARK_RED)
    return s

def draw_door(locked=True):
    s = make_surface(24, 32)
    WOOD = (140, 90, 40)
    DARK_WOOD = (110, 70, 20)
    METAL = (180, 180, 100)
    s.fill(WOOD)
    # Bordas
    for x in range(24):
        s.set_at((x, 0), DARK_WOOD)
        s.set_at((x, 31), DARK_WOOD)
    for y in range(32):
        s.set_at((0, y), DARK_WOOD)
        s.set_at((23, y), DARK_WOOD)
    # Painel decorativo
    pygame.draw.rect(s, DARK_WOOD, (3, 3, 18, 12), 1)
    pygame.draw.rect(s, DARK_WOOD, (3, 17, 18, 12), 1)
    # Maçaneta
    for x in range(17, 21):
        for y in range(14, 18):
            s.set_at((x, y), METAL)
    # Cadeado se trancada
    if locked:
        for x in range(10, 14):
            for y in range(13, 18):
                s.set_at((x, y), (200, 180, 50))
        s.set_at((11, 12), (200, 180, 50))
        s.set_at((12, 12), (200, 180, 50))
        s.set_at((11, 11), (200, 180, 50))
        s.set_at((12, 11), (200, 180, 50))
    return s

def draw_chest():
    s = make_surface(20, 16)
    BROWN = (120, 70, 30)
    GOLD = (200, 170, 50)
    s.fill(BROWN)
    # Tampa
    for x in range(20):
        for y in range(6):
            s.set_at((x, y), (140, 90, 50))
    # Faixa dourada
    for x in range(20):
        s.set_at((x, 6), GOLD)
        s.set_at((x, 7), GOLD)
    # Fechadura
    for x in range(8, 12):
        for y in range(5, 10):
            s.set_at((x, y), GOLD)
    return s

def draw_shovel():
    s = make_surface(8, 20)
    BROWN = (120, 70, 30)
    GRAY = (150, 150, 150)
    # Cabo
    for y in range(4, 18):
        s.set_at((3, y), BROWN)
        s.set_at((4, y), BROWN)
    # Pá
    for x in range(1, 7):
        for y in range(0, 6):
            s.set_at((x, y), GRAY)
    return s

def draw_rock():
    s = make_surface(16, 14)
    GRAY = (130, 130, 130)
    LGRAY = (160, 160, 160)
    DGRAY = (100, 100, 100)
    for x in range(2, 14):
        for y in range(2, 12):
            s.set_at((x, y), GRAY)
    for x in range(4, 12):
        for y in range(0, 14):
            s.set_at((x, y), GRAY)
    for x in range(3, 7):
        for y in range(2, 5):
            s.set_at((x, y), LGRAY)
    for x in range(10, 13):
        for y in range(8, 12):
            s.set_at((x, y), DGRAY)
    return s

def draw_flower(color=(255, 100, 100)):
    s = make_surface(10, 12)
    GREEN = (60, 160, 60)
    YELLOW = (255, 220, 50)
    # Caule
    for y in range(6, 12):
        s.set_at((4, y), GREEN)
        s.set_at((5, y), GREEN)
    # Pétalas
    for x in range(2, 8):
        s.set_at((x, 4), color)
    for y in range(2, 6):
        s.set_at((1, y), color)
        s.set_at((8, y), color)
    # Centro
    for x in range(3, 7):
        for y in range(2, 6):
            s.set_at((x, y), YELLOW)
    return s

def draw_book():
    s = make_surface(12, 14)
    RED = (180, 50, 50)
    CREAM = (240, 230, 200)
    s.fill(RED)
    for x in range(1, 11):
        for y in range(1, 13):
            s.set_at((x, y), CREAM)
    for y in range(1, 13):
        s.set_at((1, y), RED)
        s.set_at((2, y), RED)
    # Linhas de texto
    for y in [3, 5, 7, 9, 11]:
        for x in range(4, 10):
            s.set_at((x, y), (180, 170, 150))
    return s

def draw_bed():
    s = make_surface(32, 24)
    FRAME = (120, 80, 40)
    SHEET = (220, 220, 240)
    PILLOW = (240, 240, 255)
    # Frame
    s.fill(FRAME)
    # Colchão
    for x in range(2, 30):
        for y in range(4, 22):
            s.set_at((x, y), SHEET)
    # Travesseiro
    for x in range(3, 14):
        for y in range(5, 11):
            s.set_at((x, y), PILLOW)
    for x in range(18, 29):
        for y in range(5, 11):
            s.set_at((x, y), PILLOW)
    return s

def draw_bookshelf():
    s = make_surface(32, 32)
    WOOD = (140, 90, 40)
    BOOKS = [(180, 50, 50), (50, 100, 180), (50, 160, 50), (180, 160, 50), (160, 50, 160)]
    s.fill(WOOD)
    # Prateleiras
    for y in [8, 16, 24]:
        for x in range(32):
            s.set_at((x, y), (110, 70, 20))
    # Livros
    bx = 1
    for i, bc in enumerate(BOOKS * 2):
        bw = 4 + (i % 2)
        shelf_y = 1 + (i // 5) * 8
        for x in range(bx, min(bx + bw, 31)):
            for y in range(shelf_y, shelf_y + 7):
                s.set_at((x, y), bc)
        bx += bw + 1
        if bx > 28:
            bx = 1
    return s

def draw_stove():
    s = make_surface(32, 32)
    GRAY = (160, 160, 160)
    DARK = (100, 100, 100)
    RED = (220, 80, 50)
    s.fill(GRAY)
    # Queimadores
    for cx, cy in [(8, 8), (24, 8), (8, 20), (24, 20)]:
        for x in range(cx-4, cx+4):
            for y in range(cy-4, cy+4):
                if abs(x-cx) + abs(y-cy) < 5:
                    s.set_at((x, y), DARK)
    # Porta do forno
    for x in range(4, 28):
        for y in range(22, 30):
            s.set_at((x, y), DARK)
    pygame.draw.rect(s, (80, 80, 80), (6, 24, 20, 4), 1)
    return s

def draw_cabinet():
    s = make_surface(24, 28)
    WOOD = (150, 100, 50)
    DARK = (110, 70, 20)
    METAL = (180, 180, 180)
    s.fill(WOOD)
    # Divisória
    for y in range(28):
        s.set_at((11, y), DARK)
        s.set_at((12, y), DARK)
    # Bordas
    pygame.draw.rect(s, DARK, (0, 0, 24, 28), 1)
    # Puxadores
    for x in range(4, 8):
        for y in range(12, 15):
            s.set_at((x, y), METAL)
    for x in range(16, 20):
        for y in range(12, 15):
            s.set_at((x, y), METAL)
    return s

def draw_battery():
    s = make_surface(12, 20)
    GREEN = (50, 180, 50)
    DARK = (30, 120, 30)
    GRAY = (180, 180, 180)
    s.fill(GREEN)
    pygame.draw.rect(s, DARK, (0, 0, 12, 20), 1)
    # Terminais
    for x in range(3, 9):
        for y in range(0, 3):
            s.set_at((x, y), GRAY)
    # Indicador de carga
    for x in range(2, 10):
        for y in range(5, 15):
            s.set_at((x, y), DARK)
    for x in range(2, 8):
        for y in range(5, 12):
            s.set_at((x, y), (100, 220, 100))
    return s

def draw_car():
    s = make_surface(48, 32)
    RED_CAR = (200, 50, 50)
    DARK_RED = (150, 30, 30)
    WINDOW = (150, 200, 220, 180)
    WHEEL = (40, 40, 40)
    YELLOW = (255, 220, 50)
    s.fill((0, 0, 0, 0))
    # Corpo
    for x in range(4, 44):
        for y in range(12, 28):
            s.set_at((x, y), RED_CAR)
    # Teto
    for x in range(10, 38):
        for y in range(4, 13):
            s.set_at((x, y), RED_CAR)
    # Janelas
    for x in range(12, 22):
        for y in range(5, 12):
            s.set_at((x, y), WINDOW)
    for x in range(24, 36):
        for y in range(5, 12):
            s.set_at((x, y), WINDOW)
    # Rodas
    for cx, cy in [(10, 26), (38, 26)]:
        for x in range(cx-5, cx+5):
            for y in range(cy-4, cy+4):
                if abs(x-cx)*abs(x-cx) + abs(y-cy)*abs(y-cy) < 20:
                    s.set_at((x, y), WHEEL)
    # Faróis
    for x in range(4, 8):
        for y in range(14, 18):
            s.set_at((x, y), YELLOW)
    return s

def draw_button(color=(100, 180, 100)):
    s = make_surface(12, 12)
    for x in range(2, 10):
        for y in range(2, 10):
            s.set_at((x, y), color)
    pygame.draw.rect(s, (60, 60, 60), (2, 2, 8, 8), 1)
    for x in range(3, 6):
        for y in range(3, 6):
            s.set_at((x, y), tuple(min(255, c + 60) for c in color))
    return s

def draw_mirror():
    s = make_surface(16, 24)
    FRAME = (180, 150, 80)
    GLASS = (200, 220, 240, 180)
    s.fill(FRAME)
    for x in range(2, 14):
        for y in range(2, 20):
            s.set_at((x, y), GLASS)
    # Reflexo
    for x in range(3, 8):
        for y in range(3, 10):
            s.set_at((x, y), (220, 235, 250, 200))
    return s

def draw_box():
    s = make_surface(20, 18)
    BROWN = (180, 140, 80)
    DARK = (140, 100, 50)
    s.fill(BROWN)
    pygame.draw.rect(s, DARK, (0, 0, 20, 18), 1)
    # Fita
    for y in range(18):
        s.set_at((9, y), DARK)
        s.set_at((10, y), DARK)
    for x in range(20):
        s.set_at((x, 8), DARK)
        s.set_at((x, 9), DARK)
    return s

def draw_pillow():
    s = make_surface(20, 14)
    WHITE_P = (240, 240, 255)
    SHADOW = (200, 200, 220)
    s.fill(WHITE_P)
    pygame.draw.rect(s, SHADOW, (0, 0, 20, 14), 1)
    for x in range(2, 18):
        for y in range(2, 5):
            s.set_at((x, y), (220, 220, 240))
    return s

# ─────────────────────────────────────────────
# UI ELEMENTS
# ─────────────────────────────────────────────
def draw_selection_boy_icon():
    """Ícone grande para seleção de personagem (menino) 48x64"""
    s = make_surface(48, 64)
    # Escala 3x do sprite normal
    small = draw_boy_sprite("down", 0)
    scaled = pygame.transform.scale(small, (48, 72))
    s.blit(scaled, (0, -4))
    return s

def draw_selection_girl_icon():
    """Ícone grande para seleção de personagem (menina) 48x64"""
    s = make_surface(48, 64)
    small = draw_girl_sprite("down", 0)
    scaled = pygame.transform.scale(small, (48, 72))
    s.blit(scaled, (0, -4))
    return s

# ─────────────────────────────────────────────
# SPRITE SHEETS (walk animations)
# ─────────────────────────────────────────────
def make_spritesheet_boy():
    """Cria spritesheet 4 direções x 2 frames = 8 frames (16x24 cada)"""
    sheet = make_surface(128, 48)  # 8 frames de 16x24 em 2 linhas
    directions = ["down", "up", "left", "right"]
    for di, direction in enumerate(directions):
        for fi in range(2):
            sprite = draw_boy_sprite(direction, fi)
            sheet.blit(sprite, (di * 16 + fi * 64, 0))
    # Linha 2: frames de animação extras
    for di, direction in enumerate(directions):
        sprite = draw_boy_sprite(direction, 0)
        sheet.blit(sprite, (di * 16, 24))
    return sheet

def make_spritesheet_girl():
    sheet = make_surface(128, 48)
    directions = ["down", "up", "left", "right"]
    for di, direction in enumerate(directions):
        for fi in range(2):
            sprite = draw_girl_sprite(direction, fi)
            sheet.blit(sprite, (di * 16 + fi * 64, 0))
    for di, direction in enumerate(directions):
        sprite = draw_girl_sprite(direction, 0)
        sheet.blit(sprite, (di * 16, 24))
    return sheet

# ─────────────────────────────────────────────
# SALVAR TODOS OS ASSETS
# ─────────────────────────────────────────────
def generate_all():
    print("Gerando assets de pixel art...")

    # Sprites de personagens
    save_surface(draw_boy_sprite("down", 0),  f"{ASSETS_DIR}/sprites/boy_down_0.png")
    save_surface(draw_boy_sprite("down", 1),  f"{ASSETS_DIR}/sprites/boy_down_1.png")
    save_surface(draw_boy_sprite("up", 0),    f"{ASSETS_DIR}/sprites/boy_up_0.png")
    save_surface(draw_boy_sprite("up", 1),    f"{ASSETS_DIR}/sprites/boy_up_1.png")
    save_surface(draw_boy_sprite("left", 0),  f"{ASSETS_DIR}/sprites/boy_left_0.png")
    save_surface(draw_boy_sprite("left", 1),  f"{ASSETS_DIR}/sprites/boy_left_1.png")
    save_surface(draw_boy_sprite("right", 0), f"{ASSETS_DIR}/sprites/boy_right_0.png")
    save_surface(draw_boy_sprite("right", 1), f"{ASSETS_DIR}/sprites/boy_right_1.png")

    save_surface(draw_girl_sprite("down", 0),  f"{ASSETS_DIR}/sprites/girl_down_0.png")
    save_surface(draw_girl_sprite("down", 1),  f"{ASSETS_DIR}/sprites/girl_down_1.png")
    save_surface(draw_girl_sprite("up", 0),    f"{ASSETS_DIR}/sprites/girl_up_0.png")
    save_surface(draw_girl_sprite("up", 1),    f"{ASSETS_DIR}/sprites/girl_up_1.png")
    save_surface(draw_girl_sprite("left", 0),  f"{ASSETS_DIR}/sprites/girl_left_0.png")
    save_surface(draw_girl_sprite("left", 1),  f"{ASSETS_DIR}/sprites/girl_left_1.png")
    save_surface(draw_girl_sprite("right", 0), f"{ASSETS_DIR}/sprites/girl_right_0.png")
    save_surface(draw_girl_sprite("right", 1), f"{ASSETS_DIR}/sprites/girl_right_1.png")

    save_surface(draw_imaginary_friend(), f"{ASSETS_DIR}/sprites/imaginary_friend.png")

    # Spritesheets
    save_surface(make_spritesheet_boy(),  f"{ASSETS_DIR}/sprites/boy_sheet.png")
    save_surface(make_spritesheet_girl(), f"{ASSETS_DIR}/sprites/girl_sheet.png")

    # Mobs
    save_surface(draw_mob_slime((100, 200, 80)),   f"{ASSETS_DIR}/sprites/mob_slime_green.png")
    save_surface(draw_mob_slime((200, 100, 80)),   f"{ASSETS_DIR}/sprites/mob_slime_red.png")
    save_surface(draw_mob_slime((80, 100, 200)),   f"{ASSETS_DIR}/sprites/mob_slime_blue.png")
    save_surface(draw_mob_ghost(),                 f"{ASSETS_DIR}/sprites/mob_ghost.png")
    save_surface(draw_mob_spider(),                f"{ASSETS_DIR}/sprites/mob_spider.png")

    # Tiles
    save_surface(draw_tile_grass(),          f"{ASSETS_DIR}/tiles/grass.png")
    save_surface(draw_tile_grass_special(),  f"{ASSETS_DIR}/tiles/grass_special.png")
    save_surface(draw_tile_floor_wood(),     f"{ASSETS_DIR}/tiles/floor_wood.png")
    save_surface(draw_tile_floor_kitchen(),  f"{ASSETS_DIR}/tiles/floor_kitchen.png")
    save_surface(draw_tile_floor_bedroom(),  f"{ASSETS_DIR}/tiles/floor_bedroom.png")
    save_surface(draw_tile_wall(),           f"{ASSETS_DIR}/tiles/wall.png")
    save_surface(draw_tile_wall_office(),    f"{ASSETS_DIR}/tiles/wall_office.png")
    save_surface(draw_tile_stone(),          f"{ASSETS_DIR}/tiles/stone.png")
    save_surface(draw_tile_dark_floor(),     f"{ASSETS_DIR}/tiles/floor_dark.png")

    # Objetos
    save_surface(draw_key(),                 f"{ASSETS_DIR}/sprites/key.png")
    save_surface(draw_key((200, 200, 200)),  f"{ASSETS_DIR}/sprites/key_silver.png")
    save_surface(draw_heart(True),           f"{ASSETS_DIR}/ui/heart_full.png")
    save_surface(draw_heart(False),          f"{ASSETS_DIR}/ui/heart_empty.png")
    save_surface(draw_door(True),            f"{ASSETS_DIR}/sprites/door_locked.png")
    save_surface(draw_door(False),           f"{ASSETS_DIR}/sprites/door_open.png")
    save_surface(draw_chest(),               f"{ASSETS_DIR}/sprites/chest.png")
    save_surface(draw_shovel(),              f"{ASSETS_DIR}/sprites/shovel.png")
    save_surface(draw_rock(),                f"{ASSETS_DIR}/sprites/rock.png")
    save_surface(draw_flower((255, 100, 100)), f"{ASSETS_DIR}/sprites/flower_red.png")
    save_surface(draw_flower((100, 100, 255)), f"{ASSETS_DIR}/sprites/flower_blue.png")
    save_surface(draw_flower((255, 220, 50)),  f"{ASSETS_DIR}/sprites/flower_yellow.png")
    save_surface(draw_flower((150, 50, 200)),  f"{ASSETS_DIR}/sprites/flower_purple.png")
    save_surface(draw_book(),                f"{ASSETS_DIR}/sprites/book.png")
    save_surface(draw_bed(),                 f"{ASSETS_DIR}/sprites/bed.png")
    save_surface(draw_bookshelf(),           f"{ASSETS_DIR}/sprites/bookshelf.png")
    save_surface(draw_stove(),               f"{ASSETS_DIR}/sprites/stove.png")
    save_surface(draw_cabinet(),             f"{ASSETS_DIR}/sprites/cabinet.png")
    save_surface(draw_battery(),             f"{ASSETS_DIR}/sprites/battery.png")
    save_surface(draw_car(),                 f"{ASSETS_DIR}/sprites/car.png")
    save_surface(draw_button(),              f"{ASSETS_DIR}/sprites/button_green.png")
    save_surface(draw_button((180, 100, 100)), f"{ASSETS_DIR}/sprites/button_red.png")
    save_surface(draw_mirror(),              f"{ASSETS_DIR}/sprites/mirror.png")
    save_surface(draw_box(),                 f"{ASSETS_DIR}/sprites/box.png")
    save_surface(draw_pillow(),              f"{ASSETS_DIR}/sprites/pillow.png")

    # Ícones de seleção
    save_surface(draw_selection_boy_icon(),  f"{ASSETS_DIR}/ui/select_boy.png")
    save_surface(draw_selection_girl_icon(), f"{ASSETS_DIR}/ui/select_girl.png")

    print("Todos os assets gerados com sucesso!")

if __name__ == "__main__":
    generate_all()
    pygame.quit()
