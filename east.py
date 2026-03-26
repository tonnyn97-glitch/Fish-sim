
# import pygame

# pygame.init()

# # Create a window
# screen = pygame.display.set_mode((640, 480))
# pygame.display.set_caption("Chest Example")

# # --- Class Definition ---
# class Chest:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.is_open = False

#         # Load images (make sure these files exist in your project folder)
#         self.image_closed = pygame.image.load("chest_closed.png.png").convert_alpha()
#         self.image_open = pygame.image.load("chest_open.png.png").convert_alpha()

#         # Optionally scale images to match width/height
#         self.image_closed = pygame.transform.scale(self.image_closed, (width, height))
#         self.image_open = pygame.transform.scale(self.image_open, (width, height))

#     def check_click(self, mouse_pos):
#         mx, my = mouse_pos
#         if (self.x < mx < self.x + self.width) and (self.y < my < self.y + self.height):
#             self.is_open = True

#     def toggle_closed(self):
#         self.is_open = False

#     def draw(self, screen):
#         if self.is_open:
#             screen.blit(self.image_open, (self.x, self.y))
#         else:
#             screen.blit(self.image_closed, (self.x, self.y))


# # Instantiate an object
# my_chest = Chest(240, 140, 115, 100)
# running = True

# # Main loop
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             my_chest.check_click(event.pos)

#         if event.type == pygame.MOUSEBUTTONUP:
#             my_chest.toggle_closed()

#     # Render
#     screen.fill((0, 0, 180))
#     my_chest.draw(screen)
#     pygame.display.flip()

# pygame.quit()
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

class Chest:
    def __init__(self, x, y):
        self.closed = pygame.image.load("chest_closed.png.png").convert_alpha()
        self.open   = pygame.image.load("chest_open.png.png").convert_alpha()
        self.rect   = self.closed.get_rect(topleft=(x, y))

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            screen.blit(self.open, self.rect)
        else:
            screen.blit(self.closed, self.rect)

my_chest = Chest(240, 140)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 180))
    my_chest.draw(screen)
    pygame.display.flip()

pygame.quit()