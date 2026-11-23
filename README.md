# Faria Lima Rush

Um jovem trabalhador perdeu a hora e precisa chegar ao trabalho. Com o caos de São Paulo e o trânsito parado, ele liga o jetpack e segue pelo alto, pela região da Avenida Faria Lima. Como todo dia na cidade, o caminho não é fácil: ele precisa desviar de drones de entrega, de pombos que atacam e de patinetes elétricos desgovernados na calçada.

Para sobreviver ao trajeto, ele conta com dois aliados: **capacetes de obra** (afinal, as obras de São Paulo nunca acabam), que dão uma proteção temporária, e **cafés**, que dão a energia para chegar mais longe.

Jogo desenvolvido em Python com PyGame para o Projeto Final de **Design de Software** (Insper, 2026/2).

## Autoras

- Dora Gaudio Guerra
- Giovanna Gonçalves Oricchio

## Vídeo

▶️ [Assista ao jogo funcionando](https://youtu.be/ntOyYS1SN3o)

## Como instalar e rodar

1. Tenha o **Python 3** instalado.
2. Instale o PyGame:
   ```bash
   pip install pygame
   ```
   (se der erro, use `pip install pygame-ce`)
3. Clone ou baixe este repositório.
4. Dentro da pasta do projeto, rode:
   ```bash
   python main.py
   ```

O arquivo que deve ser executado é o **`main.py`**.

## Como jogar

| Tecla | Ação |
| --- | --- |
| Espaço (segurar) | Liga o jetpack e sobe |
| Espaço (soltar) | Cai pela gravidade |
| P | Pausa / continua |
| Enter | Começa a partida / joga de novo |
| I | Instruções (no menu) |
| Esc | Volta ao menu / sai do jogo |

**Objetivo:** ir o mais longe possível antes de perder as 3 vidas.

| Elemento | O que faz |
| --- | --- |
| ☕ Café | +10 pontos. Vem em fileiras de 5 |
| ⛑️ Capacete | Escudo: aguenta uma batida sem perder vida |
| Drone de entrega | Obstáculo no ar. À noite, alguns sobem e descem |
| Pombo-míssil | Um aviso pisca na altura do jogador e, 1 segundo depois, o pombo atravessa a tela em alta velocidade |
| Patinete elétrico | O aviso pisca no chão e, 1 segundo depois, o patinete passa pela calçada. Quem estiver no chão perde uma vida |

- **Pontuação:** metros percorridos + 10 por café. O recorde fica salvo no arquivo `recorde.txt`.
- **Depois de uma batida**, o personagem pisca e fica 1,5 s invencível.
- **Fases:** a dificuldade aumenta com a distância, e a velocidade sobe aos poucos.

| Fase | Distância | O que muda |
| --- | --- | --- |
| Manhã | 0 a 500 m | Drones, cafés e patinetes |
| Tarde | 500 a 1500 m | Mais rápido, céu laranja e começam os pombos-míssil |
| Noite | acima de 1500 m | Céu escuro, drones que se movem e velocidade aumentando a cada 500 m |

## Telas do jogo

Menu inicial → Instruções → Partida (com pause) → Game over (pontos, recorde e "NOVO RECORDE!").

## Organização do código

O código é dividido em arquivos com responsabilidades separadas e usa classes (orientação a objetos):

| Arquivo | O que faz |
| --- | --- |
| `main.py` | Inicia o pygame e troca de tela (máquina de estados: início, instruções, jogo, game over) |
| `config.py` | Constantes: tamanho da tela, física, velocidades, fases |
| `assets.py` | Carrega imagens, sons e fontes (com imagens de reserva caso algum arquivo falte) |
| `sprites.py` | Classes `Jogador`, `Fundo`, `Drone`, `Item`, `Missil` (pombo e patinete) e `Explosao` |
| `gerador.py` | Classe `Gerador`: decide quando cada obstáculo e item aparece, sem nascer um em cima do outro |
| `tela_jogo.py` | Loop principal da partida: eventos, atualização, colisões e desenho |
| `tela_inicio.py`, `tela_instrucoes.py`, `tela_game_over.py` | As demais telas |
| `recorde.py` | Lê e salva o recorde |
| `utils.py` | Função para desenhar texto na tela |
| `assets/` | Imagens (`img`), sons (`snd`), fonte (`font`) e rascunhos do design (`rascunhos`) |

## Design do jogo

O jogo começou com um documento de design e foi construído em etapas, um commit por funcionalidade. Os rascunhos estão em [`assets/rascunhos/`](assets/rascunhos/).

![Rascunho da tela do jogo, feito pela equipe](assets/rascunhos/rascunho_tela.png)

*Rascunho da tela do jogo, com as anotações das mecânicas: à noite o drone se mexe, há avisos para o pombo e o patinete, e os capacetes são escudos.*

**Ideias da equipe que viraram parte do jogo:**
- o nome **Faria Lima Rush**, o tema "trabalhador atrasado na Faria Lima" e a história;
- o patinete elétrico azul como obstáculo na calçada e a separação entre "drones no ar, patinetes no chão";
- sons diferentes para o aviso do pombo (com arrulho) e o do patinete (motor chegando).

## Créditos dos assets

| Arquivo(s) | Origem | Licença |
| --- | --- | --- |
| Todas as imagens de `assets/img/` (personagem, pombo, explosão, cenário, drone, café, capacete, coração, aviso e patinete) | Geradas com IA (Claude, da Anthropic) | — |
| Todos os sons de `assets/snd/` (efeitos e música de fundo) | Gerados com IA (Claude, da Anthropic) | — |
| `assets/font/PressStart2P-Regular.ttf` | CodeMan38, [Google Fonts](https://fonts.google.com/specimen/Press+Start+2P) | SIL Open Font License (ver `assets/font/OFL.txt`) |

## Uso de Inteligência Artificial

Usamos IA generativa (**Claude**, da Anthropic) neste projeto. Seguindo as regras da disciplina, declaramos abaixo o que foi gerado.

**O que foi gerado por IA:**
- **100% do código Python** (todos os arquivos `.py`), a partir do nosso documento de design. Cada arquivo tem um comentário no topo indicando isso.
- **Todas as imagens** do jogo (personagem, pombo, explosão, cenário, itens e patinete).
- **Todos os sons**: os efeitos sonoros e a música de fundo.

**O que fizemos nós:**
- Escolha do jogo, do nome **Faria Lima Rush**, do tema e da história; definição das mecânicas e das fases.
- Ideias do patinete, da calçada e dos sons diferentes para cada aviso.
- **Testes e bugs encontrados por nós:** cafés nascendo em cima de drones, patinetes passando por cima de drones e um "tranco" na troca de fase (a velocidade pulava de uma vez; agora acelera aos poucos).
- **Ajustes pedidos a partir dos testes:** patinete mais lento, arrulho do pombo mais parecido com o real e volume da música mais baixo.
- Montagem do repositório, commits de cada etapa, rascunhos e vídeo.

**Como usamos a IA:** pedimos ao Claude um plano de desenvolvimento dividido em commits e o código de cada etapa. Antes de cada commit, testávamos o jogo e estudávamos a explicação daquela etapa (cada função do código tem uma marca de dificuldade `[NÍVEL: FÁCIL/MÉDIO/DIFÍCIL]` para orientar o estudo). Quando encontrávamos erros testando, levávamos ao Claude, que gerava as correções. Revisamos tudo o que foi gerado, estudando e compreendendo o que cada parte do código faz, do começo ao fim.

**Histórico das conversas com a IA:**
- Conversa da Dora (código, sons, correções): https://claude.ai/share/10b5170c-e24b-4634-a77c-04f2e6d971cb
- Conversas da Giovanna (imagens, sprites, commits, vídeo e ajustes finais): trechos sobre o jogo em [`docs/conversa_giovanna/`](docs/conversa_giovanna/)
  - [Commits e imagens do jogo](docs/conversa_giovanna/1_conversa_imagens_e_commits.md)
  - [Ajustes finais, README e vídeo](docs/conversa_giovanna/2_conversa_sprites_readme_video.md)

## Referências

- Tutorial de PyGame da disciplina: https://insper.github.io/DesignDeSoftware/pygame/handout/
- Documentação do PyGame: https://www.pygame.org/docs/
