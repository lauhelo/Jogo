"""
Fase 5: Sótão
- Identificar a caixa correta com base em detalhes visuais
- Montar objeto quebrado para liberar a chave
- Resolver enigma simples para abrir baú escondido
- Inimigos: movimentação irregular, aparecem em pontos aleatórios
"""
import pygame
import random
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_ATTIC
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class AtticPhase(BasePhase):

    PHASE_KEY   = PHASE_ATTIC
    KEYS_NEEDED = 3

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

        # Várias caixas (a correta tem detalhe visual diferente)
        box_positions = [
            (4 * TS, 3 * TS, False),
            (8 * TS, 5 * TS, False),
            (12 * TS, 3 * TS, True),   # caixa correta
            (16 * TS, 6 * TS, False),
            (20 * TS, 4 * TS, False),
        ]
        for bx, by, is_correct in box_positions:
            bid = "box_correct" if is_correct else "box_wrong"
            self._add_object(bx, by, bid, "box.png")

        self._box_key = self._add_object(12 * TS + 4, 4 * TS, "key_box",
                                          "key.png", w=24, h=24)
        self._box_key.visible = False

        # Objeto quebrado (partes para montar)
        self._add_object(6 * TS, 9 * TS, "part_a", "shovel.png")
        self._add_object(18 * TS, 10 * TS, "part_b", "book.png")
        self._parts_collected = []

        self._assembled_key = self._add_object(12 * TS, 9 * TS, "key_assembled",
                                                "key.png", w=24, h=24)
        self._assembled_key.visible = False

        # Baú com enigma (resposta: 3)
        self._add_object(22 * TS, 7 * TS, "enigma_chest", "chest.png")
        self._enigma_solved = False
        self._enigma_key = self._add_object(22 * TS + 4, 8 * TS, "key_enigma",
                                             "key.png", w=24, h=24)
        self._enigma_key.visible = False

        # Porta de saída
        self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("Sótão: Encontre as 3 chaves!\n"
                         "Cuidado com os inimigos que aparecem aleatoriamente.", duration=5000)

        # Enigma
        self._enigma_text = "Tenho início, meio e fim.\nQuantas letras tem 'FIM'?\n(Pressione 1, 2, 3 ou 4 para responder)"
        self._waiting_enigma = False

    def _place_mobs(self):
        TS = TILE_SIZE
        self._add_mob("wraith", 10 * TS, 7 * TS)
        self._add_mob("wraith", 20 * TS, 3 * TS)
        self._add_mob("void_blob", 14 * TS, 11 * TS)

    def handle_event(self, event):
        super().handle_event(event)
        if self._waiting_enigma and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self._enigma_solved = True
                self._waiting_enigma = False
                self._enigma_key.visible = True
                self._enigma_key.active  = True
                self.hud.add_notification("Resposta correta! O baú abriu!", color=YELLOW_COLOR)
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_4):
                self._waiting_enigma = False
                self.show_dialog("Resposta errada! Tente novamente.")

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        if oid == "box_correct" and obj.active:
            obj.active  = False
            obj.visible = False
            self._box_key.visible = True
            self._box_key.active  = True
            self.hud.add_notification("Você encontrou a caixa certa!", color=YELLOW_COLOR)
            return

        if oid == "box_wrong":
            self.show_dialog("Caixa errada... Procure a que tem um detalhe diferente.")
            return

        if oid == "key_box" and obj.active:
            self._collect_key(player, obj)
            return

        if oid in ("part_a", "part_b") and obj.active:
            if oid in self._parts_collected:
                return
            player.pick_up(oid)
            obj.active  = False
            obj.visible = False
            self._parts_collected.append(oid)
            if len(self._parts_collected) == 2:
                self._assembled_key.visible = True
                self._assembled_key.active  = True
                self.hud.add_notification("Você montou o objeto e encontrou uma chave!", color=YELLOW_COLOR)
            else:
                self.hud.add_notification("Parte coletada! Encontre a outra.", color=(200, 180, 100))
            return

        if oid == "key_assembled" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "enigma_chest" and obj.active:
            if not self._enigma_solved:
                self._waiting_enigma = True
                self.show_dialog(self._enigma_text)
            else:
                self.hud.add_notification("Já resolvido!", color=(180, 180, 180))
            return

        if oid == "key_enigma" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"Porta trancada. ({self.keys_collected}/{self.KEYS_NEEDED} chaves)")
