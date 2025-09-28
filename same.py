from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from create_update_csv import CreateUpdateCsv

# Inicializa manipulador de CSV
create_update_csv = CreateUpdateCsv()
create_update_csv.create_csv() 

# Abre navegador
driver = webdriver.Chrome()
driver.maximize_window()

# URL do Google Flights com datas específicas
url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTEyLTExagcIARIDQ1BWcgwIAxIIL20vMGwzcTIaIxIKMjAyNS0xMi0xNmoMCAMSCC9tLzBsM3EycgcIARIDQ1BWQAFIAXABggELCP___________wGYAQE&tfu=EgoIABABGAAgAigDIgMKATA'
driver.get(url)

# Espera dinâmica
wait = WebDriverWait(driver, 60)

# 1. Espera o texto "Carregando voos" aparecer (se aparecer)
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Carregando voos')]")))
    print("⏳ Aguardando carregamento de voos...")
except:
    print("⚠️ Mensagem 'Carregando voos' não apareceu.")

# 2. Espera a mensagem sumir
try:
    wait.until_not(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Carregando voos')]")))
    print("✅ Página carregada.")
except:
    print("❌ 'Carregando voos' não sumiu. A página pode ter travado.")
    driver.quit()
    exit()

# 3. Simula ações humanas para ativar carregamento dinâmico
actions = ActionChains(driver)

# Move o mouse para o centro
body = driver.find_element(By.TAG_NAME, 'body')
actions.move_to_element(body).perform()
time.sleep(1)

# Scroll gradualmente
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, 1000);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, 1500);")
time.sleep(2)

# 4. Aguarda os cards reais de voos aparecerem
try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="listitem"]')))
    print("✅ Lista de voos carregada.")
except:
    print("❌ Os voos não apareceram.")
    driver.quit()
    exit()

# 5. Extrai os preços
elements_price = driver.find_elements(By.CSS_SELECTOR, "span[aria-label$='Reais brasileiros']")

print(f"🔍 {len(elements_price)} preços encontrados.")

for element in elements_price:
    preco = element.text.strip().replace('\xa0', ' ')
    if preco:
        print("💰", preco)
        create_update_csv.update_csv(preco)

# 6. Fecha navegador
driver.quit()
print("✅ Coleta finalizada.")
