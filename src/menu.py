import pygame
from .ui import Button
from .debug import debug_print
from .save_load import get_save_slots

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button(300, 150, 200, 50, "New Game", (100, 100, 100), (255, 255, 255)),
            Button(300, 225, 200, 50, "Load Game", (100, 100, 100), (255, 255, 255)),
            Button(300, 300, 200, 50, "Save Game", (100, 100, 100), (255, 255, 255)),
            Button(300, 375, 200, 50, "Quit", (100, 100, 100), (255, 255, 255))
        ]
        debug_print("Main menu initialized")

    def run(self):
        debug_print("Running main menu")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for button in self.buttons:
                            if button.rect.collidepoint(event.pos):
                                debug_print(f"Button clicked: {button.text}")
                                return button.text.upper().replace(" ", "_")

            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 64)
        title = font.render("Business Trainer RPG", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 100))
        self.screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(self.screen)