# Dungeon Survival

**Dungeon Survival** é um minigame de sobrevivência **top-down** desenvolvido em Python com **Pygame Zero** como projeto de estudo.

O jogador controla uma pequena bruxa dentro de uma dungeon e precisa sobreviver ao maior número possível de hordas de inimigos. O personagem se movimenta pela sala enquanto dispara automaticamente contra os inimigos que avançam pelas entradas.

A partida termina quando toda a vida do jogador é perdida.

## 🎮 Download

Se você só quer experimentar o jogo sem precisar configurar o ambiente Python ou baixar o código-fonte, é possível baixar diretamente a versão executável:

**[⬇️ Baixar Dungeon Survival (.exe)](https://github.com/dharasimic/pgzero-study/releases/tag/v1.0)**

## 🕹️ Como jogar

O objetivo é **sobreviver pelo maior tempo possível e derrotar o maior número de inimigos**.

Durante a partida:

* Movimente a personagem usando **WASD**.
* O disparo acontece **automaticamente**, na direção do mouse.
* Inimigos surgem pelas entradas da dungeon em **hordas**.
* Existem diferentes tipos de inimigos.
* Ao ser atingido, o jogador perde vida e recebe um breve período de invencibilidade.
* O HUD mostra a quantidade de vida restante e o número de inimigos derrotados.
* Pressione **ESC** para pausar ou continuar a partida.

A dificuldade aumenta conforme novas hordas são iniciadas. A primeira horda começa com 6 inimigos e cada nova horda adiciona 2 inimigos ao total.

## 👹 Inimigos

O jogo possui três tipos de inimigos:

| Inimigo       | Velocidade | Vida |
| ------------- | ---------: | ---: |
| Ogro          |         40 |    2 |
| Orc mascarado |         80 |    1 |
| Orc guerreiro |        100 |    1 |

Os inimigos entram na dungeon por diferentes pontos das paredes e perseguem o jogador dentro da sala.

❤️ Sistema de vida

O jogador começa cada partida com 6 pontos de vida, representados por três corações no HUD.

Quando um inimigo entra em contato com o jogador, um ponto de vida é perdido. Após receber dano, existe um curto período de invencibilidade antes que outro dano possa ser aplicado.
Quando a vida chega a zero, a partida termina e a tela de Game Over apresenta o tempo sobrevivido e a quantidade de inimigos derrotados.

⏸️ Pausa e áudio

O jogo possui um menu de pausa acessível pela tecla ESC.

No menu de pausa é possível:

Continuar a partida;
Sair para o menu principal;
Ativar ou desativar a música.

O jogo também possui músicas diferentes para o menu, a partida e a tela de Game Over, além de efeitos sonoros para as interações com a interface.

📊 Resultado da partida

Ao perder todas as vidas, a tela de Game Over apresenta:

Tempo sobrevivido;
Número de inimigos derrotados;
Opção de jogar novamente;
Opção de retornar ao menu principal.
🛠️ Tecnologias
Python
Pygame Zero
Pygame

O projeto utiliza recursos do Pygame para trabalhar com elementos como superfícies, máscaras de colisão, imagens, áudio e vetores, enquanto o loop principal é executado pelo Pygame Zero.

📁 Estrutura
.
├── game.py
├── images/
│   ├── frames/
│   └── ...
├── sounds/
│   ├── Music/
│   └── SFX/
├── requirements.txt
└── README.md
game.py: código principal do jogo.
images/: sprites, elementos de interface, tiles e demais recursos visuais.
images/frames/: animações, personagens, inimigos e elementos do HUD.
sounds/Music/: músicas utilizadas pelo jogo.
sounds/SFX/: efeitos sonoros.

Para executar o projeto diretamente pelo Python, é necessário ter Python instalado.

pgzrun game.py
📚 Sobre o projeto

Este projeto foi desenvolvido como estudo de Python e Pygame Zero, explorando conceitos de desenvolvimento de jogos 2D, incluindo:

Game loop;
Estados de jogo;
Movimentação;
Animações;
Colisão;
Projéteis;
IA simples de perseguição;
Sistema de hordas;
HUD;
Menus e interfaces;
Áudio;
Partículas;
Gerenciamento de recursos.

O foco desta versão é entregar uma experiência pequena e funcional de sobrevivência em uma dungeon, servindo também como base para futuros estudos e melhorias.
