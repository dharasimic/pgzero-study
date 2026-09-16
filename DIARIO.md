
# 09/09/2026

- Defini o conceito e o escopo da primeira entrega do minigame **Dungeon Survival** em Pygame Zero.
- Documentei o design, as regras, o loop de jogo, os estados, a progressao, o audio, os criterios de aceite e os itens fora do escopo em `MANUAL.md`.
- Atualizei o `README.md` com a proposta, a estrutura do projeto e as instrucoes de execucao.
- Preparei o ponto de entrada `game.py` e a dependencia `pgzero`.
- Organizei os assets de dungeon, personagens, inimigos, itens, portas e efeitos em `images/`, alem das musicas e efeitos sonoros em `sounds/`.

# 10/09/2026

- Implementei o carregamento de assets de UI em `game.py`: painéis, botões de som/música, setas de navegação e papel de fundo.
- Adicionei as imagens de UI (MediavelUI.png e UI books & more.png) e fontes para renderização de texto.
- Configurei constantes de cores, dimensões de janela e inicializacao de sons (click do menu).
- Criado estrutura para subsuperfícies e transformações de escala dos elementos de interface.
- Próxima etapa: implementar os estados do menu e input do teclado/mouse.

# 11/09/2026

- Tive problemas no momento de recortar os assets para usá-los no jogo. Acabei descobrindo um programa chamado LibreSprite, que facilitou muito visualizar os sprites animados e organizar meus assets.
- Apanhei para fazer as colisões das paredes.
- Criei a sala com tiles de chão e paredes a partir dos atlases de assets.
- Implementei a movimentação do wizard com WASD, incluindo animações de parado e de corrida.
- Adicionei colisões para impedir que o personagem atravesse as paredes.

# 14?09?2026

- Depois de uma pausa no final de semana voltei a atuar no jogo
- Implementei os projeteis da bruxinha (a protagonista do jogo)
- Implementei também o primeiro inimigo do jogo, o ogro grande
- Apanhei demais com as identações do arquivo, acabei bagunçando sem querer e virou um efeito dominó onde cada vez que eu arrumava outra coisa ficava com a identação errada mas serviu pra eu aprender algumas lições sobre identação no pyhton rs
- Implementei sistema de vida, morte de inimigos, contador de ogros mortos, timer do jogo e tela de pausa e de game over
- Dei uma pausa no dia com um bug que eu não sei ainda como resolver, de tempos em tempos os projeteis passam direto pelos orgros e eu ainda não sei o motivo.

# 16/09/2026

- Finalmente consegui arrumar o erro dos projeteis atravessando os ogros
- Com essa correção finalmente entrei na etapa final do meu projeto: o refinamento
- Começei limpando as pastas do projeto removendo os assets que eu não usei ou não pretendo usar
- Adicionei mais dois inimigos que são mais rapidos que os ogros
- Troquei a música que toca durante o jogo e adicionei ost diferentes para cada parte do jogo
