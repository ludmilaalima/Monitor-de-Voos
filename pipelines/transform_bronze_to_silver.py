# bronze > silver
import json
from pipelines.storage import CreateUpdateFiles
import re

create_update_files = CreateUpdateFiles() # DIFERENCA ENTRE AQUI E FORA

class BronzeToSilver:
    def __init__(self):
        self.bronze_file = r"data/bronze/bronze_flights_raw.jsonl"
        
    

    def load_bronzer(self):
        data = json.loads(self.bronze_file)

        for data['text'] in data:
            text = re.sub(r"\s+", " ", text) 
            text = text.split()
            position_h = create_update_files.find_h(text)
            index_price, price = create_update_files.find_price(text)
            kg_index_raw = create_update_files.find_kg(text, index_price)
            origin, destination = create_update_files.find_iatas(text)
            print(text)
            create_update_files.extract_card(text, position_h, price, kg_index_raw, origin, destination, id, data['extracted_at'])

