'''from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("")

campo_origem = driver.find_element(
    By.CSS_SELECTOR,
    'div[role="textbox"][data-placeholder="De onde?"]'
)

print(campo_origem)'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)



driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTA0LTAyagcIARIDME5OcgcIARIDMFREQAFIAXABggELCP___________wGYAQI&tfu=EgoIABABGAAgAigD&hl=pt-BR&gl=BR')

origin = driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="De onde?"]')
origin.send_keys(Keys.CONTROL, 'a')
origin.send_keys(Keys.DELETE)
origin.send_keys("CNF")


select_iata_aeroport = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option'][contains(., 'Aeroporto')]")))
select_iata_aeroport.click()
time.sleep(10)


'''wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//ul[@role='listbox']//li[@role='option'][contains(., 'Aeroporto')]"
    ))
)
primeira_opcao.click()


time.sleep(10)'''




