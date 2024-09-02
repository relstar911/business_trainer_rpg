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

    def get_current_text(self):
        return self.current_node.text

    def get_options(self):
        return [option[0] for option in self.current_node.options]

    def choose_option(self, index):
        if 0 <= index < len(self.current_node.options):
            self.current_node = self.current_node.options[index][1]
            return True
        return False

    def reset(self):
        self.current_node = self.root

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

# Add more conversation trees for other NPC types