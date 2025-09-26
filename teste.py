import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager




#######
# Configurações do navegador
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Ative depois que funcionar bem

# Inicializa o driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL do Google Flights com CPV → CNF (Ajustável)
url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhpAEgoyMDI1LTEyLTExIiAKA0NQVhIKMjAyNS0xMi0xMRoDQ05GKgJBRDIENDI4OWoHCAESA0NQVnIHCAESA0NORhoeEgoyMDI1LTEyLTE2agcIARIDQ05GcgcIARIDQ1BWQAFIAXABggELCP___________wGYAQE'

print("⏳ Acessando Google Flights...")
driver.get(url)

# Aguarda carregamento inicial
time.sleep(15)

# Tenta localizar os cards dos voos
cards = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')

voos = []
for card in cards:
    try:
        airline = card.find_element(By.CSS_SELECTOR, 'div[aria-label*="Operado por"]').text
    except:
        airline = "Desconhecida"

    try:
        times = card.find_elements(By.CSS_SELECTOR, 'div span[jscontroller]')[0].text
        departure, arrival = times.split(" – ")
    except:
        departure, arrival = "N/A", "N/A"

    try:
        duration = card.find_element(By.XPATH, './/div[contains(text(), "h") and contains(text(), "min")]').text
    except:
        duration = "N/A"

    try:
        price = card.find_element(By.XPATH, './/div[contains(text(), "R$")]').text
    except:
        price = "N/A"

    voos.append({
        "airline": airline,
        "departure": departure,
        "arrival": arrival,
        "duration": duration,
        "price": price
    })

driver.quit()

# Salva como JSON
filename = f"voos_google_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(voos, f, ensure_ascii=False, indent=2)

print(f"\n✅ {len(voos)} voos salvos em {filename}")
