import random

def generate_random_name():
    """Generate a random name for NPCs or businesses."""
    first_names = ["John", "Jane", "Mike", "Sarah", "Alex", "Emma"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def calculate_success_chance(skill_level):
    """Calculate success chance based on skill level."""
    return min(0.95, 0.3 + (skill_level * 0.1))

def format_money(amount):
    """Format money amount with commas and two decimal places."""
    return f"${amount:,.2f}"
