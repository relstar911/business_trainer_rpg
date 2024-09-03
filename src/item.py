import pygame
from .debug import debug_print

class Item:
    def __init__(self, name, x, y, item_type):
        self.name = name
        self.rect = pygame.Rect(x, y, 15, 15)
        self.item_type = item_type
        debug_print(f"Created new item: {name} of type {item_type} at position ({x}, {y})")

    def draw(self, screen):
        color = (0, 0, 255) if self.item_type == "money" else (0, 255, 0) if self.item_type == "energy" else (255, 0, 0)
        pygame.draw.rect(screen, color, self.rect)

    def apply_effect(self, player):
        if self.item_type == "money":
            amount = 100
            if hasattr(player, 'add_money') and callable(getattr(player, 'add_money')):
                player.add_money(amount)
            else:
                player.money += amount
            debug_print(f"Player gained ${amount}. New balance: ${player.money}")
            return f"You gained ${amount}. Current money: ${player.money}"
        elif self.item_type == "energy":
            energy_gain = max(0, min(25, player.max_energy - player.energy))
            player.energy = min(player.max_energy, player.energy + energy_gain)
            debug_print(f"Player gained {energy_gain} energy. New energy: {player.energy}")
            return f"You gained {energy_gain} energy. Current energy: {player.energy}/{player.max_energy}"
        elif self.item_type == "skill":
            skill_gain = 0.5
            for skill in player.skills:
                player.skills[skill] += skill_gain
            skills_str = ", ".join([f"{skill}: {value:.1f}" for skill, value in player.skills.items()])
            debug_print(f"Player skills increased. New skills: {skills_str}")
            return f"All skills increased by {skill_gain}. Current skills: {skills_str}"

    def update(self):
        # Items don't need to move, but we'll add this method for consistency
        pass