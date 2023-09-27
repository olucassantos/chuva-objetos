import pygame
from sys import exit
import random

def animacao_jogador():
    global jogador_index, movimento_jogador, direcao_jogador
    # Movimenta o jogador
    jogador_parado_retangle.x += movimento_jogador

    # Impede que o jogador saia da tela
    if jogador_parado_retangle.left <= -30:
        jogador_parado_retangle.left = -30
    elif jogador_parado_retangle.right >= 1000:
        jogador_parado_retangle.right = 1000

    # Decide qual imagem do jogador deve ser mostrada

    if movimento_jogador == 0: # Jogador está parado
        surface_jogador = jogador_parado_surfaces
        quantidade_imagens = 12
    elif movimento_jogador != 0: # Jogador está se movendo
        surface_jogador = jogador_voando_surfaces
        quantidade_imagens = 7

    # Desenha e atualiza a imagem do jogador
    if jogador_index >= quantidade_imagens:
        jogador_index = 0
    
    jogador_index += 0.11

    # Vira o jogador para a direção que ele está indo
    if direcao_jogador == 1:
        jogador = pygame.transform.flip(surface_jogador[int(jogador_index)], True, False)
    else:
        jogador = surface_jogador[int(jogador_index)]

    # Desenha o jogador na tela
    tela.blit(jogador, jogador_parado_retangle)

def animacao_objetos_chuva():
    global objetos_caindo, coracao_index, moeda_index, projetil_index

    for objeto in objetos_caindo:
        # Move o Objeto para baixo
        objeto['objeto'].y += objeto['velocidade']
        if objeto['tipo'] == 'Heart':
            tela.blit(coracao_surfaces[coracao_index], objeto['objeto'])
        elif objeto['tipo'] == 'Coin':
            tela.blit(moeda_surfaces[moeda_index], objeto['objeto'])
        elif objeto['tipo'] == 'Bullet':
            tela.blit(projetil_surfaces[projetil_index], objeto['objeto'])

        # Verifica se o objeto saiu da tela
        if objeto['objeto'].top > 540:
            objetos_caindo.remove(objeto)

def adiciona_novo_objeto():
    global objetos_caindo, coracao_surfaces, moeda_surfaces, projetil_surfaces

    objetos = ['Heart'] * 10 + ['Coin'] * 10 + ['Bullet'] * 80
    objeto = random.choice(objetos)

    posicao = (random.randint(10, 950), random.randint(-100, 0))

    if objeto == 'Heart':
        objeto_rect = coracao_surfaces[0].get_rect(center=posicao)
    elif objeto == 'Coin':
        objeto_rect = moeda_surfaces[0].get_rect(center=posicao)
    elif objeto == 'Bullet':
        objeto_rect = projetil_surfaces[0].get_rect(center=posicao)

    objetos_caindo.append({
        'tipo': objeto, # 'Heart', 'Coin', 'Bullet
        'objeto': objeto_rect, 
        'velocidade': random.randint(5, 10)
    })

# Inicializa o pygame
pygame.init()

# Cria a tela
tamanho = (960, 540)
tela = pygame.display.set_mode(tamanho)

# Define o título da janela
pygame.display.set_caption('ChuvaMortal')

# Cria o relógio para controlar o FPS
relogio = pygame.time.Clock()

# Carrega os arquivos necessários para o jogo
fonte_pixel = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

## Carrega as imagens de fundo
plano_fundo = pygame.image.load('assets/fundo/Night-Background8.png').convert()
fundo_estrelas = pygame.image.load('assets/fundo/Night-Background7.png').convert()
fundo_estrelas_2 = pygame.image.load('assets/fundo/Night-Background6.png').convert()
fundo_estrelas_3 = pygame.image.load('assets/fundo/Night-Background5.png').convert()
fundo_rochas = pygame.image.load('assets/fundo/Night-Background4.png').convert()
fundo_chao = pygame.image.load('assets/fundo/Night-Background3.png').convert()
fundo_lua = pygame.image.load('assets/fundo/Night-Background2.png').convert()
fundo_rochas_voadoras = pygame.image.load('assets/fundo/Night-Background1.png').convert()

# Transforma as imagens de fundo para o tamanho da tela
plano_fundo = pygame.transform.scale(plano_fundo, tamanho)
fundo_estrelas = pygame.transform.scale(fundo_estrelas, tamanho)
fundo_estrelas_2 = pygame.transform.scale(fundo_estrelas_2, tamanho)
fundo_estrelas_3 = pygame.transform.scale(fundo_estrelas_3, tamanho)
fundo_rochas = pygame.transform.scale(fundo_rochas, tamanho)
fundo_chao = pygame.transform.scale(fundo_chao, tamanho)
fundo_lua = pygame.transform.scale(fundo_lua, tamanho)
fundo_rochas_voadoras = pygame.transform.scale(fundo_rochas_voadoras, tamanho)

