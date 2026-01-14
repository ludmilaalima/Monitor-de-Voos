
import re
KNOW_AIRLINES = ['AZUL', 'LATAM', 'GOL']


class GoogleFlightsParser:


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
    


    def parse_card(self, text, position_h, price, kg_index_raw, origin, destination, id, extracted_at):
        
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
            return (text, escale, *kwargs)