import random
from .ui import Dialog
from .debug import debug_print
from .quest import Quest
from .conversation import ConversationTree, create_mentor_conversation

class NPC:
    def __init__(self, name, x, y, npc_type):
        debug_print(f"Initializing NPC: {name}")
        self.name = name
        self.x = x
        self.y = y
        self.npc_type = npc_type
        self.dialog_options = self.generate_dialog_options()
        self.relationship = 50  # 0-100 scale
        self.conversation_tree = create_mentor_conversation() if npc_type == "mentor" else None

    def generate_dialog_options(self):
        if self.npc_type == "mentor":
            return [
                "Would you like some advice?",
                "Let's improve your skills!",
                "How about a quick lesson?"
            ]
        elif self.npc_type == "investor":
            return [
                "Are you looking for an investment?",
                "Show me your business plan.",
                "Let's talk about your company's future."
            ]
        elif self.npc_type == "customer":
            return [
                "What products do you offer?",
                "I'm looking for a good deal.",
                "Can you help me with something?"
            ]
        elif self.npc_type == "competitor":
            return [
                "How's business going?",
                "Maybe we could collaborate sometime.",
                "Watch out, I'm planning something big!"
            ]
        return ["Hello!"]

    def interact(self, player, game):
        dialog_text = f"{self.name} says: {random.choice(self.dialog_options)}"
        debug_print(f"NPC interaction: {dialog_text}")
        options = ["Talk", "Quest", "Trade", "Leave"]
        dialog = Dialog(dialog_text, options)
        game.current_dialog = dialog

    def process_interaction(self, player, game, choice):
        debug_print(f"Processing interaction with {self.name}, choice: {choice}")
        if choice == "Talk":
            self.talk(player, game)
        elif choice == "Quest":
            self.offer_quest(player, game)
        elif choice == "Trade":
            self.trade(player, game)
        else:
            game.show_message(f"You decided to leave {self.name}.")

    def talk(self, player, game):
        difficulty = game.difficulty_manager.calculate_difficulty()
        if self.npc_type == "mentor":
            if self.conversation_tree:
                self.conversation_tree.reset()
                game.show_message(self.conversation_tree.get_current_text())
                options = self.conversation_tree.get_options()
                dialog = Dialog("", options)
                game.current_dialog = dialog
            else:
                skill = random.choice(list(player.skills.keys()))
                increase = 0.5 / difficulty
                player.skills[skill] += increase
                message = f"{self.name} mentored you and improved your {skill} skill by {increase:.2f}!"
                self.relationship += 5
        elif self.npc_type == "investor":
            if player.skills["business"] > 5 * difficulty:
                investment = random.randint(1000, 5000) * difficulty
                player.money += investment
                message = f"{self.name} invested ${investment:.0f} in your business!"
                self.relationship += 10
            else:
                message = f"{self.name} declined to invest in your business."
                self.relationship -= 5
        elif self.npc_type == "customer":
            sale = random.randint(50, 200) * difficulty
            player.money += sale
            message = f"You made a sale of ${sale:.0f} to {self.name}!"
            self.relationship += 3
        elif self.npc_type == "competitor":
            tip = random.choice(["marketing", "customer service", "product development"])
            message = f"{self.name} gives you a tip about {tip}. Your knowledge improves slightly."
            player.skills[random.choice(list(player.skills.keys()))] += 0.2 / difficulty
            self.relationship += 2
        else:
            message = f"You had a pleasant conversation with {self.name}."
            self.relationship += 1

        self.relationship = max(0, min(100, self.relationship))
        debug_print(message)
        game.show_message(message)

    def offer_quest(self, player, game):
        quest = game.quest_manager.offer_quest(player)
        if quest:
            message = f"You accepted the quest: {quest.name}\n{quest.description}"
        else:
            message = f"{self.name} doesn't have any quests for you right now."
        game.show_message(message)

    def trade(self, player, game):
        if self.npc_type == "customer":
            item = random.choice(player.inventory) if player.inventory else None
            if item:
                price = item.value * (1 + (self.relationship - 50) / 100)
                message = f"{self.name} offers to buy your {item.name} for ${price:.2f}. Accept? (Y/N)"
                game.show_message(message)
                # Handle player's response in game.py
            else:
                game.show_message("You don't have any items to trade.")
        else:
            game.show_message(f"{self.name} is not interested in trading right now.")
