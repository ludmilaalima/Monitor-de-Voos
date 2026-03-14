from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)



driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTA0LTAyagcIARIDME5OcgcIARIDMFREQAFIAXABggELCP___________wGYAQI&tfu=EgoIABABGAAgAigD&hl=pt-BR&gl=BR')

origin = driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="De onde?"]')
origin.send_keys(Keys.CONTROL, 'a')
origin.send_keys(Keys.DELETE)
origin.send_keys("CPV")


select_iata_origin = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option'][contains(., 'Aeroporto')]")))
select_iata_origin.click()



destination = driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="Para onde?"]')
destination.send_keys(Keys.CONTROL, 'a')
destination.send_keys(Keys.DELETE)
destination.send_keys('CNF')

select_iata_destination = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[@role='option'][contains(., 'Aeroporto')]")))
select_iata_destination.click()




time.sleep(10)