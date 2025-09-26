from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from create_update_csv import CreateUpdateCsv


create_update_csv = CreateUpdateCsv()
create_update_csv.create_csv() 

driver = webdriver.Chrome() #abre instancia 
driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhpAEgoyMDI1LTEyLTExIiAKA0NQVhIKMjAyNS0xMi0xMRoDQ05GKgJBRDIENDI4OWoHCAESA0NQVnIHCAESA0NORhoeEgoyMDI1LTEyLTE2agcIARIDQ05GcgcIARIDQ1BWQAFIAXABggELCP___________wGYAQE&tfu=CmxDalJJZUd4NWFuTk5SbDlSUXpCQlFXdEpWRUZDUnkwdExTMHRMUzB0TFdObFoza3hOMEZCUVVGQlIycFdlRVZGVFVGWk9FOUJFZ1pCUkRReU9Ea2FDd2p0eUFZUUFob0RRbEpNT0J4dzNwd0ISBggCIAIoASIDCgEw') #acessar navegador
driver.maximize_window()
time.sleep(5)

voos = driver.find_element(By.CSS_SELECTOR, "[aria-label$= 'Mostrar mais voos']")
voos.click()

# achar elementos
time.sleep(10)
elements_price = driver.find_elements(By.CSS_SELECTOR, "[aria-label$='Reais brasileiros']")

print(elements_price)

for element in elements_price:
    create_update_csv.update_csv(element.text)
    
    





