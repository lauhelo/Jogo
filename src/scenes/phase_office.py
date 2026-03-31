"""
Fase 2: Escritório
- Abrir armários na ordem correta baseada em símbolos na parede
- Encontrar chave em estante indicada por padrão visual
- Derrubar objeto da prateleira para revelar chave
- Inimigos: slimes que perseguem ao se aproximar
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_OFFICE
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class OfficePhase(BasePhase):

    PHASE_KEY   = PHASE_OFFICE
    KEYS_NEEDED = 3

    def _get_map_data(self):
        return [
            "wwwwwwwwwwwwwwwwwwwwwwwww",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wFFFFFFFFFFFFFFFFFFFFFFFw",
            "wwwwwwwwwwwwwwwwwwwwwwwww",
        ]

    def _place_objects(self):
        TS = TILE_SIZE

        # Símbolos na parede (pistas para ordem dos armários)
        # Ordem correta: 1 → 3 → 2
        self._cabinet_order = [1, 3, 2]
        self._cabinet_pressed = []

        # Armários
        cabinet_positions = [
            (4 * TS, 2 * TS, 1),
            (10 * TS, 2 * TS, 3),
            (16 * TS, 2 * TS, 2),
        ]
        self._cabinets = {}
        for cx, cy, cnum in cabinet_positions:
            obj = self._add_object(cx, cy, f"cabinet_{cnum}", "cabinet.png")
            self._cabinets[cnum] = obj

        # Símbolo na parede (dica visual)
        self._add_object(8 * TS, 1 * TS, "wall_clue", None, w=TS * 3, h=TS)

        # Chave 1 (nos armários na ordem correta)
        self._cabinet_key = self._add_object(10 * TS, 3 * TS, "key_cabinet",
                                              "key.png", w=24, h=24)
        self._cabinet_key.visible = False

        # Estante de livros (chave 2 no livro com padrão especial)
        shelf_positions = [
            (3 * TS, 6 * TS),
            (7 * TS, 6 * TS),
            (11 * TS, 6 * TS),   # estante com a chave
            (15 * TS, 6 * TS),
            (19 * TS, 6 * TS),
        ]
        self._special_shelf_idx = 2
        self._shelves = []
        for i, (sx, sy) in enumerate(shelf_positions):
            obj = self._add_object(sx, sy, f"shelf_{i}", "bookshelf.png")
            self._shelves.append(obj)

        self._shelf_key = self._add_object(11 * TS + 4, 7 * TS, "key_shelf",
                                            "key.png", w=24, h=24)
        self._shelf_key.visible = False

        # Objeto na prateleira para derrubar (chave 3)
        self._add_object(20 * TS, 4 * TS, "shelf_obj", "book.png")
        self._hidden_key = self._add_object(20 * TS + 4, 5 * TS, "key_hidden",
                                             "key.png", w=24, h=24)
        self._hidden_key.visible = False

        # Porta de saída
        self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("Escritório: Encontre as 3 chaves!\n"
                         "Observe os símbolos na parede para a ordem dos armários.", duration=5000)

    def _place_mobs(self):
        TS = TILE_SIZE
        self._add_mob("slime_red", 12 * TS, 8 * TS)
        self._add_mob("slime_red", 18 * TS, 5 * TS)

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        # Armários (ordem correta: 1, 3, 2)
        if oid.startswith("cabinet_") and obj.active:
            num = int(oid.split("_")[1])
            expected = self._cabinet_order[len(self._cabinet_pressed)]
            if num == expected:
                self._cabinet_pressed.append(num)
                self.hud.add_notification(f"Armário {num} aberto! ({len(self._cabinet_pressed)}/3)", color=(180, 220, 100))
                if len(self._cabinet_pressed) == 3:
                    self._cabinet_key.visible = True
                    self._cabinet_key.active  = True
                    self.hud.add_notification("A ordem correta revelou uma chave!", color=YELLOW_COLOR)
            else:
                self._cabinet_pressed = []
                self.show_dialog("Ordem errada! Observe os símbolos na parede.\nDica: 1 → 3 → 2")
            return

        if oid == "key_cabinet" and obj.active:
            self._collect_key(player, obj)
            return

        # Estantes (a do meio tem a chave)
        if oid.startswith("shelf_") and obj.active:
            idx = int(oid.split("_")[1])
            if idx == self._special_shelf_idx:
                self._shelf_key.visible = True
                self._shelf_key.active  = True
                obj.active = False
                self.hud.add_notification("Você encontrou uma chave na estante!", color=YELLOW_COLOR)
            else:
                self.show_dialog("Nada aqui... Procure a estante com o padrão diferente.")
            return

        if oid == "key_shelf" and obj.active:
            self._collect_key(player, obj)
            return

        # Objeto na prateleira (derrubar)
        if oid == "shelf_obj" and obj.active:
            obj.active  = False
            obj.visible = False
            self._hidden_key.visible = True
            self._hidden_key.active  = True
            self.hud.add_notification("Você derrubou o objeto e encontrou uma chave!", color=YELLOW_COLOR)
            return

        if oid == "key_hidden" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"Porta trancada. ({self.keys_collected}/{self.KEYS_NEEDED} chaves)")
