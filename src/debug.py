import time

DEBUG = True
LOG_LEVEL = "INFO"  # Can be "DEBUG", "INFO", "WARNING", or "ERROR"

class DebugLogger:
    def __init__(self):
        self.last_time = time.time()
        self.update_counts = {"QuestManager": 0, "MinigameManager": 0}

    def log(self, level, message):
        if DEBUG and self.should_log(level):
            current_time = time.time()
            print(f"[{level}] [{current_time - self.last_time:.2f}s] {message}")
            self.last_time = current_time

    def should_log(self, level):
        levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        return levels.index(level) >= levels.index(LOG_LEVEL)

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)

    def update(self, manager_name):
        self.update_counts[manager_name] += 1
        if self.update_counts[manager_name] % 100 == 0:
            self.debug(f"{manager_name} updated {self.update_counts[manager_name]} times")

logger = DebugLogger()

def debug_print(message):
    logger.debug(message)
