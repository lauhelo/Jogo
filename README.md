# Escape Room: O Pesadelo

**Escape Room** é um jogo de aventura e puzzle em pixel art desenvolvido em Python com Pygame, projetado especificamente para rodar em um **Raspberry Pi**. O jogo suporta 2 jogadores em modo cooperativo local.

## 🎮 História
Você estava dormindo… mas acabou entrando em um pesadelo. Você não consegue sair. Para acordar, você deve atravessar 8 fases repletas de enigmas, perigos e mistérios. Felizmente, você não está sozinho: um **Fantasma Ajudante** apareceu para guiá-lo através deste sonho sombrio.

## 📦 Instalação

### Opção 1: Instalação Automática (Raspberry Pi)
Abra o terminal na pasta do jogo e execute o script de instalação:
```bash
bash install_raspberry.sh
```

### Opção 2: Instalação Manual

#### Passo 1: Instalar Python
Certifique-se de ter o Python 3.7+ instalado:
```bash
# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3 python3-pip

# Windows
# Baixe e instale do site oficial: https://python.org

# macOS
# Use Homebrew: brew install python3
```

#### Passo 2: Criar Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

#### Passo 3: Instalar Dependências
```bash
# Instalar pygame
pip install pygame

# Ou instalar todas as dependências do arquivo requirements.txt
pip install -r requirements.txt
```

#### Passo 4: Executar o Jogo
```bash
python3 main.py
```

## 🛠️ Requisitos do Sistema

### Pré-requisitos
- **Python 3.7+** (recomendado Python 3.11+)
- Sistema operacional: Linux (Raspberry Pi), Windows ou macOS

### Bibliotecas Necessárias
*   **Pygame (>= 2.0.0):** A única biblioteca externa necessária. Responsável por toda a engine gráfica, física, áudio e entrada de dados.

**Nota:** Todas as outras dependências (os, sys, random, math) são bibliotecas padrão do Python e já vêm incluídas na instalação padrão.

## 🎮 Como Jogar

Após executar `python3 main.py`, você verá a tela de título. Pressione ENTER para começar.

O jogo é uma aventura cooperativo para 2 jogadores onde vocês devem escapar de um pesadelo resolvendo enigmas e puzzles através de 8 fases diferentes.

## 🕹️ Controles

| Ação | Jogador 1 (Humano) | Jogador 2 (Fantasma) |
| :--- | :--- | :--- |
| **Mover** | `W`, `A`, `S`, `D` | `Setas (↑, ↓, ←, →)` |
| **Interagir** | `E` | `Enter` |
| **Sair do Jogo** | `F4` | `F4` |
| **Menu de Pausa** | `Esc` | `Esc` |

### 🎮 Suporte a Joystick/Controle USB

O jogo suporta **até 2 joysticks USB** conectados simultaneamente! Você pode jogar com:
- ✅ **Teclado** (WASD + Setas)
- ✅ **Joystick USB** (1 ou 2 controles)
- ✅ **Combinação** (teclado + joystick ao mesmo tempo)

#### Como usar:

1. **Conecte 1 ou 2 joysticks USB** ao seu computador
2. **Execute o jogo:**
   ```bash
   python3 main.py
   ```
3. O jogo **detectará automaticamente** os joysticks
4. Use os **sticks analógicos** ou **D-pad** para mover
5. Use **X, A ou outro botão primário** para interagir

#### Mapeamento de Botões:

- **Analógico/D-pad**: Movimento (cima/baixo/esquerda/direita)
- **Botão X** ou **Botão A**: Interagir/Ativar
- **Botão Pause/Menu**: Pausa o jogo (via teclado ESC)

#### Compatibilidade:

Funciona com qualquer **joystick USB padrão** conectado via USB:
- ✅ Xbox One/Series controllers
- ✅ PlayStation 4/5 controllers
- ✅ Controles genéricos USB
- ✅ Arcade joysticks
- ✅ **Especial para Raspberry Pi** - ligoque o joystick USB direto à porta/hub USB do RPi

#### ⚠️ Notas:

- Teclado e joystick funcionam **simultaneamente** (você pode usar ambos)
- Se nenhum joystick estiver conectado, o jogo usa apenas teclado
- Joystick funciona **tanto em Windows como em Raspberry Pi**


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
