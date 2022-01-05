import pygame
from PIL import Image
from data import screen
import math
import random
import time

class enemyObj(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.screenData = screen()

        #Random coordinates for where they spawn
        self.x = random.randint(math.floor(self.screenData.width/100), self.screenData.width-math.floor(self.screenData.width/50))
        self.y = random.randint(math.floor(self.screenData.height/100), self.screenData.height-math.floor(self.screenData.height/4))
        
        #Sets the image and scales it
        self.length, self.height = Image.open(img).size
        self.length, self.height = self.length*5, self.height*5
        self.current_sprite = 0
        self.sprites = [pygame.transform.scale(pygame.image.load(img), (self.length, self.height))]
        for i in range(1,8):
            frame = pygame.image.load(f'assets/donut/defeated/Donut_Shot_Animated-{i}.png')
            self.sprites.append(pygame.transform.scale(frame, (self.length, self.height)))
        
        self.animation_speed = 0.045

        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        

        
        
        #Affects how fast the sprite moves
        self.deltaX = 1.5
        self.deltaY = -1.5 # TODO 1.5 and -1.5
        
        #Health
        self.health = 1
        self.alive = True
    
    def update(self, win):
        self.draw(win)
        self.image = self.sprites[int(self.current_sprite)]
        if self.health < 1:
            self.current_sprite += self.animation_speed
            if self.current_sprite > 7:
                self.alive = False

    def move(self):
        # If the enemy is touching the left or right border
        if self.x >= self.screenData.width - math.floor(self.screenData.width/100) or self.x <= 0 + math.floor(self.screenData.width/100):
            self.deltaX *= -1
        # If the enemy is touching the top or bottom border
        if self.y >= self.screenData.height - math.floor(self.screenData.height/4) or self.y <= 0:
            self.deltaY *= -1
        self.x += self.deltaX
        self.y += self.deltaY

    # displays the image of the sprite
    def draw(self, win):
        self.move()
        win.blit(self.image, (self.x, self.y))

    def stop(self):
        self.deltaX = 0
        self.deltaY = 0


    def shot(self, win):
        self.stop()
        self.health -= 1

    # If the enemy is clicked
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)