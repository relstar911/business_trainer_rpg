import random
from .ui import Dialog
from .debug import debug_print

class NPC:
    def __init__(self, name, x, y, npc_type):
        debug_print(f"Initializing NPC: {name}")
        self.name = name
        self.x = x
        self.y = y
        self.npc_type = npc_type
        self.dialog_options = self.generate_dialog_options()

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
        return ["Hello!"]

    def interact(self, player, game):
        dialog_text = f"{self.name} says: {random.choice(self.dialog_options)}"
        debug_print(f"NPC interaction: {dialog_text}")
        dialog = Dialog(dialog_text, ["Yes", "No"])
        game.current_dialog = dialog

    def process_interaction(self, player, game, choice):
        debug_print(f"Processing interaction with {self.name}, choice: {choice}")
        if choice == "Yes":
            if self.npc_type == "mentor":
                skill = random.choice(list(player.skills.keys()))
                increase = 0.5
                player.skills[skill] += increase
                message = f"{self.name} mentored you and improved your {skill} skill by {increase}!"
            elif self.npc_type == "investor":
                if player.skills["business"] > 5:
                    investment = random.randint(1000, 5000)
                    player.money += investment
                    message = f"{self.name} invested ${investment} in your business!"
                else:
                    message = f"{self.name} declined to invest in your business."
            debug_print(message)
            game.show_message(message)
        else:
            message = f"You declined to interact with {self.name}."
            debug_print(message)
            game.show_message(message)
