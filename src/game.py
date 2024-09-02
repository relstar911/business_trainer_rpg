import pygame
from .player import Player
from .npc import NPC
from .map import Map
from .quest import QuestManager
from .minigame import MinigameManager
from .item import Item
from .ui import Dialog, Button
from .save_load import save_game, load_game
from .save_menu import SaveLoadMenu
from .pause_menu import PauseMenu
from .inventory import InventoryScreen
from .debug import debug_print
from .economy import Economy
from .difficulty import DifficultyManager
from .conversation import create_mentor_conversation

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
            NPC("Investor Ivy", 30, 10, "investor"),
            NPC("Customer John", 15, 15, "customer"),
            NPC("Competitor Sam", 25, 20, "competitor")
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
        self.day_length = 1440  # 24 hours * 60 minutes
        self.time_events = [
            (360, self.morning_event),
            (720, self.noon_event),
            (1080, self.evening_event),
            (1320, self.night_event)
        ]
        self.current_event_index = 0
        self.economy = Economy()
        self.difficulty_manager = DifficultyManager()
        self.current_conversation = None
        print("Game initialized.")

        # Add a "Return to Main Menu" button
        self.menu_button = Button(10, 570, 150, 20, "Main Menu", (100, 100, 100), (255, 255, 255))

        self.last_time = pygame.time.get_ticks()

    def run(self):
        print("Starting game loop...")
        while self.running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.last_time) / 1000.0  # Convert to seconds
            self.last_time = current_time

            action = self.handle_events()
            if action == "MAIN_MENU":
                print("Returning to main menu")
                return "MAIN_MENU"
            elif action == "QUIT":
                print("Quitting game")
                return "QUIT"
            self.update(dt)
            self.render()
            self.clock.tick(60)
        print("Game loop ended.")
        return "QUIT"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event detected.")
                self.running = False
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.menu_button.rect.collidepoint(event.pos):
                        print("Main menu button clicked")
                        return "MAIN_MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed, opening pause menu")
                    return self.show_pause_menu()
                elif event.key == pygame.K_i:
                    print("I key pressed, opening inventory")
                    self.show_inventory()
                elif event.key == pygame.K_q:
                    print("Q key pressed, showing quest log")
                    self.show_quest_log()
                print(f"Key pressed: {pygame.key.name(event.key)}")
                if self.current_dialog:
                    self.handle_dialog_input(event.key)
                elif self.current_conversation:
                    self.handle_conversation_input(event.key)
                elif event.key == pygame.K_SPACE:
                    self.handle_interaction()
                else:
                    self.handle_player_movement(event.key)

    def show_pause_menu(self):
        pause_menu = PauseMenu(self.screen)
        choice = pause_menu.run()
        if choice == "RESUME":
            return None
        elif choice == "SAVE_GAME":
            self.save_game()
        elif choice == "LOAD_GAME":
            self.load_game()
        elif choice == "QUIT_TO_MAIN_MENU":
            return "MAIN_MENU"
        elif choice == "QUIT":
            return "QUIT"
        return None

    def show_inventory(self):
        inventory_screen = InventoryScreen(self.screen, self.player)
        inventory_screen.run()

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

    def handle_conversation_input(self, key):
        if key == pygame.K_UP:
            self.current_conversation.choose_option((self.current_conversation.current_option - 1) % len(self.current_conversation.get_options()))
        elif key == pygame.K_DOWN:
            self.current_conversation.choose_option((self.current_conversation.current_option + 1) % len(self.current_conversation.get_options()))
        elif key == pygame.K_RETURN:
            self.process_conversation_choice()

    def process_conversation_choice(self):
        choice = self.current_conversation.get_options()[self.current_conversation.current_option]
        if self.current_conversation.choose_option(self.current_conversation.current_option):
            if not self.current_conversation.get_options():
                self.end_conversation()
        else:
            self.end_conversation()

    def start_conversation(self, npc):
        if npc.npc_type == "mentor":
            self.current_conversation = create_mentor_conversation()
        # Add more conversation types for other NPCs
        self.show_conversation()

    def end_conversation(self):
        self.current_conversation = None
        self.show_message("The conversation has ended.")

    def show_conversation(self):
        text = self.current_conversation.get_current_text()
        options = self.current_conversation.get_options()
        self.current_dialog = Dialog(text, options)

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
        new_x, new_y = self.player.target_x + dx, self.player.target_y + dy
        if self.map.is_walkable(int(new_x), int(new_y)):
            self.player.move(dx, dy)
            print(f"Player moving to: ({self.player.target_x}, {self.player.target_y})")
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

    def update(self, dt):
        self.player.update(dt)
        self.quest_manager.update_quests(self.player, self.difficulty_manager)
        self.minigame_manager.update()
        self.time += 1
        if self.time >= self.day_length:
            self.time = 0
            self.day += 1
            self.player.energy = min(100, self.player.energy + 50)  # Rest at night
            debug_print(f"New day: {self.day}")
        
        self.check_time_events()
        difficulty = self.difficulty_manager.calculate_difficulty()
        self.economy.update(difficulty)
        self.difficulty_manager.update_player_level(self.player)

    def check_time_events(self):
        if self.current_event_index < len(self.time_events):
            event_time, event_function = self.time_events[self.current_event_index]
            if self.time >= event_time:
                event_function()
                self.current_event_index += 1

    def morning_event(self):
        debug_print("Morning event triggered")
        self.show_message("The sun rises. A new day begins!")
        # Add morning-specific events here

    def noon_event(self):
        debug_print("Noon event triggered")
        self.show_message("It's noon. The city is bustling with activity.")
        # Add noon-specific events here

    def evening_event(self):
        debug_print("Evening event triggered")
        self.show_message("The sun is setting. Businesses are closing for the day.")
        # Add evening-specific events here

    def night_event(self):
        debug_print("Night event triggered")
        self.show_message("Night has fallen. Time to rest and prepare for tomorrow.")
        # Add night-specific events here

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
                         (int(self.player.x * self.cell_size), int(self.player.y * self.cell_size), self.cell_size, self.cell_size))
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
        # Create a semi-transparent overlay for the HUD
        hud_surface = pygame.Surface((800, 100), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 128))
        self.screen.blit(hud_surface, (0, 0))

        font = pygame.font.Font(None, 24)
        y_offset = 10

        # Player name and day
        name_day = f"{self.player.name} - Day {self.day}"
        text = font.render(name_day, True, (255, 255, 255))
        self.screen.blit(text, (10, y_offset))
        y_offset += 25

        # Money and Energy
        money_energy = f"Money: ${self.player.money:.0f} | Energy: {self.player.energy:.0f}/100"
        text = font.render(money_energy, True, (255, 255, 255))
        self.screen.blit(text, (10, y_offset))
        y_offset += 25

        # Skills
        skills_text = "Skills: "
        for skill, value in self.player.skills.items():
            skills_text += f"{skill.capitalize()}: {value:.1f} | "
        skills_text = skills_text.rstrip(" |")
        text = font.render(skills_text, True, (255, 255, 255))
        self.screen.blit(text, (10, y_offset))
        y_offset += 25

        # Economy info
        economy_info = f"Market: {self.economy.market_state.capitalize()}, Inflation: {self.economy.inflation_rate:.2%}"
        text = font.render(economy_info, True, (255, 255, 255))
        self.screen.blit(text, (10, y_offset))
        y_offset += 25

        # Time
        time_str = f"{self.time // 60:02d}:{self.time % 60:02d}"
        text = font.render(time_str, True, (255, 255, 255))
        text_rect = text.get_rect(topright=(790, 10))
        self.screen.blit(text, text_rect)

        # Add quest log info
        active_quests = self.quest_manager.quest_log.get_active_quests()
        if active_quests:
            quest_info = f"Active Quests: {len(active_quests)}"
            text = font.render(quest_info, True, (255, 255, 255))
            self.screen.blit(text, (10, y_offset))
            y_offset += 25

    def draw_time(self):
        font = pygame.font.Font(None, 24)
        time_str = f"Day {self.day} - {self.time // 60:02d}:{self.time % 60:02d}"
        text = font.render(time_str, True, (255, 255, 255))
        self.screen.blit(text, (10, 70))

    def draw_menu_button(self):
        self.menu_button.draw(self.screen)

    def save_game(self):
        save_menu = SaveLoadMenu(self.screen, is_save_menu=True)
        slot = save_menu.run()
        if isinstance(slot, int):
            save_game(self, slot)
            self.show_message(f"Game saved to slot {slot}")
        elif slot == "QUIT":
            self.running = False

    def load_game(self):
        load_menu = SaveLoadMenu(self.screen, is_save_menu=False)
        slot = load_menu.run()
        if isinstance(slot, int):
            if load_game(self, slot):
                self.show_message(f"Game loaded from slot {slot}")
            else:
                self.show_message(f"No save file found in slot {slot}")
        elif slot == "QUIT":
            self.running = False

    def show_quest_log(self):
        active_quests = self.quest_manager.quest_log.get_active_quests()
        completed_quests = self.quest_manager.quest_log.get_completed_quests()
        
        quest_log_text = "Quest Log:\n\nActive Quests:\n"
        for quest in active_quests:
            quest_log_text += f"- {quest.name}: {quest.progress}/{quest.goal}\n"
        
        quest_log_text += "\nCompleted Quests:\n"
        for quest in completed_quests:
            quest_log_text += f"- {quest.name}\n"
        
        self.show_message(quest_log_text)