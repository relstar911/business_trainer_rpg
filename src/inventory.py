import pygame
from .ui import Button
from .debug import debug_print

class InventoryItem:
    def __init__(self, item, quantity=1):
        self.name = item.name
        self.item = item
        self.quantity = quantity

class InventoryScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 32)
        self.items = []
        self.back_button = Button(650, 550, 100, 40, "Back", (100, 100, 100), (255, 255, 255))
        debug_print("Initialized InventoryScreen")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.back_button.rect.collidepoint(event.pos):
                            running = False

            self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Inventory", True, (255, 255, 255))
        self.screen.blit(title, (20, 20))

        y = 80
        for inv_item in self.items:
            text = self.font.render(f"{inv_item.name} x{inv_item.quantity}", True, (255, 255, 255))
            self.screen.blit(text, (20, y))
            y += 40

        money_text = self.font.render(f"Money: ${self.player.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (20, 500))

        self.back_button.draw(self.screen)

    def add_item(self, item):
        for inv_item in self.items:
            if inv_item.name == item.name:
                inv_item.quantity += 1
                debug_print(f"Added {item.name} to inventory. New quantity: {inv_item.quantity}")
                return
        new_inv_item = InventoryItem(item)
        self.items.append(new_inv_item)
        debug_print(f"Added new item {item.name} to inventory. Quantity: 1")

    def remove_item(self, item_name, quantity=1):
        for inv_item in self.items:
            if inv_item.name == item_name:
                if inv_item.quantity < quantity:
                    debug_print(f"Cannot remove {quantity} {item_name}(s) from inventory: only {inv_item.quantity} available")
                    return False
                elif inv_item.quantity == quantity:
                    self.items.remove(inv_item)
                    debug_print(f"Removed all {quantity} {item_name}(s) from inventory")
                else:
                    inv_item.quantity -= quantity
                    debug_print(f"Removed {quantity} {item_name}(s) from inventory. New quantity: {inv_item.quantity}")
                return True
        debug_print(f"Failed to remove {item_name} from inventory: item not found")
        return False