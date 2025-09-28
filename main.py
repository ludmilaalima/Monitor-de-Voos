from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
from create_update_csv import CreateUpdateCsv
from selenium.webdriver.chrome.options import Options


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


try:
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Encontrando as opções de reserva mais baratas…')]")))
    print("achei mensagem")
except:
    print("nao apareceu")


time.sleep(10)
# achar elementos
elements_price = driver.find_elements(By.CSS_SELECTOR, "[aria-label$='Reais brasileiros']")

print(elements_price)

for element in elements_price:
    if element.text:
        create_update_csv.update_csv(element.text)
    
    





