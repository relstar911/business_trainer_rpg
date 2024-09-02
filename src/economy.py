import random
from .debug import debug_print

class Economy:
    def __init__(self):
        self.market_state = "stable"
        self.inflation_rate = 0.02
        self.interest_rate = 0.05
        self.stock_prices = {
            "TechCorp": 100,
            "FoodInc": 75,
            "EnergyLtd": 120,
            "FinanceGroup": 90
        }
        self.market_volatility = 0.1

    def update(self, difficulty):
        self.update_market_state()
        self.update_inflation(difficulty)
        self.update_interest_rate(difficulty)
        self.update_stock_prices(difficulty)

    def update_market_state(self):
        states = ["booming", "stable", "recession"]
        if random.random() < 0.1:  # 10% chance to change state
            self.market_state = random.choice(states)
            debug_print(f"Market state changed to: {self.market_state}")

    def update_inflation(self, difficulty):
        change = random.uniform(-0.005, 0.005) * difficulty
        self.inflation_rate = max(0, min(0.15, self.inflation_rate + change))
        debug_print(f"Inflation rate updated to: {self.inflation_rate:.2%}")

    def update_interest_rate(self, difficulty):
        if self.market_state == "booming":
            self.interest_rate = min(0.1, self.interest_rate + 0.005 * difficulty)
        elif self.market_state == "recession":
            self.interest_rate = max(0.01, self.interest_rate - 0.005 * difficulty)
        debug_print(f"Interest rate updated to: {self.interest_rate:.2%}")

    def update_stock_prices(self, difficulty):
        for stock in self.stock_prices:
            change = random.uniform(-5, 5) * difficulty * self.market_volatility
            if self.market_state == "booming":
                change += 2 * difficulty
            elif self.market_state == "recession":
                change -= 2 * difficulty
            self.stock_prices[stock] = max(1, self.stock_prices[stock] + change)
        debug_print(f"Stock prices updated: {self.stock_prices}")

    def get_loan_interest_rate(self, credit_score):
        return self.interest_rate + (1 - credit_score / 100) * 0.05

    def apply_inflation(self, price):
        return price * (1 + self.inflation_rate)