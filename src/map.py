import pygame

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.locations = {
            "office": {"pos": (5, 5), "size": (4, 3), "entry": (7, 7)},
            "market": {"pos": (15, 5), "size": (4, 3), "entry": (17, 7)},
            "home": {"pos": (25, 5), "size": (4, 3), "entry": (27, 7)}
        }
        self.rects = self.generate_rects()

    def generate_rects(self):
        rects = {}
        for name, info in self.locations.items():
            x, y = info["pos"]
            width, height = info["size"]
            rects[name] = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                      width * self.cell_size, height * self.cell_size)
        return rects

    def draw(self, screen):
        # Draw grid
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)

        # Draw locations
        for name, rect in self.rects.items():
            pygame.draw.rect(screen, (100, 100, 100), rect)
            font = pygame.font.Font(None, 24)
            text = font.render(name.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw entry points
        for info in self.locations.values():
            entry_x, entry_y = info["entry"]
            entry_rect = pygame.Rect(entry_x * self.cell_size, entry_y * self.cell_size, 
                                     self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (0, 255, 0), entry_rect)

    def is_walkable(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        for info in self.locations.values():
            loc_x, loc_y = info["pos"]
            width, height = info["size"]
            if loc_x <= x < loc_x + width and loc_y <= y < loc_y + height:
                entry_x, entry_y = info["entry"]
                return x == entry_x and y == entry_y
        return True

    def get_location(self, x, y):
        for name, info in self.locations.items():
            entry_x, entry_y = info["entry"]
            if x == entry_x and y == entry_y:
                return name
        return None

    def get_location_by_pos(self, pos):
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        return self.get_location(x, y)