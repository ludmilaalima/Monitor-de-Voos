# bronze > silver
import json
from pipelines.storage import CreateUpdateFiles
import re
from pathlib import Path
from parsers.google_flights_parser import GoogleFlightsParser



class BronzeToSilver:
    def __init__(self):
        self.bronze_file = Path("data/bronze/bronze_flights_raw.jsonl") 
        self.parser = GoogleFlightsParser()
        self.storage = CreateUpdateFiles()
        
    

    def load_bronze(self):
        lines_raw = []

        with self.bronze_file.open('r', encoding='utf-8') as f:
            for line in f:
                line_raw = json.loads(line)
                lines_raw.append(line_raw)
    
        #### refatorar logica de list e dict
        for item in lines_raw:
            text = re.sub(r"\s+", " ", item['text']) 
            text = text.split()
            position_h = self.parser.find_h(text)
            index_price, price = self.parser.find_price(text)
            kg_index_raw = self.parser.find_kg(text, index_price)
            origin, destination = self.parser.find_iatas(text)
            parsed = self.parser.parse_card(text, position_h, price, kg_index_raw, origin, destination, item["id"], item['extracted_at'])
            if parsed:
                self.storage.update_silver(parsed)
