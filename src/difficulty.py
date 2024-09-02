from .debug import debug_print

class DifficultyManager:
    def __init__(self):
        self.base_difficulty = 1.0
        self.player_level = 1
        debug_print("DifficultyManager initialized")

    def calculate_difficulty(self):
        return self.base_difficulty * (1 + (self.player_level - 1) * 0.1)

    def update_player_level(self, player):
        # Calculate player level based on skills
        new_level = max(int(sum(player.skills.values()) / 3), 1)
        if new_level != self.player_level:
            self.player_level = new_level
            debug_print(f"Player level updated to {self.player_level}")

    def adjust_reward(self, base_reward):
        difficulty = self.calculate_difficulty()
        adjusted_reward = base_reward * (1 + (difficulty - 1) * 0.5)
        debug_print(f"Adjusted reward from {base_reward} to {adjusted_reward}")
        return int(adjusted_reward)

    def adjust_cost(self, base_cost):
        difficulty = self.calculate_difficulty()
        adjusted_cost = base_cost * (1 + (difficulty - 1) * 0.3)
        debug_print(f"Adjusted cost from {base_cost} to {adjusted_cost}")
        return int(adjusted_cost)