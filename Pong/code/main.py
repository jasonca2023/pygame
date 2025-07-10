import pygame, sys, random

def ballAnimation():
    global ballSpeedX, ballSpeedY, playerScore, opponentScore, scoreTime
    ball.x += ballSpeedX
    ball.y += ballSpeedY

    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSpeedY *= -1
        
    if ball.left <= 0:
        playerScore += 1
        scoreTime = pygame.time.get_ticks()
    if ball.right >= screenWidth:
        opponentScore += 1
        scoreTime = pygame.time.get_ticks()
        
    if ball.colliderect(player) and ballSpeedX > 0:
        if abs(ball.right - player.left) < 10:
            ballSpeedX *= -1
        elif abs(ball.bottom - player.top) < 10 and ballSpeedY > 0:
            ballSpeedY *= -1
        elif abs(ball.top - player.bottom) < 10 and ballSpeedY < 0:
            ballSpeedY *= -1
    if ball.colliderect(opponent) and ballSpeedX < 0:
        if abs(ball.left - opponent.right) < 10:
            ballSpeedX *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ballSpeedY > 0:
            ballSpeedY *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ballSpeedY < 0:
            ballSpeedY *= -1
        
            
def playerAnimation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screenHeight:
        player.bottom = screenHeight

def opponentAI():
    if opponent.top < ball.y:
        opponent.top += opponentSpeed
    if opponent.bottom >= ball.y:
        opponent.bottom -= opponentSpeed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screenHeight:
        opponent.bottom = screenHeight

def ballRestart():
    global ballSpeedX, ballSpeedY, scoreTime

    currentTime = pygame.time.get_ticks()
    
    ball.center = (screenWidth / 2, screenHeight / 2)
    
    if currentTime - scoreTime < 2100:
        ballSpeedX, ballSpeedY = 0, 0
    else:
        ballSpeedX, ballSpeedY = 7, 7 
        ballSpeedY *= random.choice((1, -1))
        ballSpeedX *= random.choice((1, -1))
        scoreTime = None
           
pygame.init()
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')

ball = pygame.Rect(screenWidth/2 - 15, screenHeight/2 - 15, 30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight/2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight/2 - 70, 10, 140)

bgColor = pygame.Color('grey12')
lightGrey = (200, 200, 200)

ballSpeedX = 7 * random.choice((1, -1))
ballSpeedY = 7 * random.choice((1, -1))
playerSpeed = 0
opponentSpeed = 10

playerScore = 0
opponentScore = 0
gameFont = pygame.font.Font('freesansbold.ttf', 32)

bg_music = pygame.mixer.Sound('../audio/music.wav')
bg_music.set_volume(0.7)
bg_music.play(-1)

scoreTime = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerSpeed += 10
            if event.key == pygame.K_UP:
                playerSpeed -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                playerSpeed -= 10
            if event.key == pygame.K_UP:
                playerSpeed += 10

    ballAnimation() 
    playerAnimation()
    player.y += playerSpeed
    opponentAI()    

    screen.fill(bgColor)
    
    pygame.draw.rect(screen, lightGrey, player)
    pygame.draw.rect(screen, lightGrey, opponent)
    pygame.draw.ellipse(screen, lightGrey, ball)
    pygame.draw.aaline(screen, lightGrey, (screenWidth/2, 0), (screenWidth/2, screenHeight))

    if scoreTime:
        ballRestart()
        
    playerText = gameFont.render(f"{playerScore}", True, lightGrey)
    screen.blit(playerText, (660, 470))

    opponentText = gameFont.render(f"{opponentScore}", True, lightGrey)
    screen.blit(opponentText, (600, 470))
    
    pygame.display.flip()
    clock.tick(60)
