# AI Instructions for Business Trainer RPG

When working on this project, please adhere to the following guidelines:

## Code Structure and Style
1. Follow PEP 8 style guide for Python code.
2. Use meaningful variable and function names.
3. Write docstrings for all classes and functions.
4. Keep functions small and focused on a single task.

## Game Logic
1. All game state changes should be handled through the main `Game` class in `src/game.py`.
2. Player actions should be processed in `src/player.py`.
3. NPC interactions should be managed in `src/npc.py`.
4. Quest logic should be contained within `src/quest.py`.
5. Minigame implementations should be in `src/minigame.py`.

## Debugging
1. Use the custom debugging system in `src/debug.py` for all debug output.
2. Set appropriate log levels for different types of messages.

## UI and Graphics
1. All UI elements should be created and managed in `src/ui.py`.
2. Use consistent color schemes and font styles across the game.

## Game Balance
1. Ensure that player progression feels rewarding but challenging.
2. Balance the economy to prevent exploits or dead-ends.
3. Scale difficulty of quests and minigames with player skills.

## Content Creation
1. When adding new NPCs, quests, or minigames, ensure they fit the business theme.
2. Create diverse and interesting dialog options for NPCs.
3. Design quests that encourage exploration of different game mechanics.

## Testing
1. Write unit tests for all new functionality in the `tests/` directory.
2. Ensure all tests pass before committing changes.

## Documentation
1. Update `README.md` with any new features or changes to setup instructions.
2. Keep `dev_notes.md` updated with latest development progress and known issues.
3. Document any complex algorithms or game mechanics thoroughly.

## Version Control
1. Create descriptive commit messages.
2. Use feature branches for major additions.
3. Submit pull requests for review before merging into the main branch.

Remember, the goal is to create an engaging and educational business simulation game. All additions should contribute to this vision while maintaining code quality and game balance.
