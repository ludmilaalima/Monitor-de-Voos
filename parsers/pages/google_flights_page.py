'''from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTA0LTAyagcIARIDQ1BWcgcIARIDQ05GQAFIAXABggELCP___________wGYAQI&tfu=EgoIABABGAAgAigK")

campo_origem = driver.find_element(
    By.CSS_SELECTOR,
    'div[role="textbox"][data-placeholder="De onde?"]'
)

print(campo_origem)'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--lang=pt-BR")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTA0LTAyagcIARIDQ1BWcgcIARIDQ05GQAFIAXABggELCP___________wGYAQI&tfu=EgoIABABGAAgAigK")

# espera o carregamento geral
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

# tenta fechar consentimento/cookies, se aparecer
for xpath_botao in [
    "//button[normalize-space()='Aceitar tudo']",
    "//button[normalize-space()='Accept all']",
]:
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao))).click()
        break
    except:
        pass

# tenta localizar em português ou inglês
campo_origem = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//*[@role='textbox' and (@data-placeholder='De onde?' or @data-placeholder='Where from?')]"
    ))
)

print("Elemento encontrado:", campo_origem.text)
campo_origem.click()