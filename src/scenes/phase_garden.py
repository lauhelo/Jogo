"""
Fase 1: Jardim
- Encontrar pá e cavar no local com grama diferente (1ª chave)
- Seguir ordem de cores das flores (2ª chave)
- Empurrar pedra específica (3ª chave)
- Inimigos: slimes com movimentação lenta em trajetos fixos
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_GARDEN
from src.utils.assets import sprite


class GardenPhase(BasePhase):

    PHASE_KEY   = PHASE_GARDEN
    KEYS_NEEDED = 3

    def _get_map_data(self):
        # G=grama normal, g=grama especial(cavar), W=parede/cerca, S=pedra
        return [
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGgW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGgW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGgW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WGGGGGGGGGGGGGGGGGGGGGGGW",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    def _place_objects(self):
        TS = TILE_SIZE

        # Pá (necessária para cavar)
        self._add_object(3 * TS, 3 * TS, "shovel", "shovel.png")

        # Área de grama especial para cavar (chave 1)
        self._dig_spot = self._add_object(22 * TS, 2 * TS, "dig_spot", "grass_special.png",
                                          w=TS, h=TS)

        # Flores coloridas (pista para chave 2)
        # Ordem correta: vermelho → azul → amarelo → roxo
        self._flower_order = ["red", "blue", "yellow", "purple"]
        self._flower_pressed = []

        flower_positions = [
            (5 * TS, 8 * TS,  "red",    "flower_red.png"),
            (10 * TS, 5 * TS, "blue",   "flower_blue.png"),
            (15 * TS, 9 * TS, "yellow", "flower_yellow.png"),
            (20 * TS, 6 * TS, "purple", "flower_purple.png"),
        ]
        self._flowers = {}
        for fx, fy, fid, fsprite in flower_positions:
            obj = self._add_object(fx, fy, f"flower_{fid}", fsprite)
            self._flowers[fid] = obj

        # Área onde a chave 2 aparece (após flores corretas)
        self._flower_key_spot = self._add_object(12 * TS, 7 * TS, "key_flower",
                                                  "key.png", w=24, h=24)
        self._flower_key_spot.visible = False

        # Pedras (uma delas esconde a chave 3)
        rock_positions = [
            (7 * TS,  10 * TS, False),
            (14 * TS, 11 * TS, False),
            (18 * TS, 3 * TS,  True),   # pedra especial
            (21 * TS, 10 * TS, False),
        ]
        self._special_rock = None
        for rx, ry, is_special in rock_positions:
            obj = self._add_object(rx, ry, "rock_special" if is_special else "rock", "rock.png")
            if is_special:
                self._special_rock = obj
                # Adiciona à lista de paredes para bloquear passagem
                self.walls.append(pygame.Rect(rx, ry, TILE_SIZE, TILE_SIZE))

        # Chave 3 (escondida sob a pedra especial)
        self._rock_key = self._add_object(18 * TS, 3 * TS, "key_rock", "key.png", w=24, h=24)
        self._rock_key.visible = False

        # Porta de saída
        try:
            door_img = sprite("door_locked.png", scale=PIXEL_SCALE)
        except:
            door_img = None
        exit_obj = self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                                    w=TILE_SIZE, h=TILE_SIZE * 2)

        # Posições iniciais
        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        # Dica inicial
        self.show_dialog("Encontre as 3 chaves para abrir a saída!\n"
                         "P1: WASD + E para interagir   P2: Setas + Enter", duration=5000)

    def _place_mobs(self):
        TS = TILE_SIZE
        # 3 slimes com patrulha
        self._add_mob("slime_green", 8 * TS, 4 * TS, [
            (8 * TS, 4 * TS), (16 * TS, 4 * TS)
        ])
        self._add_mob("slime_green", 6 * TS, 10 * TS, [
            (6 * TS, 10 * TS), (6 * TS, 12 * TS)
        ])
        self._add_mob("slime_green", 20 * TS, 9 * TS, [
            (20 * TS, 9 * TS), (12 * TS, 9 * TS)
        ])

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        # Pegar a pá
        if oid == "shovel" and obj.active:
            player.pick_up("shovel")
            obj.active  = False
            obj.visible = False
            self.hud.add_notification("Você pegou a pá!", color=(200, 180, 100))
            return

        # Cavar no local especial (precisa da pá)
        if oid == "dig_spot" and obj.active:
            if player.has_item("shovel"):
                obj.active  = False
                obj.visible = False
                # Revela chave 1
                key1 = self._add_key(obj.rect.x + 4, obj.rect.y + 4, "key1")
                self.hud.add_notification("Você cavou e encontrou uma chave!", color=YELLOW_COLOR)
            else:
                self.show_dialog("Você precisa de uma pá para cavar aqui.")
            return

        # Flores (ordem correta)
        if oid.startswith("flower_") and obj.active:
            color = oid.replace("flower_", "")
            expected = self._flower_order[len(self._flower_pressed)]
            if color == expected:
                self._flower_pressed.append(color)
                self.hud.add_notification(f"Flor {color} ativada! ({len(self._flower_pressed)}/4)", color=(180, 220, 100))
                if len(self._flower_pressed) == 4:
                    # Revela chave 2
                    self._flower_key_spot.visible = True
                    self._flower_key_spot.active  = True
                    self.hud.add_notification("A ordem das flores revelou uma chave!", color=YELLOW_COLOR)
            else:
                self._flower_pressed = []
                self.show_dialog("Ordem errada! Observe as flores com atenção.\nDica: vermelho → azul → amarelo → roxo")
            return

        # Chave das flores
        if oid == "key_flower" and obj.active:
            self._collect_key(player, obj)
            return

        # Pedra especial (empurrar)
        if oid == "rock_special" and obj.active:
            obj.active  = False
            obj.visible = False
            # Remove da lista de paredes
            self.walls = [w for w in self.walls
                          if not (w.x == obj.rect.x and w.y == obj.rect.y)]
            # Revela chave 3
            self._rock_key.visible = True
            self._rock_key.active  = True
            self.hud.add_notification("Você empurrou a pedra e encontrou uma chave!", color=YELLOW_COLOR)
            return

        # Chave da pedra
        if oid == "key_rock" and obj.active:
            self._collect_key(player, obj)
            return

        # Chave 1 (cavada)
        if oid == "key1" and obj.active:
            self._collect_key(player, obj)
            return

        # Porta de saída
        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"A porta está trancada.\nPrecisa de {self.KEYS_NEEDED} chaves. ({self.keys_collected}/{self.KEYS_NEEDED})")


# Cor auxiliar
YELLOW_COLOR = (255, 220, 50)
