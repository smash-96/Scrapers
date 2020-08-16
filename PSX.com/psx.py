from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import string, re
import time
import csv

def check(driver,x):
    try:
        driver.find_element_by_xpath(x)
    except:
        return False
    return True

def write(a,b,c,d,e,f,word):
    data=[]
    data.append(str(a))
    data.append(str(b))
    data.append(str(c))
    data.append(str(d))
    data.append(str(e))
    data.append(str(f))

    with open(str(word) + '.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()


col=['Time','Open','High','Low','Close','Volume']


options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
#options.add_argument("--headless")
driver = webdriver.Chrome('<Add Path to your chromedriver>', options=options)
driver.get("https://dps.psx.com.pk/historical")

words = ['', '', '', ''] # Add the Company symbols you want to extract data for

for word in words:
    driver.find_element_by_xpath('//*[@id="historicalSymbolSearch"]').send_keys(str(word))
    with open(str(word) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)
    
    num1=len(driver.find_elements_by_xpath('/html/body/div[5]/div[4]/div/div[3]/div/div[2]/div[2]/select/option'))
    num2=len(driver.find_elements_by_xpath('/html/body/div[5]/div[4]/div/div[3]/div/div[3]/div[2]/select/option'))
    i = 2
    while i <= num1:
        num2=len(driver.find_elements_by_xpath('/html/body/div[5]/div[4]/div/div[3]/div/div[3]/div[2]/select/option'))
        j = 4
        while j <= 5:

            driver.find_element_by_xpath('/html/body/div[5]/div[4]/div/div[3]/div/div[2]/div[2]/select/option['+str(i)+']').click()
            driver.find_element_by_xpath('/html/body/div[5]/div[4]/div/div[3]/div/div[3]/div[2]/select/option['+str(j)+']').click()
            driver.find_element_by_xpath('//*[@id="historicalSymbolBtn"]').click()
            time.sleep(2)

            if "No data available in table" not in driver.page_source:
                trs = driver.find_elements_by_xpath('//*[@id="historicalTable"]/tbody/tr')
                for tr in trs:
                    data = str(tr.text).split()
                    write(data[0] + ' ' + data[1] + ' ' + data[2], data[3], data[4], data[5], data[6], int(data[7].replace(',', '')), word)

            j += 1
        
        i += 1
    driver.find_element_by_xpath('//*[@id="historicalSymbolSearch"]').clear()

driver.close()
