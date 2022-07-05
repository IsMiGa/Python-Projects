# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:39:17 2022

@author: isalo
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 12:07:46 2022

@author: isalo
"""

import pygame
import random
import os

#INITIALIZATION
pygame.init()

#PRINCIPAL LOOP
def principal():
    global game_over, running, mobs, bullets, all_sprites, nave, counter
    while running == True:
        if game_over == True:
            show_go_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            nave = Nave()
            all_sprites.add(nave)
            counter = 0
            for i in range(8):
                new_mob()
            
        screen.fill(BLACK)
        screen.blit(background, (0,0))
        all_sprites.draw(screen)
        bar(screen, 280, 10, nave.shield)
        all_sprites.update()
        score(counter)
        pygame.display.flip()        
            
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
             
   
    pygame.quit()   
    

#GENERAL VALUES
WIDTH = 400
HEIGHT = 500
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
counter = 0
font = pygame.font.SysFont('Arial Black', 20)

#SCREEN AND CLOCK
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTER")
clock = pygame.time.Clock()

#IMAGES
code_folder = os.path.dirname(__file__)

#IMAGE FOLDER 
img_folder = os.path.join(code_folder, 'SPRITES')

#SOUND FOLDER AND SOUND EFFECTS
snd_folder = os.path.join(code_folder, 'AUDIO')
shot = pygame.mixer.Sound(os.path.join(snd_folder, 'misil.wav'))
explosion = pygame.mixer.Sound(os.path.join(snd_folder, 'explosion.wav'))

#SPACESHIP
nave_espacial = pygame.image.load(os.path.join(img_folder, 'ship.png'))

#MOBS
asteroide = pygame.image.load(os.path.join(img_folder, 'asteroide.png'))
asteroide = pygame.transform.scale(asteroide,(60,60))

#MISSIL
misil = pygame.image.load(os.path.join(img_folder, 'misil.png'))

#BACKGROUND
background = pygame.image.load(os.path.join(img_folder, 'starfield.png'))
background = pygame.transform.scale(background, (400,500))

#EXPLOSION IMAGES 
explosiones = {}
explosiones['sz'] = []
explosiones['nave'] = []
for i in range(0,8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename))
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (60,60))
    explosiones['sz'].append(img)
    #EXPLOSION OF THE SHIP
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename))
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (65,65))
    explosiones['nave'].append(img)
    
    
#SPRITE CREATION
#SPACESHIP SPRITE
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = nave_espacial
        self.radius = 20
        self.rect = self.image.get_rect()
        self.shield = 100
        #pygame.draw.circle(self.image, RED, self.rect.center, 20)
        lugar = (int(WIDTH/2), int(HEIGHT-30))
        self.rect.center = lugar
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        
    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.x > 20:
            self.rect.x -= 7
        if teclas[pygame.K_RIGHT] and self.rect.right < WIDTH - 20:
            self.rect.x += 7
        if teclas[pygame.K_DOWN] and self.rect.bottom < HEIGHT - 20:
            self.rect.y += 7
        if teclas[pygame.K_UP] and self.rect.y > 20:
            self.rect.y -= 7
        if teclas[pygame.K_a]:
            self.shoot_timing()   

    def shoot_timing(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shot = now
            misiles = Misil(self.rect.midtop)
            shot.play()
            all_sprites.add(misiles)
            bullets.add(misiles)     
            
                          
#MISSIL SPRITE        
class Misil(pygame.sprite.Sprite):           
    def __init__(self, y):            
        pygame.sprite.Sprite.__init__(self)
        self.image = misil
        self.rect = self.image.get_rect()
        self.rect.midbottom = y
        self.radius = 15
        
    
    def update(self):
        self.rect.y -= 7
        if self.rect.bottom < 0:
            self.kill()
        colision = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
        for key in colision.keys():
            explosion.play()
            global counter
            counter += 1
            expl = Explosions(key.rect.center, 'sz' )
            all_sprites.add(expl)
            new_mob()
            score(counter)
            
            
#MOBS SPRITE         
class Asteroides(pygame.sprite.Sprite):
     def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = asteroide
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randint(20 , int(WIDTH -20))
        self.rect.centery = random.randint(0 , int(HEIGHT - 350)) 
        self.rot = 0
        self.rot_speed = random.randint(-8,8)
        self.last = pygame.time.get_ticks()
        
        
     def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last > 50:
            self.last = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
     def update(self):
            self.rotate() 
            self.rect.centery += 5
            if self.rect.top > HEIGHT:
                self.rect.centerx = random.randint(20 , int(WIDTH - 20))
                self.rect.centery = random.randint(0 , int(HEIGHT - 370))
            choques = pygame.sprite.spritecollide(nave, mobs, True, pygame.sprite.collide_circle)
            for choque in choques:
                explosion.play()
                expl = Explosions(choque.rect.center, 'sz')
                all_sprites.add(expl)
                nave.shield -= choque.radius * 2
                new_mob()
                if nave.shield <= 0:
                    finish = Explosions(nave.rect.center, 'nave')
                    all_sprites.add(finish)
                    nave.kill()


#EXPLOSIONS SPRITE 
class Explosions(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosiones[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
       now = pygame.time.get_ticks()
       if now - self.last_update > self.frame_rate:
           self.last_update = now
           self.frame += 1
           if self.frame == len(explosiones[self.size]):
               self.kill()
               #MAKE SURE THE SHIP IS DEAD, THEN SHOW PRINCIPAL SCREEN
               if not nave.alive():
                   global game_over
                   game_over = True
           else:
               center = self.rect.center
               self.image = explosiones[self.size][self.frame]
               self.rect = self.image.get_rect()
               self.rect.center = center  
               
               
#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

#SPACE SHIP SPRITE INITIALIZATION
nave = Nave()
all_sprites.add(nave)


#VARIOUS DEFINITIONS
def new_mob():
    m = Asteroides()
    mobs.add(m)
    all_sprites.add(m)
    
for i in range(8):
    new_mob()

def score(counter):    
    text_surface = font.render(f'HITS: {counter}', True, (255,255,255))
    screen.blit(text_surface, (10,5))
    
def bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    inner_rect = pygame.Rect(int(x), int(y), int(fill), int(bar_height))    
    pygame.draw.rect(surf, GREEN, inner_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def show_go_screen():
    screen.blit(background, (0,0))
    text_surface = font.render('SPACE SHOOTER', True, (255,255,255))
    text_instructions = font.render('Arrow keys to move, A to shoot', True, (255,255,255))
    text_start = font.render('Press any key to begin', True, (255,255,255))
    screen.blit(text_surface, (int((WIDTH/4)),int((HEIGHT/5))))
    screen.blit(text_instructions, (int((WIDTH/12)), int((HEIGHT/3))))
    screen.blit(text_start, (int((WIDTH/5)), int((HEIGHT/2))))
    pygame.display.flip()
    waiting = True
    while waiting == True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
    
    
    
#CALLING THE PRINCIPAL LOOP
game_over = True
running = True
principal()