from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

#google form url through which data will be entered automatically (now closed)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSesHFDcvDrniU9_H5N71njuhrTlpjtZTvBVRWLU1MYmBMTuCw/viewform?usp=sharing&ouid=117813103421978168225"

#defines options, creates selenium webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome()

#creates beautifulsoup object from the response module
response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
zillow_clone_webpage = response.text
soup = BeautifulSoup(zillow_clone_webpage, "html.parser")

#gets location prices in the webpage
prices = soup.select('span[data-test="property-card-price"]')
price_list = [price.get_text(strip=True) for price in prices]

#gets location addresses in the webpage
addresses = soup.select('address[data-test="property-card-addr"]')
address_list = [addr.get_text(strip=True) for addr in addresses]

#gets links in the webpage
links = soup.select('a.StyledPropertyCardDataArea-anchor')
base_url = "https://www.zillow.com"
link_list = [base_url + link.get("href") for link in links if link.get("href")]

#runs through all the prices, addresses and urls found via beautifulsoup, in order
for price, addr, link in zip(price_list, address_list, link_list):
    driver.get(FORM_URL)
    time.sleep(4)

    #collects all the fields on the page
    input_fields = driver.find_elements(By.CSS_SELECTOR, 'input.whsOnd')

    #inputs price in the price (1st) field
    input_fields[0].send_keys(price)
    time.sleep(1)

    #inputs address in the address (2nd) field
    input_fields[1].send_keys(addr)
    time.sleep(1)

    #inputs link in the link (3rd) field
    input_fields[2].send_keys(link)
    time.sleep(1)

    #presses submit button
    submit_button = driver.find_element(By.XPATH, '//span[contains(text(), "Enviar")]/ancestor::div[@role="button"]')
    submit_button.click()
    time.sleep(2)