import os

class DataBase:
    """Guarda as chaves e IDS fixos importantes"""
    def __init__(self):
        self.apy_key = os.environ.get("API_KEY")
        self.internal_id = os.environ.get("INTERNAL_ID")
        self.extern_id = os.environ.get("EXTERNAL_ID")
