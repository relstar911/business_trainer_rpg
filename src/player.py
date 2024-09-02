import random
import pygame
from .character import Character
from .utils import calculate_success_chance
from .debug import debug_print

class Player(Character):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.inventory = []
        self.quests = []
        self.target_x = x
        self.target_y = y
        self.move_speed = 0.1  # Adjust this value to change movement speed
        debug_print(f"Initializing Player: {name}")

    def update(self, dt):
        # Smooth movement towards target position
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance > 0.01:  # If not very close to target
            move_distance = min(self.move_speed * dt, distance)
            self.x += (dx / distance) * move_distance
            self.y += (dy / distance) * move_distance
        else:
            self.x = self.target_x
            self.y = self.target_y

    def move(self, dx, dy):
        self.target_x += dx
        self.target_y += dy

    def work(self):
        if self.energy >= 10:
            success_chance = calculate_success_chance(self.skills["business"])
            if random.random() < success_chance:
                earned = 50 * self.skills["business"]
                self.money += earned
                self.energy -= 10
                self.skills["business"] += 0.1
                debug_print(f"{self.name} worked and earned ${earned:.2f}")
                return f"{self.name} worked and earned ${earned:.2f}"
            else:
                self.energy -= 5
                debug_print(f"{self.name} worked but didn't earn any money")
                return f"{self.name} worked but didn't earn any money"
        else:
            debug_print(f"{self.name} is too tired to work")
            return f"{self.name} is too tired to work"

    def network(self):
        if self.energy >= 5:
            self.skills["networking"] += 0.2
            self.energy -= 5
            debug_print(f"{self.name} networked and improved networking skills")
            return f"{self.name} networked and improved networking skills"
        else:
            debug_print(f"{self.name} is too tired to network")
            return f"{self.name} is too tired to network"

    def market(self):
        if self.money >= 50:
            self.money -= 50
            skill_increase = random.uniform(0.1, 0.5)
            skill = random.choice(list(self.skills.keys()))
            self.skills[skill] += skill_increase
            debug_print(f"{self.name} spent $50 on marketing and improved {skill} skill by {skill_increase:.2f}")
            return f"{self.name} spent $50 on marketing and improved {skill} skill"
        else:
            debug_print(f"{self.name} doesn't have enough money for marketing")
            return f"{self.name} doesn't have enough money for marketing"

    def rest(self):
        self.energy = min(100, self.energy + 20)
        debug_print(f"{self.name} rested and recovered 20 energy")
        return f"{self.name} rested and recovered 20 energy"

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def add_quest(self, quest):
        self.quests.append(quest)

    def complete_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)
            quest.complete()
            self.money += quest.reward
            debug_print(f"{self.name} completed the quest '{quest.name}' and earned ${quest.reward}")
            return f"{self.name} completed the quest '{quest.name}' and earned ${quest.reward}"
