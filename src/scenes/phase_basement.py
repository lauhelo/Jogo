"""
Fase 7: Porão
- Usar chaves anteriores para abrir diferentes fechaduras
- Resolver sistema onde cada ação libera parte do caminho
- Ativar todos os mecanismos para revelar a chave final
- Inimigos: alta velocidade e presença constante
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_BASEMENT
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class BasementPhase(BasePhase):

    PHASE_KEY   = PHASE_BASEMENT
    KEYS_NEEDED = 3

    def _get_map_data(self):
        return [
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDWWWWWDDDDDDDDDDDDDW",
            "WDDDDDW...WDDDDDDDDDDDDDW",
            "WDDDDDW...WDDDDDDDDDDDDDW",
            "WDDDDDWWWWWDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    def _place_objects(self):
        TS = TILE_SIZE

        # Fechaduras (precisam de chaves anteriores)
        self._add_object(6 * TS, 4 * TS, "lock_1", "cabinet.png")
        self._add_object(10 * TS, 4 * TS, "lock_2", "cabinet.png")
        self._locks_opened = 0

        self._lock_key1 = self._add_object(8 * TS, 6 * TS, "key_lock1",
                                            "key.png", w=24, h=24)
        self._lock_key1.visible = False

        # Mecanismos (todos precisam ser ativados)
        mech_positions = [
            (4 * TS,  9 * TS),
            (12 * TS, 7 * TS),
            (18 * TS, 4 * TS),
            (22 * TS, 9 * TS),
        ]
        self._mechanisms = []
        for mx, my in mech_positions:
            obj = self._add_object(mx, my, "mechanism", "button_red.png")
            self._mechanisms.append(obj)
        self._mechs_activated = 0

        self._mech_key = self._add_object(13 * TS, 10 * TS, "key_mech",
                                           "key.png", w=24, h=24)
        self._mech_key.visible = False

        # Chave final (baú central)
        self._add_object(12 * TS, 5 * TS, "final_chest", "chest.png")
        self._final_key = self._add_object(12 * TS + 4, 6 * TS, "key_final",
                                            "key.png", w=24, h=24)
        self._final_key.visible = False

        # Porta de saída
        self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("Porão: Use tudo que aprendeu!\n"
                         "Abra as fechaduras e ative os mecanismos.", duration=5000)

    def _place_mobs(self):
        TS = TILE_SIZE
        self._add_mob("nightmare_spider",    8 * TS,  8 * TS)
        self._add_mob("nightmare_spider",    16 * TS, 5 * TS)
        self._add_mob("nightmare_spider",    20 * TS, 10 * TS)
        self._add_mob("shadow_creature", 10 * TS, 3 * TS)

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        if oid == "lock_1" and obj.active:
            obj.active  = False
            obj.visible = False
            self._locks_opened += 1
            self.hud.add_notification("Fechadura 1 aberta!", color=(200, 200, 100))
            if self._locks_opened == 2:
                self._lock_key1.visible = True
                self._lock_key1.active  = True
                self.hud.add_notification("Ambas as fechaduras abertas! Uma chave apareceu!", color=YELLOW_COLOR)
            return

        if oid == "lock_2" and obj.active:
            obj.active  = False
            obj.visible = False
            self._locks_opened += 1
            self.hud.add_notification("Fechadura 2 aberta!", color=(200, 200, 100))
            if self._locks_opened == 2:
                self._lock_key1.visible = True
                self._lock_key1.active  = True
                self.hud.add_notification("Ambas as fechaduras abertas! Uma chave apareceu!", color=YELLOW_COLOR)
            return

        if oid == "key_lock1" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "mechanism" and obj.active:
            obj.active  = False
            obj.visible = False
            self._mechs_activated += 1
            self.hud.add_notification(f"Mecanismo ativado! ({self._mechs_activated}/4)", color=(180, 220, 100))
            if self._mechs_activated == 4:
                self._mech_key.visible = True
                self._mech_key.active  = True
                self.hud.add_notification("Todos os mecanismos ativados! Uma chave apareceu!", color=YELLOW_COLOR)
            return

        if oid == "key_mech" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "final_chest" and obj.active:
            if self._locks_opened >= 2 and self._mechs_activated >= 4:
                obj.active  = False
                obj.visible = False
                self._final_key.visible = True
                self._final_key.active  = True
                self.hud.add_notification("O baú central revelou a chave final!", color=YELLOW_COLOR)
            else:
                self.show_dialog("O baú está trancado.\nAbra as fechaduras e ative os mecanismos primeiro.")
            return

        if oid == "key_final" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"Porta trancada. ({self.keys_collected}/{self.KEYS_NEEDED} chaves)")
