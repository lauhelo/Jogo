"""
Fase 6: Quarto 2 (Suíte)
- Coletar partes de uma chave e montá-la
- Ativar diferentes pontos do cenário para desbloquear localização
- Usar espelho para revelar chave escondida
- Inimigos: mais agressivos, seguem por mais tempo
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_BEDROOM2
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class Bedroom2Phase(BasePhase):

    PHASE_KEY   = PHASE_BEDROOM2
    KEYS_NEEDED = 3

    def _get_map_data(self):
        return [
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WBBBBBBBBBBBBBBBBBBBBBBBW",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    def _place_objects(self):
        TS = TILE_SIZE

        # Partes da chave (3 partes espalhadas)
        self._add_object(4 * TS,  3 * TS, "key_part_1", "key_silver.png")
        self._add_object(14 * TS, 9 * TS, "key_part_2", "key_silver.png")
        self._add_object(21 * TS, 4 * TS, "key_part_3", "key_silver.png")
        self._parts_found = 0

        self._assembled_key1 = self._add_object(12 * TS, 6 * TS, "key_assembled1",
                                                  "key.png", w=24, h=24)
        self._assembled_key1.visible = False

        # Pontos de ativação (3 pontos → revela localização da chave 2)
        self._activation_points = []
        act_positions = [
            (6 * TS, 7 * TS),
            (16 * TS, 3 * TS),
            (20 * TS, 10 * TS),
        ]
        for ax, ay in act_positions:
            obj = self._add_object(ax, ay, "activation_point", "button_green.png")
            self._activation_points.append(obj)
        self._activations_done = 0

        self._activation_key = self._add_object(11 * TS, 4 * TS, "key_activation",
                                                  "key.png", w=24, h=24)
        self._activation_key.visible = False

        # Espelho (revela chave 3)
        self._add_object(22 * TS, 6 * TS, "mirror", "mirror.png")
        self._mirror_key = self._add_object(22 * TS + 4, 7 * TS, "key_mirror",
                                             "key.png", w=24, h=24)
        self._mirror_key.visible = False

        # Porta de saída
        self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("Suíte: Encontre as 3 chaves!\n"
                         "Colete as partes da chave e use o espelho.", duration=5000)

    def _place_mobs(self):
        TS = TILE_SIZE
        self._add_mob("spider",    10 * TS, 6 * TS)
        self._add_mob("spider",    18 * TS, 8 * TS)
        self._add_mob("slime_red", 8 * TS,  3 * TS)

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        if oid in ("key_part_1", "key_part_2", "key_part_3") and obj.active:
            player.pick_up(oid)
            obj.active  = False
            obj.visible = False
            self._parts_found += 1
            self.hud.add_notification(f"Parte da chave coletada! ({self._parts_found}/3)", color=(200, 200, 100))
            if self._parts_found == 3:
                self._assembled_key1.visible = True
                self._assembled_key1.active  = True
                self.hud.add_notification("Você montou a chave completa!", color=YELLOW_COLOR)
            return

        if oid == "key_assembled1" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "activation_point" and obj.active:
            obj.active  = False
            obj.visible = False
            self._activations_done += 1
            self.hud.add_notification(f"Ponto ativado! ({self._activations_done}/3)", color=(180, 220, 100))
            if self._activations_done == 3:
                self._activation_key.visible = True
                self._activation_key.active  = True
                self.hud.add_notification("Todos os pontos ativados! Uma chave apareceu!", color=YELLOW_COLOR)
            return

        if oid == "key_activation" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "mirror" and obj.active:
            obj.active = False
            self._mirror_key.visible = True
            self._mirror_key.active  = True
            self.hud.add_notification("O espelho revelou uma chave escondida!", color=YELLOW_COLOR)
            return

        if oid == "key_mirror" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"Porta trancada. ({self.keys_collected}/{self.KEYS_NEEDED} chaves)")
