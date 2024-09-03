from .debug import debug_print

class ConversationNode:
    def __init__(self, text, options=None):
        self.text = text
        self.options = options or []

    def add_option(self, text, next_node):
        self.options.append((text, next_node))

class ConversationTree:
    def __init__(self, root_node):
        self.root = root_node
        self.current_node = root_node
        self.current_option = 0

    def get_current_text(self):
        return self.current_node.text

    def get_options(self):
        return [option[0] for option in self.current_node.options]

    def choose_option(self, index):
        if 0 <= index < len(self.current_node.options):
            self.current_node = self.current_node.options[index][1]
            self.current_option = 0
            return True
        return False

    def move_selection(self, direction):
        options = self.get_options()
        if options:  # Check if there are any options
            num_options = len(options)
            self.current_option = (self.current_option + direction + num_options) % num_options
        else:
            self.current_option = 0  # Reset to 0 if there are no options
        debug_print(f"Moved selection to option {self.current_option}")

    def get_selected_option(self):
        return self.current_option if self.get_options() else None

    def reset(self):
        self.current_node = self.root
        self.current_option = 0
        # If debug_print is not available, use a fallback print statement
        try:
            debug_print("Conversation tree reset")
        except NameError:
            print("Debug: Conversation tree reset")

def create_mentor_conversation():
    root = ConversationNode("Hello! What would you like to learn about today?")
    business_node = ConversationNode("Business is all about creating value for customers. What specific area interests you?")
    marketing_node = ConversationNode("Marketing is crucial for business success. It's about understanding and meeting customer needs.")
    finance_node = ConversationNode("Finance is the lifeblood of any business. It's important to manage your cash flow effectively.")

    root.add_option("Tell me about business", business_node)
    root.add_option("I want to learn about marketing", marketing_node)
    root.add_option("Can you explain finance?", finance_node)

    business_node.add_option("Thanks, that's helpful", root)
    marketing_node.add_option("I see, thank you", root)
    finance_node.add_option("Got it, thanks", root)

    return ConversationTree(root)

def create_investor_conversation():
    root = ConversationNode("Hello! I'm always on the lookout for promising investments. What can you tell me about your business?")
    pitch_node = ConversationNode("That sounds interesting. Can you give me more details about your business model?")
    financials_node = ConversationNode("I see. What about your financial projections?")
    closing_node = ConversationNode("Thank you for the information. I'll consider your proposal and get back to you.")

    root.add_option("Pitch my business idea", pitch_node)
    root.add_option("Discuss financial needs", financials_node)
    root.add_option("Ask about investment criteria", closing_node)

    pitch_node.add_option("Provide more details", financials_node)
    pitch_node.add_option("Ask for advice", closing_node)

    financials_node.add_option("Share projections", closing_node)
    financials_node.add_option("Ask about expected returns", closing_node)

    closing_node.add_option("Thank you for your time", root)

    return ConversationTree(root)

def create_customer_conversation():
    root = ConversationNode("Hi there! I'm interested in your products/services. Can you tell me more?")
    product_node = ConversationNode("That sounds good. What makes your product/service unique?")
    price_node = ConversationNode("Interesting. Can you tell me about your pricing?")
    closing_node = ConversationNode("Thank you for the information. I'll think about it and may come back later.")

    root.add_option("Explain our products/services", product_node)
    root.add_option("Discuss pricing", price_node)
    root.add_option("Ask about their needs", closing_node)

    product_node.add_option("Highlight features", price_node)
    product_node.add_option("Compare to competitors", closing_node)

    price_node.add_option("Explain pricing structure", closing_node)
    price_node.add_option("Mention any discounts", closing_node)

    closing_node.add_option("Thank you for your interest", root)

    return ConversationTree(root)

def create_competitor_conversation():
    root = ConversationNode("Hello there! I've noticed your business in the market. How's it going for you?")
    market_node = ConversationNode("The market is quite competitive, isn't it? What's your take on recent trends?")
    strategy_node = ConversationNode("Interesting perspective. How do you differentiate your business?")
    closing_node = ConversationNode("It's been great chatting. Let's keep in touch about industry developments.")

    root.add_option("Discuss market conditions", market_node)
    root.add_option("Ask about their strategy", strategy_node)
    root.add_option("Propose a collaboration", closing_node)

    market_node.add_option("Share market insights", strategy_node)
    market_node.add_option("Ask about challenges", closing_node)

    strategy_node.add_option("Discuss innovation", closing_node)
    strategy_node.add_option("Talk about customer base", closing_node)

    closing_node.add_option("Exchange contact information", root)

    return ConversationTree(root)

# Add more conversation trees for other NPC types