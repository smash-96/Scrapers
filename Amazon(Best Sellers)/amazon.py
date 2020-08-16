from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import csv


def write(ASIN,Product_Name,Product_Link,Product_Image,Active_price,Old_price,Reviews,Reviews_URL,Customer_Rating, fn):

    data=[]
    data.append(str(ASIN))
    data.append(str(Product_Name))
    data.append(str(Product_Link))
    data.append(str(Product_Image))
    data.append(str(Active_price))
    data.append(str(Old_price))
    data.append(str(Reviews))
    data.append(str(Reviews_URL))
    data.append(str(Customer_Rating))

    with open(fn + '.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()


col=['ASIN','Product_Name','Product_Link','Product_Image','Active_price','Old_price','Reviews','Reviews_URL','Customer_Rating']





options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
#options.add_argument("--headless")

# Replace url to scrape other best sellers
url = 'https://www.amazon.com/Best-Sellers-Camera-Photo-Camcorders/zgbs/photo/172421/ref=zg_bs_nav_p_1_p'

driver = webdriver.Chrome(executable_path='<Add Path to your chromedriver>', options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)


driver.get(url)
time.sleep(10)

pages = len(driver.find_elements_by_xpath('//*[@id="zg-center-div"]/div[2]/div/ul/li'))
if pages == 0:
    pages = 3

catg = str(driver.find_element_by_xpath('//*[@id="zg-right-col"]/h1/span').text)
with open(catg + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)


for j in range(0, pages - 2):
    time.sleep(4)
    lis = driver.find_elements_by_xpath('//*[@id="zg-ordered-list"]/li')
    print(len(lis))
    i = 1
    for li in lis:
        link = li.find_element_by_tag_name('a').get_attribute('href')

        asin = str(link).split('dp/')[1]
        asin = str(asin).split('/')[0]
        
        name = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/a/div').text
        
        img = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/a/span/div/img').get_attribute('src')

        try:
            rating = str(driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/div[1]/a[2]').text)

            r_url = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/div[1]/a[1]').get_attribute('href')

            c_rating = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/div[1]/a[1]').get_attribute('title')
        except:
            rating = ''
            r_url = ''
            c_rating = ''

        try:                                
            a_price = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/div[2]/a/span/span').text
            write(asin, name, link, img, a_price, '', rating, r_url, c_rating, catg)
        except:
            try:
                a_price = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/a[2]/span/span/span').text
                write(asin, name, link, img, a_price, '', rating, r_url, c_rating, catg)
            except:
                try:
                    a_price = driver.find_element_by_xpath('//*[@id="zg-ordered-list"]/li['+str(i)+']/span/div/span/div/a/span/span').text
                    write(asin, name, link, img, a_price, '', rating, r_url, c_rating, catg)
                except:
                    pass

        i += 1

    if j < pages - 3:
        driver.get(driver.find_element_by_xpath('//*[@id="zg-center-div"]/div[2]/div/ul/li['+str(pages)+']/a').get_attribute('href'))

driver.close()