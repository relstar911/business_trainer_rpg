import random
from .debug import debug_print

class Minigame:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        debug_print(f"Created new minigame: {name} (difficulty: {difficulty})")

    def play(self):
        success = random.random() > (self.difficulty / 10)
        debug_print(f"Played minigame {self.name}: {'Success' if success else 'Failure'}")
        return success

class MinigameManager:
    def __init__(self):
        self.minigames = []
        debug_print("Initialized MinigameManager")

    def add_minigame(self, minigame):
        self.minigames.append(minigame)
        debug_print(f"Added minigame to manager: {minigame.name}")

    def get_random_minigame(self):
        if self.minigames:
            minigame = random.choice(self.minigames)
            debug_print(f"Selected random minigame: {minigame.name}")
            return minigame
        debug_print("No minigames available")
        return None

    def play_minigame(self, minigame_name):
        for minigame in self.minigames:
            if minigame.name == minigame_name:
                result = minigame.play()
                debug_print(f"Played minigame {minigame_name}: {'Success' if result else 'Failure'}")
                return result
        debug_print(f"Failed to play minigame: {minigame_name} (not found)")
        return False

    def update(self):
        debug_print("MinigameManager update called")
        pass
