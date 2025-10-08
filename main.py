from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
from create_update_csv import CreateUpdateCsv
from selenium.webdriver.chrome.options import Options
import re


def extract_card(text):
        airline_name_start = text[3]
        airline_name_end = 0
        for i, _ in enumerate(text):
            if '%h' in text(airline_name_end):
                continue
            else:
                airline_name_end =  airline_name_end + 1 
             
        create_update_csv.update_csv(text)



options = Options()
options.add_argument("--disable-blink-features=AutomationControlled") # desativar flag de bot
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
        #text = list_card_voos.getText
        text = list_card_voos[i].text
        text = re.sub(r"\s+", " ", text).strip()
        text = text.split()
        print(text)
        extract_card(text)
        
    
    






