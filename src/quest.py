from .debug import debug_print

class Quest:
    def __init__(self, name, description, reward):
        self.name = name
        self.description = description
        self.reward = reward
        self.completed = False
        debug_print(f"Created new quest: {name}")

    def complete(self):
        self.completed = True
        debug_print(f"Completed quest: {self.name}")

class QuestManager:
    def __init__(self):
        self.quests = []
        debug_print("Initialized QuestManager")

    def add_quest(self, quest):
        self.quests.append(quest)
        debug_print(f"Added quest to manager: {quest.name}")

    def complete_quest(self, quest_name):
        for quest in self.quests:
            if quest.name == quest_name:
                quest.complete()
                debug_print(f"Marked quest as completed: {quest_name}")
                return True
        debug_print(f"Failed to complete quest: {quest_name} (not found)")
        return False

    def get_active_quests(self):
        active_quests = [quest for quest in self.quests if not quest.completed]
        debug_print(f"Retrieved {len(active_quests)} active quests")
        return active_quests

    def update(self):
        debug_print("QuestManager update called")
        pass
