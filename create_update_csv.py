import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import shortuuid



class CreateUpdateCsv:
    def __init__(self):
        data='data.csv'
        self.data_link = Path(data)

    def create_csv(self):
        if "data.csv" not in os.listdir(Path.cwd()):
    
            df = pd.DataFrame(columns=['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601', 'duration_minutes', 'num_stops', 'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"])
            df.to_csv("data.csv", index=False, encoding='utf-8-sig')
           

    def update_csv(self, element, escale, main_airline, all_airlines, price, kg_index_raw, origin_iata, destination_iatas, duration_iso8601, duration_minutes):
        
        date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        id = shortuuid.uuid()[:8]

        kg_index = kg_index_raw[0]
        kg_index_raw = " ".join(kg_index_raw)

        new_line = {
            'id': id,
            'origin_iata': origin_iata,
            'destination_iata': destination_iatas, 
            'departure_time_local' : element[0],
            'arrival_time_local': element[2],
            'main_airline': main_airline,
            'all_airlines': all_airlines,
            'duration_iso8601': duration_iso8601, 
            'duration_minutes': duration_minutes,
            'num_stops': int(escale), 
            'emissions_raw': kg_index_raw,
            'emissions_co2e_kg': kg_index,
            'price': price,
            "extracted_at": date
        }

        pd.DataFrame([new_line], columns = ['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601',  'duration_minutes', 'num_stops',  'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"]).to_csv(
            self.data_link, mode='a', header=False, index=False, encoding='utf-8'
        )
        