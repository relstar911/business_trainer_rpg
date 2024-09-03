import pygame
from .debug import debug_print

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(float(x), float(y), width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Dialog:
    def __init__(self, text, options=None):
        self.text = text
        self.options = options or []
        self.current_option = 0
        self.text_index = 0
        self.text_speed = 1  # Changed from 2 to 1
        self.finished_text = False

    def update(self):
        if not self.finished_text:
            self.text_index += self.text_speed
            if self.text_index >= len(self.text):
                self.finished_text = True
                self.text_index = len(self.text)

    def draw(self, screen):
        # Draw dialog box
        pygame.draw.rect(screen, (255, 255, 255), (50, 400, 700, 150), 0)
        pygame.draw.rect(screen, (0, 0, 0), (50, 400, 700, 150), 2)

        # Draw text
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text[:self.text_index], True, (0, 0, 0))
        screen.blit(text_surface, (60, 410))

        # Draw options if text is finished
        if self.finished_text and self.options:
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.current_option else (0, 0, 0)
                option_surface = font.render(option, True, color)
                screen.blit(option_surface, (60, 450 + i * 30))

    def move_selection(self, direction):
        if self.options:  # Check for non-empty options
            if len(self.options) > 0:  # Additional check to prevent division by zero
                self.current_option = (self.current_option + direction) % len(self.options)
            else:
                self.current_option = 0  # Reset to 0 if options list is empty

    def get_selected_option(self):
        return self.options[self.current_option]

class ConversationWindow:
    def __init__(self, conversation_tree, npc_name):
        self.conversation_tree = conversation_tree
        self.npc_name = npc_name
        self.font = pygame.font.Font(None, 24)
        self.selected_option = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (50, 50, 700, 500))
        text = self.font.render(f"{self.npc_name}: {self.conversation_tree.get_current_text()}", True, (0, 0, 0))
        screen.blit(text, (60, 60))

        options = self.conversation_tree.get_options()
        for i, option in enumerate(options):
            color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
            option_text = self.font.render(option, True, color)
            screen.blit(option_text, (60, 100 + i * 30))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.conversation_tree.get_options())
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.conversation_tree.get_options())
            elif event.key == pygame.K_RETURN:
                self.conversation_tree.choose_option(self.selected_option)
                self.selected_option = 0
            elif event.key == pygame.K_ESCAPE:
                return "CLOSE"
        return None

class UI:
    def __init__(self, screen, player):
        # ... other UI elements ...
        self.inventory_button = Button(700, 10, 90, 30, "Inventory", (100, 100, 100), (255, 255, 255))

    def draw(self, screen):
        # ... draw other UI elements ...
        self.inventory_button.draw(screen)

    def handle_event(self, event, game):
        # ... handle other UI events ...
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.inventory_button.rect.collidepoint(event.pos):
                    game.current_screen = "inventory"

class PlayerInfoUI:
    def __init__(self, player):
        self.player = player
        self.energy_text = f"Energy: {player.energy:.1f}/{player.max_energy}"
        self.sprint_text = "Sprinting" if player.sprinting else "Walking"

    def update(self, player):
        self.energy_text = f"Energy: {player.energy:.1f}/{player.max_energy}"
        self.sprint_text = "Sprinting" if player.sprinting else "Walking"

    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        energy_text = font.render(f"Energy: {self.player.energy:.1f}/{self.player.max_energy}", True, (255, 255, 255))
        money_text = font.render(f"Money: ${self.player.money}", True, (255, 255, 255))
        sprint_text = font.render("Sprinting" if self.player.sprinting else "Walking", True, (255, 255, 255))
        
        screen.blit(energy_text, (10, 10))
        screen.blit(money_text, (10, 40))
        screen.blit(sprint_text, (10, 70))
