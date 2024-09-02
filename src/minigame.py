import random

class Minigame:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

    def play(self):
        # Placeholder for minigame logic
        success = random.random() > (self.difficulty / 10)
        return success

class MinigameManager:
    def __init__(self):
        self.minigames = []

    def add_minigame(self, minigame):
        self.minigames.append(minigame)

    def get_random_minigame(self):
        return random.choice(self.minigames) if self.minigames else None

    def play_minigame(self, minigame_name):
        for minigame in self.minigames:
            if minigame.name == minigame_name:
                return minigame.play()
        return False

    def update(self):
        # Placeholder for any minigame-related updates that need to happen each frame
        pass
