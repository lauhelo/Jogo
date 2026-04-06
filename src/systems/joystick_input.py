"""
Joystick Input System — Suporte a controles USB conectados ao Pygame

Permite mapear 1 ou 2 joysticks USB para as ações do jogo.
Funciona com teclado simultaneamente (ambos podem ser usados).
"""
import pygame
from typing import Dict, Optional


class JoystickInputSystem:
    """
    Gerencia entrada via joysticks USB conectados.
    Detecta até 2 joysticks automaticamente.
    """

    def __init__(self):
        """Inicializa o subsistema de joystick."""
        pygame.joystick.init()
        self.joysticks = []
        self.num_joysticks = 0
        self._detect_joysticks()

        # Deadzone para analog sticks (evita drift pequeno)
        self.deadzone = 0.5

    def _detect_joysticks(self):
        """Detecta joysticks conectados."""
        try:
            joystick_count = pygame.joystick.get_count()
            if joystick_count == 0:
                print("[Joystick] Nenhum joystick conectado")
                return

            for i in range(min(joystick_count, 2)):  # Máximo 2 joysticks
                joy = pygame.joystick.Joystick(i)
                joy.init()
                self.joysticks.append(joy)
                print(f"[Joystick {i}] {joy.get_name()} conectado")
                print(f"  - Botões: {joy.get_numbuttons()}")
                print(f"  - Eixos: {joy.get_numaxes()}")
                print(f"  - Hats: {joy.get_numhats()}")

            self.num_joysticks = len(self.joysticks)
        except Exception as e:
            print(f"[Joystick] Erro ao detectar joysticks: {e}")

    def get_joystick_input(self, joystick_index: int = 0) -> Dict[str, bool]:
        """
        Retorna estado do joystick como dicionário de ações.
        
        Args:
            joystick_index: 0 ou 1 (qual joystick)
            
        Returns:
            Dict com {'up': bool, 'down': bool, 'left': bool, 'right': bool, 'action': bool}
        """
        if joystick_index >= len(self.joysticks):
            return {'up': False, 'down': False, 'left': False, 'right': False, 'action': False}

        joy = self.joysticks[joystick_index]
        result = {'up': False, 'down': False, 'left': False, 'right': False, 'action': False}

        try:
            # Lê analog stick esquerdo (eixo 0=X, 1=Y)
            if joy.get_numaxes() >= 2:
                x = joy.get_axis(0)
                y = joy.get_axis(1)

                # Threshold para considerar movimento
                if x < -self.deadzone:
                    result['left'] = True
                elif x > self.deadzone:
                    result['right'] = True

                if y < -self.deadzone:
                    result['up'] = True
                elif y > self.deadzone:
                    result['down'] = True

            # Lê D-pad / Hat (direcional analógico)
            if joy.get_numhats() > 0:
                hat = joy.get_hat(0)  # (x, y) onde cada é -1, 0 ou 1
                if hat[0] < 0:
                    result['left'] = True
                elif hat[0] > 0:
                    result['right'] = True

                if hat[1] > 0:  # Hat Y é invertido
                    result['up'] = True
                elif hat[1] < 0:
                    result['down'] = True

            # Botão de ação: X (botão 0), A (botão 0), ou equivalente
            # Tenta vários padrões de mapeamento comum
            if joy.get_numbuttons() > 0:
                # Botão 0 (X em Xbox, Cross em PlayStation, primário)
                if joy.get_button(0):
                    result['action'] = True
                # Botão 1 (A em Xbox, Circle em PlayStation, secundário)
                elif joy.get_button(1):
                    result['action'] = True
                # Botão 8 (pode ser Select/Back em alguns controles)
                elif joy.get_numbuttons() > 7 and joy.get_button(7):
                    result['action'] = True

        except Exception as e:
            print(f"[Joystick {joystick_index}] Erro ao ler: {e}")

        return result

    def get_all_joystick_states(self) -> list:
        """
        Retorna lista com estado de todos os joysticks.
        
        Returns:
            [joy0_state, joy1_state, ...] onde cada estado é um dict
        """
        return [self.get_joystick_input(i) for i in range(self.num_joysticks)]

    def has_joysticks(self) -> bool:
        """Retorna True se há pelo menos um joystick conectado."""
        return self.num_joysticks > 0

    def merge_inputs(self, keyboard_keys: Dict[str, bool], 
                    joystick_keys: Dict[str, bool]) -> Dict[str, bool]:
        """
        Mescla input de teclado e joystick.
        Joystick tem prioridade (sobrescreve teclado).
        
        Args:
            keyboard_keys: Dict de input de teclado
            joystick_keys: Dict de input de joystick
            
        Returns:
            Dict mesclado
        """
        result = keyboard_keys.copy()
        for action, pressed in joystick_keys.items():
            if pressed:
                result[action] = True
        return result
