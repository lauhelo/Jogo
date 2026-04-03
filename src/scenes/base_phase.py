"""
Classe base para todas as fases do jogo.
Gerencia: tiles, objetos interativos, mobs, colisões, câmera, HUD.
"""
import pygame
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PIXEL_SCALE,
    MAX_HEARTS, PLAYER_SPEED,
    KEY_MAP, PLAYER1_KEYS, PLAYER2_KEYS,
    UI_BG, UI_PANEL, UI_BORDER, UI_TEXT, UI_TITLE, UI_SELECTED,
    BLACK, WHITE, YELLOW, GREEN, RED,
    SCENE_GAMEOVER
)
from src.utils.assets import (
    FontManager, draw_text, draw_panel, draw_pixel_border,
    sprite, tile as load_tile
)
from src.systems.camera import Camera
from src.systems.hud import HUD
from src.entities.mob import Mob


class InteractiveObject:
    """Objeto com o qual os jogadores podem interagir."""

    def __init__(self, x, y, w, h, obj_id, image=None, visible=True):
        self.rect    = pygame.Rect(x, y, w, h)
        self.obj_id  = obj_id
        self.image   = image
        self.visible = visible
        self.active  = True
        self.glow    = 0.0   # efeito de brilho para indicar interatividade

    def draw(self, surface, camera_offset):
        if not self.visible or not self.active:
            return
        sx = self.rect.x - camera_offset[0]
        sy = self.rect.y - camera_offset[1]
        if self.image:
            surface.blit(self.image, (sx, sy))
        else:
            pygame.draw.rect(surface, (200, 200, 50), (sx, sy, self.rect.w, self.rect.h), 2)

        # Indicador de interação (brilho pulsante)
        if self.glow > 0:
            glow_surf = pygame.Surface((self.rect.w + 8, self.rect.h + 8), pygame.SRCALPHA)
            alpha = int(self.glow * 120)
            glow_surf.fill((255, 220, 50, alpha))
            surface.blit(glow_surf, (sx - 4, sy - 4))

    def update_glow(self, players, dt_ms):
        """Pulsa quando um jogador está próximo."""
        close = False
        for p in players:
            if p.alive:
                dist = math.hypot(p.rect.centerx - self.rect.centerx,
                                  p.rect.centery - self.rect.centery)
                if dist < 60:
                    close = True
                    break
        target = 1.0 if close else 0.0
        self.glow += (target - self.glow) * 0.1


