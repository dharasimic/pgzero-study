# Manual de Design - Dungeon Survival

## 1. Visao geral

Dungeon Survival e um minigame de sobrevivencia com visao top-down, inspirado no estilo de `Journey of the Prairie King`, um minigame de Stardew Valley.

O jogador escolhe um personagem, entra em uma masmorra e tenta sobreviver pelo maior tempo possivel. O personagem dispara automaticamente na direcao em que estiver mirando, enquanto o jogador se concentra em movimentacao, esquiva, coleta e posicionamento.

Esta e a especificacao da primeira entrega. Ela define as regras do jogo, os estados da partida, a progressao e a estrutura que sera implementada posteriormente.

## 2. Objetivo da primeira entrega

Entregar um ciclo de jogo completo e jogavel:

1. Abrir o jogo no menu principal.
2. Escolher um personagem diferente.
3. Iniciar uma partida em uma sala de dungeon.
4. Movimentar-se com WASD e disparar automaticamente.
5. Enfrentar hordas de inimigos que perseguem o jogador.
6. Encontrar baus, coletar frascos e receber buffs temporarios.
7. Abrir portas ao pisar em botoes no chao.
8. Entrar em novas salas geradas durante a partida.
9. Perder tres vidas, encerrar a partida e exibir o resultado.

O objetivo desta entrega e validar o loop principal de sobrevivencia. Nao fazem parte dela historia, loja, progressao permanente ou habilidades exclusivas por personagem.

## 3. Loop principal

O ciclo de uma partida sera:

1. O jogador escolhe um personagem no menu.
2. Uma sala inicial e carregada com o jogador, inimigos, obstaculos e possiveis baus.
3. O jogador se movimenta e dispara automaticamente.
4. Os inimigos surgem em hordas e avancam na direcao do jogador.
5. Derrotar inimigos aumenta um contador no topo da tela.
6. Baus comuns podem conter frascos com buffs.
7. Botoes no chao liberam portas para novas salas.
8. A dificuldade aumenta gradualmente enquanto o tempo passa.
9. Ao perder a terceira vida, a partida termina e a tela de resultado aparece.

O resultado principal da partida e formado por tempo sobrevivido e inimigos derrotados.

## 4. Regras do jogador

### 4.1 Movimentacao

- `W`: mover para cima.
- `A`: mover para a esquerda.
- `S`: mover para baixo.
- `D`: mover para a direita.
- O jogador nao pode atravessar paredes, portas fechadas ou obstaculos solidos.
- A movimentacao deve ser limitada aos limites da sala ou da camera.
- As diagonais sao permitidas quando duas teclas de direcao estao pressionadas.

### 4.2 Disparo

- O disparo e automatico durante a partida.
- A direcao do disparo sera orientada pela posição do cursos do mouse.
- Cada disparo pode atingir inimigos e desaparecer ao sair da area jogavel.
- O disparo nao deve atravessar paredes.
- O disparo deve sumir ao atingir um inimigo.

### 4.3 Vidas e dano

- O jogador comeca a partida com 3 vidas.
- As vidas são exibidas no canto superior esquerdo da tela, com os icones de coração.
- Colidir com um inimigo ou ser atingido por um ataque causa a perda de 0,5 vida.
- A perda de vida deve fazer a sprite do personagem piscar aplicar um pequeno periodo de invulnerabilidade para evitar dano repetido no mesmo instante.
- Ao perder uma vida, o jogador permanece na partida enquanto ainda tiver vidas.
- Ao perder a terceira vida, a partida termina imediatamente.

## 5. Inimigos e hordas

- Os inimigos surgem nas bordas, em pontos ocultos ao jogador.
- O comportamento basico da primeira entrega e perseguir o jogador.
- Inimigos nao devem surgir sobre o jogador, dentro de paredes, diretamente ao lado do jogador ou em locais inacessiveis.
- Derrotar um inimigo aumenta `inimigos derrotados` em 1.
- O contador de inimigos derrotados deve ser exibido no canto da tela com o icone de caveira ao lado e o somente o número de inimigos derrtados.
- A horda inicial deve ser pequena para permitir que o jogador aprenda o controle.
- A quantidade e a frequencia de surgimento aumentam com o tempo sobrevivido.
- A primeira entrega irá utilizar somente a família de inimigos orcs e ogros
- Inimigos derrotados desaparecem com uma animação de fumaça.

