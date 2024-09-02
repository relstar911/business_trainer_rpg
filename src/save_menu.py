import pygame
from .ui import Button
from .debug import debug_print
from .save_load import get_save_slots, get_save_info, MAX_SLOTS

class SaveLoadMenu:
    def __init__(self, screen, is_save_menu=True):
        self.screen = screen
        self.is_save_menu = is_save_menu
        self.buttons = []
        self.create_buttons()
        debug_print(f"{'Save' if is_save_menu else 'Load'} menu initialized")

    def create_buttons(self):
        self.buttons = []
        for i in range(1, MAX_SLOTS + 1):
            y_pos = 100 + i * 60
            self.buttons.append(Button(300, y_pos, 200, 50, f"Slot {i}", (100, 100, 100), (255, 255, 255)))
        self.buttons.append(Button(300, 500, 200, 50, "Back", (100, 100, 100), (255, 255, 255)))

    def run(self):
        debug_print(f"Running {'save' if self.is_save_menu else 'load'} menu")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for i, button in enumerate(self.buttons):
                            if button.rect.collidepoint(event.pos):
                                if i < MAX_SLOTS:
                                    debug_print(f"Slot {i+1} selected")
                                    return i + 1
                                else:
                                    debug_print("Back button clicked")
                                    return "BACK"

            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 64)
        title = font.render("Save Game" if self.is_save_menu else "Load Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)

        for i, button in enumerate(self.buttons):
            button.draw(self.screen)
            if i < MAX_SLOTS:
                info_font = pygame.font.Font(None, 24)
                info_text = info_font.render(get_save_info(i+1), True, (200, 200, 200))
                self.screen.blit(info_text, (button.rect.right + 10, button.rect.centery - 12))