class BasePhase:
    """
    Fase base com:
    - Mapa de tiles (lista 2D de strings)
    - Objetos interativos
    - Mobs
    - Sistema de chaves
    - Câmera e HUD
    """

    PHASE_KEY   = "base"
    KEYS_NEEDED = 3

    # Mapeamento tile_char → arquivo de tile
    TILE_MAP = {
        "G": "grass.png",
        "g": "grass_special.png",
        "W": "wall.png",
        "w": "wall_office.png",
        "F": "floor_wood.png",
        "K": "floor_kitchen.png",
        "B": "floor_bedroom.png",
        "D": "floor_dark.png",
        "S": "stone.png",
        ".": None,   # vazio/transparente
    }

    def __init__(self, game, players):
        self.game    = game
        self.players = players
        self.hud     = HUD()

        self.keys_collected = 0
        self.phase_complete = False
        self._transition_timer = 0
        self._paused = False

        # Objetos e mobs
        self.objects  = []   # lista de InteractiveObject
        self.mobs     = []   # lista de Mob
        self.walls    = []   # lista de pygame.Rect (colisão)
        self.key_items = []  # objetos que são chaves

        # Tiles pré-renderizados
        self._tile_cache = {}
        self._tile_surf  = None   # superfície do mapa completo
        self._map_rect   = pygame.Rect(0, 0, 800, 600)

        # Câmera
        self.camera = Camera(800, 600)

        # Fontes
        self.font_dialog = FontManager.pixel(14)
        self.font_hint   = FontManager.pixel(12)

        # Diálogo/dica ativo
        self._dialog     = None
        self._dialog_timer = 0

        # Posições iniciais dos jogadores
        self._spawn_positions = [(100, 300), (140, 300)]

        # Inicializa a fase
        self._build_map()
        self._place_objects()
        self._place_mobs()
        self._spawn_players()

        # Toca a música de gameplay ao iniciar a fase
        self.game.play_background_music('assets/sounds/background-gameplay.mp3', volume=0.2)

    def _build_map(self):
        """Subclasses definem o mapa em _get_map_data()."""
        map_data = self._get_map_data()
        if not map_data:
            return

        rows = len(map_data)
        cols = max(len(row) for row in map_data)
        map_w = cols * TILE_SIZE
        map_h = rows * TILE_SIZE

        self._map_rect = pygame.Rect(0, 0, map_w, map_h)
        self.camera = Camera(map_w, map_h)
        self._tile_surf = pygame.Surface((map_w, map_h))
        self._tile_surf.fill((20, 15, 30))

        for row_idx, row in enumerate(map_data):
            for col_idx, char in enumerate(row):
                tile_file = self.TILE_MAP.get(char)
                if tile_file:
                    t = self._get_tile(tile_file)
                    self._tile_surf.blit(t, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

                # Paredes sólidas
                if char in ("W", "w", "S"):
                    self.walls.append(pygame.Rect(
                        col_idx * TILE_SIZE, row_idx * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE
                    ))

        # Bordas do mapa como paredes
        self.walls.append(pygame.Rect(0, 0, map_w, TILE_SIZE))           # topo
        self.walls.append(pygame.Rect(0, map_h - TILE_SIZE, map_w, TILE_SIZE))  # base
        self.walls.append(pygame.Rect(0, 0, TILE_SIZE, map_h))           # esquerda
        self.walls.append(pygame.Rect(map_w - TILE_SIZE, 0, TILE_SIZE, map_h))  # direita

    def _get_tile(self, filename):
        if filename not in self._tile_cache:
            self._tile_cache[filename] = load_tile(filename, scale=PIXEL_SCALE)
        return self._tile_cache[filename]

    def _get_map_data(self):
        """Retorna lista de strings representando o mapa. Subclasses implementam."""
        return []

    def _place_objects(self):
        """Subclasses posicionam objetos interativos."""
        pass

    def _place_mobs(self):
        """Subclasses posicionam mobs."""
        pass

    def _spawn_players(self):
        """Posiciona jogadores nas posições iniciais."""
        for i, player in enumerate(self.players):
            if i < len(self._spawn_positions):
                px, py = self._spawn_positions[i]
                player.x = float(px)
                player.y = float(py)
                player.rect.x = px
                player.rect.y = py
            player.restore_hearts()

    def _add_object(self, x, y, obj_id, sprite_name=None, w=None, h=None):
        """Adiciona objeto interativo."""
        img = None
        if sprite_name:
            try:
                img = sprite(sprite_name, scale=PIXEL_SCALE)
            except:
                pass
        iw = w or (img.get_width() if img else TILE_SIZE)
        ih = h or (img.get_height() if img else TILE_SIZE)
        obj = InteractiveObject(x, y, iw, ih, obj_id, img)
        self.objects.append(obj)
        return obj

    def _add_key(self, x, y, key_id):
        """Adiciona uma chave coletável."""
        try:
            img = sprite("key.png", scale=PIXEL_SCALE)
        except:
            img = None
        obj = InteractiveObject(x, y, 24, 24, key_id, img)
        self.objects.append(obj)
        self.key_items.append(obj)
        return obj

    def _add_mob(self, mob_type, x, y, patrol_points=None):
        mob = Mob(mob_type, x, y, patrol_points)
        self.mobs.append(mob)
        return mob

    # ─── Diálogo ─────────────────────────────────────────────────────────────
    def show_dialog(self, text, duration=3000):
        self._dialog       = text
        self._dialog_timer = duration

    # ─── Interação ───────────────────────────────────────────────────────────
    def _check_interactions(self, player, key_pressed):
        """Verifica se o jogador está próximo de um objeto e pressiona ação."""
        if not key_pressed:
            # Reseta o estado de "tecla pressionada" para permitir nova interação
            if hasattr(player, "_last_action_state"):
                player._last_action_state = False
            return

        # Evita interações múltiplas em um único clique (debounce)
        if getattr(player, "_last_action_state", False):
            return
        player._last_action_state = True

        # Encontra o objeto mais próximo dentro do alcance
        closest_obj = None
        min_dist = 60 # Alcance aumentado para 60 pixels

        for obj in self.objects:
            if not obj.active:
                continue
            # Se o objeto não for visível, só permite interação se for uma chave (que pode estar oculta)
            if not obj.visible and not obj.obj_id.startswith("key"):
                continue

            dist = math.hypot(
                player.rect.centerx - obj.rect.centerx,
                player.rect.centery - obj.rect.centery
            )
            if dist < min_dist:
                min_dist = dist
                closest_obj = obj

        if closest_obj:
            self._on_interact(player, closest_obj)

    def _on_interact(self, player, obj):
        """Subclasses implementam lógica de interação."""
        pass

    def _collect_key(self, player, obj):
        """Coleta uma chave."""
        obj.active  = False
        obj.visible = False
        self.keys_collected += 1
        player.pick_up(obj.obj_id)
        self.hud.add_notification(f"Chave coletada! ({self.keys_collected}/{self.KEYS_NEEDED})",
                                  color=(255, 220, 50))
        if hasattr(self.game, 'play_sfx'):
            self.game.play_sfx('key_collect')
        if self.keys_collected >= self.KEYS_NEEDED:
            self._unlock_exit()

    def _unlock_exit(self):
        """Desbloqueia a saída quando todas as chaves são coletadas."""
        self.hud.add_notification("A saída foi desbloqueada!", color=(100, 220, 100))
        if hasattr(self.game, 'play_sfx'):
            self.game.play_sfx('door_unlock')
        # Ativa a porta de saída
        for obj in self.objects:
            if obj.obj_id == "exit_door":
                try:
                    obj.image = sprite("door_open.png", scale=PIXEL_SCALE)
                except:
                    pass

    # ─── Update ──────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Abre o menu de pausa
                from src.scenes.pause_scene import PauseScene
                self._paused = True
                self.game._scene = PauseScene(self.game, self)

    def update(self, dt_ms):
        if self._paused:
            return

        keys = pygame.key.get_pressed()

        # Input dos jogadores
        p1_action = keys[KEY_MAP["e"]]
        p2_action = keys[KEY_MAP["return"]]

        p1_key_map = {k: KEY_MAP[v] for k, v in PLAYER1_KEYS.items()}
        p2_key_map = {k: KEY_MAP[v] for k, v in PLAYER2_KEYS.items()}

        alive_players = [p for p in self.players if p.alive]

        if self.players[0].alive:
            self.players[0].handle_input(keys, p1_key_map, self.walls, self.players, self._map_rect)
            self._check_interactions(self.players[0], p1_action)

        if len(self.players) > 1 and self.players[1].alive:
            self.players[1].handle_input(keys, p2_key_map, self.walls, self.players, self._map_rect)
            self._check_interactions(self.players[1], p2_action)

        # Animação dos jogadores
        for p in self.players:
            p.update_animation(dt_ms)

        # Mobs
        for mob in self.mobs:
            mob.update(alive_players, self.walls, dt_ms)
            for p in mob.check_collision(alive_players):
                if p.take_damage():
                    self.hud.add_notification(f"P{p.player_id} levou dano!", color=(220, 80, 80))

        # Objetos (glow)
        for obj in self.objects:
            obj.update_glow(self.players, dt_ms)

        # Verifica game over
        if all(not p.alive for p in self.players):
            self._transition_timer += dt_ms
            if self._transition_timer >= 2000:
                self.game.change_scene(SCENE_GAMEOVER)
                return

        # Verifica saída
        self._check_exit()

        # Câmera
        self.camera.update(alive_players if alive_players else self.players, dt_ms)

        # HUD
        self.hud.update(dt_ms)

        # Diálogo
        if self._dialog_timer > 0:
            self._dialog_timer -= dt_ms
            if self._dialog_timer <= 0:
                self._dialog = None

        # Lógica específica da fase
        self._phase_update(dt_ms)

    def _phase_update(self, dt_ms):
        """Subclasses implementam lógica adicional."""
        pass

    def _check_exit(self):
        """Verifica se um jogador chegou na porta de saída."""
        if self.keys_collected < self.KEYS_NEEDED:
            return
        for obj in self.objects:
            if obj.obj_id == "exit_door" and obj.active:
                for p in self.players:
                    if p.alive and p.rect.colliderect(obj.rect):
                        self._on_phase_complete()
                        return

    def _on_phase_complete(self):
        """Avança para a próxima fase."""
        if not self.phase_complete:
            self.phase_complete = True
            self.hud.add_notification("Fase concluída! Avançando...", color=(100, 220, 100))
            self.game.advance_phase()

    # ─── Draw ─────────────────────────────────────────────────────────────────
    def draw(self, surface):
        offset = self.camera.get_offset()

        # Tiles
        if self._tile_surf:
            surface.blit(self._tile_surf, (-offset[0], -offset[1]))
        else:
            surface.fill((30, 25, 40))

        # Objetos
        for obj in self.objects:
            obj.draw(surface, offset)

        # Mobs
        for mob in self.mobs:
            mob.draw(surface, offset)

        # Jogadores
        for p in self.players:
            p.draw(surface, offset)

        # HUD
        self.hud.draw(surface, self.players, self.PHASE_KEY,
                      self.keys_collected, self.KEYS_NEEDED)

        # Diálogo
        if self._dialog:
            self._draw_dialog(surface, self._dialog)

        # Overlay de game over
        if all(not p.alive for p in self.players) and self._transition_timer > 0:
            alpha = min(180, int(self._transition_timer / 1500 * 180))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            surface.blit(overlay, (0, 0))

    def _draw_dialog(self, surface, text):
        """Caixa de diálogo na parte inferior."""
        lines = text.split("\n")
        box_h = 20 + len(lines) * 18
        box_y = SCREEN_HEIGHT - box_h - 10
        box_rect = pygame.Rect(40, box_y, SCREEN_WIDTH - 80, box_h)
        draw_panel(surface, box_rect, (10, 8, 20), (80, 60, 120), alpha=220)
        for i, line in enumerate(lines):
            draw_text(surface, line, 52, box_y + 8 + i * 18,
                      self.font_dialog, (220, 210, 240), shadow=True)
