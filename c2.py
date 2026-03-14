import pygame
pygame.init()

SW, SH  = 800, 600 #screen width and height 
CANVAS  = 400# canvas size (square)
CX, CY  = (SW - CANVAS) // 2, 80# centering canvas, hardcoded y of canvas 
CELL    = 10# canvas pixel size
GRID    = CANVAS // CELL # number of cells in one row/column
SCALE   = 3
FPS     = 60

GREY   = ( 40,  40,  55)# grid lines and text
Highlight = ( 80, 200, 255)# highlight color for selected palette and canvas border

PALETTE = [# colors for user to choose from, 16 total
    (255,255,255),(180,180,180),( 80, 80, 80),(  0,  0,  0),
    (255, 60, 60),(255,160, 40),(255,220, 50),( 70,200, 70),
    ( 60,160,255),(120, 80,255),(220, 80,220),(255, 80,160),
    (255,180,100),(130, 80, 40),( 40,160,140),(255,220,180),
] 

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Draw Character")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("ariel", 14)


class DrawScreen:
    def __init__(self):
        self.grid   = [[None]*GRID for i in range(GRID)]#change   
        self.color  = (255, 255, 255)
        self.eraser = False
        self.held   = False

    def cell(self, mx, my):#mx, my mouse cordinates 
        rx, ry = mx - CX, my - CY
        if 0 <= rx < CANVAS and 0 <= ry < CANVAS:
            return rx // CELL, ry // CELL
        return None

    def to_surface(self):
        base = pygame.Surface((GRID, GRID), pygame.SRCALPHA)#could use convert_alpha() but would manullly need to set transperancy using surface.set_alpha(val) or some orther alternative , SRCALPHA is defualt transparnt
        for gy in range(GRID):
            for gx in range(GRID):
                if self.grid[gy][gx]:
                    base.set_at((gx, gy), self.grid[gy][gx])
        return pygame.transform.scale(base, (GRID*SCALE, GRID*SCALE))

    def has_pixels(self):
        return any(self.grid[y][x] for y in range(GRID) for x in range(GRID))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.held = True
            for i, col in enumerate(PALETTE):
                row, ci = divmod(i, 8)
                px = 20 + ci*36; py = SH - 80 + row*36
                if px <= event.pos[0] <= px+30 and py <= event.pos[1] <= py+30:
                    self.color  = col
                    self.eraser = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.held = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:     self.eraser = not self.eraser
            if event.key == pygame.K_c:     self.grid = [[None]*GRID for _ in range(GRID)]
            if event.key == pygame.K_RETURN and self.has_pixels(): return "play"

        return None

    def update(self):
        if self.held:
            cell = self.cell(*pygame.mouse.get_pos())
            if cell:
                gx, gy = cell
                self.grid[gy][gx] = None if self.eraser else self.color

    def draw(self, surf):
        surf.fill((18, 18, 28))
        pygame.draw.rect(surf, (10,10,18), (CX-1, CY-1, CANVAS+2, CANVAS+2))

        for gy in range(GRID):
            for gx in range(GRID):
                c = self.grid[gy][gx]
                if c:
                    pygame.draw.rect(surf, c, (CX+gx*CELL, CY+gy*CELL, CELL, CELL))

        for i in range(GRID+1):
            pygame.draw.line(surf, GREY, (CX+i*CELL, CY), (CX+i*CELL, CY+CANVAS))
            pygame.draw.line(surf, GREY, (CX, CY+i*CELL), (CX+CANVAS, CY+i*CELL))

        pygame.draw.rect(surf, Highlight, (CX-1, CY-1, CANVAS+2, CANVAS+2), 2)

        for i, col in enumerate(PALETTE):
            row, ci = divmod(i, 8)
            px = 20 + ci*36; py = SH - 80 + row*36
            pygame.draw.rect(surf, col, (px, py, 30, 30), border_radius=4)
            if col == self.color and not self.eraser:
                pygame.draw.rect(surf, Highlight, (px-2, py-2, 34, 34), 2, border_radius=5)

        mode = "ERASER" if self.eraser else "DRAW"
        surf.blit(font.render(f"[E] {mode}   [C] Clear   ENTER: Done", True, (120,140,180)), (20, SH-18))
        if self.has_pixels():
            s = font.render("ENTER to continue ", True, Highlight)
            surf.blit(s, (SW - s.get_width() - 20, SH-18))


class PlayScreen:
    def __init__(self, char_surf):
        self.char = char_surf
        self.x    = (SW - char_surf.get_width())  // 2
        self.y    = (SH - char_surf.get_height()) // 2

    def handle_event(self, event):
        return None

    def draw(self, surf):
        surf.fill((12, 12, 20))
        surf.blit(self.char, (self.x, self.y))


class App:
    def __init__(self):
        self.draw_screen = DrawScreen()
        self.play_screen = None
        self.mode = "draw"

    def run(self):
        while True:
            clock.tick(FPS)
            events = pygame.event.get()

            for ev in events:
                if ev.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    pygame.quit(); raise SystemExit

            if self.mode == "draw":
                for ev in events:
                    if self.draw_screen.handle_event(ev) == "play":
                        return self.draw_screen.to_surface()  # exit and send surface back
                self.draw_screen.update()
                self.draw_screen.draw(screen)

            pygame.display.flip()


#App().run()