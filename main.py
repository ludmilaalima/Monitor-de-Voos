from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
from create_update_csv import CreateUpdateCsv
from selenium.webdriver.chrome.options import Options
import re
from pprint import pprint


KNOW_AIRLINES = ['AZUL', 'LATAM', 'LATAM AIRLINES BRASIL']


def search(a):
     '''
     pesquisa
     
     '''

def parse_card(tokens):
    ...


def extract_card(text):
    
    kwargs = {}
   

    airline_name_count = 0

    for i in range(3, len(text)):
        extract = text[i]
        find_h = re.search(r'\b\d+h\b', extract)

        if find_h:
            break
        else:
            airline_name_count += 1

    airline_name = text[3]
    # inicio e fim da string 
    if airline_name_count > 1:
        airline_name_start = 3
        airline_name_end = airline_name_start + airline_name_count
        airline_name = text[airline_name_start:airline_name_end]

     
        #kwargs["airline_name"] = airline_name

        print(airline_name, airline_name_start, airline_name_end)

    # quantas paradas 
    escale = ''
    for i in range(0, len(text)): 
        if text[i] == 'Sem':
            escale = text[i]
        elif text[i] in ('parada', 'paradas'):
            escale = text[i-1]


    # aeroporto inicial e final
    raw_airline = airline_name
    main_airline, all_airlines = extract_airlines(raw_airline)

    kwargs["main_airline"] = main_airline
    kwargs["all_airlines"] = all_airlines
 
    create_update_csv.update_csv(text, escale, **kwargs)


def extract_airlines(raw_airline, know_airlines=KNOW_AIRLINES):
    if raw_airline is None:
        return None

    

    if isinstance(raw_airline, list):
        raw_airline = " ".join(raw_airline)
    else:
        raw_airline = str(raw_airline)
    raw_airline = raw_airline.upper()
    

    found = []
    for airline in know_airlines:
        if airline in raw_airline:
            found.append(airline)

    
    main_airline = found[0]
    all_airlines = " | ".join(found)

    return main_airline, all_airlines





options = Options()
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options) #abre instancia 

create_update_csv = CreateUpdateCsv()
create_update_csv.create_csv() 


#acessar navegador
driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTEyLTExagcIARIDQ1BWcgwIAxIIL20vMGwzcTIaIxIKMjAyNS0xMi0xNmoMCAMSCC9tLzBsM3EycgcIARIDQ1BWQAFIAXABggELCP___________wGYAQE&tfu=EgoIABABGAAgAigDIgMKATA')
driver.maximize_window()


'''voos = driver.find_element(By.CSS_SELECTOR, "[aria-label$= 'Mostrar mais voos']")
voos.click()

wait = WebDriverWait(driver, 60)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label$='Mostrar menos voos']")))'''


wait = WebDriverWait(driver, 20)
#driver.save_screenshot("erro.png")
wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verificando preços de várias fontes')]")))
wait.until_not(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verificando preços de várias fontes')]")))


time.sleep(10)
# achar elementos
list_card_voos = driver.find_elements(By.CSS_SELECTOR, "li.pIav2d")



for i, _ in enumerate(list_card_voos):
    if list_card_voos[i]:
        text = list_card_voos[i].text
        text = re.sub(r"\s+", " ", text)#.strip()
        text = text.split()
        print(text)
        extract_card(text)
        
    
    






