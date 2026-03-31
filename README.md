# ESCAPE ROOM — Pixel Art para 2 Jogadores

> *"Você estava dormindo… mas acabou entrando em um pesadelo. Você não consegue sair."*

Jogo de Escape Room em pixel art para **2 jogadores simultâneos**, desenvolvido em Python + Pygame, otimizado para **Raspberry Pi**.

---

## Como Jogar

### Requisitos
- Python 3.x
- Pygame 2.x

### Instalação no Raspberry Pi

```bash
bash install_raspberry.sh
```

### Executar o Jogo

```bash
python3 main.py
```

---

## Controles

| Ação       | Jogador 1 | Jogador 2     |
|------------|-----------|---------------|
| Mover      | WASD      | Setas         |
| Interagir  | E         | Enter         |
| Sair       | F4        | F4            |
| Menu       | ESC       | ESC           |

---

## Telas do Jogo

### Tela de Título
Menu principal com opções: **Jogar**, **Créditos** e **Sair**.

### Seleção de Personagem
Cada jogador escolhe independentemente seu personagem:
- **Menino** — camisa azul
- **Menina** — blusa rosa e saia

**Jogador 1** usa `A/D` para navegar e `E` para confirmar.
**Jogador 2** usa `◄/►` para navegar e `Enter` para confirmar.

### Introdução
Sequência de texto narrando a história: os jogadores entram em um pesadelo e precisam encontrar a saída. O amigo imaginário aparece para ajudar.

---

## Fases

| # | Fase             | Chaves | Inimigos                    |
|---|------------------|--------|-----------------------------|
| 1 | Jardim           | 3      | Slimes com patrulha fixa    |
| 2 | Escritório       | 3      | Slimes que perseguem        |
| 3 | Cozinha          | 3      | Slimes rápidos              |
| 4 | Quarto 1         | 3      | Slimes + Fantasmas          |
| 5 | Sótão            | 3      | Fantasmas irregulares       |
| 6 | Quarto 2 (Suíte) | 3      | Aranhas agressivas          |
| 7 | Porão            | 3      | Aranhas rápidas             |
| 8 | Garagem (Final)  | 5      | Múltiplos inimigos rápidos  |

### Mecânicas por Fase

**Jardim**
- Encontrar a pá e cavar na grama diferente (1ª chave)
- Ativar flores na ordem correta: vermelho → azul → amarelo → roxo (2ª chave)
- Empurrar a pedra especial (3ª chave)

**Escritório**
- Abrir armários na ordem: 1 → 3 → 2 (1ª chave)
- Encontrar a estante com padrão especial (2ª chave)
- Derrubar objeto da prateleira (3ª chave)

**Cozinha**
- Ativar botões: verde → vermelho → verde (1ª chave)
- Usar faca para abrir saco (2ª chave)
- Empilhar caixas para área elevada (3ª chave)

**Quarto 1**
- Encontrar o travesseiro correto (1ª chave)
- Acionar objetos: livro → espelho → caixa (2ª chave)
- Ler livro de pistas e abrir baú (3ª chave)

**Sótão**
- Identificar a caixa correta (1ª chave)
- Coletar e montar as 2 partes do objeto (2ª chave)
- Resolver o enigma: "FIM" tem 3 letras (3ª chave)

**Quarto 2 (Suíte)**
- Coletar 3 partes da chave e montar (1ª chave)
- Ativar 3 pontos do cenário (2ª chave)
- Usar o espelho (3ª chave)

**Porão**
- Abrir as 2 fechaduras (1ª chave)
- Ativar 4 mecanismos (2ª chave)
- Abrir o baú central (3ª chave)

**Garagem (Final)**
- Instalar bateria no painel elétrico
- Encontrar chave do carro no compartimento secreto
- Seguir sequência: combustível → ignição → marcha
- Abrir o portão
- Dar partida no carro e escapar!

---

## Sistema de Vida

- Cada jogador começa com **3 corações**
- Ao encostar em um inimigo, perde 1 coração
- Há **invulnerabilidade temporária** após levar dano (efeito de piscar)
- Ao perder todos os corações, volta para a **fase anterior**

---

## Estrutura do Projeto

```
escape_room/
├── main.py                    # Entrada do jogo
├── install_raspberry.sh       # Script de instalação
├── assets/
│   ├── sprites/               # Personagens, inimigos, objetos
│   ├── tiles/                 # Tiles de chão e parede
│   └── ui/                    # Corações, ícones de seleção
└── src/
    ├── game.py                # Engine principal
    ├── constants.py           # Configurações globais
    ├── entities/
    │   ├── player.py          # Entidade jogador
    │   └── mob.py             # Entidade inimigo
    ├── systems/
    │   ├── hud.py             # Interface do usuário
    │   └── camera.py          # Sistema de câmera
    ├── utils/
    │   └── assets.py          # Carregamento de assets
    └── scenes/
        ├── title_scene.py     # Tela de título
        ├── select_scene.py    # Seleção de personagem
        ├── intro_scene.py     # Introdução/história
        ├── gameover_scene.py  # Game over e vitória
        ├── credits_scene.py   # Créditos
        ├── base_phase.py      # Classe base das fases
        ├── phase_garden.py    # Fase 1: Jardim
        ├── phase_office.py    # Fase 2: Escritório
        ├── phase_kitchen.py   # Fase 3: Cozinha
        ├── phase_bedroom1.py  # Fase 4: Quarto 1
        ├── phase_attic.py     # Fase 5: Sótão
        ├── phase_bedroom2.py  # Fase 6: Quarto 2
        ├── phase_basement.py  # Fase 7: Porão
        └── phase_garage.py    # Fase 8: Garagem (Final)
```

---

## Créditos

História escrita por **Alicia**. Desenvolvido com Python + Pygame.
