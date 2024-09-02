import pygame
from .player import Player
from .npc import NPC
from .map import Map
from .quest import QuestManager
from .minigame import MinigameManager
from .ui import Button, Dialog

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Business Trainer RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.map = Map(40, 30)
        self.player = Player("Entrepreneur", 10, 10)
        self.npcs = [
            NPC("Mentor Mike", 20, 10, "mentor"),
            NPC("Investor Ivy", 30, 10, "investor")
        ]
        self.quest_manager = QuestManager()
        self.minigame_manager = MinigameManager()
        self.ui_elements = []

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_player_movement(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_player_movement(self, key):
        dx, dy = 0, 0
        if key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        elif key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_DOWN:
            dy = 1

        new_x, new_y = self.player.x + dx, self.player.y + dy
        if self.map.is_walkable(new_x, new_y):
            self.player.move(dx, dy)
            location = self.map.get_location(new_x, new_y)
            if location:
                self.handle_location_action(location)
            self.check_npc_interaction()

    def handle_mouse_click(self, pos):
        for ui_element in self.ui_elements:
            if isinstance(ui_element, Button) and ui_element.is_clicked(pos):
                # Handle button click
                pass

    def handle_location_action(self, location):
        if location == "office":
            self.player.work()
        elif location == "market":
            self.player.market()
        elif location == "home":
            self.player.rest()

    def check_npc_interaction(self):
        for npc in self.npcs:
            if npc.x == self.player.x and npc.y == self.player.y:
                npc.interact(self.player, self)

    def show_message(self, message):
        dialog = Dialog(message, ["OK"])
        dialog.show(self.screen)

    def update(self):
        self.quest_manager.update()
        self.minigame_manager.update()

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black
        self.map.draw(self.screen)
        self.draw_characters()
        self.draw_player_info()
        self.draw_ui_elements()
        pygame.display.flip()

    def draw_characters(self):
        cell_size = 20
        # Draw player
        pygame.draw.rect(self.screen, (0, 255, 0), 
                         (self.player.x * cell_size, self.player.y * cell_size, cell_size, cell_size))
        # Draw NPCs
        for npc in self.npcs:
            pygame.draw.rect(self.screen, (255, 0, 0), 
                             (npc.x * cell_size, npc.y * cell_size, cell_size, cell_size))

    def draw_player_info(self):
        font = pygame.font.Font(None, 24)
        info = f"Money: ${self.player.money:.0f} | Energy: {self.player.energy:.0f}"
        text = font.render(info, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        skills_info = f"Business: {self.player.skills['business']:.1f} | Networking: {self.player.skills['networking']:.1f} | Marketing: {self.player.skills['marketing']:.1f}"
        skills_text = font.render(skills_info, True, (255, 255, 255))
        self.screen.blit(skills_text, (10, 40))

    def draw_ui_elements(self):
        for ui_element in self.ui_elements:
            ui_element.draw(self.screen)
