import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def update(self):
        self.player_input()
        self.apply_gravity()


def display_score():

    current_time = int(pygame.time.get_ticks()/1000  ) - start_time
    score_surface = test_font.render(f'{current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5
            if obstacle_rectangle.bottom == 300:
                screen.blit(snail_surface,obstacle_rectangle)
            else:
                screen.blit(fly_surface,obstacle_rectangle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]       
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle):
                return False
    return True

def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf",50)
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_surface = test_font.render("My game", False, (64,64,64))
# score_rect = score_surface.get_rect(center = (400,50))

#obstacles
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []


#player
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

#intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_name = test_font.render("IQ Test",False, (111,196,169))
game_name_rectangle = game_name.get_rect(center = (400,80))

game_message = test_font.render("Press space to run",False,(111,196,169))
game_message_rectangle = game_message.get_rect(center = (400,320))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
        if game_active: 
            if event.type == obstacle_timer:
                if randint(0,1):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1100),210)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]



    if game_active:
        screen.blit(ground_surface,(0,300))
        screen.blit(sky_surface,(0,0))
        # pygame.draw.rect(screen,"#c0e8ec",score_rect)
        # pygame.draw.rect(screen,"#c0e8ec",score_rect,20)
        # screen.blit(score_surface,score_rect)
        score = display_score()

        
        # snail_rectangle.x -= 4
        # if snail_rectangle.right < 0:
        #     snail_rectangle.left = 800
        # screen.blit(snail_surface,snail_rectangle)
        
        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom>=300:
            player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface,player_rectangle)
        player.draw(screen)
        player.update()
    

        #collisions
        game_active = collisions(player_rectangle,obstacle_rect_list)
        
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rectangle)
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0
        
        score_message = test_font.render(f"Your score: {score}",False,(111,196,169))
        score_message_rectangle = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rectangle)
        if score == 0:
            screen.blit(game_message,game_message_rectangle)
        else:
            screen.blit(score_message,score_message_rectangle)


    # keys = pygame.key.get_pressed() 
    # keys[pygame.K_SPACE]:
    #if player_rectangle.colliderect(snail_rectangle):
     #   print("collision")         
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rectangle.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())
        

    #draw all elements
    pygame.display.update()
    clock.tick(60)