import pygame
from src.game import Game
from src.menu import MainMenu
from src.debug import debug_print
from src.save_menu import SaveLoadMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Business Trainer RPG")
    clock = pygame.time.Clock()

    game = None
    running = True
    while running:
        menu = MainMenu(screen)
        choice = menu.run()

        if choice == "NEW_GAME":
            debug_print("Starting new game")
            game = Game()
            game_result = game.run()
            if game_result == "QUIT":
                running = False
        elif choice == "LOAD_GAME":
            debug_print("Loading game")
            load_menu = SaveLoadMenu(screen, is_save_menu=False)
            slot = load_menu.run()
            if isinstance(slot, int):
                game = Game()
                if game.load_game(slot):
                    game_result = game.run()
                    if game_result == "QUIT":
                        running = False
        elif choice == "SAVE_GAME":
            if game:
                debug_print("Saving game")
                game.save_game()
            else:
                debug_print("No active game to save")
        elif choice == "QUIT":
            debug_print("Quitting game")
            running = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
