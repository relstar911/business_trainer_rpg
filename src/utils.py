import random
import pygame
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

def distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def is_point_inside_rect(point, rect):
    """Check if a point is inside a pygame Rect."""
    return rect.collidepoint(point)

def clamp(value, min_value, max_value):
    """Clamp a value between a minimum and maximum."""
    return max(min_value, min(value, max_value))

def lerp(start, end, t):
    """Linear interpolation between start and end values."""
    return start + (end - start) * t

def format_time(minutes):
    """Format minutes into a time string (HH:MM)."""
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"

def generate_unique_id():
    """Generate a unique identifier."""
    return f"id_{random.randint(1000, 9999)}_{random.randint(1000, 9999)}"

def load_image(path):
    """Load an image and return a pygame surface."""
    try:
        image = pygame.image.load(path)
        debug_print(f"Loaded image: {path}")
        return image
    except pygame.error:
        debug_print(f"Failed to load image: {path}")
        return None

def scale_image(image, scale):
    """Scale a pygame surface by a given factor."""
    if image:
        new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        return pygame.transform.scale(image, new_size)
    return None

def calculate_level(experience):
    """Calculate level based on experience points."""
    return int(experience ** 0.5) + 1

def experience_for_next_level(current_level):
    """Calculate total experience required to reach the next level."""
    return (current_level + 1) ** 2
