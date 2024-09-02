import pygame

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

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Dialog:
    def __init__(self, text, options):
        self.text = text
        self.options = options
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        button_width = 100
        button_height = 40
        spacing = 20
        total_width = len(self.options) * button_width + (len(self.options) - 1) * spacing
        start_x = (800 - total_width) // 2
        y = 400

        for i, option in enumerate(self.options):
            x = start_x + i * (button_width + spacing)
            self.buttons.append(Button(x, y, button_width, button_height, option, (200, 200, 200), (0, 0, 0)))

    def draw(self, screen):
        # Draw dialog background
        pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 400))
        
        # Draw text
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 250))
        screen.blit(text_surface, text_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_clicked(event.pos):
                    return button.text
        return None

    def show(self, screen):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                result = self.handle_input(event)
                if result:
                    return result

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)
