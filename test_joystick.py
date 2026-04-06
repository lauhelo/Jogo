#!/usr/bin/env python3
"""
Test Joystick Support — Teste básico do sistema de joystick
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("╔════════════════════════════════════════════════════════╗")
print("║         TESTE DE SUPORTE A JOYSTICK                 ║")
print("╚════════════════════════════════════════════════════════╝\n")

# Teste 1: Importar pygame
print("[1/4] Verificando Pygame...")
try:
    import pygame
    print("  ✓ Pygame importado com sucesso")
except ImportError as e:
    print(f"  ✗ Erro: {e}")
    sys.exit(1)

# Teste 2: Importar JoystickInputSystem
print("[2/4] Verificando JoystickInputSystem...")
try:
    from src.systems.joystick_input import JoystickInputSystem
    print("  ✓ JoystickInputSystem importado com sucesso")
except ImportError as e:
    print(f"  ✗ Erro: {e}")
    sys.exit(1)

# Teste 3: Inicializar Pygame e JoystickInputSystem
print("[3/4] Inicializando Pygame e JoystickInputSystem...")
try:
    pygame.init()
    pygame.joystick.init()
    joy_system = JoystickInputSystem()
    print(f"  ✓ Inicializado com sucesso")
    print(f"  - Joysticks detectados: {joy_system.num_joysticks}")
    
    if joy_system.has_joysticks():
        for i, joy in enumerate(joy_system.joysticks):
            print(f"    [{i}] {joy.get_name()}")
    else:
        print(f"    (Nenhum joystick conectado - tudo bem, teclado funciona)")
except Exception as e:
    print(f"  ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 4: Testar leitura de input
print("[4/4] Testando leitura de input...")
try:
    if joy_system.has_joysticks():
        input_state = joy_system.get_joystick_input(0)
        print(f"  ✓ Input state (joystick 0): {input_state}")
    else:
        input_state = joy_system.get_joystick_input(0)
        print(f"  ✓ Input state (sem joystick): {input_state}")
        print(f"    (Este é o comportamento esperado quando sem joystick)")
except Exception as e:
    print(f"  ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n╔════════════════════════════════════════════════════════╗")
print("║          TODOS OS TESTES PASSARAM! ✓                 ║")
print("╚════════════════════════════════════════════════════════╝\n")

print("Sistema de joystick está funcionando normalmente.")
print("Você pode jogar com teclado, joystick, ou ambos!\n")
