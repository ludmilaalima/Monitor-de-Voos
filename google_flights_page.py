from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsers import google_flights_parser
from pipelines import storage, checkpoint
import re
import os



storage = storage.CreateUpdateFiles()
storage.create_storage()

parser = google_flights_parser.GoogleFlightsParser()


chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)



driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTA0LTAyagcIARIDME5OcgcIARIDMFREQAFIAXABggELCP___________wGYAQI&tfu=EgoIABABGAAgAigD&hl=pt-BR&gl=BR')

origin = driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="De onde?"]')
origin.send_keys(Keys.CONTROL, 'a')
origin.send_keys(Keys.DELETE)
origin.send_keys("CPV")


select_iata_origin = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option'][contains(., 'Aeroporto')]")))
select_iata_origin.click()


time.sleep(3)
destination = driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="Para onde?"]')
destination.send_keys(Keys.CONTROL, 'a')
destination.send_keys(Keys.DELETE)
destination.send_keys('CNF')

select_iata_destination = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option'][contains(., 'Aeroporto')]")))

select_iata_destination.click()
origin.send_keys(Keys.F5)

wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verificando preços de várias fontes')]")))
wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verificando preços de várias fontes')]")))
list_card_voos = driver.find_elements(By.CSS_SELECTOR, "li.pIav2d")



for i, _ in enumerate(list_card_voos):
    if list_card_voos[i]:
        # colocar raw aqui retornando id e extracao, o resto permanesce
        text = list_card_voos[i].text
        f = storage.update_bronze(text)
        print(text)
        text = re.sub(r"\s+", " ", text) 
        text = text.split()
        position_h = parser.find_h(text)
        index_price, price = parser.find_price(text)
        kg_index_raw = parser.find_kg(text, index_price)
        origin, destination = parser.find_iatas(text)
        

### update no silver
'''from pathlib import Path

bronze_path = Path('data/bronze/bronze_flights_raw_CPVeCNF.jsonl')
checkpoint_path = Path('data/checkpoints/bronze_flights_raw_CPVeCNF.offset')


checkpoint = checkpoint.process_jsonl_incremental(bronze_path, checkpoint_path)'''