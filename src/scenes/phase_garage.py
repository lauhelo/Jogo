"""
Fase 8: Garagem (Fase Final)
- Encontrar e instalar bateria para restaurar energia
- Localizar chave do carro em compartimento secreto
- Abastecer/ativar o carro seguindo sequência correta
- Abrir portão após resolver sistema elétrico
- Dar partida no carro e sair
- Inimigos: maior frequência e velocidade
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_GARAGE, SCENE_WIN
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class GaragePhase(BasePhase):

    PHASE_KEY   = PHASE_GARAGE
    KEYS_NEEDED = 5   # Mais objetivos na fase final

    def _get_map_data(self):
        return [
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WDDDDDDDDDDDDDDDDDDDDDDDW",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    def _place_objects(self):
        TS = TILE_SIZE

        # Carro (destino final)
        self._car_obj = self._add_object(10 * TS, 5 * TS, "car", "car.png",
                                          w=TS * 3, h=TS)

        # Bateria (precisa ser instalada)
        self._add_object(3 * TS, 3 * TS, "battery", "battery.png")
        self._battery_installed = False

        # Painel elétrico
        self._add_object(3 * TS, 8 * TS, "electric_panel", "cabinet.png")
        self._panel_activated = False

        # Compartimento secreto (chave do carro)
        self._add_object(20 * TS, 3 * TS, "secret_compartment", "box.png")
        self._car_key_found = False
        self._car_key_obj = self._add_object(20 * TS + 4, 4 * TS, "car_key",
                                              "key.png", w=24, h=24)
        self._car_key_obj.visible = False

        # Sequência de ativação do carro (botões em ordem)
        self._car_sequence = ["fuel", "ignition", "gear"]
        self._car_steps_done = []

        self._add_object(12 * TS, 8 * TS, "fuel_btn",      "button_green.png")
        self._add_object(15 * TS, 8 * TS, "ignition_btn",  "button_red.png")
        self._add_object(18 * TS, 8 * TS, "gear_btn",      "button_green.png")

        # Portão (abre após sistema elétrico)
        self._gate_obj = self._add_object(23 * TS, 1 * TS, "gate", "door_locked.png",
                                           w=TS, h=TS * 3)
        self._gate_open = False

        # Chaves de progresso (representam etapas concluídas)
        self._step_keys = []
        for i in range(5):
            k = self._add_object(0, 0, f"step_key_{i}", "key.png", w=1, h=1)
            k.visible = False
            k.active  = False
            self._step_keys.append(k)

        # Saída final (carro saindo)
        self._add_object(23 * TS, 5 * TS, "exit_door", "door_open.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("GARAGEM — Fase Final!\n"
                         "Instale a bateria, encontre a chave do carro\n"
                         "e abra o portão para escapar!", duration=6000)

        # Progresso interno
        self._progress = 0   # 0-5

    def _place_mobs(self):
        TS = TILE_SIZE
        # Mobs reduzidos para dificuldade balanceada (dreamcore)
        self._add_mob("nightmare_spider",    16 * TS, 4 * TS)
        self._add_mob("shadow_creature", 10 * TS, 10 * TS)

    def _advance_progress(self):
        self._progress += 1
        if self._progress <= 5:
            k = self._step_keys[self._progress - 1]
            k.active  = True
            self.keys_collected = self._progress
            if self._progress >= 5:
                self._unlock_exit()

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        # Pegar bateria
        if oid == "battery" and obj.active:
            player.pick_up("battery")
            obj.active  = False
            obj.visible = False
            self.hud.add_notification("Você pegou a bateria!", color=(200, 220, 100))
            return

        # Instalar bateria no painel
        if oid == "electric_panel" and obj.active:
            if player.has_item("battery"):
                player.remove_item("battery")
                obj.active = False
                self._battery_installed = True
                self._panel_activated   = True
                self._advance_progress()
                self.hud.add_notification("Bateria instalada! Energia restaurada!", color=YELLOW_COLOR)
            else:
                self.show_dialog("O painel elétrico está sem energia.\nPrecisa de uma bateria.")
            return

        # Compartimento secreto
        if oid == "secret_compartment" and obj.active:
            if self._battery_installed:
                obj.active  = False
                obj.visible = False
                self._car_key_obj.visible = True
                self._car_key_obj.active  = True
                self.hud.add_notification("Compartimento aberto! Chave do carro encontrada!", color=YELLOW_COLOR)
            else:
                self.show_dialog("O compartimento está bloqueado.\nPrecisa restaurar a energia primeiro.")
            return

        # Chave do carro
        if oid == "car_key" and obj.active:
            player.pick_up("car_key")
            obj.active  = False
            obj.visible = False
            self._car_key_found = True
            self._advance_progress()
            self.hud.add_notification("Você pegou a chave do carro!", color=YELLOW_COLOR)
            return

        # Sequência de ativação do carro
        if oid == "fuel_btn" and obj.active:
            if "fuel" not in self._car_steps_done:
                self._car_steps_done.append("fuel")
                obj.active = False
                obj.visible = False
                self.hud.add_notification("Combustível verificado!", color=(180, 220, 100))
                self._check_car_sequence()
            return

        if oid == "ignition_btn" and obj.active:
            if "fuel" in self._car_steps_done and "ignition" not in self._car_steps_done:
                self._car_steps_done.append("ignition")
                obj.active = False
                obj.visible = False
                self.hud.add_notification("Ignição ativada!", color=(180, 220, 100))
                self._check_car_sequence()
            elif "fuel" not in self._car_steps_done:
                self.show_dialog("Verifique o combustível primeiro!")
            return

        if oid == "gear_btn" and obj.active:
            if "ignition" in self._car_steps_done and "gear" not in self._car_steps_done:
                self._car_steps_done.append("gear")
                obj.active = False
                obj.visible = False
                self.hud.add_notification("Marcha engatada!", color=(180, 220, 100))
                self._check_car_sequence()
            elif "ignition" not in self._car_steps_done:
                self.show_dialog("Ative a ignição primeiro!")
            return

        # Carro (dar partida)
        if oid == "car" and obj.active:
            if len(self._car_steps_done) == 3 and self._car_key_found and self._gate_open:
                self._advance_progress()
                self.hud.add_notification("O carro está pronto! Saindo...", color=YELLOW_COLOR)
                self._on_phase_complete()
            elif not self._car_key_found:
                self.show_dialog("Você precisa da chave do carro!")
            elif len(self._car_steps_done) < 3:
                self.show_dialog("O carro não está pronto.\nSiga a sequência: combustível → ignição → marcha")
            elif not self._gate_open:
                self.show_dialog("O portão está fechado!\nAbra o portão primeiro.")
            return

        # Portão
        if oid == "gate" and obj.active:
            if self._panel_activated and len(self._car_steps_done) == 3:
                obj.active  = False
                try:
                    obj.image = sprite("door_open.png", scale=PIXEL_SCALE)
                except:
                    pass
                self._gate_open = True
                self._advance_progress()
                self.hud.add_notification("Portão aberto! O caminho está livre!", color=YELLOW_COLOR)
            else:
                self.show_dialog("O portão está trancado.\nPrecisa de energia e do carro pronto.")
            return

        # Saída final
        if oid == "exit_door":
            if self._gate_open and self._car_key_found and len(self._car_steps_done) == 3:
                self._on_phase_complete()
            else:
                self.show_dialog("Você ainda não pode sair.\nPrepare o carro e abra o portão!")

    def _check_car_sequence(self):
        if len(self._car_steps_done) == 3:
            self._advance_progress()
            self.hud.add_notification("Carro pronto! Abra o portão para sair!", color=YELLOW_COLOR)

    def _on_phase_complete(self):
        """Fase final → cena de vitória."""
        if not self.phase_complete:
            self.phase_complete = True
            self.hud.add_notification("VOCÊ ESCAPOU! Parabéns!", color=(255, 220, 50))
            self.game.change_scene(SCENE_WIN)
