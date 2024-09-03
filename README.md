# Business Trainer RPG

![Game Logo](assets/images/logo.png)

## Project Description

Business Trainer RPG is an engaging role-playing game where players step into the shoes of an aspiring entrepreneur. Navigate the complex world of business, interact with various NPCs, complete challenging quests, and participate in exciting minigames to build your business empire!

## Features

- Immersive business world to explore
- Dynamic NPC interactions with expanded conversation trees
- Complex business management simulation
- Engaging quests and challenges with integrated minigames
- Character progression and skill development system
- Dynamic economy system with market states and stock prices
- Adaptive difficulty system
- Save and load game progress
- Sprint functionality (Hold 'Y' to sprint)
- Energy management system for player actions
- Detailed map with various locations and obstacles

## Recent Changes

- Implemented a dynamic economy system with market states, inflation, and stock prices
- Added an adaptive difficulty system that adjusts based on player performance
- Enhanced the quest system with integrated minigames
- Improved NPC interactions with more complex conversation trees
- Implemented energy management for player movement and actions
- Added sprint functionality for faster player movement
- Enhanced save/load system to include more game state information

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/business_trainer_rpg.git
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
  - `character.py`: Base character class
  - `npc.py`: Non-player character interactions
  - `map.py`: Game world and environment
  - `quest.py`: Quest system and management
  - `minigame.py`: Minigame implementations
  - `economy.py`: Economic system simulation
  - `difficulty.py`: Adaptive difficulty management
  - `conversation.py`: Conversation system for NPCs
  - `ui.py`: User interface elements
  - `utils.py`: Utility functions
  - `debug.py`: Debugging utilities
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

## Debugging

The game uses a custom debugging system. To enable or disable debug output, modify the `DEBUG` variable in `src/debug.py`. You can also adjust the logging level to control the verbosity of the output.

To use debug printing in your code:

```
from .debug import logger

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error")
```