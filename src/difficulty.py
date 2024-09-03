from .debug import debug_print

class DifficultyManager:
    def __init__(self):
        self.current_difficulty = 1.0
        self.max_difficulty = 10.0
        self.player_performance_factor = 1.0
        debug_print("Initialized DifficultyManager")

    def calculate_difficulty(self):
        return min(self.max_difficulty, self.current_difficulty * self.player_performance_factor)

    def update_difficulty(self, player):
        avg_skill = sum(player.skills.values()) / len(player.skills)
        
        # Normalize the average skill to a range of 0.5 to 2.0
        min_skill, max_skill = 0, 100  # Adjust these values based on your game's skill range
        normalized_skill = (avg_skill - min_skill) / (max_skill - min_skill)
        skill_factor = 0.5 + (normalized_skill * 1.5)  # Maps to 0.5 (min) to 2.0 (max)
        
        # Ensure skill_factor stays within the desired range
        skill_factor = max(0.5, min(2.0, skill_factor))
        
        # Adjust difficulty based on player's money
        money_factor = min(2.0, max(0.5, player.money / 10000))  # Scale based on 10,000 being "average"
        
        # Adjust difficulty based on completed quests
        completed_quests = sum(1 for quest in player.quests if quest.completed)
        quest_factor = min(2.0, max(0.5, completed_quests / 10))  # Scale based on 10 quests being "average"
        
        # Calculate the overall performance factor
        self.player_performance_factor = (skill_factor + money_factor + quest_factor) / 3
        
        # Update the current difficulty based on the player_performance_factor
        # Calculate the target difficulty based on player performance
        # Calculate the target difficulty based on player performance, ensuring it's not below 1.0
        target_difficulty = max(1.0, self.current_difficulty * self.player_performance_factor)
        
        # Gradually adjust the current difficulty towards the target
        adjustment_rate = 0.2  # Adjust this value to control the speed of difficulty changes
        self.current_difficulty += (target_difficulty - self.current_difficulty) * adjustment_rate
        
        # Ensure the difficulty stays within the allowed range
        self.current_difficulty = max(1.0, min(self.max_difficulty, self.current_difficulty))
        
        actual_difficulty = self.calculate_difficulty()
        debug_print(f"Difficulty updated: {actual_difficulty:.2f} (Base: {self.current_difficulty:.2f}, Performance: {self.player_performance_factor:.2f})")

    def adjust_reward(self, base_reward):
        difficulty = self.calculate_difficulty()
        adjustment_factor = 1 + (difficulty - 1) * 0.2  # Increased from 0.1 to 0.2
        return base_reward * adjustment_factor