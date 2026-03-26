import pygame

pygame.init()

screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()

seaw3ed = pygame.image.load("seaw3ed.png").convert_alpha()
pygame.Surface.set_colorkey(seaw3ed, [255,0,255])

frameWidth = 100
frameHeight = 100
numFrames = 4

RowNum = 0

ticker = 0
frameNum = 0

xpos = 200
ypos = 125

running = True
while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
           
    ticker +=1
   
    if ticker % 12 == 0:
        frameNum +=2
       
        if frameNum >= numFrames:
            frameNum = 0
           
    screen.fill((0,0,0))
   
    screen.blit(seaw3ed, (xpos, ypos),
                (frameWidth * frameNum, RowNum * frameHeight, frameWidth, frameHeight))
   
    pygame.display.flip()
    clock.tick(60)

pygame.quit()