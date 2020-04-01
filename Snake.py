import pygame
import random
import math

#initializing pygame
pygame.init()

#Setting screen
screenX, screenY = 801, 601
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption('Snake')

#Initializing Elements for the game
foodsize = 25
snakeSize = 25
snakeX, snakeY = random.randint(2, 15) * snakeSize, random.randint(2, 11)* snakeSize
snake_length = 1
snake = []
snakeSpeed = snakeSize
snakeDirection = 0
score = 0
#Snake Direction Assigning to 0 means no direction currently
#1 for upward
#2 for downward
#3 for left
#4 for right

foodX, foodY = random.randint(2, 15) * snakeSize, random.randint(2, 11)* snakeSize

gameover = False
gameoverText = ''

def drawFood():
    global foodX, foodY, foodsize
    foodRect = pygame.Rect(foodX,foodY, foodsize,foodsize)
    pygame.draw.rect(screen, (255,0,0), foodRect)

def changeFood():
    global foodX, foodY, snakeSize
    foodX, foodY = random.randint(0, 31) * snakeSize, random.randint(0, 23) * snakeSize
    drawFood()

def drawSnake():
    global snake, snake_length
    for x, y in snake:
        rect = pygame.Rect(x,y, snakeSize, snakeSize)
        pygame.draw.rect(screen, (0,255,0), rect)

def moveSnake():  # (x coordinate of snake, y cordinate of snake, direction of snake)
    global snake, snakeDirection, gameover, screenY, screenX, snakeX, snakeY, gameoverText
    x, y = snake[-1]
    if snakeDirection == 1:
        if y <= 0:
            gameover = True
            gameoverText = 'OUT OF BOUNDS'
        else:
            snakeY -= snakeSpeed
    if snakeDirection == 2:
        if y >= screenY - snakeSize - snakeSize:
            gameover = True
            gameoverText = 'OUT OF BOUNDS'
        else:
            snakeY += snakeSpeed
    if snakeDirection == 3:
        if x <= 0:
            gameover = True
            gameoverText = 'OUT OF BOUNDS'
        else:
            snakeX -= snakeSpeed
    if snakeDirection == 4:
        if x >= screenX - snakeSize - snakeSize:
            gameover = True
            gameoverText = 'OUT OF BOUNDS'
        else:
            snakeX += snakeSpeed
    drawSnake()

def drawGrid():
    global snakeSize, screenX, screenY
    rows = screenY //snakeSize
    cols = screenX // snakeSize
    for i in range(rows+1):
        pygame.draw.line(screen, (255,255,255), (0, i*snakeSize), (screenX, i*snakeSize))
    for i in range(cols+1):
        pygame.draw.line(screen, (255,255,255), (i*snakeSize, 0), (i*snakeSize, screenY))

def ifSnakeEatsFood(sx,sy,fx,fy):
    global snake_length, score
    dis = math.sqrt((sx-fx)**2 + (sy-fy)**2)
    if dis < foodsize:
        changeFood()
        snake_length += 3
        score += 10
    else:
        return False

def ifSnakeEatsSnake():
    global snake, gameover, gameoverText
    if snake[-1] in snake[:-1]:
        gameover = True
        gameoverText = 'YOU ATE YOURSELF'

def gameOverText():
    global snakeSpeed, gameoverText, score

    screen.fill((0,0,0))
    font1 = pygame.font.Font('freesansbold.ttf', 100)
    font2 = pygame.font.Font('freesansbold.ttf', 50)
    font3 = pygame.font.Font('freesansbold.ttf', 20)
    gameovertext1 = font1.render('Game Over', True, (255,255,255))
    screen.blit(gameovertext1, (100,100))
    gameovertext2 = font2.render(gameoverText, True, (255,255,255))
    gameovertext3 = font2.render('Your Score is %d'%score, True, (255, 255, 255))
    gameovertext4 = font2.render('Press Space to Play again', True, (255, 255, 255))
    gameovertext5 = font3.render('Developed by Gaurav Verma', True, (255, 0,0))
    gameovertext6 = font3.render('Developer\'s email: vermagourav2001@gmail.com', True, (255, 0, 0))
    screen.blit(gameovertext2, (100, 250))
    screen.blit(gameovertext3, (120, 350))
    screen.blit(gameovertext4, (120, 450))
    screen.blit(gameovertext5, (200, 550))
    screen.blit(gameovertext6, (120, 580))

def showScore():
    global score
    font = pygame.font.Font('freesansbold.ttf', 25)
    scoretxt = font.render('Score: '+str(score), True,(255,255,255))
    screen.blit(scoretxt, (620,20))

def restart():
    global gameover,score, snakeX, snakeDirection, snake_length, snakeY, snake, foodY, foodX
    gameover = False
    score = 0
    snakeX, snakeY = random.randint(2, 11) * snakeSize, random.randint(2, 8) * snakeSize
    foodX, foodY = random.randint(2, 15) * snakeSize, random.randint(2, 11) * snakeSize
    snake_length = 1
    snake = []
    snakeDirection = 0


running = True
clock = pygame.time.Clock()
while running:
    if gameover:
        gameOverText()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart()
    else:
        pygame.time.delay(50)
        clock.tick(60)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snakeDirection != 2:
                    snakeDirection = 1
                if event.key == pygame.K_DOWN and snakeDirection != 1:
                    snakeDirection = 2
                if event.key == pygame.K_LEFT and snakeDirection != 4:
                    snakeDirection = 3
                if event.key == pygame.K_RIGHT and snakeDirection != 3:
                    snakeDirection = 4

        #Growing snake
        part = []
        part.append(snakeX)
        part.append(snakeY)
        snake.append(part)

        if len(snake) > snake_length:
            del snake[0]
        ifSnakeEatsSnake()
        #drawGrid()
        ifSnakeEatsFood(snakeX, snakeY, foodX, foodY)
        drawFood()
        moveSnake()
        showScore()
    pygame.display.update()
