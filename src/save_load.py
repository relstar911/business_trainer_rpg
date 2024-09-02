import json
import os

from src.npc import NPC
from src.quest import Quest
from .debug import debug_print
from .item import Item  # Add this import

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
        },
        "day": game_state.day,
        "time": game_state.time,
        "items": [{"name": item.name, "x": item.x, "y": item.y, "item_type": item.item_type} for item in game_state.items],
        "npcs": [{"name": npc.name, "x": npc.x, "y": npc.y, "npc_type": npc.npc_type} for npc in game_state.npcs],
        "quests": [{"name": quest.name, "description": quest.description, "reward": quest.reward, "completed": quest.completed} for quest in game_state.quest_manager.quests],
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
    
    game_state.day = save_data["day"]
    game_state.time = save_data["time"]
    
    game_state.items = [
        Item(item["name"], item["x"], item["y"], item["item_type"])
        for item in save_data["items"]
    ]
    
    game_state.npcs = [
        NPC(npc["name"], npc["x"], npc["y"], npc["npc_type"])
        for npc in save_data["npcs"]
    ]
    
    game_state.quest_manager.quests = [
        Quest(quest["name"], quest["description"], quest["reward"])
        for quest in save_data["quests"]
    ]
    for quest, saved_quest in zip(game_state.quest_manager.quests, save_data["quests"]):
        quest.completed = saved_quest["completed"]
    
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