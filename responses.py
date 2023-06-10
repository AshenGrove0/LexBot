import random as r

def get_response(message) -> str:
    processed_message = message.lower()

    if processed_message == "hello there!":
        return "General Kenobi"
        
    
    if processed_message == "have you heard of the tale of darth plagueis the wise?":
        return "No, it's not a story the Jedi have told me"


    if processed_message == "roll":
        return str(r.randint(1,6))

    if processed_message == "!help":
        return "`This is a help answer!`"

