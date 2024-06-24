from datetime import datetime

@staticmethod
def get_time() -> str:
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")