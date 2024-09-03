import random
from .debug import debug_print

class Economy:
    def __init__(self):
        self.market_state = "stable"
        self.min_inflation_rate = 0.005  # 0.5% minimum inflation rate
        self.max_inflation_rate = 0.15  # 15% maximum inflation rate
        self.inflation_rate = max(self.min_inflation_rate, min(self.max_inflation_rate, 0.02))
        self.interest_rate = 0.05
        self.stock_prices = {
            "TechCorp": 100,
            "FoodInc": 75,
            "EnergyLtd": 120,
            "FinanceGroup": 90
        }
        self.market_volatility = 0.05
        self.max_daily_change = 15  # Maximum $15 change per day
        debug_print("Initialized Economy")

    def update(self, difficulty):
        self.update_market_state()
        self.update_inflation(difficulty)
        self.update_interest_rate(difficulty)
        self.update_stock_prices(difficulty)

    def update_market_state(self):
        states = ["booming", "stable", "recession"]
        change_probability = 0.05  # 5% chance to change state each update
        if random.random() < change_probability:
            new_state = random.choice(states)
            if new_state != self.market_state:
                self.market_state = new_state
                debug_print(f"Market state changed to: {self.market_state}")
                self.apply_market_state_effects()

    def apply_market_state_effects(self):
        if self.market_state == "booming":
            self.market_volatility = 0.07
            self.inflation_rate = min(self.max_inflation_rate, self.inflation_rate * 1.2)
        elif self.market_state == "recession":
            self.market_volatility = 0.09
            self.inflation_rate = max(self.min_inflation_rate, self.inflation_rate * 0.8)
        else:  # stable
            self.market_volatility = 0.05
            # Inflation rate remains unchanged

        debug_print(f"Market volatility set to: {self.market_volatility}")
        debug_print(f"Inflation rate adjusted to: {self.inflation_rate:.2%}")

    def update_inflation(self, difficulty):
        change = random.uniform(-0.005, 0.005) * difficulty
        self.inflation_rate = max(self.min_inflation_rate, min(self.max_inflation_rate, self.inflation_rate + change))
        debug_print(f"Inflation rate updated to: {self.inflation_rate:.2%}")

    def update_interest_rate(self, difficulty):
        if self.market_state == "booming":
            self.interest_rate = min(0.1, self.interest_rate + 0.005 * difficulty)
        elif self.market_state == "recession":
            self.interest_rate = max(0.01, self.interest_rate - 0.005 * difficulty)
        debug_print(f"Interest rate updated to: {self.interest_rate:.2%}")

    def update_stock_prices(self, difficulty):
        for stock in self.stock_prices:
            base_change = random.uniform(-5, 5) * difficulty * self.market_volatility
            if self.market_state == "booming":
                base_change += 2 * difficulty
            elif self.market_state == "recession":
                base_change -= 2 * difficulty
            
            # Limit the change to the maximum daily change
            change = max(min(base_change, self.max_daily_change), -self.max_daily_change)
            
            new_price = self.stock_prices[stock] + change
            self.stock_prices[stock] = max(1, new_price)  # Ensure the price doesn't go below 1
        debug_print(f"Stock prices updated: {self.stock_prices}")

    def get_loan_interest_rate(self, credit_score):
        return self.interest_rate + (1 - credit_score / 100) * 0.05

    def apply_inflation(self, price):
        return price * (1 + self.inflation_rate)