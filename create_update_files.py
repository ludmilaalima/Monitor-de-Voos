import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import shortuuid
import json



class CreateUpdateFiles:
    def __init__(self):
        # bronze - raw
        data_bronze_raw =  'bronze_flights_raw.jsonl'
        self.data_bronze_raw = Path(data_bronze_raw)

        # silver 
        data='silver_flights.csv'
        self.data_silver = Path(data)


        

    def create_storage(self):

        if self.data_bronze_raw.name not in os.listdir(Path.cwd()):
            open(self.data_bronze_raw, 'a', encoding='utf-8').close()


        if self.data_silver.name not in os.listdir(Path.cwd()):
    
            df = pd.DataFrame(columns=['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601', 'duration_minutes', 'num_stops', 'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"])
            df.to_csv(self.data_silver, index=False, encoding='utf-8-sig')



    def save_bronze(self, text):


        date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        id = shortuuid.uuid()[:8]

        register = {'id': id, "extracted_at": date, 'text': text}
        with open(self.data_bronze_raw, 'a', encoding='utf-8') as f:
            f.write(json.dumps(register, ensure_ascii=False) + '\n')


        return id, date


    def update_silver(self, text, escale, id, extracted_at, main_airline, all_airlines, price, kg_index_raw, origin_iata, destination_iata, duration_iso8601, duration_minutes):



        kg_index = kg_index_raw[0]
        kg_index_raw = " ".join(kg_index_raw)

        new_line = {
            'id': id,
            'origin_iata': origin_iata,
            'destination_iata': destination_iata, 
            'departure_time_local' : text[0],
            'arrival_time_local': text[2],
            'main_airline': main_airline,
            'all_airlines': all_airlines,
            'duration_iso8601': duration_iso8601, 
            'duration_minutes': duration_minutes,
            'num_stops': int(escale), 
            'emissions_raw': kg_index_raw,
            'emissions_co2e_kg': kg_index,
            'price': price,
            "extracted_at": extracted_at
        }


        pd.DataFrame([new_line], columns = ['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601',  'duration_minutes', 'num_stops',  'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"]).to_csv(
            self.data_silver, mode='a', header=False, index=False, encoding='utf-8'
        )
        