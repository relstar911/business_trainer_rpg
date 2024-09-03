import random
import pygame
import time
from .player import Player
from .npc import NPC
from .map import Map
from .quest import QuestManager
from .minigame import MinigameManager
from .economy import Economy
from .difficulty import DifficultyManager
from .inventory import InventoryScreen
from .debug import debug_print, info_print, warning_print, error_print
from .ui import ConversationWindow, Button, Dialog
from .save_load import save_game, load_game
from .pause_menu import PauseMenu
from .item import Item
from .utils import format_money, calculate_success_chance
from .conversation import create_mentor_conversation, create_investor_conversation, create_customer_conversation, create_competitor_conversation

class Game:
    def __init__(self, screen):
        self.screen = screen
        pygame.init()
        pygame.display.set_caption("Business Trainer RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.screen_width, self.screen_height = screen.get_size()
        self.player = Player("Entrepreneur", self.screen_width // 2, self.screen_height // 2)
        self.map = Map(40, 30)  # Keeping the original smaller map dimensions
        self.npcs = [
            NPC("Mentor Mike", self.screen_width * 0.25, self.screen_height * 0.25, "mentor", self.map),
            NPC("Investor Ivy", self.screen_width * 0.75, self.screen_height * 0.5, "investor", self.map),
            NPC("Customer John", self.screen_width * 0.375, self.screen_height * 0.375, "customer", self.map),
            NPC("Competitor Sam", self.screen_width * 0.625, self.screen_height * 0.625, "competitor", self.map)
        ]
        self.quest_manager = QuestManager()
        self.minigame_manager = MinigameManager()
        self.economy = Economy()
        self.difficulty_manager = DifficultyManager()
        self.inventory_screen = InventoryScreen(self.screen, self.player)
        self.current_dialog = None
        self.pause_menu = PauseMenu(self.screen)
        self.day = 1
        self.time = 0
        self.day_length = 1440  # 24 hours in minutes
        self.items = [
            Item("Money Bag", self.screen_width * 0.125, self.screen_height * 0.125, "money"),
            Item("Energy Drink", self.screen_width * 0.5, self.screen_height * 0.375, "energy"),
            Item("Skill Book", self.screen_width * 0.875, self.screen_height * 0.625, "skill")
        ]
        self.interaction_target = None
        self.current_conversation = None
        self.menu_button = Button(10, self.screen_height - 30, 150, 20, "Main Menu", (100, 100, 100), (255, 255, 255))
        self.status_message = ""
        self.last_update_time = time.time()
        self.dt = 0
        self.current_minigame = None
        self.message = None
        self.message_timer = 0
        self.message_duration = 3000  # 3 seconds
        self.last_economy_update = time.time()
        self.last_npc_update = time.time()
        self.economy_update_interval = 5  # Update economy every 5 seconds
        self.npc_update_interval = 1  # Update NPCs every 1 second
        self.buildings = {
            "office": {"pos": (self.screen_width * 0.125, self.screen_height * 0.125), "size": (80, 60)},
            "market": {"pos": (self.screen_width * 0.375, self.screen_height * 0.125), "size": (80, 60)},
            "home": {"pos": (self.screen_width * 0.625, self.screen_height * 0.125), "size": (80, 60)}
        }
        self.time_events = [
            (360, self.morning_event),
            (720, self.noon_event),
            (1080, self.evening_event),
            (1320, self.night_event)
        ]
        self.current_event_index = 0
        info_print("Game initialized.")

    def run(self, dt):
        info_print("Starting game loop...")
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
            
            action = self.handle_events()
            if action == "PAUSE":
                self.toggle_pause()
                pause_result = self.show_pause_menu()
                if pause_result == "RESUME":
                    self.toggle_pause()
                elif pause_result == "MAIN_MENU":
                    self.reset_game_state()
                    self.running = False
                    return "MAIN_MENU"
                elif pause_result == "QUIT":
                    self.reset_game_state()
                    self.running = False
                    return "QUIT"
            elif action == "MAIN_MENU":
                self.reset_game_state()
                self.running = False
                return "MAIN_MENU"
            elif action == "QUIT":
                info_print("Quitting game")
                return "QUIT"
            
            self.update(dt)
            self.render()

        info_print("Game loop ended.")
        return "QUIT"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                info_print("Quit event detected.")
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.menu_button.rect.collidepoint(event.pos):
                        info_print("Main menu button clicked")
                        return "PAUSE"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    info_print("Escape key pressed, opening pause menu")
                    return "PAUSE"
                elif event.key == pygame.K_i:
                    info_print("I key pressed, opening inventory")
                    self.show_inventory()
                elif event.key == pygame.K_q:
                    info_print("Q key pressed, showing quest log")
                    self.show_quest_log()
                elif event.key == pygame.K_SPACE:
                    self.handle_interaction()
                elif event.key == pygame.K_y:
                    self.player.start_sprint()
                debug_print(f"Key pressed: {pygame.key.name(event.key)}")
                if self.current_dialog:
                    self.handle_dialog_input(event.key)
                elif self.current_conversation:
                    self.handle_conversation_input(event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_y:
                    self.player.stop_sprint()

        if not self.paused:
            # Handle continuous movement only when not paused
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            if dx != 0 or dy != 0:
                self.player.move(dx, dy, self.map)

        return None

    def update(self, dt):
        current_time = time.time()
        
        if current_time - self.last_economy_update >= self.economy_update_interval:
            self.economy.update(self.difficulty_manager.calculate_difficulty())
            self.last_economy_update = current_time
            debug_print("Economy updated", force=True)

        if current_time - self.last_npc_update >= self.npc_update_interval:
            for npc in self.npcs:
                npc.update(dt)
            for item in self.items:
                item.update()
            self.last_npc_update = current_time
            debug_print("NPCs and items updated", force=True)

        self.player.update(dt)
        self.quest_manager.update_quests(self.player, self.difficulty_manager)
        self.minigame_manager.update()
        self.time += dt * 60  # Convert dt to minutes
        if self.time >= self.day_length:
            self.time = 0
            self.day += 1
            self.player.energy = min(100, self.player.energy + 50)
            info_print(f"New day: {self.day}")
        
        self.check_time_events()
        self.difficulty_manager.update_difficulty(self.player)

        if self.current_minigame:
            self.current_minigame.update()
            if self.current_minigame.is_finished():
                self.end_minigame()
        if self.message_timer > 0:
            self.message_timer -= dt * 1000  # Convert dt to milliseconds
            if self.message_timer <= 0:
                self.message = None

        self.check_interactions()

        if self.player.energy <= 0:
            self.show_message("You're out of energy! Rest to recover.")
            # Implement a resting mechanism or other way to recover energy

    def render(self):
        if not self.paused:
            # Render game elements
            self.map.draw(self.screen)
            for item in self.items:
                item.draw(self.screen)
            self.player.draw(self.screen)
            for npc in self.npcs:
                npc.draw(self.screen)
            if self.current_dialog:
                self.current_dialog.draw(self.screen)
            self.draw_player_info()
            self.draw_time()
            if self.message:
                self.draw_message()
            self.menu_button.draw(self.screen)
            for name, building in self.buildings.items():
                pygame.draw.rect(self.screen, (100, 100, 150), pygame.Rect(building["pos"], building["size"]))
                font = pygame.font.Font(None, 20)
                text = font.render(name, True, (255, 255, 255))
                self.screen.blit(text, (building["pos"][0], building["pos"][1] - 20))
        else:
            # Render pause menu
            self.pause_menu.draw(self.screen)

        pygame.display.flip()

    def check_interactions(self):
        self.interaction_target = None
        for npc in self.npcs:
            if npc.is_in_range(self.player):
                self.interaction_target = npc
                break
        
        if not self.interaction_target:
            location = self.map.get_location(self.player.rect.x, self.player.rect.y)
            if location:
                self.interaction_target = location

    def handle_interaction(self):
        info_print("Handling interaction...")
        if self.interaction_target:
            if isinstance(self.interaction_target, NPC):
                info_print(f"Interacting with NPC: {self.interaction_target.name}")
                self.start_conversation(self.interaction_target)
            elif isinstance(self.interaction_target, str):  # Location
                info_print(f"Interacting with location: {self.interaction_target}")
                self.handle_location_interaction(self.interaction_target)
        else:
            info_print("No interaction target.")
            self.show_message("There's nothing to interact with here.")

    def start_conversation(self, npc):
        if npc.npc_type == "mentor":
            self.current_conversation = create_mentor_conversation()
        elif npc.npc_type == "investor":
            self.current_conversation = create_investor_conversation()
        elif npc.npc_type == "customer":
            self.current_conversation = create_customer_conversation()
        elif npc.npc_type == "competitor":
            self.current_conversation = create_competitor_conversation()
        self.show_conversation()

    def handle_location_interaction(self, location):
        if location == "office":
            self.start_work_minigame()
        elif location == "market":
            self.open_market_menu()
        elif location == "home":
            self.player.rest()

    def start_work_minigame(self):
        minigame = self.minigame_manager.get_random_minigame()
        result = self.minigame_manager.play_minigame(self, minigame)
        if result is None:
            self.show_message("Minigame interrupted.")
        elif result:
            success_chance = calculate_success_chance(self.player.skills["business"])
            if random.random() < success_chance:
                reward = 100 * self.difficulty_manager.current_difficulty
                self.player.money += reward
                self.show_message(f"Great job! You earned {format_money(reward)} from your work.")
            else:
                self.show_message("You completed the task, but it didn't yield the expected results. Keep improving!")
        else:
            self.show_message("You didn't perform well at work. Try again tomorrow.")

    def open_market_menu(self):
        minigame = self.minigame_manager.get_random_minigame()
        result = self.minigame_manager.play_minigame(self, minigame)
        if result is None:
            self.show_message("Marketing campaign interrupted.")
        elif result:
            success_chance = calculate_success_chance(self.player.skills["marketing"])
            if random.random() < success_chance:
                skill_increase = 0.1 * self.difficulty_manager.current_difficulty
                self.player.skills["marketing"] += skill_increase
                self.show_message(f"Your marketing efforts were successful! Marketing skill increased by {skill_increase:.2f}")
            else:
                self.show_message("Your campaign was completed but didn't have the desired impact. Keep practicing!")
        else:
            self.show_message("Your marketing campaign didn't go as planned. Keep practicing!")

    def show_inventory(self):
        self.inventory_screen.run()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            return "PAUSE"
        else:
            return "RESUME"

    def show_pause_menu(self):
        return self.pause_menu.run()

    def check_item_pickup(self):
        for item in self.items[:]:
            if self.player.rect.colliderect(item.rect):
                self.inventory_screen.add_item(item)
                self.items.remove(item)
                self.show_message(f"You picked up a {item.name}!")

    def use_item(self, item_name):
        if self.inventory_screen.remove_item(item_name):
            # Apply item effect
            for item in self.items:
                if item.name == item_name:
                    message = item.apply_effect(self.player)
                    self.show_message(message)
                    break

    def show_message(self, message):
        info_print(f"Showing message: {message}")
        self.message = message
        self.message_timer = self.message_duration

    def draw_player_info(self):
        font = pygame.font.Font(None, 24)
        money_text = font.render(f"Money: {format_money(self.player.money)}", True, (255, 255, 255))
        energy_text = font.render(f"Energy: {self.player.energy:.0f}/100", True, (255, 255, 255))
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(energy_text, (10, 40))

    def draw_time(self):
        font = pygame.font.Font(None, 24)
        time_str = f"Day {self.day} - {int(self.time) // 60:02d}:{int(self.time) % 60:02d}"
        text = font.render(time_str, True, (255, 255, 255))
        self.screen.blit(text, (10, 70))

    def draw_message(self):
        if self.message:
            font = pygame.font.Font(None, 32)
            text = font.render(self.message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 550))
            pygame.draw.rect(self.screen, (0, 0, 0, 128), text_rect.inflate(20, 20))
            self.screen.blit(text, text_rect)

    def check_time_events(self):
        if self.current_event_index < len(self.time_events):
            event_time, event_function = self.time_events[self.current_event_index]
            if self.time >= event_time:
                event_function()
                self.current_event_index += 1

    def morning_event(self):
        info_print("Morning event triggered")
        self.status_message = "The sun rises. A new day begins!"

    def noon_event(self):
        info_print("Noon event triggered")
        self.status_message = "It's noon. The city is bustling with activity."
    def evening_event(self):
        info_print("Evening event triggered")
        self.status_message = "The sun is setting. Businesses are closing for the day."

    def night_event(self):
        info_print("Night event triggered")
        self.status_message = "Night has fallen. Time to rest and prepare for tomorrow."
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

    def handle_dialog_input(self, key):
        if self.current_dialog:
            if key == pygame.K_RETURN:
                self.current_dialog = None
            # Add more dialog input handling as needed

    def handle_conversation_input(self, key):
        if self.current_conversation:
            if key == pygame.K_UP:
                self.current_conversation.move_selection(-1)
            elif key == pygame.K_DOWN:
                self.current_conversation.move_selection(1)
            elif key == pygame.K_RETURN:
                self.process_conversation_choice()

    def process_conversation_choice(self):
        if self.current_conversation.choose_option(self.current_conversation.get_selected_option()):
            self.show_conversation()
        else:
            self.end_conversation()

    def show_conversation(self):
        text = self.current_conversation.get_current_text()
        options = self.current_conversation.get_options()
        self.current_dialog = Dialog(text, options)

    def end_conversation(self):
        self.current_conversation = None
        self.current_dialog = None

    def save_game_state(self, slot):
        from .save_load import save_game  # Import the save_game function

        save_data = {
            "player": {
                "name": self.player.name,
                "x": self.player.x,
                "y": self.player.y,
                "money": self.player.money,
                "energy": self.player.energy,
                "skills": self.player.skills,
                "inventory": [{"name": item.name, "quantity": item.quantity} for item in self.player.inventory]
            },
            "day": self.day,
            "time": self.time,
            "items": [{"name": item.name, "x": item.rect.x, "y": item.rect.y, "item_type": item.item_type} for item in self.items],
            "npcs": [{"name": npc.name, "x": npc.x, "y": npc.y, "npc_type": npc.npc_type} for npc in self.npcs],
            "quests": self.quest_manager.get_save_data(),
            "economy": {
                "market_state": self.economy.market_state,
                "inflation_rate": self.economy.inflation_rate,
                "interest_rate": self.economy.interest_rate,
                "stock_prices": self.economy.stock_prices
            },
            "difficulty": self.difficulty_manager.current_difficulty
        }
        save_game(save_data, slot)  # Pass 'save_data' to save_game function
        self.show_message(f"Game saved to slot {slot}")
        # Add any penalties or effects here