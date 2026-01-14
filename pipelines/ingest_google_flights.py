# site > bronze

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
from pipelines.storage import CreateUpdateFiles




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
        create_update_files.update_bronze(text)

driver.quit()
     
        