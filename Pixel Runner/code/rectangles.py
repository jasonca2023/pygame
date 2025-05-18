import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()

test_font = pygame.font.Font('Fonts/slkscr.ttf', 50)

sky_surface = pygame.image.load('graphics/sky.jpeg').convert()
ground_surface = pygame.image.load('graphics/terrain_7.png').convert()
text_surface = test_font.render('My game', False, 'Black')

snail_surface = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 320))

player_surface = pygame.image.load('graphics/character/character_walk_1.png')
player_rect = player_surface.get_rect(midbottom = (50, 305))
                                      
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (-5, 300))
    screen.blit(text_surface, (290, 10))

    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
        
    screen.blit(snail_surface, snail_rect)
    
    screen.blit(player_surface, player_rect)
            
    pygame.display.update()
    clock.tick(60)

