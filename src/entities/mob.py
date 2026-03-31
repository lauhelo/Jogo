"""
Entidade Mob — inimigos com comportamentos variados.
"""
import pygame
import math
import random
from src.constants import TILE_SIZE, PIXEL_SCALE
from src.utils.assets import sprite


class Mob(pygame.sprite.Sprite):
    """
    Inimigo com comportamentos:
    - patrol: caminha em trajeto fixo
    - chase:  persegue o jogador ao se aproximar
    - random: movimentação irregular/aleatória
    - fast:   perseguição rápida e persistente
    """

    MOB_TYPES = {
        "slime_green": {"sprite": "mob_slime_green.png", "speed": 0.6,  "behavior": "patrol",  "detect_range": 0},
        "slime_red":   {"sprite": "mob_slime_red.png",   "speed": 1.0,  "behavior": "chase",   "detect_range": 120},
        "slime_blue":  {"sprite": "mob_slime_blue.png",  "speed": 1.4,  "behavior": "chase",   "detect_range": 160},
        "ghost":       {"sprite": "mob_ghost.png",       "speed": 1.2,  "behavior": "random",  "detect_range": 80},
        "spider":      {"sprite": "mob_spider.png",      "speed": 1.8,  "behavior": "fast",    "detect_range": 200},
    }

    def __init__(self, mob_type: str, x: int, y: int, patrol_points=None):
        super().__init__()
        cfg = self.MOB_TYPES.get(mob_type, self.MOB_TYPES["slime_green"])
        self.mob_type       = mob_type
        self.x              = float(x)
        self.y              = float(y)
        self.speed          = cfg["speed"]
        self.behavior       = cfg["behavior"]
        self.detect_range   = cfg["detect_range"]
        self.patrol_points  = patrol_points or []
        self._patrol_idx    = 0
        self._patrol_dir    = 1
        self._random_timer  = 0
        self._random_dx     = 0
        self._random_dy     = 0
        self._chasing       = False

        img = sprite(cfg["sprite"], scale=PIXEL_SCALE)
        self.image = img
        self.rect  = img.get_rect(topleft=(x, y))

    def update(self, players, walls, dt_ms):
        """Atualiza IA do mob."""
        if self.behavior == "patrol":
            self._do_patrol(walls)
        elif self.behavior in ("chase", "fast"):
            self._do_chase(players, walls)
        elif self.behavior == "random":
            self._do_random(players, walls, dt_ms)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    # ─── Comportamentos ──────────────────────────────────────────────────────
    def _do_patrol(self, walls):
        if not self.patrol_points:
            return
        tx, ty = self.patrol_points[self._patrol_idx]
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist < 4:
            self._patrol_idx = (self._patrol_idx + self._patrol_dir) % len(self.patrol_points)
        else:
            self._move(dx / dist * self.speed, dy / dist * self.speed, walls)

    def _do_chase(self, players, walls):
        target = self._nearest_player(players)
        if target is None:
            return
        px, py = target.get_center()
        dx = px - self.x
        dy = py - self.y
        dist = math.hypot(dx, dy)

        if self.behavior == "fast" or dist < self.detect_range:
            self._chasing = True

        if self._chasing and dist > 0:
            self._move(dx / dist * self.speed, dy / dist * self.speed, walls)

    def _do_random(self, players, walls, dt_ms):
        self._random_timer -= dt_ms
        if self._random_timer <= 0:
            angle = random.uniform(0, 2 * math.pi)
            self._random_dx = math.cos(angle) * self.speed
            self._random_dy = math.sin(angle) * self.speed
            self._random_timer = random.randint(400, 1200)

        # Se jogador próximo, persegue
        target = self._nearest_player(players)
        if target:
            px, py = target.get_center()
            dist = math.hypot(px - self.x, py - self.y)
            if dist < self.detect_range:
                dx = px - self.x
                dy = py - self.y
                if dist > 0:
                    self._move(dx / dist * self.speed, dy / dist * self.speed, walls)
                return

        self._move(self._random_dx, self._random_dy, walls)

    # ─── Utilitários ─────────────────────────────────────────────────────────
    def _move(self, dx, dy, walls):
        self.x += dx
        self.rect.x = int(self.x)
        for w in walls:
            if self.rect.colliderect(w):
                if dx > 0:
                    self.rect.right = w.left
                else:
                    self.rect.left = w.right
                self.x = float(self.rect.x)
                self._random_dx *= -1

        self.y += dy
        self.rect.y = int(self.y)
        for w in walls:
            if self.rect.colliderect(w):
                if dy > 0:
                    self.rect.bottom = w.top
                else:
                    self.rect.top = w.bottom
                self.y = float(self.rect.y)
                self._random_dy *= -1

    def _nearest_player(self, players):
        best, best_dist = None, float("inf")
        for p in players:
            if not p.alive:
                continue
            dist = math.hypot(p.get_center()[0] - self.x, p.get_center()[1] - self.y)
            if dist < best_dist:
                best, best_dist = p, dist
        return best

    def check_collision(self, players):
        """Retorna lista de jogadores atingidos."""
        hit = []
        for p in players:
            if p.alive and self.rect.colliderect(p.rect):
                hit.append(p)
        return hit

    def draw(self, surface, camera_offset=(0, 0)):
        sx = self.rect.x - camera_offset[0]
        sy = self.rect.y - camera_offset[1]
        surface.blit(self.image, (sx, sy))
