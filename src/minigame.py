import random

import pygame
from .debug import debug_print, error_print
from .utils import calculate_success_chance

class Minigame:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.score = 0
        debug_print(f"Created new minigame: {name} (difficulty: {difficulty})")

    def setup(self):
        pass

    def update(self, events):
        pass

    def draw(self, screen):
        pass

    def is_finished(self):
        return True

    def get_result(self):
        success_chance = calculate_success_chance(self.difficulty)
        return random.random() < success_chance

class BusinessQuizMinigame(Minigame):
    def __init__(self, difficulty):
        super().__init__("Business Quiz", difficulty)
        self.questions = self.generate_questions()
        self.current_question = 0
        self.selected_answer = None
        self.finished = False

    def generate_questions(self):
        # Add more questions and adjust difficulty
        questions = [
            {"question": "What does ROI stand for?", "answers": ["Return on Investment", "Rate of Inflation", "Risk of Insolvency", "Retail Operating Income"], "correct": 0},
            {"question": "Which of these is not a type of business organization?", "answers": ["Sole Proprietorship", "Partnership", "Corporation", "Friendship"], "correct": 3},
            {"question": "What is the primary goal of a business?", "answers": ["Maximize profit", "Provide employment", "Pay taxes", "Produce goods"], "correct": 0},
            {"question": "What does B2B stand for in business?", "answers": ["Back to Business", "Business to Business", "Business to Buyer", "Buyer to Business"], "correct": 1},
            {"question": "Which financial statement shows a company's assets, liabilities, and equity?", "answers": ["Income Statement", "Cash Flow Statement", "Balance Sheet", "Equity Statement"], "correct": 2},
        ]
        random.shuffle(questions)
        return questions[:self.difficulty + 2]  # Number of questions based on difficulty

    def update(self, events):
        if self.is_finished():
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    self.selected_answer = event.key - pygame.K_1
                elif event.key == pygame.K_RETURN and self.selected_answer is not None:
                    if self.selected_answer == self.questions[self.current_question]["correct"]:
                        self.score += 1
                    self.current_question += 1
                    self.selected_answer = None
                    if self.current_question >= len(self.questions):
                        self.finished = True

    def draw(self, screen):
        font = pygame.font.Font(None, 32)
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            text = font.render(question["question"], True, (255, 255, 255))
            screen.blit(text, (50, 50))
            for i, answer in enumerate(question["answers"]):
                color = (255, 255, 0) if i == self.selected_answer else (200, 200, 200)
                text = font.render(f"{i+1}. {answer}", True, color)
                screen.blit(text, (50, 100 + i * 40))
        else:
            text = font.render(f"Quiz completed! Score: {self.score}/{len(self.questions)}", True, (255, 255, 255))
            screen.blit(text, (50, 50))

    def is_finished(self):
        return self.finished

class MarketingCampaignMinigame(Minigame):
    def __init__(self, difficulty):
        super().__init__("Marketing Campaign", difficulty)
        self.target_audience = random.choice(["Young Adults", "Families", "Seniors", "Professionals"])
        self.budget = 1000 * difficulty
        self.channels = {"TV": 0, "Social Media": 0, "Print": 0, "Radio": 0}
        self.effectiveness = {"TV": 0.8, "Social Media": 1.2, "Print": 0.6, "Radio": 0.7}

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.channels["TV"] += 100
                elif event.key == pygame.K_2:
                    self.channels["Social Media"] += 100
                elif event.key == pygame.K_3:
                    self.channels["Print"] += 100
                elif event.key == pygame.K_4:
                    self.channels["Radio"] += 100

        total_spent = sum(self.channels.values())
        if total_spent > self.budget:
            for channel in self.channels:
                self.channels[channel] = int(self.channels[channel] * (self.budget / total_spent))

        self.score = sum(amount * self.effectiveness[channel] for channel, amount in self.channels.items())

    def draw(self, screen):
        font = pygame.font.Font(None, 32)
        text = font.render(f"Target Audience: {self.target_audience}", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        text = font.render(f"Budget: ${self.budget}", True, (255, 255, 255))
        screen.blit(text, (50, 90))
        for i, (channel, amount) in enumerate(self.channels.items()):
            text = font.render(f"{i+1}. {channel}: ${amount}", True, (200, 200, 200))
            screen.blit(text, (50, 130 + i * 40))
        text = font.render(f"Campaign Effectiveness: {self.score:.2f}", True, (255, 255, 0))
        screen.blit(text, (50, 290))

class MinigameManager:
    def __init__(self):
        self.minigames = [BusinessQuizMinigame, MarketingCampaignMinigame]
        debug_print("Initialized MinigameManager")

    def get_random_minigame(self):
        minigame_class = random.choice(self.minigames)
        return minigame_class(difficulty=1)  # Default difficulty to 1

    def play_minigame(self, game, minigame):
        if not hasattr(game, 'screen'):
            error_print("Error: game object does not have a screen attribute")
            return None

        if not isinstance(game.screen, pygame.Surface):
            error_print("Error: game.screen is not a valid pygame Surface")
            return None

        minigame.setup()
        clock = pygame.time.Clock()
        running = True
        while running and not minigame.is_finished():
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    debug_print("Quit event detected during minigame")
                    return None  # Indicate that the game was quit
            
            minigame.update(events)
            
            game.screen.fill((0, 0, 0))
            minigame.draw(game.screen)
            pygame.display.flip()
            clock.tick(60)
        
        if running:
            result = minigame.get_result()
            debug_print(f"Minigame completed with result: {result}")
            return result
        else:
            debug_print("Minigame interrupted")
            return None

    def update(self):
        debug_print("MinigameManager update called")
