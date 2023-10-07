import pygame
from sys import exit
from random import randint, choice

def animacao_rochas():
    global movimento_rochas

    if fundo_rochas_voadoras_rect.y <= -20:
        movimento_rochas = 1
    elif fundo_rochas_voadoras_rect.y >= 20:
        movimento_rochas = -1
    
    fundo_rochas_voadoras_rect.y += movimento_rochas

    tela.blit(fundo_rochas_voadoras, fundo_rochas_voadoras_rect)

def animacao_estrelas():
    global index_estrelas
    index_estrelas += 0.22

    if (index_estrelas >= 4):
        index_estrelas = 0
    
    if (int(index_estrelas) == 0):
        tela.blit(fundo_estrelas, (0, 0))
    elif (int(index_estrelas) == 1):
        tela.blit(fundo_estrelas_2, (0, 0))
    else:
        tela.blit(fundo_estrelas_3, (0, 0))

def animacao_personagem():
    global jogador_index
    # Calcula o movimento do personagem
    jogador_retangulo.x += movimento_personagem

    if jogador_retangulo.right >= 960:
        jogador_retangulo.right = 960
    elif jogador_retangulo.left <= 0:
        jogador_retangulo.left = 0

    # jogador_surface = null

    if movimento_personagem == 0: # Jogador está parado
        jogador_superficies = jogador_parado_superficies
    else: # Jogador está se movimentando
        jogador_superficies = jogador_voando_superficies

    # Avança para o proximo frame
    jogador_index += 0.11
    if jogador_index > len(jogador_superficies) - 1:
        jogador_index = 0

    if direcao_personagem == 1:
        jogador = pygame.transform.flip(jogador_superficies[int(jogador_index)], True, False)
    else:
        jogador = jogador_superficies[int(jogador_index)]

    # Desenha o jogador na tela
    tela.blit(jogador, jogador_retangulo)

def adicionar_objeto():
    global lista_chuva_objetos

    objetos_lista_aleatoria = ['Coração'] * 10 + ['Moeda'] * 10 + ['Projetil'] * 80
    tipo_objeto = choice(objetos_lista_aleatoria)

    posicao = (randint(10, 950), randint(-100, 0))
    velocidade = randint(5, 10)

    if tipo_objeto == 'Projetil':
        objeto_rect = projetil_superficies[0].get_rect(center=posicao)
    elif tipo_objeto == 'Coração':
        objeto_rect = coracao_superficies[0].get_rect(center=posicao)
    elif tipo_objeto == 'Moeda':
        objeto_rect = moeda_superficies[0].get_rect(center=posicao)

    lista_chuva_objetos.append({
        'tipo': tipo_objeto,
        'retangulo': objeto_rect,
        'velocidade': velocidade
    })

def movimento_objetos_chuva():
    global lista_chuva_objetos

    for objeto in lista_chuva_objetos:

        objeto['retangulo'].y += objeto['velocidade']

        if objeto['tipo'] == 'Projetil':
            tela.blit(projetil_superficies[projetil_index], objeto['retangulo'])
        elif objeto['tipo'] == 'Coração':
            tela.blit(coracao_superficies[projetil_index], objeto['retangulo'])
        elif objeto['tipo'] == 'Moeda':
            tela.blit(moeda_superficies[projetil_index], objeto['retangulo'])

        if objeto['retangulo'].y > 540:
            lista_chuva_objetos.remove(objeto)

def colisoes_jogador():
    global coracao, moeda

    for objeto in lista_chuva_objetos:
        if jogador_retangulo.colliderect(objeto['retangulo']):
            if objeto['tipo'] == 'Coração':
                coracao += 1
            elif objeto['tipo'] == 'Moeda':
                moeda += 1
            elif objeto['tipo'] == 'Projetil':
                coracao -= 1

            # Remove o objeto da lista, logo da tela
            lista_chuva_objetos.remove(objeto)

def mostra_textos():
    global moeda, coracao

    texto_moedas = fonte_pixel.render(f"{moeda}", True, '#FFFFFF')
    texto_coracoes = fonte_pixel.render(f"{coracao}", True, '#FFFFFF')

    logo_moeda = pygame.transform.scale(moeda_superficies[0], (30, 30))
    logo_coracao = pygame.transform.scale(coracao_superficies[0], (40, 40))

    tela.blit(texto_coracoes, (12, 10))
    tela.blit(texto_moedas, (12, 50))

    tela.blit(logo_coracao, (60, 0))
    tela.blit(logo_moeda, (65, 45))

# Inicializa o pygame
pygame.init()

# Cria a tela
tamanho = (960, 540)
tela = pygame.display.set_mode(tamanho)

# Define o Titulo da Janela
pygame.display.set_caption("ChuvaMortal")

##
## Importa os arquivos necessários
##

