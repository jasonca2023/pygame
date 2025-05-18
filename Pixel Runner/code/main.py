import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time 
    
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (410, 50))
    
    screen.blit(score_surface, score_rect)

    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom > 305:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else:
        return []
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()

test_font = pygame.font.Font('../fonts/slkscr.ttf', 50)

game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('../sound/chill.wav')
bg_music.play(loops = -1)


sky_surface = pygame.image.load('../graphics/sky.jpeg').convert()
ground_surface = pygame.image.load('../graphics/terrain_7.png').convert()

snail_surface = pygame.image.load('../graphics/snail1.png').convert_alpha()

fly_surface = pygame.image.load('../graphics/fly1.png').convert_alpha()

obstacle_rect_list = []

player_surface = pygame.image.load('../graphics/character/character_walk_1.png')
player_rect = player_surface.get_rect(midbottom = (50, 305))
player_gravity = 0

player_stand = pygame.image.load('../graphics/character/character_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 50))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 330))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
                                      
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:    
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -25

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -25

        else:
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                     game_active = True
                     start_time = int(pygame.time.get_ticks() / 100)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                snail_rect = snail_surface.get_rect(bottomright = (randint(2000, 2200), 320))
                obstacle_rect_list.append(snail_rect)
            else:
                fly_rect = fly_surface.get_rect(bottomright = (randint(2000, 2200), 190))
                obstacle_rect_list.append(fly_rect)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (-5, 300))
        
        score = display_score()

        snail_rect = snail_surface.get_rect(bottomright = (randint(2000, 2200), 320))
        screen.blit(snail_surface, snail_rect)

        player_gravity += 1
        player_rect.y += player_gravity
    
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        
        screen.blit(player_surface, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_rect, obstacle_rect_list)
            
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        obstacle_rect_list.clear()
        
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
