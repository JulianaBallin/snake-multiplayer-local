# SNAKE MULTIPLAYER LOCAL -- WORKFLOW DE DESENVOLVIMENTO

**Versão:** 1.0
**Data:** 2026-05-21

---

## 1. Objetivo

Guiar o desenvolvimento do Snake Multiplayer Local por meio de Pull Requests curtos, seguros e verificáveis, garantindo qualidade técnica e rastreabilidade. O trabalho é dividido entre **3 integrantes**, cada um responsável por um conjunto de atividades coeso.

---

## 2. Princípios

1. Nada entra na `main` sem um Pull Request revisado.
2. Cada PR deve ter escopo pequeno, coeso e testável manualmente.
3. O domínio (`core/`) é isolado e não deve importar `client/`.
4. O projeto deve permanecer funcional ao final de cada PR.
5. Commits em português, formato convencional: `tipo(arquivo): descrição`.

---

## 3. Divisão de Atividades

### Integrante 1 -- Ana Beatriz Maciel Nunes

Responsável pela **camada de domínio (core/)** e mecânica principal.

| PR | Branch | Escopo |
|----|--------|--------|
| 1 | `feat/core-config-entities` | `config.py`, `commands.py`, `entities.py`, `scene.py`, `utils.py` |
| 2 | `feat/core-world-logica` | `world.py`: tick, colisoes, pontuacao e spawn de comida |
| 3 | `feat/mecanica-power-up` | Mecânica inédita: item especial (power-up) no tabuleiro |

### Integrante 2 -- Fernando Luiz Da Silva Freire

Responsável pela **camada de apresentação (client/)** e loop do jogo.

| PR | Branch | Escopo |
|----|--------|--------|
| 4 | `feat/client-controls` | `controls.py`: InputMapper para J1 (WASD) e J2 (Setas) |
| 5 | `feat/client-renderer` | `renderer.py`: grade, cobras, comidas, HUD |
| 6 | `feat/client-game-loop` | `game.py`: loop principal e transicoes de cena |

### Integrante 3 -- Juliana Ballin Lima

Responsável pela **infraestrutura, documentação e mecânica extra**.

| PR | Branch | Escopo |
|----|--------|--------|
| 7 | `feat/estrutura-base` | `main.py`, `requirements.txt`, `.gitignore`, estrutura de pastas |
| 8 | `chore/readme-c4-docs` | `README.md`, `docs/diagrams/*.puml`, `docs/WORKFLOW.md`, `LICENSE` |
| 9 | `feat/mecanica-velocidade` | Mecânica inédita: aumento progressivo de velocidade por pontuação |

---

## 4. Fluxo Operacional

### 4.1 Preparação

```bash
git checkout main
git pull
git checkout -b feat/nome-da-atividade
```

### 4.2 Desenvolvimento

- Implementar apenas o escopo definido para o PR.
- Manter a separação `core/` (logica) e `client/` (apresentação).
- Centralizar novas constantes em `core/config.py`.
- Não introduzir dependências sem aprovação da equipe.

### 4.3 Validação local

```bash
cd snake-multiplayer-local
python src/main.py
```

Testar manualmente:

- Jogo inicia no menu.
- Cobras se movem com WASD e Setas.
- Colisão com parede e corpo funciona.
- Alimento aparece e cobra cresce ao comer.
- Placar atualiza corretamente.
- Tela de fim de jogo exibe vencedor e pontuação.

### 4.4 Publicação

```bash
git add <arquivos-relevantes>
git commit -m "feat(arquivo): descricao objetiva"
git push origin feat/nome-da-atividade
```

---

## 5. Estrutura do Pull Request

### 5.1 Titulo

Formato: `feat: descricao` / `fix: descricao` / `chore: descricao`

### 5.2 Descricao

Todo PR deve conter:

- **Objetivo:** problema ou funcionalidade que o PR resolve.
- **O que foi implementado:** lista objetiva de mudancas.
- **Decisoes técnicas:** justificativas quando relevante.
- **Como testar:** passos para validar a mudanca.

---

## 6. Checklist de Revisao

### Arquitetura

- [ ] `core/` nao importa `client/`
- [ ] Sem importacoes circulares
- [ ] Constantes centralizadas em `core/config.py`

### Qualidade

- [ ] Codigo tipado (type hints)
- [ ] Sem numeros magicos fora de `config.py`
- [ ] Funcoes coesas e legíveis

### Funcionalidade

- [ ] Jogo executa sem erros (`python src/main.py`)
- [ ] Mecanica testada manualmente
- [ ] Sem regressoes visíveis

---

## 7. Sincronizacao Pos-Merge

Apos o PR ser aprovado e mesclado:

```bash
git checkout main
git pull
git branch -d <branch-do-pr>
git status
```

---

## 8. Convencao de Nomenclatura de Commits

```
feat(config): adicionar constantes de velocidade progressiva
fix(world): corrigir colisao cabeca a cabeca simultanea
chore(docs): atualizar diagrama C4 nivel 2
```

Commits devem ser pequenos, descritivos e alinhados ao objetivo do PR.
