from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import csv
import traceback
from bs4 import BeautifulSoup
import urllib.request

def check(driver,x):
        try:
                driver.find_element_by_xpath(x)
        except:
                return False
        return True

def write(mainC,tag,bname,pname,item,price,image,color,size,unit,desc):
    if mainC=='' or mainC==' ':
        mainC='N/A'
    data=[]
    data.append(str(mainC))
    data.append(str(tag))
    data.append(str(bname))
    data.append(str(pname))
    data.append(str(item))
    data.append(str(price))
    data.append(str(image))
    data.append(str(color))
    data.append(str(size))
    data.append(str(unit))
    data.append(str(desc))    
        
    with open('Info2.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()

col=['Handle','tags','Brand Name','Product Name','Item #','Product Price','Product Picture','Color','Size','Unit','Product Description']

with open('Info2.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
#options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='<Add Path to your chromedriver>',chrome_options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)
urls=[
        'https://aquaforestaquarium.com/collections/lighting-system',
        'https://aquaforestaquarium.com/collections/filtration',
        'https://aquaforestaquarium.com/collections/heaters',
        'https://aquaforestaquarium.com/collections/tools',
        'https://aquaforestaquarium.com/collections/water-testing-treatment',
        'https://aquaforestaquarium.com/collections/layout-material',
        'https://aquaforestaquarium.com/collections/live-plants',
        'https://aquaforestaquarium.com/collections/miscellaneous',
        'https://aquaforestaquarium.com/collections/substrate-system',
        'https://aquaforestaquarium.com/collections/liquids-supplements',
        'https://aquaforestaquarium.com/collections/aquarium-tank-cabinet',
        'https://aquaforestaquarium.com/collections/co2-systems']

for url in urls:
        driver.get(url)
        time.sleep(5)

        lnk=driver.current_url
        links=[]
        val=str(lnk).split('/')
        val=str(val[len(val)-1])

        if val=='liquids-supplements':
                val="liquids-amp-supplements"
        elif val=='aquarium-tank-cabinet':
                val="aquarium-tank-amp-cabinet"
        elif val=='water-testing-treatment':
                val="water-testing-amp-treatment"
                

        mainC=driver.find_element_by_xpath('//*[@id="'+str(val)+'"]/main/div[1]/div/header/h1').text
        try:
                if check(driver,'//*[@id="'+str(val)+'"]/main/div[1]/div[2]/div/div/div/ul')==True:
                        lis=driver.find_elements_by_xpath('//*[@id="'+str(val)+'"]/main/div[1]/div[2]/div/div/div/ul/li')
                        for i in range(2,len(lis)):
                                elem=driver.find_elements_by_xpath('//*[@id="'+str(val)+'"]/main/div[1]/div[1]/div/div')
                                for e in elem:
                                        link=e.find_element_by_tag_name('a').get_attribute('href')
                                        links.append(link)
                                if i<len(lis)-1:
                                        driver.find_element_by_xpath('//*[@id="'+str(val)+'"]/main/div[1]/div[2]/div/div/div/ul/li['+str(i+1)+']/a').click()
                                        time.sleep(2)


                else:
                        elem=driver.find_elements_by_xpath('//*[@id="'+str(val)+'"]/main/div[1]/div/div/div')
                        for e in elem:
                                link=e.find_element_by_tag_name('a').get_attribute('href')
                                links.append(link)
        except:
                pass
                        
        print(len(links))
        for link in links:
                try:
                        newTab = 'window.open("' + link + '", "_blank");'
                        driver.execute_script(newTab)
                        driver.switch_to_window(driver.window_handles[1])
                        time.sleep(2)

                        lnk=driver.current_url
                        response = urllib.request.urlopen(lnk)
                        html = response.read()
                        soup = BeautifulSoup(html, 'html.parser')
                        h2=soup.find_all('h2')
                        for h in h2:
                                pname=h.text
                                break        
                        tag=mainC+', '+pname                
                        if check(driver,'//*[@id="productSelect-option-0"]/option[2]')==True:
                                num=len(driver.find_elements_by_xpath('//*[@id="productSelect-option-0"]/option'))
                                i=1
                                while i<=num:
                                        size=driver.find_element_by_xpath('//*[@id="productSelect-option-0"]/option['+str(i)+']').text
                                        driver.find_element_by_xpath('//*[@id="productSelect-option-0"]/option['+str(i)+']').click()
                                        time.sleep(3)
                                        if "Sold Out" not in driver.page_source:
                                                img=1
                                                image=''
                                                if check(driver,'//*[@id="productThumbs"]/li['+str(img)+']/a/img')==True:
                                                        while check(driver,'//*[@id="productThumbs"]/li['+str(img)+']/a/img')==True:
                                                                try:
                                                                        driver.find_element_by_xpath('//*[@id="productThumbs"]/li['+str(img)+']/a/img').click()
                                                                        time.sleep(2)
                                                                        imaget=str(driver.find_element_by_xpath('//*[@id="productPhotoImg"]').get_attribute('src'))+'; '
                                                                        image=str(image)+imaget
                                                                except:
                                                                        pass
                                                                img+=1
                                                else:
                                                        image=driver.find_element_by_xpath('//*[@id="productPhotoImg"]').get_attribute('src')
                                                price=str(driver.find_element_by_xpath('//*[@id="productPrice"]').text)
                                                price=price[0:len(price)-2]+'.'+price[len(price)-2:]        
                                                desc=driver.find_element_by_class_name('product-description').get_attribute("outerHTML")
                                                
                                                if i==1:
                                                        write(mainC,tag,' ',pname,' ',price,image,' ',size,' ',desc)
                                                else:
                                                        write(mainC,tag,' ',' ',' ',price,image,' ',size,' ',' ')

                                        i+=1
                        else:
                                #if "Sold Out" not in driver.page_source:
                                price=str(driver.find_element_by_xpath('//*[@id="productPrice"]').text)
                                price=price[0:len(price)-2]+'.'+price[len(price)-2:]        
                                desc=driver.find_element_by_class_name('product-description').get_attribute("outerHTML")
                                img=1
                                image=''
                                if check(driver,'//*[@id="productThumbs"]/li['+str(img)+']/a/img')==True:
                                        while check(driver,'//*[@id="productThumbs"]/li['+str(img)+']/a/img')==True:
                                                try:
                                                        driver.find_element_by_xpath('//*[@id="productThumbs"]/li['+str(img)+']/a/img').click()
                                                        time.sleep(2)
                                                        imaget=str(driver.find_element_by_xpath('//*[@id="productPhotoImg"]').get_attribute('src'))+'; '
                                                        image=str(image)+imaget
                                                except:
                                                        pass
                                                img+=1
                                else:
                                        image=driver.find_element_by_xpath('//*[@id="productPhotoImg"]').get_attribute('src')
                                write(mainC,tag,' ',pname,' ',price,image,' ',' ',' ',desc)
                except:
                        pass

                driver.execute_script('window.close()')
                driver.switch_to_window(driver.window_handles[0])
driver.close()
