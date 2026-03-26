import pygame
pygame.init()

SW, SH = 800, 600
CELL   = 10
GRID   = 40
SCALE  = 3
CX, CY = 200, 80

PALETTE = [
    (255,255,255),(180,180,180),(80,80,80),(0,0,0),
    (255,60,60),(255,160,40),(255,220,50),(70,200,70),
    (60,160,255),(120,80,255),(220,80,220),(255,80,160),
]

screen = pygame.display.set_mode((SW, SH))
clock  = pygame.time.Clock()

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
                for i, col in enumerate(PALETTE):
                    px = 20 + (i % 6) * 36
                    py = SH - 80 + (i // 6) * 36
                    if px <= e.pos[0] <= px+30 and py <= e.pos[1] <= py+30:
                        self.color = col
            if e.type == pygame.MOUSEBUTTONUP:
                self.held = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return self.to_surface()  # done — return the character surface

        if self.held:
            cell = self.get_cell(*pygame.mouse.get_pos())
            if cell:
                self.grid[cell[1]][cell[0]] = self.color

        return None

    def draw(self):
        screen.fill((18, 18, 28))

        # canvas
        for y in range(GRID):
            for x in range(GRID):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x],
                                     (CX+x*CELL, CY+y*CELL, CELL, CELL))
        # grid lines
        for i in range(GRID+1):
            pygame.draw.line(screen, (40,40,55), (CX+i*CELL, CY), (CX+i*CELL, CY+GRID*CELL))
            pygame.draw.line(screen, (40,40,55), (CX, CY+i*CELL), (CX+GRID*CELL, CY+i*CELL))
        pygame.draw.rect(screen, (80,200,255), (CX-1, CY-1, GRID*CELL+2, GRID*CELL+2), 2)

        # palette
        for i, col in enumerate(PALETTE):
            px = 20 + (i % 6) * 36
            py = SH - 80 + (i // 6) * 36
            pygame.draw.rect(screen, col, (px, py, 30, 30), border_radius=4)
            if col == self.color:
                pygame.draw.rect(screen, (80,200,255), (px-2, py-2, 34, 34), 2)

        pygame.display.flip()


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
            return result  # character surface ready

char_surf = run_creator() 