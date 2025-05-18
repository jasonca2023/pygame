import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
import random

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True

        self.allSprites = pygame.sprite.Group()
        self.collisionSprites = pygame.sprite.Group()

        bgHeight = pygame.image.load('../graphics/background.png').get_height()
        self.scaleFactor = windowHeight / bgHeight

        BG(self.allSprites, self.scaleFactor)
        Ground([self.allSprites, self.collisionSprites], self.scaleFactor)
        self.plane = Plane(self.allSprites, self.scaleFactor / 2)

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, random.randint(800, 1400))

        self.font = pygame.font.Font('../graphics/font/flappy-bird-font.ttf', 30)
        self.score = 0
        self.startOffset = 0

        self.menuSurf = pygame.image.load('../graphics/ui/ui1.png').convert_alpha()
        self.menuRect = self.menuSurf.get_rect(center = (windowWidth / 2, windowHeight / 2))

        self.music = pygame.mixer.Sound('../sound/Background music.wav')
        self.music.set_volume(5)
        self.music.play(loops = -1)
        
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collisionSprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            for sprite in self.collisionSprites:
                if sprite.sprite_type == 'obstacle':
                    sprite.kill
            self.active = False
            self.plane.kill()

    def displayScore(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.startOffset) // 1000
            y = windowHeight / 10
        else:
            y = windowHeight / 2 + (self.menuRect.height / 1.7)
            
        scoreSurf = self.font.render(str(self.score), False, 'black')
        scoreRect = scoreSurf.get_rect(midtop = (windowWidth / 2, y))

        self.display_surface.blit(scoreSurf, scoreRect)

    def run(self):
        lastTime = time.time()
        while True:
            dt = time.time() - lastTime
            lastTime = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.allSprites, self.scaleFactor / 2)
                        self.active = True
                        self.startOffset = pygame.time.get_ticks()
                    
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.allSprites, self.collisionSprites], self.scaleFactor * 1.069)
                    

            self.allSprites.update(dt)
            self.allSprites.draw(self.display_surface)
            self.displayScore()
            
            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menuSurf, self.menuRect)
            pygame.display.update()
            self.clock.tick(framerate)

if __name__ == '__main__':
    game = Game()
    game.run()
