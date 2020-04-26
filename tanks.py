import pygame
import os

pygame.init()
size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tanks')
pygame.mixer.init()

hit_sound = pygame.mixer.Sound(os.path.join('hit.wav'))
shoot_sound = pygame.mixer.Sound(os.path.join('shoot.wav'))
hit_sound.set_volume(0.1)
shoot_sound.set_volume(0.1)

fps = 20
obj_size = (25, 25)

tank1_part = pygame.Surface(obj_size)
tank1_part.fill((0, 0, 200))

tank2_part = pygame.Surface(obj_size)
tank2_part.fill((200, 0, 0))

bullet = pygame.Surface((5, 5))
bullet.fill((0, 0, 0))

clock = pygame.time.Clock()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Tank:
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.hp = 3
        
    def move(self, speed):
        if self.direction == UP:
            self.y -= int(speed / fps)
        elif self.direction == DOWN:
            self.y += int(speed / fps)
        elif self.direction == RIGHT:
            self.x -= int(speed / fps)
        elif self.direction == LEFT:
            self.x += int(speed / fps)


class Bullet:
    
    def __init__(self):
        self.x = 1000
        self.y = 1000
        self.direction = UP
        self.is_moving = False
        
    def move(self, speed):
        if self.direction == UP:
            self.y -= int(speed / fps)
        elif self.direction == DOWN:
            self.y += int(speed / fps)
        elif self.direction == RIGHT:
            self.x -= int(speed / fps)
        elif self.direction == LEFT:
            self.x += int(speed / fps)  
            
    def check(self, tank):
        if self.x > tank.x and self.x < tank.x + obj_size[0] and self.y > tank.y and self.y < tank.y + obj_size[1]:
            hit_sound.play()
            tank.hp -= 1
            self.is_moving = False
            self.x = 1000
            self.y = 1000
        


font = pygame.font.Font('freesansbold.ttf', 18)

game_over = False

tank1 = Tank(1, 1, DOWN)
bullet1 = Bullet()

tank2 = Tank(size[0] - 26, 1, DOWN)
bullet2 = Bullet()

winner = ''

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_w and tank1.direction != DOWN:
                tank1.direction = UP
            if event.key == pygame.K_s and tank1.direction != UP:
                tank1.direction = DOWN
            if event.key == pygame.K_d and tank1.direction != RIGHT:
                tank1.direction = LEFT
            if event.key == pygame.K_a and tank1.direction != LEFT:
                tank1.direction = RIGHT
            if event.key == pygame.K_RETURN and bullet1.is_moving == False:
                shoot_sound.play()
                bullet1.is_moving = True
                bullet1.x = tank1.x + 10
                bullet1.y = tank1.y + 10
                bullet1.direction = tank1.direction
                
                
            if event.key == pygame.K_UP and tank2.direction != DOWN:
                tank2.direction = UP
            if event.key == pygame.K_DOWN and tank2.direction != UP:
                tank2.direction = DOWN
            if event.key == pygame.K_LEFT and tank2.direction != RIGHT:
                tank2.direction = RIGHT
            if event.key == pygame.K_RIGHT and tank2.direction != LEFT:
                tank2.direction = LEFT
            if event.key == pygame.K_SPACE and bullet2.is_moving == False:
                shoot_sound.play()
                bullet2.is_moving = True
                bullet2.x = tank2.x + 10
                bullet2.y = tank2.y + 10
                bullet2.direction = tank2.direction            
      
    tank1.move(80)
    tank2.move(80)
      
    if tank1.x + 12 >= size[0]:
        tank1.x = 0
    if tank1.y + 12 >= size[1]: 
        tank1.y = 0
    if tank1.x + 12 < 0:
        tank1.x = size[0] - 13
    if tank1.y + 12 < 0:
        tank1.y = size[1] - 13
        
    if tank2.x + 12 >= size[0]:
        tank2.x = 0
    if tank2.y + 12 >= size[1]: 
        tank2.y = 0
    if tank2.x + 12 < 0:
        tank2.x = size[0] - 13
    if tank2.y + 12 < 0:
        tank2.y = size[1] - 13   
        
    if bullet1.x >= size[0] or bullet1.y >= size[1] or bullet1.x < 0 or bullet1.y < 0:
        bullet1.x = 1000
        bullet1.y = 1000
        bullet1.is_moving = False
    
    if bullet1.is_moving:
        bullet1.move(120)
        bullet1.check(tank2)
        
    if bullet2.x >= size[0] or bullet2.y >= size[1] or bullet2.x < 0 or bullet2.y < 0:
        bullet2.x = 1000
        bullet2.y = 1000
        bullet2.is_moving = False
    
    if bullet2.is_moving:
        bullet2.move(120)  
        bullet2.check(tank1)
    
    tank1_hp = font.render('HP: ' + str(tank1.hp), True, (0, 0, 255))
    tank2_hp = font.render('HP: ' + str(tank2.hp), True, (255, 0, 0))
    
    if tank1.hp <= 0 or tank2.hp <= 0:
        if tank1.hp <= 0 and winner == '':
            winner = font.render('PLAYER2 wins!!!', True, (255, 0, 0))
            tank1_hp = font.render('HP: 0', True, (0, 0, 255))
        elif winner == '':
            winner = font.render('PLAYER1 wins!!!', True, (0, 0, 255))
            tank2_hp = font.render('HP: 0', True, (255, 0, 0)) 
        screen.fill((255, 255, 255))
        screen.blit(tank2_hp, (size[0] - 50, 2))
        screen.blit(tank1_hp, (2, 2))
        screen.blit(winner, (120, 180))
        pygame.display.flip()
        pygame.time.wait(5000)
        game_over = True
    else:
        clock.tick(fps)
        screen.fill((255, 255, 255))
        screen.blit(tank1_part, (tank1.x, tank1.y))
        screen.blit(bullet, (bullet1.x, bullet1.y))
        screen.blit(tank2_part, (tank2.x, tank2.y))
        screen.blit(bullet, (bullet2.x, bullet2.y))
        screen.blit(tank1_hp, (2, 2))
        screen.blit(tank2_hp, (size[0] - 50, 2))
        pygame.display.flip()
    
pygame.quit()