import pygame
from src.game import Game
from src.debug import debug_print, info_print
from src.menu import MainMenu
from src.pause_menu import PauseMenu
from src.save_menu import SaveLoadMenu
from src.save_load import save_game, load_game
import time

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Business Trainer RPG")

    info_print("Game started")

    clock = pygame.time.Clock()
    running = True
    game = None

    while running:
        menu = MainMenu(screen)
        choice = menu.run()

        if choice == "NEW_GAME":
            debug_print("Starting new game")
            game = Game(screen)  # Pass the screen here
            game_result = run_game(game, screen, clock)
            if game_result == "QUIT":
                running = False
            elif game_result == "MAIN_MENU":
                game = None
                last_update_time = time.time()  # Reset time when returning to main menu
        elif choice == "LOAD_GAME":
            debug_print("Loading game")
            load_menu = SaveLoadMenu(screen, is_save_menu=False)
            slot = load_menu.run()
            if isinstance(slot, int):
                game = Game(screen)
                if load_game(game, slot):
                    game_result = run_game(game, screen, clock)
                    if game_result == "QUIT":
                        running = False
                    elif game_result == "MAIN_MENU":
                        game = None
        elif choice == "SAVE_GAME":
            if game:
                debug_print("Saving game")
                save_menu = SaveLoadMenu(screen, is_save_menu=True)
                slot = save_menu.run()
                if isinstance(slot, int):
                    save_game(game, slot)
            else:
                debug_print("No game to save")
        elif choice == "QUIT":
            debug_print("Quitting game")
            running = False

    pygame.quit()
    info_print("Game ended")

def run_game(game, screen, clock):
    last_update_time = time.time()
    while True:
        current_time = time.time()
        dt = current_time - last_update_time
        last_update_time = current_time

        result = game.run(dt)
        if result == "PAUSE":
            pause_menu = PauseMenu(screen)
            pause_result = pause_menu.run()
            if pause_result == "RESUME":
                last_update_time = time.time()  # Reset time after resuming
                continue
            elif pause_result == "SAVE_GAME":
                save_menu = SaveLoadMenu(screen, is_save_menu=True)
                slot = save_menu.run()
                if isinstance(slot, int):
                    save_game(game, slot)
                    last_update_time = time.time()  # Reset time after saving
            elif pause_result == "LOAD_GAME":
                load_menu = SaveLoadMenu(screen, is_save_menu=False)
                slot = load_menu.run()
                if isinstance(slot, int):
                    new_game = Game(screen)
                    if load_game(new_game, slot):
                        game = new_game
                        last_update_time = time.time()  # Reset time after loading
            elif pause_result == "QUIT_TO_MAIN_MENU":
                return "MAIN_MENU"
            elif pause_result == "QUIT":
                return "QUIT"
        elif result == "QUIT":
            return "QUIT"
        elif result == "MAIN_MENU":
            return "MAIN_MENU"

        clock.tick(60)

if __name__ == "__main__":
    main()
