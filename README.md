# Escape Room: O Pesadelo

**Escape Room** é um jogo de aventura e puzzle em pixel art desenvolvido em Python com Pygame, projetado especificamente para rodar em um **Raspberry Pi**. O jogo suporta 2 jogadores em modo cooperativo local.

## 🎮 História
Você estava dormindo… mas acabou entrando em um pesadelo. Você não consegue sair. Para acordar, você deve atravessar 8 fases repletas de enigmas, perigos e mistérios. Felizmente, você não está sozinho: um **Fantasma Ajudante** apareceu para guiá-lo através deste sonho sombrio.

##  Como Rodar no Raspberry Pi

### Pré-requisitos
Certifique-se de ter o Python 3 instalado no seu sistema.

### Instalação Automática
Abra o terminal na pasta do jogo e execute o script de instalação:
```bash
bash install_raspberry.sh
```

### Execução Manual
Se preferir instalar manualmente as bibliotecas necessárias:
```bash
sudo apt-get update
sudo apt-get install python3-pygame
python3 main.py
```

## 🛠️ Requisitos do Sistema

### Pré-requisitos
- **Python 3.7+** (recomendado Python 3.11+)
- Sistema operacional: Linux (Raspberry Pi), Windows ou macOS

### Bibliotecas Necessárias
*   **Pygame (>= 2.0.0):** A única biblioteca externa necessária. Responsável por toda a engine gráfica, física, áudio e entrada de dados.

**Nota:** Todas as outras dependências (os, sys, random, math) são bibliotecas padrão do Python e já vêm incluídas na instalação padrão.

## 🕹️ Controles

| Ação | Jogador 1 (Humano) | Jogador 2 (Fantasma) |
| :--- | :--- | :--- |
| **Mover** | `W`, `A`, `S`, `D` | `Setas (↑, ↓, ←, →)` |
| **Interagir** | `E` | `Enter` |
| **Sair do Jogo** | `F4` | `F4` |
| **Menu de Pausa** | `Esc` | `Esc` |



## 🗺️ Fases do Jogo

1.  **Jardim:** Encontre a pá, cave na grama e ative as flores na ordem correta.
2.  **Escritório:** Ordem dos armários (1→3→2) e estante especial.
3.  **Cozinha:** Botões coloridos e empilhamento de caixas.
4.  **Quarto 1:** Travesseiro correto e sequência de objetos.
5.  **Sótão:** Identificação de caixas e montagem de itens.
6.  **Quarto 2 (Suíte):** Coleta de partes de chave e pontos de ativação.
7.  **Porão:** Fechaduras duplas e mecanismos complexos.
8.  **Garagem (Final):** Instalação de bateria, combustível e fuga de carro!
---
**Dica:** Preste atenção no ambiente e em todas as pistas para sair do sonho!
