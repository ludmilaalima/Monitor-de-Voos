from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()
driver.get("https://www.google.com/travel/flights/search?tfs=CBwQAhpAEgoyMDI1LTEyLTExIiAKA0NQVhIKMjAyNS0xMi0xMRoDQ05GKgJBRDIENDI4OWoHCAESA0NQVnIHCAESA0NORhoeEgoyMDI1LTEyLTE2agcIARIDQ05GcgcIARIDQ1BWQAFIAXABggELCP___________wGYAQE&tfu=CmxDalJJZUd4NWFuTk5SbDlSUXpCQlFXdEpWRUZDUnkwdExTMHRMUzB0TFdObFoza3hOMEZCUVVGQlIycFdlRVZGVFVGWk9FOUJFZ1pCUkRReU9Ea2FDd2p0eUFZUUFob0RRbEpNT0J4dzNwd0ISBggCIAIoASIDCgEw")
driver.maximize_window()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

wait = WebDriverWait(driver, 20)

# botão "Mostrar mais voos"
locator = (By.CSS_SELECTOR, "button[aria-label='Mostrar mais voos']")

btn = wait.until(EC.presence_of_element_located(locator))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
wait.until(EC.element_to_be_clickable(locator))

try:
    btn.click()
except ElementClickInterceptedException:
    # se algum header/overlay interceptar, clica via JS
    driver.execute_script("arguments[0].click();", btn)

