import random
from .character import Character
from .utils import calculate_success_chance

class Player(Character):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.inventory = []
        self.quests = []

    def work(self):
        if self.energy >= 10:
            success_chance = calculate_success_chance(self.skills["business"])
            if random.random() < success_chance:
                earned = 50 * self.skills["business"]
                self.money += earned
                self.energy -= 10
                self.skills["business"] += 0.1
                print(f"{self.name} worked and earned ${earned:.2f}")
            else:
                self.energy -= 5
                print(f"{self.name} worked but didn't earn any money")
        else:
            print(f"{self.name} is too tired to work")

    def network(self):
        if self.energy >= 5:
            self.skills["networking"] += 0.2
            self.energy -= 5
            print(f"{self.name} networked and improved networking skills")
        else:
            print(f"{self.name} is too tired to network")

    def market(self):
        if self.energy >= 8:
            success_chance = calculate_success_chance(self.skills["marketing"])
            if random.random() < success_chance:
                earned = 30 * self.skills["marketing"]
                self.money += earned
                self.energy -= 8
                self.skills["marketing"] += 0.1
                print(f"{self.name} marketed and earned ${earned:.2f}")
            else:
                self.energy -= 4
                print(f"{self.name} marketed but didn't earn any money")
        else:
            print(f"{self.name} is too tired to market")

    def rest(self):
        self.energy = min(100, self.energy + 20)
        print(f"{self.name} rested and recovered 20 energy")

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
            print(f"{self.name} completed the quest '{quest.name}' and earned ${quest.reward}")
