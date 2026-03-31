"""
Fase 3: Cozinha
- Ativar botões na ordem correta para liberar o forno com a chave
- Usar item para abrir saco contendo a chave
- Combinar objetos para alcançar área elevada
- Inimigos: slimes mais rápidos que bloqueiam caminhos
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_KITCHEN
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class KitchenPhase(BasePhase):

    PHASE_KEY   = PHASE_KITCHEN
    KEYS_NEEDED = 3

    def _get_map_data(self):
        return [
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WKKKKKKKKKKKKKKKKKKKKKKKW",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    def _place_objects(self):
        TS = TILE_SIZE

        # Botões (ordem correta: verde → vermelho → verde)
        self._button_order = ["green", "red", "green"]
        self._button_pressed = []

        self._add_object(5 * TS, 4 * TS, "btn_green", "button_green.png")
        self._add_object(9 * TS, 4 * TS, "btn_red",   "button_red.png")
        self._add_object(13 * TS, 4 * TS, "btn_green2", "button_green.png")

        # Fogão (liberado pelos botões)
        self._stove = self._add_object(7 * TS, 2 * TS, "stove", "stove.png")
        self._stove_key = self._add_object(7 * TS + 4, 3 * TS, "key_stove",
                                            "key.png", w=24, h=24)
        self._stove_key.visible = False

        # Saco (precisa de faca/item)
        self._add_object(17 * TS, 8 * TS, "bag", "box.png")
        self._bag_key = self._add_object(17 * TS + 4, 9 * TS, "key_bag",
                                          "key.png", w=24, h=24)
        self._bag_key.visible = False

        # Item (faca/utensílio)
        self._add_object(3 * TS, 9 * TS, "knife", "shovel.png")

        # Área elevada (precisa de caixas empilhadas)
        self._add_object(21 * TS, 2 * TS, "high_area_key", "key.png", w=24, h=24)
        self._high_key = self.objects[-1]
        self._high_key.visible = False

        # Caixas para empilhar
        self._add_object(15 * TS, 10 * TS, "box1", "box.png")
        self._add_object(19 * TS, 10 * TS, "box2", "box.png")
        self._boxes_combined = False

        # Porta de saída
        self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("Cozinha: Encontre as 3 chaves!\n"
                         "Ative os botões na ordem certa e explore os objetos.", duration=5000)

    def _place_mobs(self):
        TS = TILE_SIZE
        self._add_mob("slime_blue", 10 * TS, 7 * TS)
        self._add_mob("slime_blue", 16 * TS, 4 * TS)
        self._add_mob("slime_red",  20 * TS, 9 * TS)

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        # Botões (ordem: verde, vermelho, verde)
        if oid in ("btn_green", "btn_red", "btn_green2") and obj.active:
            color = "red" if oid == "btn_red" else "green"
            expected = self._button_order[len(self._button_pressed)]
            if color == expected:
                self._button_pressed.append(color)
                self.hud.add_notification(f"Botão {color} ativado! ({len(self._button_pressed)}/3)", color=(180, 220, 100))
                if len(self._button_pressed) == 3:
                    self._stove_key.visible = True
                    self._stove_key.active  = True
                    self.hud.add_notification("O forno abriu! Há uma chave dentro!", color=YELLOW_COLOR)
            else:
                self._button_pressed = []
                self.show_dialog("Sequência errada! Tente novamente.\nDica: verde → vermelho → verde")
            return

        if oid == "key_stove" and obj.active:
            self._collect_key(player, obj)
            return

        # Pegar faca
        if oid == "knife" and obj.active:
            player.pick_up("knife")
            obj.active  = False
            obj.visible = False
            self.hud.add_notification("Você pegou a faca!", color=(200, 180, 100))
            return

        # Abrir saco
        if oid == "bag" and obj.active:
            if player.has_item("knife"):
                obj.active  = False
                obj.visible = False
                self._bag_key.visible = True
                self._bag_key.active  = True
                self.hud.add_notification("Você abriu o saco e encontrou uma chave!", color=YELLOW_COLOR)
            else:
                self.show_dialog("Você precisa de algo afiado para abrir o saco.")
            return

        if oid == "key_bag" and obj.active:
            self._collect_key(player, obj)
            return

        # Caixas (combinar para alcançar área elevada)
        if oid in ("box1", "box2") and obj.active:
            player.pick_up(oid)
            obj.active  = False
            obj.visible = False
            if player.has_item("box1") and player.has_item("box2"):
                self._boxes_combined = True
                self._high_key.visible = True
                self._high_key.active  = True
                self.hud.add_notification("Você empilhou as caixas e alcançou a área elevada!", color=YELLOW_COLOR)
            else:
                self.hud.add_notification("Pegou uma caixa! Encontre a outra.", color=(200, 180, 100))
            return

        if oid == "high_area_key" and obj.active:
            if self._boxes_combined:
                self._collect_key(player, obj)
            else:
                self.show_dialog("Muito alto para alcançar! Precisa de algo para subir.")
            return

        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"Porta trancada. ({self.keys_collected}/{self.KEYS_NEEDED} chaves)")
