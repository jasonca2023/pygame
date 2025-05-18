import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
        
        bgImage = pygame.image.load('/Users/jasonca2/Documents/Pygame/Flappy bird/graphics/background.png').convert()

        fullHeight = bgImage.get_height() * scaleFactor
        fullWidth = bgImage.get_width() * scaleFactor
        fullSizedImage = pygame.transform.scale(bgImage, (fullWidth, fullHeight))

        self.image = pygame.Surface((fullWidth * 2, fullHeight))
        self.image.blit(fullSizedImage, (0, 0))
        self.image.blit(fullSizedImage, (fullWidth, 0))
        
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)

        self.sprite_type = 'ground'
        
        groundSurf = pygame.image.load('/Users/jasonca2/Documents/Pygame/Flappy bird/graphics/ground.png').convert_alpha()
        fullSizeImage = pygame.transform.scale(groundSurf, pygame.math.Vector2(groundSurf.get_size()) * scaleFactor)

        self.image = pygame.Surface((fullSizeImage.get_width() * 2, fullSizeImage.get_height()), pygame.SRCALPHA)
        self.image.blit(fullSizeImage, (0, 0))
        self.image.blit(fullSizeImage, (fullSizeImage.get_width(), 0))
        
        self.rect = self.image.get_rect(bottomleft = (0, 800))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)        

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
            
class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)

        self.import_frames(scaleFactor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(midleft = (windowWidth / 20, windowHeight / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.gravity = 2000
        self.direction = 0

        self.mask = pygame.mask.from_surface(self.image)

        self.jumpSound = pygame.mixer.Sound('/Users/jasonca2/Documents/Pygame/Flappy bird/sound/jump.wav')
        self.jumpSound.set_volume(0.05)
        
    def import_frames(self, scaleFactor):
        self.frames = []
        for i in range(2):
            surf = pygame.image.load(f'/Users/jasonca2/Documents/Pygame/Flappy bird/graphics/plane{i}.png').convert_alpha()
            scaledSurface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scaleFactor)
            self.frames.append(scaledSurface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jumpSound.play()
        self.direction = -400

    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotatedPlane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotatedPlane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)

        self.sprite_type = 'obstacle'

        orientation = choice(('up', 'down'))
        surf = pygame.image.load(f'/Users/jasonca2/Documents/Pygame/Flappy bird/graphics/obstacles/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scaleFactor)

        x = windowWidth + randint(40, 100)
        
        if orientation == 'up':
            y = windowHeight + randint(10, 50)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
