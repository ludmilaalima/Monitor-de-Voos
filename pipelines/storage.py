import re
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import shortuuid
import json



class CreateUpdateFiles:
    def __init__(self):
        # bronze - raw
        data_bronze_raw =  Path("data/bronze/bronze_flights_raw.jsonl") 
        self.data_bronze_raw = Path(data_bronze_raw)

        # silver 
        data='data/silver/silver_flights.csv'
        self.data_silver = Path(data)


    def create_storage(self):

        if self.data_bronze_raw.exists() :
            open(self.data_bronze_raw, 'a', encoding='utf-8').close()


        if self.data_silver.exists():
    
            df = pd.DataFrame(columns=['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601', 'duration_minutes', 'num_stops', 'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"])
            df.to_csv(self.data_silver, index=False, encoding='utf-8-sig')


    def update_bronze(self, text):

        date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        id = shortuuid.uuid()[:8]

        register = {'id': id, "extracted_at": date, 'text': text}
        with open(self.data_bronze_raw, 'a', encoding='utf-8') as f:
            f.write(json.dumps(register, ensure_ascii=False) + '\n')




    def update_silver(self, id, origin_iata, destination_iata, departure_time_local, arrival_time_local, main_airline, all_airlines,  duration_iso8601,  duration_minutes, num_stops, emissions_raw,  price, extracted_at):


        kg_index = emissions_raw[0]
        kg_index_raw = " ".join(kg_index_raw)

        new_line = {
            'id': id,
            'origin_iata': origin_iata,
            'destination_iata': destination_iata, 
            'departure_time_local' : departure_time_local,
            'arrival_time_local': arrival_time_local,
            'main_airline': main_airline,
            'all_airlines': all_airlines,
            'duration_iso8601': duration_iso8601, 
            'duration_minutes': duration_minutes,
            'num_stops': int(num_stops), 
            'emissions_raw': kg_index_raw,
            'emissions_co2e_kg': kg_index,
            'price': price,
            "extracted_at": extracted_at
        }


        pd.DataFrame([new_line], columns = ['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601',  'duration_minutes', 'num_stops',  'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"]).to_csv(
            self.data_silver, mode='a', header=False, index=False, encoding='utf-8'
        )
        