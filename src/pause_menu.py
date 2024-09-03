import pygame
from .ui import Button
from .debug import debug_print

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button(300, 200, 200, 50, "Resume", (100, 100, 100), (255, 255, 255)),
            Button(300, 275, 200, 50, "Save Game", (100, 100, 100), (255, 255, 255)),
            Button(300, 350, 200, 50, "Load Game", (100, 100, 100), (255, 255, 255)),
            Button(300, 425, 200, 50, "Quit to Main Menu", (100, 100, 100), (255, 255, 255)),
            Button(300, 500, 200, 50, "Quit Game", (100, 100, 100), (255, 255, 255))
        ]
        debug_print("Pause menu initialized")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "RESUME"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for button in self.buttons:
                            if button.rect.collidepoint(event.pos):
                                return button.text.upper().replace(" ", "_")

            self.draw(self.screen)
            pygame.display.flip()

    def draw(self, screen):
        screen.fill((0, 0, 0, 128))  # Semi-transparent black background
        font = pygame.font.Font(None, 64)
        title = font.render("Paused", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 100))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)