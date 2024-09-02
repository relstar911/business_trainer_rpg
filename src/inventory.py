import pygame
from .ui import Button
from .debug import debug_print

class InventoryScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.buttons = [
            Button(650, 500, 120, 50, "Close", (100, 100, 100), (255, 255, 255))
        ]
        debug_print("Inventory screen initialized")

    def run(self):
        debug_print("Running inventory screen")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for button in self.buttons:
                            if button.rect.collidepoint(event.pos):
                                if button.text == "Close":
                                    running = False

            self.render()
            pygame.display.flip()

    def render(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Draw inventory title
        title = self.font.render("Inventory", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)

        # Draw inventory items
        for i, item in enumerate(self.player.inventory):
            item_text = self.small_font.render(f"{item.name} ({item.item_type})", True, (255, 255, 255))
            self.screen.blit(item_text, (50, 100 + i * 30))

        # Draw close button
        for button in self.buttons:
            button.draw(self.screen)