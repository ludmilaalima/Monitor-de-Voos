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
    
            df = pd.DataFrame(columns=['id', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601', 'destination_iata', 'num_stops', 'origin_iata','emissions_co2e_kg', 'price', "extracted_at"])
            df.to_csv("data.csv", index=False, encoding='utf-8-sig')
           

    def update_csv(self, element, escale, main_airline=None, all_airlines=None):
        
        date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        id = shortuuid.uuid()[:8]


        new_line = {
            'id': id,
            'departure_time_local' : element[0],
            'arrival_time_local': element[2],
            'main_airline': main_airline ,
            'all_airlines': all_airlines,
            'duration_iso8601': element[4:6], 
            'destination_iata': 0, 
            'num_stops': 0 if escale == 'Sem' else escale, 
            'origin_iata': 0,
            'emissions_co2e_kg': element[10:11],
            'price': element[18],
            "extracted_at": date
        }

        pd.DataFrame([new_line], columns = ['id', 'departure_time_local', 'arrival_time_local', 'airline_name', 'duration_iso8601', 'destination_iata', 'num_stops', 'origin_iata', 'emissions_co2e_kg', 'price', "extracted_at"]).to_csv(
            self.data_link, mode='a', header=False, index=False, encoding='utf-8'
        )
        