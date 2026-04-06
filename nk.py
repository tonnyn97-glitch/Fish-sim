import pygame
import random
import time
pygame.init()
SW, SH = 1300, 700
screen = pygame.display.set_mode((SW,SH))#x,y
pygame.display.set_caption("Fish Simulator")
clock = pygame.time.Clock()

#Images
background_image = pygame.transform.scale(pygame.image.load('background_image.png').convert_alpha(), (SW, SH))
background_image2 = pygame.transform.scale(pygame.image.load('background_image2.png').convert_alpha(), (SW, SH))
shrimp_img = pygame.image.load("shrimp.png").convert_alpha()
fishImage = pygame.image.load("oct.png").convert_alpha()
FISH_SCALE = .5  # change this number to resize fish and have same scale
fishImage = pygame.transform.scale(fishImage, (int(fishImage.get_width() * FISH_SCALE), int(fishImage.get_height() * FISH_SCALE)))
seaweed_img = pygame.image.load("seaw3ed.png").convert_alpha()
pygame.Surface.set_colorkey(seaweed_img, [255, 0, 255])
bgx = 0 #background x variable for side scroller
bg_width = background_image.get_width()
chest_closed_img = pygame.image.load("chest_closed.png.png").convert_alpha()
chest_open_img   = pygame.image.load("chest_open.png.png").convert_alpha()
CELL  = 10
GRID  = 40
SCALE = 3
CX, CY = 200, 80

PALETTE = [
    (255,255,255),(180,180,180),(80,80,80),(0,0,0),
    (255,60,60),(255,160,40),(255,220,50),(70,200,70),
    (60,160,255),(120,80,255),(220,80,220),(255,80,160),
] #color list

