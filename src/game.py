"""
Game — classe principal que gerencia o loop do jogo,
transições de cena e estado global.
"""
import os
import pygame
import sys
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    SCENE_TITLE, SCENE_SELECT, SCENE_INTRO,
    SCENE_GAME, SCENE_GAMEOVER, SCENE_WIN, SCENE_CREDITS,
    PHASE_ORDER, PHASE_GARDEN,
)
from src.systems.joystick_input import JoystickInputSystem


class Game:
    """
    Gerenciador principal do jogo.
    Controla o loop, transições de cena e estado compartilhado.
    """

    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()  # Inicializar mixer para áudio
        except Exception as e:
            print(f"Aviso: mixer não pôde inicializar (sem som): {e}")

        self._load_common_sounds()

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

        # Inicializa sistema de joystick
        self.joystick_system = JoystickInputSystem()

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

    def play_background_music(self, music_path, volume=0.25, loop=True):
        """Toca música de fundo em loop."""
        if not pygame.mixer.get_init() or not os.path.isfile(music_path):
            return
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            print(f"Tocando música: {music_path} (volume: {volume})")
        except Exception as e:
            print(f"Falha ao carregar {music_path}: {e}")

    def stop_background_music(self):
        """Para a música de fundo."""
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def _load_sound(self, candidate_files, volume=0.5):
        if not pygame.mixer.get_init():
            return None
        for p in candidate_files:
            if os.path.isfile(p):
                try:
                    s = pygame.mixer.Sound(p)
                    s.set_volume(volume)
                    return s
                except Exception as e:
                    print(f"Falha ao carregar som {p}: {e}")
        return None

    def _load_common_sounds(self):
        self.sfx = {
            'key_collect': self._load_sound(['assets/sounds/key_collect.wav', 'assets/sounds/key_collect.ogg'], 0.5),
            'door_unlock': self._load_sound(['assets/sounds/door_unlock.wav', 'assets/sounds/door_unlock.ogg'], 0.6),
            'game_over':   self._load_sound(['assets/sounds/game_over.wav', 'assets/sounds/game_over.ogg'], 0.5),
            'victory':     self._load_sound(['assets/sounds/victory.wav', 'assets/sounds/victory.ogg'], 0.7),
            'metal_click': self._load_sound(['assets/sounds/metal_click.wav', 'assets/sounds/metal_click.ogg'], 0.75),
        }

    def play_sfx(self, key):
        if not hasattr(self, 'sfx') or self.sfx.get(key) is None:
            return
        try:
            self.sfx[key].play()
        except Exception:
            pass

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

        # Importações locais para evitar circularidade
        if phase_key == "garden":
            from src.scenes.phase_garden import GardenPhase
            self._phase_obj = GardenPhase(self, self.players)
        elif phase_key == "office":
            from src.scenes.phase_office import OfficePhase
            self._phase_obj = OfficePhase(self, self.players)
        elif phase_key == "kitchen":
            from src.scenes.phase_kitchen import KitchenPhase
            self._phase_obj = KitchenPhase(self, self.players)
        elif phase_key == "bedroom1":
            from src.scenes.phase_bedroom1 import Bedroom1Phase
            self._phase_obj = Bedroom1Phase(self, self.players)
        elif phase_key == "attic":
            from src.scenes.phase_attic import AtticPhase
            self._phase_obj = AtticPhase(self, self.players)
        elif phase_key == "bedroom2":
            from src.scenes.phase_bedroom2 import Bedroom2Phase
            self._phase_obj = Bedroom2Phase(self, self.players)
        elif phase_key == "basement":
            from src.scenes.phase_basement import BasementPhase
            self._phase_obj = BasementPhase(self, self.players)
        elif phase_key == "garage":
            from src.scenes.phase_garage import GaragePhase
            self._phase_obj = GaragePhase(self, self.players)
        else:
            from src.scenes.phase_garden import GardenPhase
            self._phase_obj = GardenPhase(self, self.players)
            
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
        """Reinicia a fase atual."""
        # Mantém o phase_idx atual
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
