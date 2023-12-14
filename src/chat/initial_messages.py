from .Message import Message


def init_message_history() -> None:
    return [
        (Message(role="assistant", message=x)).toLLMDict()
        for x in [
            "Hi there! I'm Lisa, your digital product advisor. 😊",
            "I'm here to find a suitable laptop for you. Let's go through a few questions to help me understand your preferences...",
            "Let's start: What do you usually use your laptop for?",
        ]
    ]
