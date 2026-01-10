# bronze > silver
import json



class BronzeToSilver:
    def __init__(self):
        self.bronze_file = r"data/bronze/bronze_flights_raw.jsonl"

    

    def load_bronzer(self):
        data = json.loads(self.bronze_file)