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
        data_bronze_raw =  Path("data/bronze/bronze_flights_raw_CPVeCNF.jsonl") 
        self.data_bronze_raw = Path(data_bronze_raw)

        # silver 
        data= Path('data/silver/silver_flights_CPVeCNF.csv')
        self.data_silver = Path(data)

        #checkpoint
        self.checkpoint = Path("data/checkpoints/bronze_flights_raw_CPVeCNF.offset")


    def create_storage(self):

        if not self.data_bronze_raw.exists():
            open(self.data_bronze_raw, 'a', encoding='utf-8').close()


        if not self.data_silver.exists():
    
            df = pd.DataFrame(columns=['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601', 'duration_minutes', 'num_stops', 'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"])
            df.to_csv(self.data_silver, index=False, encoding='utf-8-sig')
        
        
        if not self.checkpoint.exists():
            self.checkpoint.write_text('0', encoding='utf-8')



    def update_bronze(self, text):

        extracted_at = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        id = shortuuid.uuid()[:8]

        register = {'id': id, "extracted_at": extracted_at, 'text': text}
        with open(self.data_bronze_raw, 'a', encoding='utf-8') as f:
            f.write(json.dumps(register, ensure_ascii=False) + '\n')

            


    def update_silver(self, id, origin_iata, destination_iata, departure_time_local, arrival_time_local, main_airline, all_airlines,  duration_iso8601,  duration_minutes, num_stops, emissions_raw,  price, extracted_at):


        #kg_index = emissions_raw[0]
        #kg_index_raw = " ".join(kg_index_raw)

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
            'emissions_raw': 0,
            'emissions_co2e_kg': 0,
            'price': price,
            "extracted_at": extracted_at
        }


        pd.DataFrame([new_line], columns = ['id', 'origin_iata', 'destination_iata', 'departure_time_local', 'arrival_time_local', 'main_airline', 'all_airlines', 'duration_iso8601',  'duration_minutes', 'num_stops',  'emissions_raw', 'emissions_co2e_kg', 'price', "extracted_at"]).to_csv(
            self.data_silver, mode='a', header=False, index=False, encoding='utf-8'
        )
        