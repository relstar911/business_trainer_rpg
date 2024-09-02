import pygame
from .player import Player
from .npc import NPC
from .map import Map
from .quest import QuestManager
from .minigame import MinigameManager
from .ui import Dialog
from .item import Item

class Game:
    def __init__(self):
        print("Initializing Game...")
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Business Trainer RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.cell_size = 20
        self.map = Map(40, 30)
        self.player = Player("Entrepreneur", 10, 10)
        self.npcs = [
            NPC("Mentor Mike", 20, 10, "mentor"),
            NPC("Investor Ivy", 30, 10, "investor")
        ]
        self.quest_manager = QuestManager()
        self.minigame_manager = MinigameManager()
        self.items = [
            Item("Money Bag", 5, 15, "money"),
            Item("Energy Drink", 15, 25, "energy"),
            Item("Skill Book", 25, 15, "skill")
        ]
        self.interaction_target = None
        self.current_dialog = None
        self.time = 0
        self.day = 1
        print("Game initialized.")

    def run(self):
        print("Starting game loop...")
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        print("Game loop ended.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event detected.")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)}")
                if self.current_dialog:
                    self.handle_dialog_input(event.key)
                elif event.key == pygame.K_SPACE:
                    self.handle_interaction()
                else:
                    self.handle_player_movement(event.key)

    def handle_dialog_input(self, key):
        print(f"Handling dialog input: {pygame.key.name(key)}")
        if key == pygame.K_UP:
            self.current_dialog.move_selection(-1)
        elif key == pygame.K_DOWN:
            self.current_dialog.move_selection(1)
        elif key == pygame.K_SPACE:
            selected_option = self.current_dialog.get_selected_option()
            print(f"Selected dialog option: {selected_option}")
            self.process_dialog_option(selected_option)

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
        
        print(f"Player movement: dx={dx}, dy={dy}")
        self.move_player(dx, dy)

    def move_player(self, dx, dy):
        new_x, new_y = self.player.x + dx, self.player.y + dy
        if self.map.is_walkable(new_x, new_y):
            self.player.move(dx, dy)
            print(f"Player moved to: ({self.player.x}, {self.player.y})")
            self.check_interaction_target()
            self.check_item_pickup()
        else:
            print(f"Cannot move to: ({new_x}, {new_y})")

    def check_interaction_target(self):
        self.interaction_target = None
        for npc in self.npcs:
            if abs(npc.x - self.player.x) <= 1 and abs(npc.y - self.player.y) <= 1:
                self.interaction_target = npc
                print(f"Interaction target set: {npc.name}")
                return
        location = self.map.get_location(self.player.x, self.player.y)
        if location:
            self.interaction_target = location
            print(f"Interaction target set: {location}")

    def handle_interaction(self):
        print("Handling interaction...")
        if self.interaction_target:
            if isinstance(self.interaction_target, NPC):
                print(f"Interacting with NPC: {self.interaction_target.name}")
                self.interaction_target.interact(self.player, self)
            elif isinstance(self.interaction_target, str):  # Location
                print(f"Interacting with location: {self.interaction_target}")
                self.handle_location_action(self.interaction_target)
        else:
            print("No interaction target.")

    def handle_location_action(self, location):
        print(f"Handling location action: {location}")
        if location == "office":
            message = self.player.work()
        elif location == "market":
            message = self.player.market()
        elif location == "home":
            message = self.player.rest()
        self.show_message(message)

    def check_item_pickup(self):
        for item in self.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                item.apply_effect(self.player)
                self.items.remove(item)
                print(f"Item picked up: {item.name}")
                self.show_message(f"You picked up a {item.name}!")

    def show_message(self, message):
        print(f"Showing message: {message}")
        self.current_dialog = Dialog(message, ["OK"])

    def process_dialog_option(self, option):
        print(f"Processing dialog option: {option}")
        if isinstance(self.interaction_target, NPC):
            self.interaction_target.process_interaction(self.player, self, option)
        self.current_dialog = None

    def update(self):
        self.quest_manager.update()
        self.minigame_manager.update()
        self.time += 1
        if self.time >= 1440:  # 24 hours * 60 minutes
            self.time = 0
            self.day += 1
            self.player.energy = min(100, self.player.energy + 50)  # Rest at night
            print(f"New day: {self.day}")

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black
        self.map.draw(self.screen)
        self.draw_characters()
        self.draw_items()
        self.draw_player_info()
        self.draw_time()
        if self.current_dialog:
            self.current_dialog.draw(self.screen)
        pygame.display.flip()

    def draw_characters(self):
        # Draw player
        pygame.draw.rect(self.screen, (0, 255, 0), 
                         (self.player.x * self.cell_size, self.player.y * self.cell_size, self.cell_size, self.cell_size))
        # Draw NPCs
        for npc in self.npcs:
            color = (255, 255, 0) if npc == self.interaction_target else (255, 0, 0)
            pygame.draw.rect(self.screen, color, 
                             (npc.x * self.cell_size, npc.y * self.cell_size, self.cell_size, self.cell_size))

    def draw_items(self):
        for item in self.items:
            pygame.draw.rect(self.screen, (0, 0, 255), 
                             (item.x * self.cell_size, item.y * self.cell_size, self.cell_size, self.cell_size))

    def draw_player_info(self):
        font = pygame.font.Font(None, 24)
        info = f"Money: ${self.player.money:.0f} | Energy: {self.player.energy:.0f}"
        text = font.render(info, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        skills_info = f"Business: {self.player.skills['business']:.1f} | Networking: {self.player.skills['networking']:.1f} | Marketing: {self.player.skills['marketing']:.1f}"
        skills_text = font.render(skills_info, True, (255, 255, 255))
        self.screen.blit(skills_text, (10, 40))

    def draw_time(self):
        font = pygame.font.Font(None, 24)
        time_str = f"Day {self.day} - {self.time // 60:02d}:{self.time % 60:02d}"
        text = font.render(time_str, True, (255, 255, 255))
        self.screen.blit(text, (10, 70))
