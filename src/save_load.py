import json
import os

from src.inventory import InventoryItem
from src.npc import NPC
from src.quest import Quest, QuestManager
from .debug import debug_print
from .item import Item  # Add this import
from .npc import NPC
from .quest import Quest

SAVE_FOLDER = "saves"
MAX_SLOTS = 5

def ensure_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        debug_print(f"Created save folder: {SAVE_FOLDER}")

def save_game(game_state, slot):
    ensure_save_folder()
    filename = os.path.join(SAVE_FOLDER, f"save_{slot}.json")
    
    save_data = {
        "player": {
            "name": game_state.player.name,
            "x": game_state.player.x,
            "y": game_state.player.y,
            "money": game_state.player.money,
            "energy": game_state.player.energy,
            "skills": game_state.player.skills,
            "sprinting": game_state.player.sprinting,
            "sprint_speed": game_state.player.sprint_speed,
            "move_energy_cost": game_state.player.move_energy_cost,
            "sprint_energy_cost": game_state.player.sprint_energy_cost,
            "inventory": [{"name": item.name, "quantity": item.quantity} for item in game_state.inventory_screen.items],
        },
        "day": game_state.day,
        "time": game_state.time,
        "items": [{"name": item.name, "x": item.x, "y": item.y, "item_type": item.item_type} for item in game_state.items],
        "npcs": [{"name": npc.name, "x": npc.x, "y": npc.y, "npc_type": npc.npc_type} for npc in game_state.npcs],
        "quests": game_state.quest_manager.get_save_data(),
        "economy": {
            "market_state": game_state.economy.market_state,
            "inflation_rate": game_state.economy.inflation_rate,
            "interest_rate": game_state.economy.interest_rate,
            "stock_prices": game_state.economy.stock_prices
        },
        "difficulty": game_state.difficulty_manager.current_difficulty
    }
    
    with open(filename, 'w') as f:
        json.dump(save_data, f)
    
    debug_print(f"Game saved to slot {slot}")

def load_game(game_state, slot):
    filename = os.path.join(SAVE_FOLDER, f"save_{slot}.json")
    
    if not os.path.exists(filename):
        debug_print(f"No save file found in slot {slot}")
        return False
    
    with open(filename, 'r') as f:
        save_data = json.load(f)
    
    # Update game state with loaded data
    game_state.player.name = save_data["player"]["name"]
    game_state.player.x = save_data["player"]["x"]
    game_state.player.y = save_data["player"]["y"]
    game_state.player.money = save_data["player"]["money"]
    game_state.player.energy = save_data["player"]["energy"]
    game_state.player.skills = save_data["player"]["skills"]
    
    game_state.player.sprinting = save_data["player"]["sprinting"]
    game_state.player.sprint_speed = save_data["player"]["sprint_speed"]
    game_state.player.move_energy_cost = save_data["player"]["move_energy_cost"]
    game_state.player.sprint_energy_cost = save_data["player"]["sprint_energy_cost"]
    
    game_state.day = save_data["day"]
    game_state.time = save_data["time"]
    
    game_state.items = [
        Item(item["name"], item["x"], item["y"], item["item_type"])
        for item in save_data["items"]
    ]
    
    # Ensure game_state.map is initialized before loading NPCs
    if game_state.map is None:
        debug_print("Warning: game_state.map is not initialized. NPCs may not be loaded correctly.")
    
    game_state.npcs = []
    for npc in save_data["npcs"]:
        try:
            new_npc = NPC(npc["name"], npc["x"], npc["y"], npc["npc_type"], game_state.map)
            game_state.npcs.append(new_npc)
        except Exception as e:
            debug_print(f"Error loading NPC {npc['name']}: {str(e)}")
    
    # Load quests
    game_state.quest_manager.load_save_data(save_data["quests"])
    
    # Load inventory
    game_state.inventory_screen.items = [
        InventoryItem(Item(item["name"], 0, 0, ""), item["quantity"])
        for item in save_data["inventory"]
    ]
    
    debug_print(f"Game loaded from slot {slot}")
    return True

def get_save_slots():
    ensure_save_folder()
    save_files = [f for f in os.listdir(SAVE_FOLDER) if f.startswith("save_") and f.endswith(".json")]
    return [int(f.split("_")[1].split(".")[0]) for f in save_files]

def get_save_info(slot):
    filename = os.path.join(SAVE_FOLDER, f"save_{slot}.json")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            save_data = json.load(f)
        return f"Slot {slot}: Day {save_data['day']}, ${save_data['player']['money']}"
    return f"Slot {slot}: Empty"