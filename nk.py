import pygame
import random
import time
pygame.init()
screen = pygame.display.set_mode((800,600))#x,y
pygame.display.set_caption("Fish Simulator")
clock = pygame.time.Clock()

#Images
background_image = pygame.image.load('background_image.png').convert_alpha()
background_image2 = pygame.image.load('background_image2.png').convert_alpha()
shrimp_img = pygame.image.load("shrimp.png").convert_alpha()
fishImage = pygame.image.load("oct.png").convert_alpha()

bgx = 0 #background x variable for side scroller
bg_width = background_image.get_width()

def game_over_screen(screen, clock):
    font_big = pygame.font.SysFont("Arial", 72, bold=True)
    title = font_big.render("GAME OVER", True, (220, 40, 40))
    title1 = font_big.render("You died", True, (220, 40, 40))

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
           
        screen.fill((0, 20, 60))
        screen.blit(title, (400 - title.get_width() // 2, 220))
        screen.blit(title1, (400 - title1.get_width() // 2, 320))
        pygame.display.flip()

    pygame.quit()

def check_game_over(is_dead):
    if is_dead:
        game_over_screen(screen, clock)

class Fish:
    def __init__(self):
        self.fishImage = fishImage
        self.rect=fishImage.get_rect()
        self.rect= self.rect.inflate(-70,-70)
        pygame.Surface.set_colorkey (self.fishImage, [255,0,255])
        self.xpos = random.randint(0, 700)
        self.ypos = random.randint(0, 550)
        self.speed = 1
        self.die=False
        self.vx = 0
        self.vy = 0
        self.w = 50 #width
        self.h = 60 #height
        self.health = 118
        self.last_change_time = time.time() #grab starting time
        self.rect.topleft = (self.xpos, self.ypos)

    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.vx = 3
        elif keys[pygame.K_LEFT]:
            self.vx = -3
        else:
            self.vx = 0
            
        if keys[pygame.K_UP]:
            self.vy = -3
        elif keys[pygame.K_DOWN]:
            self.vy = 3
        else:
            self.vy = 0.1

        self.rect.x += self.vx
        self.rect.y += self.vy
       

        if self.rect.right > 800:
            self.rect.right=800

        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > 600:
             self.rect.bottom = 600 

        elif self.rect.top < 0:
            self.rect.top = 0

        self.xpos = self.rect.centerx - (self.fishImage.get_width() / 2)
        self.ypos = self.rect.centery - (self.fishImage.get_height() / 2)
        

      

    def draw(self, screen):
        screen.blit(self.fishImage, (self.xpos, self.ypos))
        pygame.draw.rect(screen, (245, 25, 21), self.rect, 2) #hitbox

        if self.health>118:
            self.health=118
        if self.health<0:
            self.die=True
        pygame.draw.rect(screen,(0, 255, 0), (self.xpos+35, self.ypos+40, self.health, 5))#healthbar
       
    def collide(self, FUD):
        #checks every food to see if the fish is colliding with it
        #if so, remove that food
        for food in FUD[:]:
             if self.rect.colliderect(food.rect):
                self.health += 5
                FUD.remove(food)
               
class Food():
    def __init__(self, shrimp_img):
        
        self.rect = shrimp_img.get_rect().inflate(-10, -10)
        self.rect.x = random.randint(810, 1100)
        self.rect.y = random.randint(10, 550)
        
    def move(self):
    
        self.rect.x-= 1
               
    def draw(self, screen, shrimp_img):
        screen.blit(shrimp_img, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
       
class bubble:
    def __init__(self, x, y):
        self.xpos = x
        self.ypos = y
        self.image = pygame.image.load("bubble.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image, (20, 20))

    def move(self):
        self.xpos += random.randrange(-2, 3)
        #self.ypos -= random.randrange(0, 3) if 0 not moving up
        self.ypos -= random.randrange(1, 3) # always moving up
        if self.ypos < 0:
            #self.ypos = random.randrange(500, 700)
            self.ypos = random.randrange(610, 700)# you want bubbles to reset bwlow screen 500 is on screen, screen is 600 px long
            # i cant run the the code cuz i dont have the images but might want to change x pos too to make it more random

    def draw(self, screen):
        #screen.blit(self.image, (self.xpos, self.ypos))#
        screen.blit(self.image2, (self.xpos, self.ypos))# use transformw image not old one


# instantiate a fish object
fish = Fish()
food = []
ticker = 0
flakeBag = []
for i in range(50):
    #flakeBag.append(bubble(random.randrange(0, 500), random.randrange(-500, 0)))# if game slow i might know why, ps this line is why
    flakeBag.append(bubble(random.randrange(0, 800), random.randrange(600, 1000)))# SCRREN IS 800 WIDE 500 TOO NARROW OF RANGE,
    #REMBER NEGATIVES ARE ABOVE SCREEN WE WANT TO SPAWN BUBBLES BELOW SCREEN


running = True
while running:# Game loop########################################################
    clock.tick(60)
    #input/event section-----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #physics/update section--------------------------
    keys = pygame.key.get_pressed() #get input
    fish.move(keys)
    fish.collide(food)
    bgx -= 2
    if bgx <= -bg_width:
        bgx = 0
   

    #spawn food every 60 ticks
    ticker += 1
    if ticker % 60 == 0: #change 60 for more or less spawning
        fish.health-=10
        food.append(Food(shrimp_img)) #create food
        ticker = 0 #reset ticker
    '''  
    for i in range(len(food)):
        food[i].move()
    for i in range(len(flakeBag)):
        flakeBag[i].move()
        flakeBag[i].draw(screen)
    ''' #not drawing becuse not in render section
   
    #render section----------------------------------
    # Fill the screen with a background color
    screen.fill((0, 150, 255))

    # Draw the fish
    screen.blit(background_image, (bgx,0))
    screen.blit(background_image2, (bgx + bg_width,0))
    fish.draw(screen)
    for i in range(len(food)):
        food[i].draw(screen,shrimp_img)
   
    for i in range(len(food)):
        food[i].move()
    for i in range(len(flakeBag)):
        flakeBag[i].move()
        flakeBag[i].draw(screen)#MOVED TO RENDER
       
    # Update the display
    check_game_over(fish.die)
    pygame.display.flip()

    #end of game loop!#######################################################

pygame.quit()