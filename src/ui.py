import pygame
from .debug import debug_print

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
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
    def __init__(self, text, options):
        debug_print(f"Creating dialog: {text}")
        self.text = text
        self.options = options
        self.selected_option = 0

    def draw(self, screen):
        debug_print("Drawing dialog")
        # Draw dialog background
        pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 400))
        
        # Draw text
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 250))
        screen.blit(text_surface, text_rect)

        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (200, 200, 200)
            option_surface = font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(400, 350 + i * 40))
            screen.blit(option_surface, option_rect)

        # Draw instruction
        instruction = font.render("Use arrow keys to select, SPACE to confirm", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(400, 500))
        screen.blit(instruction, instruction_rect)

    def move_selection(self, direction):
        self.selected_option = (self.selected_option + direction) % len(self.options)
        debug_print(f"Dialog selection moved to: {self.get_selected_option()}")

    def get_selected_option(self):
        return self.options[self.selected_option]