## Carrega as imagens do jogador para dentro de uma lista
jogador_parado_surfaces = []
for imagem in range(1, 14):
    img = pygame.image.load(f'assets/jogador/parado/Hero Boy Idle{imagem}.png').convert_alpha()
    jogador_parado_surfaces.append(img)

jogador_voando_surfaces = []
for imagem in range(1, 9):
    img = pygame.image.load(f'assets/jogador/voar/Hero Boy Fly{imagem}.png').convert_alpha()
    jogador_voando_surfaces.append(img)

coracao_surfaces = []
coracao_index = 0
for imagem in range(1, 4):
    img = pygame.image.load(f'assets/objetos/coracao/Heart{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    coracao_surfaces.append(img)

moeda_surfaces = []
moeda_index = 0
for imagem in range(1, 5):
    img = pygame.image.load(f'assets/objetos/moeda/Coin-A{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    moeda_surfaces.append(img)

projetil_surfaces = []
projetil_index = 0
for imagem in range(1, 4):
    img = pygame.image.load(f'assets/objetos/projetil/Hero Bullet{imagem}.png').convert_alpha()
    projetil_surfaces.append(img)

# Define um index para qual imagem será usada
jogador_index = 0

# Define um retângulo para posicionar a imagem do jogador
jogador_parado_retangle = jogador_parado_surfaces[jogador_index].get_rect(center=(100, 430))

# Define a velocidade de movimento do jogador
movimento_jogador = 0

# Define a direção que o jogador está indo
direcao_jogador = 0

# Cria uma lista de objetos que caem do céu
objetos_caindo = []

# Cria um novo evento para adicionar objetos na lista
objetos_caindo_timer = pygame.USEREVENT + 1
pygame.time.set_timer(objetos_caindo_timer, 500)

animacao_coracoes_timer = pygame.USEREVENT + 2
pygame.time.set_timer(animacao_coracoes_timer, 100)

animacao_moedas_timer = pygame.USEREVENT + 3
pygame.time.set_timer(animacao_moedas_timer, 100)

animacao_projetil_timer = pygame.USEREVENT + 4
pygame.time.set_timer(animacao_projetil_timer, 50)

# Laço principal do jogo
while True:

    # Le os eventos do jogo
    for evento in pygame.event.get():

        # Verifica se o jogador quer sair
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Verifica se o jogador pressionou alguma tecla
        if evento.type == pygame.KEYDOWN:

            # Verifica se o jogador pressionou a seta para direita
            if evento.key == pygame.K_RIGHT:
                movimento_jogador = 5
                direcao_jogador = 1

            # Verifica se o jogador pressionou a seta para esquerda
            if evento.key == pygame.K_LEFT:
                movimento_jogador = -5
                direcao_jogador = -1

        # Verifica se o jogador soltou alguma tecla
        if evento.type == pygame.KEYUP:
                
                # Verifica se o jogador soltou a seta para direita
                if evento.key == pygame.K_RIGHT:
                    movimento_jogador = 0
    
                # Verifica se o jogador soltou a seta para esquerda
                if evento.key == pygame.K_LEFT:
                    movimento_jogador = 0

        if evento.type == objetos_caindo_timer:
            adiciona_novo_objeto()

        if evento.type == animacao_coracoes_timer:
            coracao_index += 1
            if coracao_index >= len(coracao_surfaces):
                coracao_index = 0

        if evento.type == animacao_moedas_timer:
            moeda_index += 1
            if moeda_index >= len(moeda_surfaces):
                moeda_index = 0
        
        if evento.type == animacao_projetil_timer:
            projetil_index += 1
            if projetil_index >= len(projetil_surfaces):
                projetil_index = 0


    # Desenha o fundo do jogo
    tela.blit(plano_fundo, (0, 0))
    tela.blit(fundo_estrelas, (0, 0))
    tela.blit(fundo_estrelas_2, (0, 0))
    tela.blit(fundo_estrelas_3, (0, 0))
    tela.blit(fundo_rochas, (0, 0))
    tela.blit(fundo_chao, (0, 0))
    tela.blit(fundo_lua, (0, 0))
    tela.blit(fundo_rochas_voadoras, (0, 0))

    # Anima o personagem 
    animacao_jogador()
    animacao_objetos_chuva()

    # Atualiza a tela
    pygame.display.update()

    # Define o FPS (quantas vezes o loop será executado por segundo)
    relogio.tick(60)