class Quest:
    def __init__(self, name, description, reward):
        self.name = name
        self.description = description
        self.reward = reward
        self.completed = False

    def complete(self):
        self.completed = True

class QuestManager:
    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        self.quests.append(quest)

    def complete_quest(self, quest_name):
        for quest in self.quests:
            if quest.name == quest_name:
                quest.complete()
                return True
        return False

    def get_active_quests(self):
        return [quest for quest in self.quests if not quest.completed]

    def update(self):
        # Placeholder for any quest-related updates that need to happen each frame
        pass
