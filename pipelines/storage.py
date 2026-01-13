import re
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import shortuuid
import json


KNOW_AIRLINES = ['AZUL', 'LATAM', 'GOL']

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
    

    def find_h(text):
        position_h = 0

        for i in range(3, len(text)):
            extract = text[i]
            find_h = re.search(r'\b\d+h\b', extract)

            if find_h:
                break
            else:
                position_h += 1

        return position_h


    def find_price(text):
        for i, string in enumerate(text):
            if 'R$' in string:
                return i, text[i+1]
        return None, None
        

    def find_kg(text, price_index):
        for i, string in enumerate(text):
            if 'kg' in string:
                return text[i-1:price_index]
        
        return None, None
            
    def find_iatas(text):
        for string in text:
            match = re.search(r'\b([A-Z]{3})\s*[-–—]\s*([A-Z]{3})\b', string)
            if match:
                origin_iata = match.group(1)
                destination_iata = match.group(2)
                return origin_iata, destination_iata
        

        return None, None
    
    def extract_airlines(raw_airline, know_airlines=KNOW_AIRLINES):
        if raw_airline is None:
            return None, None

        if isinstance(raw_airline, list):
            raw_airline = " ".join(raw_airline)

        raw_airline = raw_airline.upper()


        found = []
        for airline in know_airlines:
            if airline in raw_airline:
                found.append(airline) 

        raw_airline = raw_airline.split()
        all_airlines = []
        for string in raw_airline: # GOL, LATAN, AZUL
            for know_airline in found: # AZUL, LATAM, GOL
                if know_airline in string:
                    if know_airline in all_airlines:
                        continue
                    all_airlines.append(know_airline)

        main_airline = all_airlines[0]
        all_airlines = " | ".join(all_airlines)

        return main_airline, all_airlines

            
    def extract_card(self, text, position_h, price, kg_index_raw, origin, destination, id, extracted_at):
        
        kwargs = {}
        all_airline_name = ''
        
        airline_name_start = 3
        airline_name_end = airline_name_start + position_h 
        # inicio e fim da string 
        if position_h > 1:
            all_airline_name = text[airline_name_start:airline_name_end]
        else:
            all_airline_name = text[3]

        # quantas paradas 
        escale = ''
        for i in range(0, len(text)): 
            if text[i] == 'Sem':
                escale = 0
            elif text[i] in ('parada', 'paradas'):
                escale = text[i-1]


        # aeroporto inicial e final
        raw_airline = all_airline_name
        main_airline, all_airlines = self.extract_airlines(raw_airline)


        #duration iso8601
        hour = text[airline_name_end]
        minute = text[airline_name_end+1]

        if len(minute) > 3:
            minute = 00

        print(f"{hour} {minute}")

        # consertar horas 
        hour = hour.replace("h", "")

        kwargs["id"] = id
        kwargs['extracted_at'] = extracted_at
        kwargs["main_airline"] = main_airline
        kwargs["all_airlines"] = all_airlines
        kwargs["price"] = float(price)
        kwargs["kg_index_raw"] = kg_index_raw
        kwargs["origin_iata"] = origin
        kwargs["destination_iata"] = destination
        kwargs["duration_iso8601"] = f"PT{hour}H{minute}M"
        kwargs["duration_minutes"] = int(hour) * 60 + int(minute)

        
        # campos obrigatorios
        check_all = [id, origin, destination, price, text[0], text[2]]
        all_not_null = all(v is not None for v in check_all)

        if all_not_null:
            self.update_silver(text, escale, **kwargs)



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
        