# Carrega a fonte do Jogo
fonte_pixel = pygame.font.Font('assets/font/PixelType.ttf', 50)

# Carrega o plano de fundo
plano_fundo = pygame.image.load('assets/fundo/Night-Background8.png').convert()
fundo_estrelas = pygame.image.load('assets/fundo/Night-Background7.png').convert_alpha()
fundo_estrelas_2 = pygame.image.load('assets/fundo/Night-Background6.png').convert_alpha()
fundo_estrelas_3 = pygame.image.load('assets/fundo/Night-Background5.png').convert_alpha()
fundo_rochas = pygame.image.load('assets/fundo/Night-Background4.png').convert_alpha()
fundo_chao = pygame.image.load('assets/fundo/Night-Background3.png').convert_alpha()
fundo_lua = pygame.image.load('assets/fundo/Night-Background2.png').convert_alpha()
fundo_rochas_voadoras = pygame.image.load('assets/fundo/Night-Background1.png').convert_alpha()

# Transforma o tamanho da imagem de fundo
plano_fundo = pygame.transform.scale(plano_fundo, tamanho)
fundo_estrelas = pygame.transform.scale(fundo_estrelas, tamanho)
fundo_estrelas_2 = pygame.transform.scale(fundo_estrelas_2, tamanho)
fundo_estrelas_3 = pygame.transform.scale(fundo_estrelas_3, tamanho)
fundo_rochas = pygame.transform.scale(fundo_rochas, tamanho)
fundo_chao = pygame.transform.scale(fundo_chao, tamanho)
fundo_lua = pygame.transform.scale(fundo_lua, tamanho)
fundo_rochas_voadoras = pygame.transform.scale(fundo_rochas_voadoras, tamanho)
fundo_rochas_voadoras_rect = fundo_rochas_voadoras.get_rect(topleft = (0, 0))

index_estrelas = 0
movimento_rochas = 1

# Carrega as imagens do personagem
jogador_index = 0
jogador_parado_superficies = []
jogador_voando_superficies = []

# Carrega o jogador parado
for imagem in range(1, 14):
    img = pygame.image.load(f'assets/jogador/parado/Hero Boy Idle{imagem}.png').convert_alpha()
    jogador_parado_superficies.append(img)

# Carrega o jogador se movimentando
for imagem in range(1, 9):
    img = pygame.image.load(f'assets/jogador/voar/Hero Boy Fly{imagem}.png').convert_alpha()
    jogador_voando_superficies.append(img)

jogador_retangulo = jogador_parado_superficies[jogador_index].get_rect( center = (100, 430))

# Carrega o coração
coracao_superficies = []
coracao_index = 0
for imagem in range(1, 4):
    img = pygame.image.load(f'assets/objetos/coracao/Heart{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    coracao_superficies.append(img)

# Carrega a Moeda
moeda_superficies = []
moeda_index = 0
for imagem in range(1, 5):
    img = pygame.image.load(f'assets/objetos/moeda/Coin-A{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    moeda_superficies.append(img)

# Carrega o Projetil
projetil_superficies = []
projetil_index = 0
for imagem in range(1, 4):
    img = pygame.image.load(f'assets/objetos/projetil/Hero Bullet{imagem}.png').convert_alpha()
    projetil_superficies.append(img)

# Guarda os objetos que vão cair do céu
lista_chuva_objetos = []

# Cria um relógio para controlar os FPS
relogio = pygame.time.Clock()

# Controla se o personagem está andando (negativo esquerda, positivo direita)
movimento_personagem = 0
direcao_personagem = 0

# Cria um evento para adicionar um objeto na tela
novo_objeto_timer = pygame.USEREVENT + 1
pygame.time.set_timer(novo_objeto_timer, 500)

jogo_ativo = True

moeda = 0
coracao = 3

# Loop principal do jogo
while jogo_ativo:
    # EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                movimento_personagem = 10
                direcao_personagem = 1

            if evento.key == pygame.K_LEFT:
                movimento_personagem = -10
                direcao_personagem = 0

            if evento.key == pygame.K_ESCAPE:
                jogo_ativo = False

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT:
                movimento_personagem = 0

            if evento.key == pygame.K_LEFT:
                movimento_personagem = 0

        if evento.type == novo_objeto_timer:
            adicionar_objeto()

    # Desenha o fundo na tela
    tela.blit(plano_fundo, (0, 0))
    
    animacao_estrelas()

    tela.blit(fundo_rochas, (0, 0))
    tela.blit(fundo_chao, (0, 0))
    tela.blit(fundo_lua, (0, 0))

    animacao_rochas()
    
    # Faz a chamada da função animação do personagem
    animacao_personagem()

    movimento_objetos_chuva()

    colisoes_jogador()

    mostra_textos()

    # Atualiza a tela com o conteudo
    pygame.display.update()

    # Define a quantidade de frames por segundo
    relogio.tick(60)