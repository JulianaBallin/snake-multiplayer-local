# SNAKE MULTIPLAYER LOCAL: WORKFLOW DE DESENVOLVIMENTO

**Versão:** 1.1
**Data:** 2026-05-21

---

## 1. Objetivo

Guiar o desenvolvimento do Snake Multiplayer Local por meio de Pull Requests curtos, seguros e verificáveis, garantindo qualidade técnica e rastreabilidade. O trabalho é dividido entre **3 integrantes**, cada um responsável por um conjunto coeso de atividades e por um diagrama C4.

---

## 2. Princípios

1. Nada entra na `main` sem um Pull Request revisado.
2. Cada PR deve ter escopo pequeno, coeso e testável manualmente.
3. O domínio (`core/`) é isolado e não deve importar `client/`.
4. O projeto deve permanecer funcional ao final de cada PR.
5. Commits em português, formato convencional: `tipo(arquivo): descrição`.

---

## 3. Divisão de Atividades

### Juliana Ballin Lima: Infraestrutura base e Diagrama C4 Nível 2 (Container)

Responsável pela **estrutura do projeto, camada de domínio e documentação base**. Implementa primeiro para que Fernando e Ana possam partir de uma base funcional.

| PR | Branch | Escopo |
|----|--------|--------|
| 1 | `feat/infraestrutura-base` | `main.py`, `requirements.txt`, `.gitignore`, estrutura de pastas (`src/core/`, `src/client/`, `docs/`), `core/config.py`, `core/commands.py`, `core/scene.py`, `core/utils.py`, `core/entities.py` (Snake, Food), `core/world.py` (tick, colisões, pontuação), `README.md`, `LICENSE`, `docs/WORKFLOW.md`, `docs/diagrams/c4_nivel2_container.puml` |

### Fernando Luiz Da Silva Freire: Camada de apresentação e Diagrama C4 Nível 1 (Contexto)

Responsável pela **camada client/**: leitura de input, renderização e loop do jogo. Parte dos arquivos de Juliana.

| PR | Branch | Escopo |
|----|--------|--------|
| 5 | `feat/client-controls` | `client/controls.py`: InputMapper para 4 jogadores (WASD, Setas, IJKL, Numpad) |
| 6 | `feat/client-renderer` | `client/renderer.py`: grade, cobras, comidas, HUD e telas de menu e fim de jogo |
| 7 | `feat/client-game-loop` | `client/game.py`: loop principal, transições de cena e orquestração |
| 8 | `chore/docs-nivel1` | `docs/diagrams/c4_nivel1_contexto.puml` (Diagrama C4 Nível 1) |

### Ana Beatriz Maciel Nunes: Mecânica inédita e Diagrama C4 Nível 3 (Componente)

Responsável por uma **mecânica inédita** no jogo e pelo diagrama de componentes mais detalhado.

| PR | Branch | Escopo |
|----|--------|--------|
| 9 | `feat/mecanica-ana` | Mecânica inédita a definir (ex.: power-up de velocidade, escudo temporário, teletransporte) |
| 10 | `chore/docs-nivel3` | `docs/diagrams/c4_nivel3_componente.puml` (Diagrama C4 Nível 3) |

---

## 4. Ordem de Implementação Sugerida

```
PR 1 (Juliana: feat/infraestrutura-base)
              |
+-------------+-------------+
|                           |
PR 2-5 (Fernando)    PR 6-7 (Ana)
```

Fernando pode iniciar seu PR assim que o PR 1 de Juliana for mesclado. Ana pode iniciar a qualquer momento após o PR 1.

---

## 5. Fluxo Operacional

### 5.1 Preparação

```bash
git checkout main
git pull
git checkout -b feat/nome-da-atividade
```

### 5.2 Desenvolvimento

- Implementar apenas o escopo definido para o PR.
- Manter a separação `core/` (lógica) e `client/` (apresentação).
- Centralizar novas constantes em `core/config.py`.
- Não introduzir dependências sem aprovação da equipe.

### 5.3 Validação local

```bash
python src/main.py
```

Testar manualmente:

- Jogo inicia no menu com controles de 4 jogadores.
- Cada cobra se move com seus controles (WASD, Setas, IJKL, Numpad).
- Colisão com parede, corpo próprio e adversário funciona.
- Alimento aparece e cobra cresce ao comer.
- Placar atualiza corretamente para todos os 4 jogadores.
- Tela de fim de jogo exibe vencedor e placar completo.

### 5.4 Publicação

```bash
git add <arquivos-relevantes>
git commit -m "feat(arquivo): descrição objetiva"
git push origin feat/nome-da-atividade
```

---

## 6. Estrutura do Pull Request

### 6.1 Título

Formato: `feat: descrição` / `fix: descrição` / `chore: descrição`

### 6.2 Descrição

Todo PR deve conter:

- **Objetivo:** problema ou funcionalidade que o PR resolve.
- **O que foi implementado:** lista objetiva de mudanças.
- **Decisões técnicas:** justificativas quando relevante.
- **Como testar:** passos para validar a mudança.

---

## 7. Checklist de Revisão

### Arquitetura

- [ ] `core/` não importa `client/`
- [ ] Sem importações circulares
- [ ] Constantes centralizadas em `core/config.py`

### Qualidade

- [ ] Código tipado (type hints)
- [ ] Sem números mágicos fora de `config.py`
- [ ] Funções coesas e legíveis

### Funcionalidade

- [ ] Jogo executa sem erros (`python src/main.py`)
- [ ] Mecânica testada manualmente com 2+ jogadores
- [ ] Sem regressões visíveis

---

## 8. Sincronização Pós-Merge

Após o PR ser aprovado e mesclado:

```bash
git checkout main
git pull
git branch -d <branch-do-pr>
git status
```

---

## 9. Convenção de Nomenclatura de Commits

```
feat(config): adicionar constantes de 4 jogadores
fix(world): corrigir colisão cabeça a cabeça simultânea
chore(docs): adicionar diagrama C4 nível 2 container
```

Commits devem ser pequenos, descritivos e alinhados ao objetivo do PR.