### Progressao da dificuldade

A progressao sera baseada no tempo, sem exigir fases fixas:

- **Inicio:** poucos inimigos, surgimento mais espacoso e salas simples.
- **Meio da partida:** mais inimigos ativos, menor intervalo entre hordas e maior pressao de perseguicao.
- **Partida avancada:** hordas maiores e salas com mais obstaculos, mantendo sempre uma rota possivel de fuga.

Os valores exatos de quantidade, intervalo e velocidade serao ajustados durante os testes de jogabilidade. A regra importante e que a dificuldade aumente de forma gradual e previsivel.

## 6. Salas, portas e botoes

- A sala e construida com os tileset de dungeon disponiveis em `images/`.
- Uma porta fechada bloqueia a passagem para uma sala ainda nao acessivel.
- Um botao fica visivel no chao dentro da sala.
- Ao passar por cima do botao, ele e ativado automaticamente.
- A ativacao abre a porta correspondente.
- O botao nao exige tecla de interacao.
- Depois de aberta, a porta permanece aberta durante a partida.
- Ao atravessar a porta, uma nova sala e criada ou carregada.
- A nova sala deve conter uma area de entrada segura para o jogador.
- A camera deve acompanhar o personagem sem revelar areas fora da sala.

Na primeira entrega, a geracao de salas pode ser feita a partir de um conjunto pequeno de modelos predefinidos escolhidos aleatoriamente. Geracao procedural completa fica fora do escopo inicial.

## 7. Baus e frascos

### 7.1 Baus comuns

- Um bau comum fica fechado ate o jogador se aproximar e apertar `F` nele.
- Ao ser aberto, ele revela um frasco.
- Cada bau comum so pode ser aberto uma vez.
- O jogador coleta o frasco ao encostar nele.
- O efeito do frasco e aplicado imediatamente.

### 7.2 Buffs dos frascos

Os frascos serao temporarios e terao efeitos simples, para que o jogador consiga entender o beneficio durante uma partida:

- **Amarelo = Velocidade:** aumenta a velocidade de movimento por um periodo.
- **Azul = Disparo mais rapido:** reduz o intervalo entre disparos por um periodo.
- **Vermelho = Tiro poderoso:** aumenta o dano dos disparos.
- **Verde = Proteção:** torna o personagem imune.

Na primeira entrega, cada frasco deve ter apenas um efeito. O HUD deve mostrar o buff ativo e, o tempo restante. Nao havera inventario: o efeito e aplicado no momento da coleta.
Existem duas versões de cada frasco, a normal e a grande. A versão normal dura 10 segundos e a grande, 20.

## 8. Estados do jogo

O jogo deve ter os seguintes estados claros:

### Menu principal

Deve permitir:

- Iniciar uma partida.
- Abrir a tela de controles.
- Silenciar ou reativar a musica.
- Silenciar ou reativar os efeitos sonoros.
- Sair do jogo.

### Selecao de personagem

- É acessada ao clicar no botão de iniciar a partida.
- Exibe os personagens disponiveis com os personagens fazer suas animações idle.
- Permite confirmar um personagem antes de iniciar.
- Na primeira entrega, os personagens diferem apenas visualmente.
- Nenhum personagem possui buff ou debuff exclusivo.\
- Botão de iniciar partida.

### Tela de controles

Deve exibir:

- `WASD`: movimentacao.
- `ESC`: pausar.
- Um botão para voltar ao menu principal.

### Partida

- Mostra o personagem, inimigos, sala, baus, portas e projeteis.
- Mostra vidas, tempo sobrevivido, inimigos derrotados e buffs ativos.
- Mantem a musica e os efeitos de acordo com as preferencias de audio.

