import random
import pygame

from src import game, player
from src.character import Character
from .ui import Dialog, ConversationWindow
from .debug import debug_print, info_print
from .conversation import create_mentor_conversation, create_investor_conversation, create_customer_conversation, create_competitor_conversation

class NPC(Character):
    def __init__(self, name, x, y, npc_type, game_map):
        super().__init__(name, x, y)
        self.npc_type = npc_type
        self.game_map = game_map
        self.rect = pygame.Rect(x, y, 20, 20)
        self.movement_timer = 0
        self.movement_interval = 2  # Move every 2 seconds
        self.interaction_range = 30
        self.conversation_tree = self.get_conversation_tree()
        info_print(f"Initializing NPC: {name}")

    def update(self, dt):
        super().update(dt)
        self.movement_timer += dt
        if self.movement_timer >= self.movement_interval:
            self.move_randomly()
            self.movement_timer = 0

    def move_randomly(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        new_x = self.x + dx
        new_y = self.y + dy
        if self.game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def get_conversation_tree(self):
        if self.npc_type == "mentor":
            return create_mentor_conversation()
        elif self.npc_type == "investor":
            return create_investor_conversation()
        elif self.npc_type == "customer":
            return create_customer_conversation()
        elif self.npc_type == "competitor":
            return create_competitor_conversation()
        else:
            return None

    def interact(self, player, game):
        if self.is_in_range(player):
            if self.conversation_tree:
                game.current_dialog = ConversationWindow(self.conversation_tree, self.name)
            else:
                dialog_text = f"{self.name} says: Hello, I'm a {self.npc_type}!"
                options = ["Talk", "Quest", "Trade", "Leave"]
                game.current_dialog = Dialog(dialog_text, options)
        else:
            debug_print(f"Player is too far from {self.name} to interact")

    def is_in_range(self, player):
        distance = ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5
        return distance <= self.interaction_range

    def offer_quest(self, player, game, npc_type):
        if npc_type == "mentor":
            return self.offer_mentor_quest(player, game)
        elif npc_type == "investor":
            return self.offer_investor_quest(player, game)
        elif npc_type == "customer":
            return self.offer_customer_quest(player, game)
        elif npc_type == "competitor":
            return self.offer_competitor_quest(player, game)
        else:
            return f"{self.name} doesn't have any quests for you at the moment."

    def offer_mentor_quest(self, player, game):
        # Implement mentor-specific quest logic here
        return f"{self.name} offers you a mentorship quest."

    def offer_investor_quest(self, player, game):
        # Implement investor-specific quest logic here
        return f"{self.name} proposes an investment opportunity quest."

    def offer_customer_quest(self, player, game):
        # Implement customer-specific quest logic here
        return f"{self.name} requests a customer satisfaction quest."

    def offer_competitor_quest(self, player, game):
        # Implement competitor-specific quest logic here
        return f"{self.name} challenges you to a competitive quest."

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        font = pygame.font.Font(None, 20)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (self.rect.x, self.rect.y - 20))
