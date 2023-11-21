import pygame
import sys
import random
import time

# Pygame Init
init_status = pygame.init()
if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 320
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

# FPS controller
fpsController = pygame.time.Clock()

# Game settings
delta = 10
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]
foodPos = [400, 50]
foodSpawn = True
direction = 'RIGHT'
changeto = ''
score = 0
base_speed =  15

# Función para elegir el color de la serpiente
def chooseSnakeColor():
    color_selected = False
    snake_color = green  # Color predeterminado

    while not color_selected:
        playSurface.fill(white)
        menuFont = pygame.font.SysFont('monaco', 36)
        menuText = menuFont.render("Choose Snake Color:", True, black)
        menuTextRect = menuText.get_rect()
        menuTextRect.midtop = (width // 2, height // 4)
        playSurface.blit(menuText, menuTextRect)

        # Opciones de colores para elegir
        color_options = [
            ("Green", green),
            ("Red", red),
            ("Blue", pygame.Color(0, 0, 255)),
            ("Yellow", pygame.Color(255, 255, 0)),
        ]

        # Mostrar opciones de colores
        y_position = height // 2
        for text, color in color_options:
            option_font = pygame.font.SysFont('monaco', 24)
            option_text = option_font.render(text, True, black)
            option_text_rect = option_text.get_rect()
            option_text_rect.midtop = (width // 2, y_position)
            playSurface.blit(option_text, option_text_rect)
            y_position += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_color = green
                    color_selected = True
                elif event.key == pygame.K_2:
                    snake_color = red
                    color_selected = True
                elif event.key == pygame.K_3:
                    snake_color = pygame.Color(0, 0, 255)
                    color_selected = True
                elif event.key == pygame.K_4:
                    snake_color = pygame.Color(255, 255, 0)
                    color_selected = True
    return snake_color

# Permitir al jugador elegir el color de la serpiente antes de iniciar el juego
snake_color = chooseSnakeColor()

# Nueva función para obtener la velocidad del juego basada en la longitud de la serpiente
def getSpeed():
    global base_speed, snakeBody
    return base_speed + len(snakeBody) // 2  # Incrementa la velocidad cada vez que la serpiente crece en 2 segmentos

# Función para hacer destellar la comida
def flashFood():
    original_food = playSurface.copy()  # Copia de la superficie actual

    for _ in range(3):  # Destellar tres veces
        pygame.display.flip()
        pygame.time.delay(100)  # Esperar 100 milisegundos
        playSurface.blit(original_food, (0, 0))  # Restaurar la superficie original
        pygame.display.flip()
        pygame.time.delay(100)  # Esperar 100 milisegundos
        
# Game Over
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()

# Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('monaco', 32)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (320, 100)
    playSurface.blit(Ssurf, Srect)

# Define un nuevo color para el fondo
background_color = pygame.Color(205, 125, 200) 

#Menu de inicio
def startMenu():
    menuFont = pygame.font.SysFont('monaco', 36)
    menuText = menuFont.render("Snake Game", True, green)
    menuTextRect = menuText.get_rect()
    menuTextRect.midtop = (width // 2, height // 4)

    startFont = pygame.font.SysFont('monaco', 24)
    startText = startFont.render("Press Enter to Start", True, black)
    startTextRect = startText.get_rect()
    startTextRect.midtop = (width // 2, height // 2)

    playSurface.fill(background_color)
    playSurface.blit(menuText, menuTextRect)
    playSurface.blit(startText, startTextRect)
    pygame.display.flip()

# Mostrar el menú de inicio inicialmente
startMenu()

# Función para hacer crecer la serpiente al comer
def growSnake():
    global snakeBody
    new_segment = list(snakeBody[-1])  # Crear una nueva parte del cuerpo en la posición de la última
    snakeBody.append(new_segment)  # Agregar la nueva parte al cuerpo

# Esperar hasta que el jugador presione Enter para comenzar el juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Iniciar el juego
                startMenu = False

    if not startMenu:
        break

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                changeto = 'LEFT'
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                changeto = 'UP'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    changeto = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    changeto = 'LEFT'
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    changeto = 'UP'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    changeto = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Validate direction
        if changeto == 'RIGHT' and direction != 'LEFT':
            direction = changeto
        if changeto == 'LEFT' and direction != 'RIGHT':
            direction = changeto
        if changeto == 'UP' and direction != 'DOWN':
            direction = changeto
        if changeto == 'DOWN' and direction != 'UP':
            direction = changeto

        # Update snake position
        if direction == 'RIGHT':
            snakePos[0] += delta
        if direction == 'LEFT':
            snakePos[0] -= delta
        if direction == 'DOWN':
            snakePos[1] += delta
        if direction == 'UP':
            snakePos[1] -= delta

        # Snake body mechanism
        
        snakeBody.insert(0, list(snakePos))
        if snakePos == foodPos:
            foodSpawn = False
            score += 1
            growSnake()  # Llamar a la función para hacer crecer la serpiente
        else:
            snakeBody.pop()
        if foodSpawn == False:
            foodPos = [random.randrange(1, width // 10) * delta, random.randrange(1, height // 10) * delta]
            foodSpawn = True
        playSurface.fill(background_color)  # Llena la superficie con el nuevo color de fondo

        for pos in snakeBody:
            pygame.draw.rect(playSurface, snake_color, pygame.Rect(pos[0], pos[1], delta, delta))
        pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], delta, delta))

        # Bounds
        if snakePos[0] >= width or snakePos[0] < 0:
            gameOver()
        if snakePos[1] >= height or snakePos[1] < 0:
            gameOver()

        # Self hit
        for block in snakeBody[1:]:
            if snakePos == block:
                gameOver()
        showScore()
        pygame.display.flip()
        fpsController.tick(20) 

        # actualizar la posición de la comida y otras condiciones de juego...
        fpsController.tick(getSpeed())  # Ajusta la velocidad del juego según la longitud de la serpiente   