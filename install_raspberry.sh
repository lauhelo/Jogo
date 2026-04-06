#!/bin/bash
# Script de instalação do Escape Room para Raspberry Pi
# Execute com: bash install_raspberry.sh

echo "=== Instalando Escape Room no Raspberry Pi ==="

# Atualiza pacotes
sudo apt-get update -y

# Instala Python e pygame
sudo apt-get install -y python3 python3-pip python3-pygame

# Instala pygame via pip (versão mais recente)
pip3 install pygame --upgrade

echo ""
echo "=== Instalação concluída! ==="
echo ""
echo "Para jogar, execute:"
echo "  cd $(pwd)"
echo "  python3 main.py"
echo ""
echo "Controles:"
echo "  Jogador 1: WASD para mover, E para interagir"
echo "  Jogador 2: Setas para mover, Enter para interagir"
echo "  F4: Sair do jogo"
