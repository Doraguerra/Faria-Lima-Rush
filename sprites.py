"""Classes (sprites) do jogo Atrasado na Faria Lima."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import CHAO_Y, TETO_Y, JOGADOR_X, GRAVIDADE, EMPURRAO, VEL_MAX


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
        if self.rect.top < TETO_Y:  # passou no teto; se tiver <= da bug e voa para sempre
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