### Pausa

Ao pressionar `ESC`, a partida deve parar de atualizar e exibir:

- Continuar.
- Silenciar ou reativar a musica.
- Silenciar ou reativar os efeitos sonoros.
- Voltar ao menu principal.
- Sair do jogo.

Ao voltar ao menu principal ou sair, a partida atual e descartada. A primeira entrega nao tera confirmacao adicional nem salvamento de progresso.

### Fim de jogo

Ao perder tres vidas, exibir:

- Mensagem de que o jogador morreu.
- Quantidade de inimigos derrotados.
- Tempo sobrevivido.
- Opcao para jogar novamente.
- Opcao para voltar ao menu principal.
- Opcao para sair do jogo.

## 9. Audio

- A musica de fundo toca durante o menu e a partida, respeitando o estado de silencio.
- Os efeitos sonoros devem ser usados para disparos, acertos, dano, coleta de frascos, abertura de baus, ativacao de botoes, portas, pausa e fim de jogo quando houver assets adequados.
- O silencio da musica e o silencio dos efeitos sao configuracoes independentes.
- A configuracao deve valer no menu, na partida e na pausa.
- As pastas previstas sao `sounds/Music/` e `sounds/SFX/`.

## 10. Estrutura tecnica planejada

Esta e a organizacao esperada para a implementacao:

- **Gerenciamento de estado:** menu principal, selecao, controles, partida, pausa e fim de jogo.
- **Dados da partida:** personagem escolhido, vidas, tempo, derrotas, sala atual e buffs ativos.
- **Entidades:** jogador, projeteis, inimigos, baus comuns, frascos, botoes e portas.
- **Colisoes:** paredes, limites da sala, inimigos, projeteis, baus, frascos, botoes e portas.
- **Geracao de salas:** modelos predefinidos de salas e regras para conectar entrada, saida e botao.
- **Audio:** controle independente de musica e efeitos sonoros.
- **HUD:** vidas, cronometro, derrotas e buffs.
- **Recursos:** imagens em `images/` e audio em `sounds/`.

As responsabilidades devem permanecer separadas: o desenho apresenta o estado atual, a atualizacao aplica regras do jogo e os eventos de entrada alteram apenas as acoes correspondentes. A implementacao deve continuar compativel com as convencoes do Pygame Zero, como `draw()`, `update()`, eventos de teclado, `Actor` e `clock`.

## 11. Fora do escopo da primeira entrega

- Habilidades unicas por personagem.
- Melhorias permanentes entre partidas.
- Loja, moedas ou sistema de economia.
- Chefes.
- Historia, dialogos ou missoes.
- Multiplayer.
- Salvamento de partidas.
- Ranking online.
- Geracao procedural completa e infinita.
- Grande variedade de inimigos.

Esses itens podem ser avaliados depois que o loop de sobrevivencia estiver estavel.

## 12. Criterios de aceite

A primeira entrega sera considerada pronta quando:

- O jogo iniciar no menu principal sem iniciar uma partida automaticamente.
- O jogador conseguir escolher um personagem e iniciar a partida.
- WASD movimentar o personagem e ESC pausar ou retomar a partida.
- O disparo automatico funcionar sem botao de tiro.
- Inimigos surgirem, perseguirem o jogador e poderem ser derrotados.
- O contador de tempo e de inimigos derrotados funcionar.
- O jogador perder vidas ao receber dano e a partida terminar na terceira vida.
- Existir pelo menos um bau comum com frasco funcional.
- Um botao abrir uma porta e permitir acesso a outra sala.
- Houver mais de um modelo de sala ou uma variacao equivalente durante a partida.
- Musica e efeitos puderem ser silenciados separadamente no menu e na pausa.
- O menu de pausa puder voltar ao menu principal e sair do jogo.
- A tela de fim de jogo mostrar derrotas e tempo sobrevivido.
- Os assets existentes forem usados sem depender de arquivos que nao estejam no projeto.