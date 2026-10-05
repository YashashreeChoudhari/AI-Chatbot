conversation = []

MAX_HISTORY = 20

def add_user_message(message):
    conversation.append({
        "role": "user",
        "message": message
    })

    trim_history()


def add_ai_message(message):
    conversation.append({
        "role": "assistant",
        "message": message
    })

    trim_history()


def get_conversation():
    return conversation


def trim_history():
    global conversation
    conversation = conversation[-MAX_HISTORY:]


# NEW FUNCTION
def clear_history():
    global conversation
    conversation.clear()