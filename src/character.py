class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.money = 1000
        self.energy = 100
        self.skills = {"business": 1, "networking": 1, "marketing": 1}

    def move(self, dx, dy):
        self.x += dx
        self.y += dy