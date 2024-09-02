import random

class Item:
    def __init__(self, name, x, y, item_type):
        self.name = name
        self.x = x
        self.y = y
        self.item_type = item_type

    def apply_effect(self, player):
        if self.item_type == "money":
            player.money += 100
        elif self.item_type == "energy":
            player.energy = min(100, player.energy + 25)
        elif self.item_type == "skill":
            for skill in player.skills:
                player.skills[skill] += 0.5