class CharCreator:
    def __init__(self):
        self.grid  = [[None]*GRID for _ in range(GRID)]
        self.color = (255, 255, 255)
        self.held  = False

    def get_cell(self, mx, my):
        rx, ry = mx - CX, my - CY
        if 0 <= rx < GRID*CELL and 0 <= ry < GRID*CELL:
            return rx // CELL, ry // CELL
        return None

    def to_surface(self):
        surf = pygame.Surface((GRID, GRID), pygame.SRCALPHA)
        for y in range(GRID):
            for x in range(GRID):
                if self.grid[y][x]:
                    surf.set_at((x, y), self.grid[y][x])
        return pygame.transform.scale(surf, (GRID*SCALE, GRID*SCALE))

    def update(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.held = True
                for i, col in enumerate(PALETTE):#gives item and its index
                    px = 20 + (i % 6) * 36
                    py = 500 + (i // 6) * 36
                    if px <= e.pos[0] <= px+30 and py <= e.pos[1] <= py+30:
                        self.color = col
            if e.type == pygame.MOUSEBUTTONUP:
                self.held = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return self.to_surface()

        if self.held:
            cell = self.get_cell(*pygame.mouse.get_pos())
            if cell:
                self.grid[cell[1]][cell[0]] = self.color
        return None

    def draw(self):
        screen.fill((18, 18, 28))
        for y in range(GRID):
            for x in range(GRID):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x],
                                     (CX+x*CELL, CY+y*CELL, CELL, CELL))
        for i in range(GRID+1):
            pygame.draw.line(screen, (40,40,55), (CX+i*CELL, CY), (CX+i*CELL, CY+GRID*CELL))
            pygame.draw.line(screen, (40,40,55), (CX, CY+i*CELL), (CX+GRID*CELL, CY+i*CELL))
        pygame.draw.rect(screen, (80,200,255), (CX-1, CY-1, GRID*CELL+2, GRID*CELL+2), 2)

        for i, col in enumerate(PALETTE):
            px = 20 + (i % 6) * 36
            py = 500 + (i // 6) * 36
            pygame.draw.rect(screen, col, (px, py, 30, 30), border_radius=4)
            if col == self.color:
                pygame.draw.rect(screen, (80,200,255), (px-2, py-2, 34, 34), 2)

        font = pygame.font.SysFont("Arial", 16)
        screen.blit(font.render("Draw your enemy ENTER when done", True, (80,200,255)), (CX, 50))
        pygame.display.flip()

class Enemy:
    def __init__(self, surf):
        self.image = surf
        self.rect  = surf.get_rect(topleft=(SW+20, random.randint(50, SH-150)))

    def update(self):
        self.rect.x -= 3  # move left toward player

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_offscreen(self):
        return self.rect.right < 0
    
def run_creator():
    creator = CharCreator()
    while True:
        clock.tick(60)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
        result = creator.update(events)
        creator.draw()
        if result:
            return result
class Chest:
    def __init__(self, x):
        self.closed = pygame.transform.scale(chest_closed_img, (220, 200))  # width, height
        self.open   = pygame.transform.scale(chest_open_img,   (220, 200))
        self.rect   = self.closed.get_rect(topleft=(x,SH-210))  # sits on floor
        self.xpos   = x

    def update(self):
        self.rect.x -= 2  # scroll with background

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            screen.blit(self.open, self.rect)
        else:
            screen.blit(self.closed, self.rect)

    def is_offscreen(self):
        return self.rect.right < 0
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

class Seaweed:
    def __init__(self, x, y, seaweed_img):
        self.xpos = x
        self.ypos = y
        self.seaweed_img = seaweed_img
        self.frameWidth = 100
        self.frameHeight = 100
        self.numFrames = 4
        self.rowNum = 0
        self.frameNum = 0
        self.ticker = 0

    def update(self):
        # Animate frames
        self.ticker += 1
        if self.ticker % 12 == 0:
            self.frameNum += 2
            if self.frameNum >= self.numFrames:
                self.frameNum = 0

        # Scroll left with background (match bgx speed of -2)
        self.xpos -= 1

    def draw(self, screen):
        screen.blit(self.seaweed_img, (self.xpos, self.ypos),
                    (self.frameWidth * self.frameNum, self.rowNum * self.frameHeight,
                     self.frameWidth, self.frameHeight))

    def is_offscreen(self):
        return self.xpos < -self.frameWidth  # True once fully past left edge

class Fish:
    def __init__(self):
        self.fishImage = fishImage
        self.rect = fishImage.get_rect()
        self.rect = self.rect.inflate(-int(70 * FISH_SCALE), -int(70 * FISH_SCALE))
        pygame.Surface.set_colorkey(self.fishImage, [255, 0, 255])
        self.xpos = random.randint(0, SW - fishImage.get_width())
        self.ypos = random.randint(0, SH - fishImage.get_height())
        self.die = False
        self.vx = 0
        self.vy = 0
        self.health = self.rect.width  # healthbar width = hitbox width, scales automatically
        self.max_health = self.rect.width
        self.last_change_time = time.time()
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
       

        if self.rect.right > SW:
            self.rect.right=SW

        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > SH:
             self.rect.bottom = SH 

        elif self.rect.top < 0:
            self.rect.top = 0

        self.xpos = self.rect.centerx - (self.fishImage.get_width() / 2)
        self.ypos = self.rect.centery - (self.fishImage.get_height() / 2)


    def draw(self, screen):
        screen.blit(self.fishImage, (self.xpos, self.ypos))

        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.die = True

        # healthbar offset scales with fish size
        bar_x = self.rect.left
        bar_y = self.rect.bottom + 4
        pygame.draw.rect(screen, (80, 0, 0),   (bar_x, bar_y, self.max_health, int(6 * FISH_SCALE)))
        pygame.draw.rect(screen, (0, 255, 0),  (bar_x, bar_y, self.health,     int(6 * FISH_SCALE)))
    def collide(self, FUD):
        #checks every food to see if the fish is colliding with it
        #if so, remove that food
        for food in FUD[:]:
             if self.rect.colliderect(food.rect):
                self.health += 20
                FUD.remove(food)
               
class Food():
    def __init__(self, shrimp_img):
        
        self.rect = shrimp_img.get_rect().inflate(-10, -10)
        self.rect.x = random.randint(SW+10, SW+500)
        self.rect.y = random.randint(10, SH-self.rect.height)
        
    def move(self):
    
        self.rect.x-= 1
               
    def draw(self, screen, shrimp_img):
        screen.blit(shrimp_img, self.rect)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
       
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
            self.ypos = random.randrange(SH+10, SH+120)# you want bubbles to reset bwlow screen 500 is on screen, screen is SH px long
            # i cant run the the code cuz i dont have the images but might want to change x pos too to make it more random

    def draw(self, screen):
        #screen.blit(self.image, (self.xpos, self.ypos))#
        screen.blit(self.image2, (self.xpos, self.ypos))# use transformw image not old one


# instantiate a fish object

food = []
ticker = 0
flakeBag = []
for i in range(1000):
    #flakeBag.append(bubble(random.randrange(0, 500), random.randrange(-500, 0)))# if game slow i might know why, ps this line is why
    flakeBag.append(bubble(random.randrange(0, SW), random.randrange(0, SH+300)))# SCRREN IS SW WIDE 500 TOO NARROW OF RANGE,
    #REMBER NEGATIVES ARE ABOVE SCREEN WE WANT TO SPAWN BUBBLES BELOW SCREEN

SPACING = 120
GROUND_Y = SH-100#tie seaweed to realtive ground
seaweed_list = [Seaweed(i * SPACING, GROUND_Y, seaweed_img) for i in range(SW // SPACING + 1)]
chest_list = []
last_chest_time = time.time()
enemy_surf     = run_creator()   # draw the enemy in character creator
enemy_list     = []
last_enemy_time = time.time()
fish = Fish()
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
    bgx -= 1
    if bgx <= -bg_width:
        bgx = 0
   
   #############
   # spawn enemy every 2 seconds
    if time.time() - last_enemy_time >= 2:
        enemy_list.append(Enemy(enemy_surf))
        last_enemy_time = time.time()

    # update and cull offscreen enemies
    enemy_list = [e for e in enemy_list if not e.is_offscreen()]
    for e in enemy_list:
        e.update()

    # check collision with fish
    for e in enemy_list[:]:
        if fish.rect.colliderect(e.rect):
            fish.health -= 10
            enemy_list.remove(e)

   ################

    #spawn food every 60 ticks
    ticker += 1
    if ticker % 60 == 0: #change 60 for more or less spawning
        fish.health-=2
        food.append(Food(shrimp_img)) #create food
        ticker = 0 #reset ticker
    
    seaweed_list = [sw for sw in seaweed_list if not sw.is_offscreen()]
    for sw in seaweed_list:
        sw.update()
    if len(seaweed_list) == 0 or seaweed_list[-1].xpos <= SW - SPACING:
        seaweed_list.append(Seaweed(SW, GROUND_Y, seaweed_img))
    
        # spawn a chest every 10 seconds
    if time.time() - last_chest_time >= 10:
        chest_list.append(Chest(SW+20))
        last_chest_time = time.time()

    chest_list = [c for c in chest_list if not c.is_offscreen()]
    for c in chest_list:
        c.update()

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
    screen.blit(background_image, (bgx, 0))
    screen.blit(background_image2, (bgx + bg_width, 0))

    for c in chest_list:      # behind seaweed
        c.draw(screen)
    # for sw in seaweed_list:   # in front of chest
    #     sw.draw(screen)
    for e in enemy_list:
        e.draw(screen) 
    fish.draw(screen)         # fish on top

    for i in range(len(food)):
        food[i].draw(screen,shrimp_img)
   
    for i in range(len(food)):
        food[i].move()
    for i in range(len(flakeBag)):
        flakeBag[i].move()
        flakeBag[i].draw(screen)#MOVED TO RENDER
    for sw in seaweed_list:
        sw.draw(screen)
    # Update the display
    check_game_over(fish.die)
    pygame.display.flip()

    #end of game loop!#######################################################

pygame.quit()