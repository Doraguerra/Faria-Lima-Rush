"""Classes (sprites) do jogo Atrasado na Faria Lima."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import random
import pygame
from config import CHAO_Y, TETO_Y, JOGADOR_X, GRAVIDADE, EMPURRAO, VEL_MAX
from config import LARGURA, VIDAS_INICIAIS, TEMPO_INVENCIVEL
from config import TEMPO_AVISO_MISSIL, VEL_MISSIL


# [NÍVEL: DIFÍCIL] — a física (gravidade + empurrão) e a animação por tempo.
class Jogador(pygame.sprite.Sprite):
    """O aluno atrasado: corre no chão e voa com o jetpack."""

    def __init__(self, assets):
        """Cria o jogador parado no chão, do lado esquerdo da tela."""
        pygame.sprite.Sprite.__init__(self)
        self.quadros_correndo = assets['jogador_correndo']
        self.quadros_voando = assets['jogador_voando']
        self.image = self.quadros_correndo[0]
        self.rect = self.image.get_rect()
        self.rect.x = JOGADOR_X
        self.rect.bottom = CHAO_Y
        self.mask = pygame.mask.from_surface(self.image)
        # rect.y só guarda números inteiros; self.y guarda a posição com
        # casas decimais, para a gravidade (0.5) não ser arredondada para 0.
        self.y = float(self.rect.y)
        self.vel_y = 0
        self.voando = False
        self.quadro = 0
        self.tempo_quadro = 120  # milissegundos entre um quadro e outro
        self.ultimo_quadro = pygame.time.get_ticks()
        self.vidas = VIDAS_INICIAIS
        self.invencivel_ate = 0
        self.imagem_vazia = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.escudo = False

    def update(self):
        """Aplica a física do jetpack e escolhe o quadro da animação."""
        if self.voando:
            self.vel_y -= EMPURRAO
        self.vel_y += GRAVIDADE
        self.vel_y = max(-VEL_MAX, min(VEL_MAX, self.vel_y))
        self.y += self.vel_y
        self.rect.y = int(self.y)
        if self.rect.bottom >= CHAO_Y:  # encostou no chão
            self.rect.bottom = CHAO_Y
            self.y = float(self.rect.y)
            self.vel_y = 0
        # "<" e não "<=": com "<=", ao encostar no teto o jogador ficava preso
        # (a gravidade de 0.5 era arredondada para 0 pelo int() e ele era
        # empurrado de volta ao teto a cada quadro).
        if self.rect.top < TETO_Y:  # passou do teto
            self.rect.top = TETO_Y
            self.y = float(self.rect.y)
            self.vel_y = 0
        self.animar()

    def no_chao(self):
        """Devolve True se o jogador está encostado no chão."""
        return self.rect.bottom >= CHAO_Y

    def animar(self):
        """Troca o quadro da animação a cada self.tempo_quadro milissegundos."""
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_quadro >= self.tempo_quadro:
            self.ultimo_quadro = agora
            self.quadro += 1
        if self.no_chao():
            quadros = self.quadros_correndo
        else:
            quadros = self.quadros_voando
        # O operador % faz o número "dar a volta": 0, 1, 0, 1, ...
        self.image = quadros[self.quadro % len(quadros)]
        # Piscando: a cada 100 ms alterna entre a imagem e uma imagem vazia.
        if self.esta_invencivel() and (agora // 100) % 2 == 0:
            self.image = self.imagem_vazia

    def esta_invencivel(self):
        """Devolve True se o jogador ainda está piscando depois de uma batida."""
        return pygame.time.get_ticks() < self.invencivel_ate

    def levar_dano(self):
        """Tira uma vida (ou o escudo) e deixa o jogador invencível um tempo.

        Devolve True se o dano valeu e False se o jogador estava invencível.
        """
        if self.esta_invencivel():
            return False
        if self.escudo:
            self.escudo = False
        else:
            self.vidas -= 1
        self.invencivel_ate = pygame.time.get_ticks() + TEMPO_INVENCIVEL
        return True


# [NÍVEL: MÉDIO] — a ideia das duas cópias é nova; o código é curto.
class Fundo:
    """Uma camada de fundo que anda para a esquerda e se repete sem fim.

    Não é um Sprite: não colide com nada, só é desenhada.
    """

    def __init__(self, imagem, fator, y):
        """fator = fração da velocidade do mundo (0.3 = anda a 30%)."""
        self.imagem = imagem
        self.fator = fator
        self.y = y
        self.x = 0.0
        self.largura = imagem.get_width()

    def update(self, velocidade):
        """Anda para a esquerda; quando sai inteira da tela, volta ao início."""
        self.x -= velocidade * self.fator
        if self.x <= -self.largura:
            self.x += self.largura

    def desenhar(self, tela):
        """Desenha duas cópias lado a lado, como uma esteira de supermercado."""
        tela.blit(self.imagem, (self.x, self.y))
        tela.blit(self.imagem, (self.x + self.largura, self.y))


# [NÍVEL: FÁCIL] — parecido com a classe Meteor do tutorial.
class Drone(pygame.sprite.Sprite):
    """Drone de entrega: obstáculo que vem da direita."""

    def __init__(self, imagem, movel):
        """Cria o drone fora da tela, à direita, numa altura sorteada."""
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = LARGURA
        self.rect.y = random.randint(TETO_Y, CHAO_Y - self.rect.height)
        if movel:
            self.vel_y = random.choice([-2, 2])
        else:
            self.vel_y = 0

    def update(self, velocidade):
        """Anda para a esquerda (e sobe/desce, se for móvel)."""
        self.rect.x -= velocidade
        self.rect.y += self.vel_y
        if self.rect.top <= TETO_Y or self.rect.bottom >= CHAO_Y:
            self.vel_y = -self.vel_y  # bateu no teto/chão: inverte
        if self.rect.right < 0:
            self.kill()  # saiu da tela: some de todos os grupos


# [NÍVEL: FÁCIL]
class Item(pygame.sprite.Sprite):
    """Coisa que o jogador pode pegar: 'cafe' ou 'capacete'."""

    def __init__(self, imagem, tipo, x, y):
        """Cria o item na posição (x, y). tipo diz o que ele é."""
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.tipo = tipo

    def update(self, velocidade):
        """Anda para a esquerda junto com o cenário."""
        self.rect.x -= velocidade
        if self.rect.right < 0:
            self.kill()


AVISO = 'aviso'
ATACANDO = 'atacando'


# [NÍVEL: DIFÍCIL] — uma mini máquina de estados (AVISO -> ATACANDO).
class Missil(pygame.sprite.Sprite):
    """Pombo-míssil: primeiro um aviso pisca, depois o pombo atravessa a tela."""

    def __init__(self, quadros, imagem_aviso, altura):
        """Começa no estado AVISO, na borda direita, na altura dada."""
        pygame.sprite.Sprite.__init__(self)
        self.quadros = quadros
        self.imagem_aviso = imagem_aviso
        self.imagem_vazia = pygame.Surface(imagem_aviso.get_size(), pygame.SRCALPHA)
        self.altura = altura
        self.estado = AVISO
        self.inicio = pygame.time.get_ticks()
        self.image = imagem_aviso
        self.rect = self.image.get_rect()
        self.rect.right = LARGURA - 10
        self.rect.centery = altura
        # Máscara vazia: durante o aviso, encostar não machuca.
        self.mask = pygame.mask.Mask(self.rect.size)
        self.quadro = 0

    def update(self, velocidade):
        """Pisca o aviso; depois de TEMPO_AVISO_MISSIL, vira pombo e ataca."""
        agora = pygame.time.get_ticks()
        if self.estado == AVISO:
            if (agora // 150) % 2 == 0:
                self.image = self.imagem_aviso
            else:
                self.image = self.imagem_vazia
            if agora - self.inicio >= TEMPO_AVISO_MISSIL:
                # Troca de estado: agora ele é o pombo, fora da tela à direita.
                self.estado = ATACANDO
                self.image = self.quadros[0]
                self.rect = self.image.get_rect()
                self.rect.left = LARGURA
                self.rect.centery = self.altura
                self.mask = pygame.mask.from_surface(self.image)
        else:
            self.rect.x -= velocidade + VEL_MISSIL
            self.quadro += 1
            # Troca a asa a cada 6 quadros do jogo (// 6).
            self.image = self.quadros[(self.quadro // 6) % len(self.quadros)]
            if self.rect.right < 0:
                self.kill()


# [NÍVEL: MÉDIO] — igual à classe Explosion do tutorial (jogo_v15).
class Explosao(pygame.sprite.Sprite):
    """Animação de explosão que some sozinha quando acaba."""

    def __init__(self, quadros, centro):
        """Começa no primeiro quadro, centralizada no ponto dado."""
        pygame.sprite.Sprite.__init__(self)
        self.quadros = quadros
        self.quadro = 0
        self.image = self.quadros[0]
        self.rect = self.image.get_rect()
        self.rect.center = centro
        self.ultimo_quadro = pygame.time.get_ticks()
        self.tempo_quadro = 60

    def update(self, velocidade):
        """Anda com o cenário e passa para o próximo quadro a cada 60 ms."""
        self.rect.x -= velocidade
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_quadro >= self.tempo_quadro:
            self.ultimo_quadro = agora
            self.quadro += 1
            if self.quadro == len(self.quadros):
                self.kill()  # acabou a animação
            else:
                centro = self.rect.center
                self.image = self.quadros[self.quadro]
                self.rect = self.image.get_rect()
                self.rect.center = centro
