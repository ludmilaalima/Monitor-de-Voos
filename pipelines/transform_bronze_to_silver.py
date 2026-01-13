# bronze > silver
import json
from pipelines.storage import CreateUpdateFiles
import re
from pathlib import Path



class BronzeToSilver:
    def __init__(self):
        self.bronze_file = Path("data/bronze/bronze_flights_raw.jsonl")
        self.create_update_files = CreateUpdateFiles() 
        
    

    def load_bronzer(self):
        lines_raw = []

        with self.bronze_file.open('r', encoding='utf-8') as f:
            for line in f:
                line_raw = json.loads(line)
                lines_raw.append(line_raw)
    
        #### refatorar logica de list e dict
        for line in lines_raw['text']:
            text = re.sub(r"\s+", " ", text) 
            text = text.split()
            position_h = self.create_update_files.find_h(text)
            index_price, price = self.create_update_files.find_price(text)
            kg_index_raw = self.create_update_files.find_kg(text, index_price)
            origin, destination = self.create_update_files.find_iatas(text)
            print(text)
            self.create_update_files.extract_card(text, position_h, price, kg_index_raw, origin, destination, line, line['extracted_at'])

