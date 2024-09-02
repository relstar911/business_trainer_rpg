from .debug import debug_print

class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.money = 1000
        self.energy = 100
        self.skills = {"business": 1, "networking": 1, "marketing": 1}
        debug_print(f"Created new character: {name} at position ({x}, {y})")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        debug_print(f"{self.name} moved to position ({self.x}, {self.y})")