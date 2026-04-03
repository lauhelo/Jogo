"""
Fase 4: Quarto 1
- Identificar o travesseiro correto e encontrar a chave escondida
- Acionar objetos na ordem correta para abrir gaveta secreta
- Usar pistas de um livro para descobrir qual objeto guarda a chave
- Inimigos: surgem próximos ao jogador, movimentação moderada
"""
import pygame
from src.scenes.base_phase import BasePhase
from src.constants import TILE_SIZE, PIXEL_SCALE, PHASE_BEDROOM1
from src.utils.assets import sprite

YELLOW_COLOR = (255, 220, 50)


class Bedroom1Phase(BasePhase):

    PHASE_KEY   = PHASE_BEDROOM1
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

        # Cama com travesseiros (o do meio tem a chave)
        self._add_object(5 * TS, 3 * TS, "bed", "bed.png", w=TS * 2, h=TS)

        pillow_positions = [
            (5 * TS,  2 * TS, False),
            (7 * TS,  2 * TS, True),   # travesseiro correto
            (9 * TS,  2 * TS, False),
        ]
        self._pillow_key = None
        for px, py, is_correct in pillow_positions:
            pid = "pillow_correct" if is_correct else "pillow_wrong"
            obj = self._add_object(px, py, pid, "pillow.png")
        self._pillow_key_item = self._add_object(7 * TS + 4, 3 * TS, "key_pillow",
                                                  "key.png", w=24, h=24)
        self._pillow_key_item.visible = False

        # Objetos para acionar em ordem (gaveta secreta)
        # Ordem: livro → espelho → caixa
        self._drawer_order = ["book_obj", "mirror_obj", "box_obj"]
        self._drawer_pressed = []

        self._add_object(3 * TS,  8 * TS, "book_obj",   "book.png")
        self._add_object(12 * TS, 5 * TS, "mirror_obj", "mirror.png")
        self._add_object(18 * TS, 9 * TS, "box_obj",    "box.png")

        self._drawer_key = self._add_object(10 * TS, 7 * TS, "key_drawer",
                                             "key.png", w=24, h=24)
        self._drawer_key.visible = False

        # Livro com pistas (revela qual objeto tem a chave 3)
        self._add_object(20 * TS, 3 * TS, "clue_book", "book.png")
        self._clue_read = False

        # Objeto que guarda a chave 3 (revelado pelo livro)
        self._add_object(22 * TS, 8 * TS, "secret_obj", "chest.png")
        self._secret_key = self._add_object(22 * TS + 4, 9 * TS, "key_secret",
                                             "key.png", w=24, h=24)
        self._secret_key.visible = False

        # Porta de saída
        self._add_object(23 * TS, 6 * TS, "exit_door", "door_locked.png",
                         w=TS, h=TS * 2)

        self._spawn_positions = [(2 * TS, 6 * TS), (2 * TS, 8 * TS)]

        self.show_dialog("Quarto 1: Encontre as 3 chaves!\n"
                         "Leia o livro para descobrir pistas.", duration=5000)

    def _place_mobs(self):
        TS = TILE_SIZE
        # Surgem próximos ao jogador
        self._add_mob("shadow_creature",  8 * TS, 10 * TS)
        self._add_mob("void_blob", 15 * TS, 7 * TS)
        self._add_mob("wraith",      20 * TS, 5 * TS)

    def _on_interact(self, player, obj):
        oid = obj.obj_id

        # Travesseiro correto
        if oid == "pillow_correct" and obj.active:
            obj.active  = False
            obj.visible = False
            self._pillow_key_item.visible = True
            self._pillow_key_item.active  = True
            self.hud.add_notification("Você encontrou uma chave no travesseiro!", color=YELLOW_COLOR)
            return

        if oid == "pillow_wrong":
            self.show_dialog("Nada aqui... Tente o travesseiro do meio.")
            return

        if oid == "key_pillow" and obj.active:
            self._collect_key(player, obj)
            return

        # Gaveta secreta (ordem: livro → espelho → caixa)
        if oid in self._drawer_order and obj.active:
            if oid in self._drawer_pressed:
                return

            expected = self._drawer_order[len(self._drawer_pressed)]
            if oid == expected:
                self._drawer_pressed.append(oid)
                self.hud.add_notification(f"Objeto ativado! ({len(self._drawer_pressed)}/3)", color=(180, 220, 100))
                if len(self._drawer_pressed) == 3:
                    self._drawer_key.visible = True
                    self._drawer_key.active  = True
                    self.hud.add_notification("A gaveta secreta abriu!", color=YELLOW_COLOR)
            else:
                self._drawer_pressed = []
                self.show_dialog("Ordem errada! Recomeçando...\nDica: livro → espelho → caixa")
            return

        if oid == "key_drawer" and obj.active:
            self._collect_key(player, obj)
            return

        # Livro de pistas
        if oid == "clue_book" and obj.active:
            self._clue_read = True
            self.show_dialog("O livro diz:\n\"O tesouro está guardado no baú\nno canto mais escuro do quarto.\"")
            return

        # Objeto secreto (baú)
        if oid == "secret_obj" and obj.active:
            if self._clue_read:
                obj.active  = False
                obj.visible = False
                self._secret_key.visible = True
                self._secret_key.active  = True
                self.hud.add_notification("Você abriu o baú e encontrou uma chave!", color=YELLOW_COLOR)
            else:
                self.show_dialog("Parece um baú comum... Talvez haja uma pista em algum livro.")
            return

        if oid == "key_secret" and obj.active:
            self._collect_key(player, obj)
            return

        if oid == "exit_door":
            if self.keys_collected >= self.KEYS_NEEDED:
                self._on_phase_complete()
            else:
                self.show_dialog(f"Porta trancada. ({self.keys_collected}/{self.KEYS_NEEDED} chaves)")
