from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path

from selenium.webdriver.chrome.options import Options
import re

from test import CreateUpdateFiles



KNOW_AIRLINES = ['AZUL', 'LATAM', 'GOL']


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

            

def extract_card(text, position_h, price, kg_index_raw, origin, destination, id, extracted_at):
    
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
    main_airline, all_airlines = extract_airlines(raw_airline)


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
        create_update_files.update_silver(text, escale, **kwargs)


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





options = Options()
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options) #abre instancia 

create_update_files = CreateUpdateFiles()
create_update_files.create_storage() 


#acessar navegador
driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI2LTAyLTE3agcIARIDRk9ScgwIAxIIL20vMGwzcTIaIxIKMjAyNi0wMi0yMWoMCAMSCC9tLzBsM3EycgcIARIDRk9SQAFIAXABggELCP___________wGYAQE&tfu=EgoIABABGAAgAigDIgMKATA')
#('https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI2LTAyLTE3agcIARIDQ1BWcgwIAxIIL20vMGwzcTIaIxIKMjAyNi0wMi0yMWoMCAMSCC9tLzBsM3EycgcIARIDQ1BWQAFIAXABggELCP___________wGYAQE&tfu=EgoIABABGAAgAigDIgMKATA')
driver.maximize_window()

# tempo para que os itens aparecam
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verificando preços de várias fontes')]")))
wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verificando preços de várias fontes')]")))
time.sleep(10)


# achar elementos
list_card_voos = driver.find_elements(By.CSS_SELECTOR, "li.pIav2d")



for i, _ in enumerate(list_card_voos):
    if list_card_voos[i]:
        # colocar raw aqui retornando id e extracao, o resto permanesce
        text = list_card_voos[i].text
        id, extracted_at = create_update_files.save_bronze(text)

        text = re.sub(r"\s+", " ", text) 
        text = text.split()
        position_h = find_h(text)
        index_price, price = find_price(text)
        kg_index_raw = find_kg(text, index_price)
        origin, destination = find_iatas(text)
        print(text)
        extract_card(text, position_h, price, kg_index_raw, origin, destination, id, extracted_at)
        
    
    






