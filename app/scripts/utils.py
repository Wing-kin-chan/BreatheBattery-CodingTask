from datetime import datetime
import string
import random

@staticmethod
def get_time() -> str:
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

@staticmethod
def generate_key() -> str:
    all_characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random string from the set of all characters
    random_string = ''.join(random.choice(all_characters) for _ in range(50))
    return str(random_string)