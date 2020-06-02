'''from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver.get('https://www.skyscanner.es/transporte/vuelos/mad/nrt/200811/200827/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home')
timeout = 10
try:
    element_present = EC.presence_of_element_located((By.XPATH, '//iframe[@sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox"]'))
    WebDriverWait(driver, timeout).until(element_present)
    el=driver.find_elements_by_xpath('//iframe[@sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox"]')[0]
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(el, 39, 39)
    action.click()
    action.perform()
except TimeoutException:
    print ("Timed out waiting for page to load")'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver.get('https://www.skyscanner.es/transporte/vuelos/mad/nrt/200811/200827/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home')

timeout = 20
try:
    element_present = EC.presence_of_element_located((By.XPATH, "//span[@class='BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN BpkText_bpk-text--bold__4yauk']"))
    WebDriverWait(driver, timeout).until(element_present)
    for i in driver.get_cookies():
        print(i)
except TimeoutException:
    print ("Timed out waiting for page to load")
driver.quit()
