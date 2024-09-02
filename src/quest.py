from .debug import debug_print
import random

class Quest:
    def __init__(self, name, description, base_reward, quest_type, difficulty):
        self.name = name
        self.description = description
        self.base_reward = base_reward
        self.reward = base_reward
        self.completed = False
        self.quest_type = quest_type
        self.difficulty = difficulty
        self.progress = 0
        self.goal = self.set_goal()
        debug_print(f"Created new quest: {name} (Type: {quest_type}, Difficulty: {difficulty})")

    def set_goal(self):
        if self.quest_type == "collect":
            return random.randint(5, 15) * self.difficulty
        elif self.quest_type == "earn":
            return random.randint(1000, 5000) * self.difficulty
        elif self.quest_type == "skill":
            return random.randint(2, 5) * self.difficulty
        else:
            return 1

    def adjust_reward(self, difficulty_manager):
        self.reward = difficulty_manager.adjust_reward(self.base_reward)
        debug_print(f"Adjusted quest reward for {self.name}: {self.reward}")

    def update_progress(self, amount=1):
        self.progress += amount
        if self.progress >= self.goal:
            self.complete()
        debug_print(f"Updated progress for quest {self.name}: {self.progress}/{self.goal}")

    def complete(self):
        self.completed = True
        debug_print(f"Completed quest: {self.name}")

class QuestLog:
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
        debug_print("Initialized QuestLog")

    def add_quest(self, quest):
        self.active_quests.append(quest)
        debug_print(f"Added quest to log: {quest.name}")

    def complete_quest(self, quest):
        if quest in self.active_quests:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            quest.complete()
            debug_print(f"Moved quest to completed: {quest.name}")

    def get_active_quests(self):
        return self.active_quests

    def get_completed_quests(self):
        return self.completed_quests

class QuestManager:
    def __init__(self):
        self.quest_log = QuestLog()
        self.available_quests = self.generate_quests()
        debug_print("Initialized QuestManager")

    def generate_quests(self):
        quests = [
            Quest("Networking Novice", "Meet and talk to 5 different NPCs", 100, "collect", 1),
            Quest("Money Maker", "Earn $5000 through various activities", 500, "earn", 2),
            Quest("Skill Master", "Improve any skill to level 3", 300, "skill", 2),
            Quest("Market Domination", "Complete 3 successful marketing campaigns", 400, "collect", 3),
            Quest("Investment Guru", "Successfully pitch to 2 investors", 600, "collect", 3),
            Quest("Business Tycoon", "Own and operate 3 successful businesses", 1000, "collect", 4),
        ]
        debug_print(f"Generated {len(quests)} quests")
        return quests

    def offer_quest(self, player):
        if self.available_quests:
            quest = random.choice(self.available_quests)
            self.available_quests.remove(quest)
            self.quest_log.add_quest(quest)
            debug_print(f"Offered quest to player: {quest.name}")
            return quest
        debug_print("No available quests to offer")
        return None

    def update_quests(self, player, difficulty_manager):
        for quest in self.quest_log.get_active_quests():
            quest.adjust_reward(difficulty_manager)
            if quest.quest_type == "earn" and player.money >= quest.goal:
                quest.update_progress(player.money)
            elif quest.quest_type == "skill" and any(skill >= quest.goal for skill in player.skills.values()):
                quest.update_progress()
        debug_print("Updated all active quests")

    def complete_quest(self, quest, player):
        self.quest_log.complete_quest(quest)
        player.money += quest.reward
        debug_print(f"Player completed quest {quest.name} and earned ${quest.reward}")
