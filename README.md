# Dungeon Survival

Projeto de estudo em Python com Pygame Zero para criar um minigame de sobrevivencia top-down em uma dungeon.

O jogador escolhe um personagem, dispara automaticamente, enfrenta hordas de inimigos, coleta buffs em baus e abre novas salas ao ativar botoes no chao. A partida termina quando as tres vidas acabam.

## Primeira entrega

- Menu principal com selecao de personagem, controles, audio e saida.
- Partida com movimentacao por WASD e disparo automatico.
- Hordas de inimigos, vidas, tempo e contador de derrotas.
- Baus comuns, frascos com buffs e baus mimic.
- Botoes que abrem portas para novas salas.
- Menu de pausa acionado por ESC.
- Tela de fim de jogo com o resultado da partida.

Personagens terao apenas diferencas visuais nesta primeira versao. Melhorias permanentes, chefes, historia, multiplayer e geracao procedural completa ficam para etapas futuras.

## Estrutura

- `game.py`: ponto de entrada planejado para o jogo.
- `MANUAL.md`: documento de design, regras, progressao e criterios de aceite.
- `images/`: tiles e demais imagens do jogo.
- `sounds/Music/`: musicas.
- `sounds/SFX/`: efeitos sonoros.
- `requirements.txt`: dependencia do Pygame Zero.

## Executar

Com Python e as dependencias instaladas:

```bash
pip install -r requirements.txt
pgzrun game.py
```