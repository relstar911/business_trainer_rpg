import random
import pygame
from .character import Character
from .utils import calculate_success_chance, format_money
from .debug import debug_print, info_print

class Player(Character):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.rect = pygame.Rect(x, y, 20, 20)  # Add this line
        self.speed = 2  # Add this line
        self.sprinting = False
        self.sprint_speed = 4  # Changed from 1.5 to 4 for more noticeable effect
        self.move_energy_cost = 0.1
        self.sprint_energy_cost = 0.3
        self.quests = []
        self.inventory = []  # We'll keep this for compatibility, but use InventoryScreen for management
        self.current_location = None
        self.money = 1000
        self.energy = 100
        self.max_energy = 100
        self.skills = {"business": 1, "networking": 1, "marketing": 1}
        info_print(f"Initializing Player: {name}")
    def update(self, dt):
        super().update(dt)
        # Add time-based energy regeneration
        self.energy = min(self.max_energy, self.energy + 0.1 * dt)
        # Update skills
        for skill in self.skills:
            self.skills[skill] += 0.001 * dt  # Very slow passive skill increase
        debug_print(f"Player skills updated: {self.skills}")

    def update(self, dt):
        super().update(dt)
        # Add time-based energy regeneration
        self.energy = min(self.max_energy, self.energy + 0.1 * dt)

    def move(self, dx, dy, game_map):
        speed = self.sprint_speed if self.sprinting else self.speed
        energy_cost = self.sprint_energy_cost if self.sprinting else self.move_energy_cost
        
        new_x = self.x + dx * speed
        new_y = self.y + dy * speed
        
        if game_map.is_walkable(new_x, new_y):
            if self.energy >= energy_cost:
                self.x = new_x
                self.y = new_y
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
                self.energy -= energy_cost
                self.update_location(game_map)
                debug_print(f"Player moved to ({self.x}, {self.y}). Energy: {self.energy}")
            else:
                debug_print("Not enough energy to move.")
        else:
            debug_print(f"Cannot move to ({new_x}, {new_y}). Position not walkable.")
            return False  # Indicate that movement was not successful

    def update(self, dt):
        for skill in self.skills:
            self.skills[skill] += 0.001 * dt  # Very slow passive skill increase
        debug_print(f"Player skills updated: {self.skills}")

    def add_item(self, item):
        self.inventory.append(item)  # This method might not be needed anymore, as we're using InventoryScreen

    def use_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                item.use(self)
                self.inventory.remove(item)
                debug_print(f"Used {item_name}")
                return True
        return False

    def rest(self):
        energy_gain = min(50, self.max_energy - self.energy)
        self.energy = min(self.max_energy, self.energy + energy_gain)
        debug_print(f"Player rested. Energy increased by {energy_gain}")
        return f"You rested and regained {energy_gain} energy. Current energy: {self.energy:.1f}"

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (self.rect.x, self.rect.y - 20))
        money_text = font.render(format_money(self.money), True, (255, 255, 0))
        screen.blit(money_text, (self.rect.x, self.rect.y + self.rect.height + 5))
        energy_text = font.render(f"Energy: {int(self.energy)}", True, (0, 0, 255))
        screen.blit(energy_text, (self.rect.x, self.rect.y + self.rect.height + 25))

    def update_location(self, game_map):
        self.current_location = game_map.get_location(self.x, self.y)
        if self.current_location:
            debug_print(f"Player entered: {self.current_location}")

    def start_sprint(self):
        self.sprinting = True
        debug_print("Player started sprinting")

    def stop_sprint(self):
        self.sprinting = False
        debug_print("Player stopped sprinting")

    def add_money(self, amount):
        self.money += amount
        debug_print(f"Player {self.name} gained ${amount}. New balance: ${self.money}")

    def remove_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            debug_print(f"Player {self.name} spent ${amount}. New balance: ${self.money}")
            return True
        else:
            debug_print(f"Player {self.name} doesn't have enough money. Current balance: ${self.money}")
            return False

    def add_quest(self, quest):
        self.quests.append(quest)
        debug_print(f"Player {self.name} received new quest: {quest.name}")
    def complete_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)
            quest.complete()
            self.money += quest.reward
            debug_print(f"{self.name} completed the quest '{quest.name}' and earned ${quest.reward}")
            return f"{self.name} completed the quest '{quest.name}' and earned ${quest.reward}"
            debug_print(f"Player {self.name} completed quest: {quest.name}")

    def add_to_inventory(self, item):
        self.inventory.append(item)
        debug_print(f"Player {self.name} added {item.name} to inventory")

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            debug_print(f"Player {self.name} removed {item.name} from inventory")
            return True
        return False

    def remove_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return True
        return False

