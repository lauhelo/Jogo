"""
Entidade Player — suporta menino e menina, animação de 4 direções.
"""
import pygame
import time
from src.constants import (
    TILE_SIZE, PIXEL_SCALE, PLAYER_SPEED, MAX_HEARTS,
    INVULNERABILITY_MS, BOY_COLOR, GIRL_COLOR
)
from src.utils.assets import sprite


class Player(pygame.sprite.Sprite):
    """
    Jogador com sprite de pixel art, animação de caminhada,
    sistema de 3 corações e inventário de itens.
    """

    def __init__(self, player_id: int, gender: str, x: int, y: int):
        super().__init__()
        self.player_id  = player_id   # 1 ou 2
        self.gender     = gender      # "boy" ou "girl"
        self.x          = float(x)
        self.y          = float(y)
        self.speed      = PLAYER_SPEED
        self.hearts     = MAX_HEARTS
        self.max_hearts = MAX_HEARTS
        self.alive      = True
        self.inventory  = []          # lista de strings de itens coletados
        self.direction  = "down"
        self.moving     = False
        self.color      = BOY_COLOR if gender == "boy" else GIRL_COLOR

        # Animação
        self._anim_timer    = 0
        self._anim_frame    = 0
        self._anim_interval = 200  # ms por frame

        # Invulnerabilidade
        self._invuln_until  = 0
        self._blink_state   = True
        self._blink_timer   = 0

        # Carrega sprites
        self._sprites = self._load_sprites()
        self.image    = self._sprites["down"][0]
        self.rect     = self.image.get_rect(topleft=(int(x), int(y)))

    def _load_sprites(self):
        prefix = self.gender
        dirs = ["down", "up", "left", "right"]
        result = {}
        for d in dirs:
            frames = []
            for f in range(2):
                frames.append(sprite(f"{prefix}_{d}_{f}.png", scale=PIXEL_SCALE))
            result[d] = frames
        return result

    # ─── Movimento ───────────────────────────────────────────────────────────
    def handle_input(self, keys, key_map: dict, walls, others):
        """Processa input e move o jogador, verificando colisão."""
        dx, dy = 0, 0
        moved  = False

        if keys[key_map["up"]]:
            dy = -self.speed
            self.direction = "up"
            moved = True
        elif keys[key_map["down"]]:
            dy = self.speed
            self.direction = "down"
            moved = True
        if keys[key_map["left"]]:
            dx = -self.speed
            self.direction = "left"
            moved = True
        elif keys[key_map["right"]]:
            dx = self.speed
            self.direction = "right"
            moved = True

        self.moving = moved

        if moved:
            self._try_move(dx, dy, walls, others)

    def _try_move(self, dx, dy, walls, others):
        """Move com resolução de colisão separada por eixo."""
        # Eixo X
        self.x += dx
        self.rect.x = int(self.x)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                else:
                    self.rect.left = wall.right
                self.x = float(self.rect.x)

        # Eixo Y
        self.y += dy
        self.rect.y = int(self.y)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                else:
                    self.rect.top = wall.bottom
                self.y = float(self.rect.y)

        # Colisão com o outro jogador
        for other in others:
            if other is self:
                continue
            if self.rect.colliderect(other.rect):
                # Empurra de volta
                if dx > 0:
                    self.rect.right = other.rect.left
                elif dx < 0:
                    self.rect.left = other.rect.right
                if dy > 0:
                    self.rect.bottom = other.rect.top
                elif dy < 0:
                    self.rect.top = other.rect.bottom
                self.x = float(self.rect.x)
                self.y = float(self.rect.y)

    # ─── Animação ────────────────────────────────────────────────────────────
    def update_animation(self, dt_ms: int):
        now = pygame.time.get_ticks()

        # Blink de invulnerabilidade
        if now < self._invuln_until:
            if now - self._blink_timer > 120:
                self._blink_state = not self._blink_state
                self._blink_timer = now
        else:
            self._blink_state = True

        # Frame de animação
        if self.moving:
            self._anim_timer += dt_ms
            if self._anim_timer >= self._anim_interval:
                self._anim_timer = 0
                self._anim_frame = 1 - self._anim_frame
        else:
            self._anim_frame = 0

        self.image = self._sprites[self.direction][self._anim_frame]

    # ─── Dano e vida ─────────────────────────────────────────────────────────
    def take_damage(self):
        now = pygame.time.get_ticks()
        if now < self._invuln_until:
            return False
        self.hearts -= 1
        self._invuln_until = now + INVULNERABILITY_MS
        self._blink_timer  = now
        if self.hearts <= 0:
            self.hearts = 0
            self.alive  = False
        return True

    def restore_hearts(self):
        self.hearts = self.max_hearts
        self.alive  = True

    def is_invulnerable(self):
        return pygame.time.get_ticks() < self._invuln_until

    # ─── Inventário ──────────────────────────────────────────────────────────
    def pick_up(self, item: str):
        if item not in self.inventory:
            self.inventory.append(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def remove_item(self, item: str):
        if item in self.inventory:
            self.inventory.remove(item)

    # ─── Desenho ─────────────────────────────────────────────────────────────
    def draw(self, surface, camera_offset=(0, 0)):
        if not self._blink_state:
            return
        sx = self.rect.x - camera_offset[0]
        sy = self.rect.y - camera_offset[1]
        surface.blit(self.image, (sx, sy))

        # Indicador de jogador (número acima)
        self._draw_indicator(surface, sx, sy)

    def _draw_indicator(self, surface, sx, sy):
        font = pygame.font.SysFont("courier", 10, bold=True)
        label = f"P{self.player_id}"
        color = BOY_COLOR if self.gender == "boy" else GIRL_COLOR
        rendered = font.render(label, False, color)
        surface.blit(rendered, (sx + self.rect.width // 2 - rendered.get_width() // 2, sy - 12))

    def get_center(self):
        return self.rect.centerx, self.rect.centery
