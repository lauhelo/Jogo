#!/usr/bin/env python3.11
"""
ESCAPE ROOM — Jogo pixel art para 2 jogadores no Raspberry Pi.

Controles:
  Jogador 1: WASD para mover, E para interagir
  Jogador 2: Setas para mover, Enter para interagir
  F4: Sair do jogo
"""
import os
import sys

# Garante que o diretório do jogo está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurações para Raspberry Pi (sem som se não houver dispositivo)
# os.environ.setdefault("SDL_AUDIODRIVER", "dummy")  # Comentado para habilitar áudio

from src.game import Game


def main():
    # Inicia o jogo com tratamento de erro para diagnóstico
    try:
        game = Game()
        game.run()
    except Exception as e:
        import traceback
        with open("crash_log.txt", "w") as f:
            f.write(f"ERRO CRÍTICO: {str(e)}\n")
            f.write(traceback.format_exc())
        print(f"O jogo fechou devido a um erro: {e}")
        print("Detalhes salvos em crash_log.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
