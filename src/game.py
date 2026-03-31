"""
Game — classe principal que gerencia o loop do jogo,
transições de cena e estado global.
"""
import pygame
import sys
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    SCENE_TITLE, SCENE_SELECT, SCENE_INTRO,
    SCENE_GAME, SCENE_GAMEOVER, SCENE_WIN, SCENE_CREDITS,
    PHASE_ORDER, PHASE_GARDEN,
)


class Game:
    """
    Gerenciador principal do jogo.
    Controla o loop, transições de cena e estado compartilhado.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        # Tenta modo fullscreen para Raspberry Pi; fallback para janela
        try:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.NOFRAME
            )
        except:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock   = pygame.time.Clock()
        self.running = True

        # Estado global
        self.player_genders  = ["boy", "girl"]   # definido na tela de seleção
        self.current_phase   = PHASE_GARDEN
        self.phase_idx       = 0
        self.players         = []

        # Cenas
        self._scene_key = None
        self._scene     = None
        self._phase_obj = None   # fase atual (se em SCENE_GAME)

        # Inicia na tela de título
        self.change_scene(SCENE_TITLE)

    # ─── Navegação de cenas ──────────────────────────────────────────────────
    def change_scene(self, scene_key: str):
        """Troca para uma nova cena."""
        self._scene_key = scene_key
        self._scene     = self._build_scene(scene_key)

    def _build_scene(self, key: str):
        """Instancia a cena correspondente à chave."""
        if key == SCENE_TITLE:
            from src.scenes.title_scene import TitleScene
            return TitleScene(self)

        elif key == SCENE_SELECT:
            from src.scenes.select_scene import SelectScene
            return SelectScene(self)

        elif key == SCENE_INTRO:
            from src.scenes.intro_scene import IntroScene
            return IntroScene(self)

        elif key == SCENE_GAME:
            return self._build_phase(self.current_phase)

        elif key == SCENE_GAMEOVER:
            from src.scenes.gameover_scene import GameOverScene
            return GameOverScene(self)

        elif key == SCENE_WIN:
            from src.scenes.gameover_scene import WinScene
            return WinScene(self)

        elif key == SCENE_CREDITS:
            from src.scenes.credits_scene import CreditsScene
            return CreditsScene(self)

        else:
            # Fallback para título
            from src.scenes.title_scene import TitleScene
            return TitleScene(self)

    def _build_phase(self, phase_key: str):
        """Instancia a fase correspondente."""
        # Cria jogadores se necessário
        if not self.players:
            self._create_players()

        phase_map = {
            "garden":   "src.scenes.phase_garden.GardenPhase",
            "office":   "src.scenes.phase_office.OfficePhase",
            "kitchen":  "src.scenes.phase_kitchen.KitchenPhase",
            "bedroom1": "src.scenes.phase_bedroom1.Bedroom1Phase",
            "attic":    "src.scenes.phase_attic.AtticPhase",
            "bedroom2": "src.scenes.phase_bedroom2.Bedroom2Phase",
            "basement": "src.scenes.phase_basement.BasementPhase",
            "garage":   "src.scenes.phase_garage.GaragePhase",
        }

        class_path = phase_map.get(phase_key)
        if not class_path:
            from src.scenes.phase_garden import GardenPhase
            return GardenPhase(self, self.players)

        module_path, class_name = class_path.rsplit(".", 1)
        import importlib
        module = importlib.import_module(module_path)
        PhaseClass = getattr(module, class_name)
        self._phase_obj = PhaseClass(self, self.players)
        return self._phase_obj

    def _create_players(self):
        """Cria os objetos Player com os gêneros escolhidos."""
        from src.entities.player import Player
        genders = self.player_genders
        self.players = [
            Player(1, genders[0], 100, 300),
            Player(2, genders[1], 140, 300),
        ]

    # ─── Progressão de fases ─────────────────────────────────────────────────
    def advance_phase(self):
        """Avança para a próxima fase."""
        self.phase_idx += 1
        if self.phase_idx >= len(PHASE_ORDER):
            self.change_scene(SCENE_WIN)
        else:
            self.current_phase = PHASE_ORDER[self.phase_idx]
            # Restaura vida dos jogadores
            for p in self.players:
                p.restore_hearts()
                p.inventory.clear()
            self.change_scene(SCENE_GAME)

    def retry_phase(self):
        """Volta para a fase anterior (ou reinicia a atual se for a primeira)."""
        if self.phase_idx > 0:
            self.phase_idx -= 1
        self.current_phase = PHASE_ORDER[self.phase_idx]
        for p in self.players:
            p.restore_hearts()
            p.inventory.clear()
        self.change_scene(SCENE_GAME)

    # ─── Loop principal ──────────────────────────────────────────────────────
    def run(self):
        while self.running:
            dt_ms = self.clock.tick(FPS)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4:
                        self.running = False
                if self._scene:
                    self._scene.handle_event(event)

            # Update
            if self._scene:
                self._scene.update(dt_ms)

            # Draw
            self.screen.fill((0, 0, 0))
            if self._scene:
                self._scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
