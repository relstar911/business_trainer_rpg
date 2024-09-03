import pygame
from .debug import debug_print

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_size = 20  # Adjust as needed
        self.tiles = [[0 for _ in range(width)] for _ in range(height)]
        self.locations = {
            "office": {"pos": (100, 100), "size": (80, 60), "entry": (140, 160)},
            "market": {"pos": (300, 100), "size": (80, 60), "entry": (340, 160)},
            "home": {"pos": (500, 100), "size": (80, 60), "entry": (540, 160)}
        }
        self.rects = self.generate_rects()
        self.obstacles = []  # List to store obstacles
        self.background_color = (20, 20, 30)  # Dark blue-gray background
        debug_print(f"Map initialized with dimensions {width}x{height}")

    def is_walkable(self, x, y):
        tile_x, tile_y = int(x // self.tile_size), int(y // self.tile_size)
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            return self.tiles[tile_y][tile_x] == 0  # Assuming 0 represents walkable tiles
        return False

    def generate_rects(self):
        return {name: pygame.Rect(info["pos"], info["size"]) for name, info in self.locations.items()}

    def draw(self, screen):
        # Fill the screen with the dark background color
        screen.fill(self.background_color)

        # Draw locations
        for name, rect in self.rects.items():
            pygame.draw.rect(screen, (100, 100, 150), rect)  # Lighter blue for buildings
            font = pygame.font.Font(None, 24)
            text = font.render(name.capitalize(), True, (255, 255, 255))  # White text
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw entry points
        for info in self.locations.values():
            entry_x, entry_y = info["entry"]
            pygame.draw.circle(screen, (0, 255, 0), (entry_x, entry_y), 5)  # Green entry points

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (200, 50, 50), obstacle)  # Red obstacles

    def get_location(self, x, y, player_size=(20, 20)):
        player_radius = max(player_size) / 2  # Use the larger dimension for a circular check
        for name, info in self.locations.items():
            entry_x, entry_y = info["entry"]
            distance = ((x - entry_x) ** 2 + (y - entry_y) ** 2) ** 0.5
            if distance < player_radius + 10:  # Add a small buffer for easier entry
                debug_print(f"Player at location: {name}")
                return name
        return None

    def add_location(self, name, pos, size, entry):
        self.locations[name] = {"pos": pos, "size": size, "entry": entry}
        self.rects[name] = pygame.Rect(pos, size)
        debug_print(f"Added new location: {name}")

    def remove_location(self, name):
        if name in self.locations:
            del self.locations[name]
            del self.rects[name]
            debug_print(f"Removed location: {name}")
        else:
            debug_print(f"Attempted to remove non-existent location: {name}")

    def add_obstacle(self, x, y, width, height):
        obstacle = pygame.Rect(x, y, width, height)
        self.obstacles.append(obstacle)
        debug_print(f"Added new obstacle at ({x}, {y})")

    def remove_obstacle(self, obstacle):
        if obstacle in self.obstacles:
            self.obstacles.remove(obstacle)
            debug_print(f"Removed obstacle at ({obstacle.x}, {obstacle.y})")
        else:
            debug_print(f"Attempted to remove non-existent obstacle")