"""Gerador: decide quando cada obstáculo e item aparece."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import random
import pygame
from config import LARGURA, TETO_Y, CHAO_Y
from config import VEL_PATINETE, FAIXA_PATINETE
from sprites import Drone
from sprites import Item
from sprites import Missil
from assets import tocar


# [NÍVEL: DIFÍCIL] — temporizadores com get_ticks() (mesma ideia do limite
# de tiros do jogo_v16 do tutorial), agora para vários tipos de objeto.
class Gerador:
    """Guarda o instante em que cada tipo de objeto deve nascer."""

    def __init__(self, assets):
        """Marca os primeiros horários de nascimento (em milissegundos)."""
        self.assets = assets
        agora = pygame.time.get_ticks()
        self.proximo_drone = agora + 1500
        self.proximo_cafe = agora + 2500
        self.proximo_missil = agora + 4000
        self.proximo_capacete = agora + random.randint(20000, 30000)
        self.proximo_patinete = agora + 6000

    def atualizar(self, fase, jogador, grupos):
        """Cria os objetos cujo horário chegou e sorteia o próximo horário."""
        agora = pygame.time.get_ticks()
        if agora >= self.proximo_drone:
            imagem = self.assets['drone']
            # Procura uma altura onde o drone não nasça em cima de um item.
            y = self.sortear_altura_livre(imagem.get_width(), imagem.get_height(), grupos['itens'])
            if y is None:
                self.proximo_drone = agora + 200  # sem espaço: tenta de novo em 0,2 s
            else:
                movel = fase['drones_moveis'] and random.random() < 0.5
                drone = Drone(imagem, movel)
                drone.rect.y = y
                grupos['todos'].add(drone)
                grupos['obstaculos'].add(drone)
                minimo, maximo = fase['intervalo_drone']
                self.proximo_drone = agora + random.randint(minimo, maximo)
        if agora >= self.proximo_cafe:
            if self.criar_fileira_de_cafes(grupos):
                self.proximo_cafe = agora + random.randint(3000, 5000)
            else:
                self.proximo_cafe = agora + 300  # sem espaço: tenta de novo em 0,3 s
        if fase['misseis'] and agora >= self.proximo_missil:
            # O aviso aparece na altura em que o jogador está AGORA.
            missil = Missil(self.assets['pombo'], self.assets['aviso'], jogador.rect.centery)
            grupos['todos'].add(missil)
            grupos['obstaculos'].add(missil)
            tocar(self.assets['som_aviso'])
            self.proximo_missil = agora + random.randint(3000, 6000)
        # [NÍVEL: FÁCIL] — reaproveita a classe Missil: o patinete é um
        # "míssil de chão". Muda só a imagem e a altura (sempre rente à rua).
        if agora >= self.proximo_patinete:
            quadros = self.assets['patinete']
            altura = CHAO_Y - quadros[0].get_height() // 2  # o meio do patinete, encostado no chão
            patinete = Missil(quadros, self.assets['aviso'], altura, VEL_PATINETE)
            grupos['todos'].add(patinete)
            grupos['obstaculos'].add(patinete)
            tocar(self.assets['som_aviso'])
            self.proximo_patinete = agora + random.randint(6000, 10000)
        if agora >= self.proximo_capacete:
            imagem = self.assets['capacete']
            y = self.sortear_altura_livre(imagem.get_width(), imagem.get_height(), grupos['obstaculos'])
            if y is None:
                self.proximo_capacete = agora + 300
            else:
                capacete = Item(imagem, 'capacete', LARGURA, y)
                grupos['todos'].add(capacete)
                grupos['itens'].add(capacete)
                self.proximo_capacete = agora + random.randint(25000, 40000)

    # [NÍVEL: MÉDIO] — colliderect e inflate são do pygame.Rect.
    def area_livre(self, retangulo, grupo):
        """Devolve True se nenhum sprite do grupo encosta no retângulo.

        O retângulo é aumentado em 20 px de cada lado (inflate) para sobrar
        uma folga: assim as coisas não nascem coladas umas nas outras.
        """
        com_folga = retangulo.inflate(40, 40)
        for sprite in grupo:
            if com_folga.colliderect(sprite.rect):
                return False
        return True

    # [NÍVEL: MÉDIO]
    def sortear_altura_livre(self, largura, altura, grupo):
        """Sorteia uma altura (y) livre na borda direita da tela, acima da calçada.

        Tenta até 10 sorteios. Devolve o y encontrado, ou None se não achar.
        """
        for tentativa in range(10):
            # Só até a FAIXA_PATINETE: a calçada fica livre para os patinetes.
            y = random.randint(TETO_Y, FAIXA_PATINETE - altura)
            retangulo = pygame.Rect(LARGURA, y, largura, altura)
            if self.area_livre(retangulo, grupo):
                return y
        return None

    # [NÍVEL: FÁCIL]
    def criar_fileira_de_cafes(self, grupos):
        """Cria 5 cafés em fila numa altura livre de obstáculos.

        Devolve True se criou e False se não achou espaço.
        """
        imagem = self.assets['cafe']
        largura_fileira = 4 * 50 + imagem.get_width()  # do 1º ao fim do 5º café
        y = self.sortear_altura_livre(largura_fileira, imagem.get_height(), grupos['obstaculos'])
        if y is None:
            return False
        for i in range(5):
            cafe = Item(imagem, 'cafe', LARGURA + i * 50, y)
            grupos['todos'].add(cafe)
            grupos['itens'].add(cafe)
        return True
