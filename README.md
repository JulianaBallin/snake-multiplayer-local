<p align="center">
  <img src="docs/diagrams/logo.svg" alt="Snake Multiplayer Local" width="420">
</p>

<p align="center">
  Jogo da cobrinha <strong>multiplayer local</strong> para 2 jogadores simultâneos,<br>
  para <strong>até 4 jogadores simultâneos</strong>, construido sobre a arquitetura do Asteroids Singleplayer.<br>
  <em>Atividade 0010 | UEA · Tópicos Especiais I</em>
</p>

---

<h2 align="center">Tecnologias Utilizadas</h2>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Pygame" src="https://img.shields.io/badge/pygame-2.x-green?style=for-the-badge&logo=python&logoColor=white">
  <img alt="C4" src="https://img.shields.io/badge/C4%20Model-Diagramas-9B59B6?style=for-the-badge">
  <img alt="PlantUML" src="https://img.shields.io/badge/PlantUML-Documentação-FBBC04?style=for-the-badge">
</p>

---

<h2 align="center">Descrição do Projeto</h2>

Este projeto é o clássico jogo da cobrinha reimplementado como **multiplayer local** para dois jogadores no mesmo teclado. A base arquitetural foi herdada do repositório [asteroids_single-player](../asteroids_single-player), mantendo a separação entre domínio (`core/`) e apresentação (`client/`).

Cada jogador controla uma cobra independente. A cobra cresce ao comer alimentos, e o jogo termina quando uma cobra colide com a parede, com o próprio corpo ou com o corpo da cobra adversária.

---

<h2 align="center">Mecanica do Jogo</h2>

**Objetivo**

Comer o maior número de alimentos possível sem colidir com paredes, com o próprio corpo ou com a cobra adversária.

**Regras**

- O tabuleiro tem 40 x 30 células de 20 px cada.
- A cobra se move uma célula por tick (a cada 0,12 s).
- Ao comer um alimento, a cobra cresce 3 células e um novo alimento aparece.
- Colisão com parede, corpo próprio ou corpo do adversário elimina a cobra.
- Colisão de cabeça contra cabeça no mesmo tick elimina ambas as cobras.
- A partida termina quando pelo menos uma cobra é eliminada.
- Vence quem sobreviver. Em caso de morte simultânea, vence quem tiver maior pontuação.

---

<h2 align="center">Controles</h2>

| Jogador | Cima | Baixo | Esquerda | Direita |
|---------|------|-------|----------|---------|
| **J1 (Ciano)** | `W` | `S` | `A` | `D` |
| **J2 (Amarelo)** | `↑` | `↓` | `←` | `→` |
| **J3 (Verde)** | `I` | `K` | `J` | `L` |
| **J4 (Vermelho)** | `Num8` | `Num2` | `Num4` | `Num6` |

`ESC` encerra o jogo a qualquer momento.

---

<h2 align="center">Estrutura do Projeto</h2>

```text
snake-multiplayer-local/
├── src/
│   ├── main.py              # ponto de entrada
│   ├── core/
│   │   ├── config.py        # constantes, cores e posicoes iniciais
│   │   ├── commands.py      # PlayerCommand (direcao por frame)
│   │   ├── entities.py      # Snake (corpo, direcao, grow) e Food
│   │   ├── world.py         # estado do jogo, tick, colisoes e pontuacao
│   │   ├── scene.py         # enum SceneState
│   │   └── utils.py         # celulas livres e posicao aleatoria
│   └── client/
│       ├── game.py          # loop principal e transicoes de cena
│       ├── renderer.py      # renderizacao de entidades e HUD
│       └── controls.py      # mapeamento de teclas para PlayerCommand
├── docs/
│   └── diagrams/
│       ├── logo.svg
│       ├── c4_nivel1_contexto.puml
│       ├── c4_nivel2_container.puml
│       └── c4_nivel3_componente.puml
├── requirements.txt
├── LICENSE
└── README.md
```

---

<h2 align="center">Como Executar</h2>

**1. Clonar o repositório**

```bash
git clone https://github.com/JulianaBallin/snake-multiplayer-local.git
cd snake-multiplayer-local
```

**2. Criar ambiente virtual**

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
```

**3. Instalar dependências**

```bash
pip install -r requirements.txt
```

**4. Iniciar o jogo**

```bash
python src/main.py
```

---

<h2 align="center">Dependências</h2>

```txt
pygame>=2.5.0
```

---

<h2 align="center">Decisoes Arquiteturais</h2>

A arquitetura segue o mesmo padrão do projeto Asteroids Singleplayer:

| Camada | Pacote | Responsabilidade |
|--------|--------|------------------|
| Domínio | `core/` | Toda a logica do jogo: entidades, mundo, colisoes e regras. Sem dependência de pygame. |
| Apresentação | `client/` | Loop do jogo, renderizacao e mapeamento de input. Depende de pygame e de `core/`. |
| Entrada | `main.py` | Ponto de entrada mínimo que instancia `Game` e chama `run()`. |

O isolamento do domínio permite testar a logica do jogo sem inicializar display ou audio.

---

<h2 align="center">Diagramas C4</h2>

Os diagramas estão em `docs/diagrams/` no formato PlantUML (`.puml`).

Para renderizar, use o [PlantUML Online Server](https://www.plantuml.com/plantuml/uml/) ou o plugin PlantUML no VS Code.

| Arquivo | Nivel | Descricao |
|---------|-------|-----------|
| `c4_nivel1_contexto.puml` | Nivel 1 | Visao geral: jogadores, sistema e pygame |
| `c4_nivel2_container.puml` | Nivel 2 | Containers: main, core e client |
| `c4_nivel3_componente.puml` | Nivel 3 | Componentes internos de core e client |

---

<h2 align="center">Limitações</h2>

- Até 4 jogadores simultâneos no mesmo teclado.
- Sem suporte a joystick ou controle externo.
- Sem salvamento de pontuação entre partidas.

---

<h2 align="center">Referências</h2>

- Playlist de referência: [youtube.com/playlist?list=PLlEgNdBJEO-n8k9SR49AshB9j7b5Iw7hZ](https://www.youtube.com/playlist?list=PLlEgNdBJEO-n8k9SR49AshB9j7b5Iw7hZ)
- Documentação do pygame: [pygame.org/docs](https://www.pygame.org/docs/)
- C4 Model: [c4model.com](https://c4model.com)

---

<h2 align="center">Equipe</h2>

<p align="center">

| Nome |
| ---- |
| Ana Beatriz Maciel Nunes |
| Fernando Luiz Da Silva Freire |
| Juliana Ballin Lima |

</p>

---

<h3 align="center">UEA · Tópicos Especiais I · Atividade 0010: Snake Multiplayer Local</h3>
