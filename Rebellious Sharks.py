import pygame
import math
import random

# Initializing Pygame
pygame.init()

# Setting our screen size
screenX, screenY = 800, 600
screen = pygame.display.set_mode((screenX, screenY))

# Setting game title
pygame.display.set_caption('Rebellious Shark')

# Setting Game Icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Whether game is running or not
running = True

firebullet = False
showBullet = False

#Initalizing images
bgImg = pygame.image.load('ocean.png')              #background image
enemyImg = pygame.image.load('shark.png')           #Enemy image
shipImg = pygame.image.load('spaceship.png')        #Player image
bulletImg = pygame.image.load('laser.png')          #Bullet image

#Variables used
shipX = 330
shipY = 450
bulletX, bulletY = 0, 0
enemyX, enemyY = 0, 0
enemyListX, enemyListY = [], []
enemies = 20
shipMovement = 10
shipChange = 0

Score = 0
gamenotover = True

#Drawing our ship on screen
def showShip(sX, sY):

    screen.blit(pygame.transform.scale(shipImg, (100, 100)), (sX, sY))

#Generating enemies X and Y positions randomly
def enemy():
    e = 0
    while e < enemies:
        enemyListX.append(random.randint(0, screenX - 100))
        enemyListY.append(random.randint(-1200, -10))
        e += 1
enemy()

#Generating and showing enemies
def showEnemies():
    e = 0
    while e < enemies:
        screen.blit(pygame.transform.scale(enemyImg, (100, 100)), (enemyListX[e], enemyListY[e]))
        e+=1

#shooting bullet
def bullet():
    global  showBullet
    showBullet = True
    if showBullet:
        screen.blit(bulletImg, (bulletX, bulletY))

#Moving enemies top to bottom
def moveEnemies():
    for i in range(enemies):
        if gamenotover:
            enemyListY[i] += 1.5

#checking if bullet hits the enemy
def checkbullethit(ex,ey,bx,by):
    dis = math.sqrt(((ex-bx)**2) + ((ey-by)**2))
    if dis < 100:
        return True
    else:
        return False

#Checking if enemy hits our player
def checkshiphit(ex,ey,sx,sy):
    dis = math.sqrt(((ex-sx)**2) + ((ey-sy)**2))
    if dis < 150:
        return True
    else:
        return False

#show Score on screen
def showScore():
    global Score
    font = pygame.font.Font('freesansbold.ttf', 32)
    s = font.render('Score: ' + str(Score), True, (255,255,255))
    screen.blit(s, (20,20))

#Game Over
def gameover():
    font = pygame.font.Font('freesansbold.ttf', 110)
    s = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(s, (80, 120))

# Everything inside this loop
while running:

    #Setting background
    screen.blit(bgImg, (0, 0))


    #Events
    for event in pygame.event.get():
        #If user clicks the red cross
        if event.type == pygame.QUIT:
            running = False

        #HAndling Key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipChange -= shipMovement
            if event.key == pygame.K_UP:
                shipY -= 5
            if event.key == pygame.K_RIGHT:
                shipChange += shipMovement
            if event.key == pygame.K_SPACE:
                bulletX = shipX + 37
                bulletY = shipY
                firebullet = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shipChange = 0

    #moving ship left or right
    shipX += shipChange

    showEnemies()
    moveEnemies()

    #checking if bullet is ready to fire
    if firebullet:
        bullet()
        bulletY -= 40


    #Looping through all the enmies
    for i in range(enemies):
        #checking if bullet hits any enemy
        checkbullet = checkbullethit(enemyListX[i], enemyListY[i], bulletX, bulletY)

        # checking if any enemy hits our ship
        checkship = checkbullethit(enemyListX[i], enemyListY[i], shipX, shipY)

        if checkship:
            gamenotover = False
            gameover()

        if checkbullet:
            #Bullet will disappear
            showBullet = False

            #Chaging enemy position to random again and it will come again from top
            enemyListX[i]= random.randint(0, screenX - 100)
            enemyListY[i]=random.randint(-900, -10)

            #incrementing score
            Score += 1
            #IDK why I did this!
            bulletX, bulletY = -100, -100


    # Preventing ship to go out of screen
    if shipX <= 0:
        shipX = 0
    elif shipX >= screenX-100:
        shipX = screenX - 100

    showShip(shipX, shipY)
    showScore()

    #Most important thing!!!!
    pygame.display.update()
