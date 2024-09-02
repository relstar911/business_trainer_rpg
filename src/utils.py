import random
from .debug import debug_print

def generate_random_name():
    """Generate a random name for NPCs or businesses."""
    first_names = ["John", "Jane", "Mike", "Sarah", "Alex", "Emma"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    debug_print(f"Generated random name: {name}")
    return name

def calculate_success_chance(skill_level):
    """Calculate success chance based on skill level."""
    chance = min(0.95, 0.3 + (skill_level * 0.1))
    debug_print(f"Calculated success chance: {chance:.2f} for skill level {skill_level}")
    return chance

def format_money(amount):
    """Format money amount with commas and two decimal places."""
    formatted = f"${amount:,.2f}"
    debug_print(f"Formatted money amount: {formatted}")
    return formatted
