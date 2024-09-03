# Business Trainer RPG

![Game Logo](assets/images/logo.png)

## Project Description

Business Trainer RPG is an engaging role-playing game where players step into the shoes of an aspiring entrepreneur. Navigate the complex world of business, interact with various NPCs, complete challenging quests, and participate in exciting minigames to build your business empire!

## Features

- Immersive business world to explore
- Dynamic NPC interactions with expanded conversations
- Business management simulation
- Engaging quests and challenges
- Fun minigames to test your skills
- Character progression and skill development
- Save and load game progress
- Toggle button to enhance player movement speed
- Sprint functionality (Hold 'Y' to sprint)
- Highly detailed map for precise movement
- Smooth, physics-based movement system
- NPCs with simple up-and-down movement and obstacle avoidance

## Recent Changes

- Improved NPC interactions with expanded conversation trees
- Implemented Pokemon-style dialog system
- Added minigames to quests for more engaging gameplay
- Separated items from NPCs for better world layout
- Improved interaction range for NPCs

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/relstar911/business_trainer_rpg.git
   ```
2. Navigate to the project directory:
   ```
   cd business_trainer_rpg
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\Activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Run the Game

1. Ensure your virtual environment is activated.
2. Run the game:
   ```
   python main.py
   ```

## Project Structure

- `main.py`: Entry point of the game
- `src/`: Source code directory
  - `game.py`: Main game loop and logic
  - `player.py`: Player character management
  - `world.py`: Game world and environment
  - `npc.py`: Non-player character interactions
  - `quest.py`: Quest system
  - `minigame.py`: Minigame implementations
  - `ui.py`: User interface elements
  - `utils.py`: Utility functions
- `assets/`: Game assets (images, sounds, fonts)
- `data/`: Game data (quests, NPCs, minigames)
- `tests/`: Unit tests

## Contributing

We welcome contributions to the Business Trainer RPG project! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to Pygame for providing the game development framework
- Inspiration drawn from classic business simulation games
- Special thanks to all contributors and playtesters

## Contact

For any questions or feedback, please open an issue on this repository or contact the maintainer at [your-email@example.com].

Happy gaming and business building!

## Development Workflow

When making changes to the Business Trainer RPG codebase, please follow this checklist to ensure all relevant files are updated:

1. **Update Core Game Logic**
   - [ ] src/game.py
   - [ ] src/player.py
   - [ ] src/character.py
   - [ ] src/npc.py
   - [ ] src/map.py

2. **Update Game Systems**
   - [ ] src/quest.py
   - [ ] src/minigame.py
   - [ ] src/utils.py

3. **Update User Interface**
   - [ ] src/ui.py

4. **Update Data Files** (if applicable)
   - [ ] data/quests.json
   - [ ] data/npcs.json
   - [ ] data/minigames.json

5. **Update Main Entry Point**
   - [ ] main.py

6. **Update Tests** (if applicable)
   - [ ] tests/test_game.py
   - [ ] tests/test_player.py
   - [ ] Any other relevant test files

7. **Update Documentation**
   - [ ] README.md
   - [ ] Any other documentation files

8. **Review and Test**
   - [ ] Run the game to ensure all changes work as expected
   - [ ] Run all tests to ensure nothing was broken

9. **Commit Changes**
   - [ ] Stage all updated files
   - [ ] Commit with a descriptive message of the changes made

## Debugging

The game uses a custom debugging system. To enable or disable debug output, modify the `DEBUG` variable in `src/debug.py`. You can also adjust the `LOG_LEVEL` to control the verbosity of the output.

Debug levels:
- DEBUG: Most verbose, shows all debug messages
- INFO: Shows informational messages and above
- WARNING: Shows warnings and errors
- ERROR: Shows only error messages

To use debug printing in your code:

```
from .debug import logger

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error")
```