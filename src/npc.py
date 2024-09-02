from .character import Character
import random
from .ui import Dialog

class NPC(Character):
    def __init__(self, name, x, y, role):
        super().__init__(name, x, y)
        self.role = role
        self.dialog_options = self.generate_dialog_options()

    def generate_dialog_options(self):
        if self.role == "mentor":
            return [
                "Would you like some advice?",
                "Let's improve your skills!",
                "How about a quick lesson?"
            ]
        elif self.role == "investor":
            return [
                "Are you looking for an investment?",
                "Show me your business plan.",
                "Let's talk about your company's future."
            ]

    def interact(self, player, game):
        dialog = Dialog(f"{self.name}: {random.choice(self.dialog_options)}", ["Yes", "No"])
        choice = dialog.show(game.screen)
        
        if choice == "Yes":
            if self.role == "mentor":
                skill = random.choice(list(player.skills.keys()))
                player.skills[skill] += 0.5
                game.show_message(f"{self.name} mentored {player.name} and improved their {skill} skill")
            elif self.role == "investor":
                if player.skills["business"] > 5:
                    investment = random.randint(1000, 5000)
                    player.money += investment
                    game.show_message(f"{self.name} invested ${investment} in {player.name}'s business")
                else:
                    game.show_message(f"{self.name} declined to invest in {player.name}'s business")
        else:
            game.show_message(f"{player.name} declined to interact with {self.name}")
