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

def conv(x):
    z=str(x).rstrip("'")
    z=z[2:]
    return z

def write(condition,classv,sclass,med):
    data=[]
    data.append(str(condition))
    data.append(str(classv))
    if sclass!=' ':
        a=str(str(sclass).encode("utf-8"))
        a=conv(a)
        data.append(a)
    else:
        data.append(sclass)
    if med!='':
        b=str(str(med).encode("utf-8"))
        b=conv(b)
        data.append(b)
    else:
        data.append(med)    
    with open('Info.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()

def check(driver,elem):  
    try:
        elem.find_element_by_tag_name('ul')
    except:
        return False
    return True

def check2(driver,elem):
    try:
        elem.find_element_by_class_name('class2')
    except:
        return False
    return True

def scrap():
    col=['Condition','Class','Sub Class','Medication']
    with open('Info.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

    url = "https://amhonline.amh.net.au/auth"
    options=webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    #options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys("<email>")
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("<password>")
    driver.find_element_by_xpath('//*[@id="Login"]').click()
    time.sleep(5)

    med=''
    elem=driver.find_elements_by_xpath('//*[@id="banner"]/div/ul/li[2]/ul/li')
    for e in elem:
        link=e.find_element_by_tag_name('a').get_attribute('href')
        newTab = 'window.open("' + link + '", "_blank");'
        driver.execute_script(newTab)
        driver.switch_to_window(driver.window_handles[1])

        time.sleep(2)
        cond=driver.find_element_by_xpath('//*[@id="document-header"]/h1').text
        val=str(cond).lower()
        val=val.replace(' and','')
        val=val.replace(' ','-')
        val=val.replace(',','')
        val=val.replace('vaccines','vaccines-chap')
        print(val)
        tags=driver.find_element_by_xpath('//*[@id="'+str(val)+'-drug-information"]/ul')
        tags2=tags.find_elements_by_class_name('class')
        print(len(tags2))
        for ts in tags2:
            clas=ts.text
            clas=str(clas).split('\n')
            clas=str(clas[0])
            print("class "+clas)
            if check(driver,ts)==True:
                tags3=ts.find_element_by_tag_name('ul')
                if check2(driver,tags3)==True:
                    tags4=tags3.find_elements_by_class_name('class2')
                    for ts1 in tags4:
                        sclass=ts1.text
                        sclass=str(sclass).split('\n')
                        sclass=str(sclass[0])
                        print("sclass "+sclass)
                        if check(driver,ts1)==True:
                            tags5=ts1.find_element_by_tag_name('ul')
                            tags6=tags5.find_elements_by_class_name('monograph')
                            for ts2 in tags6:
                                print("Med "+str(ts2.text))
                                med=med+'; '+str(ts2.text)
                            write(cond,clas,sclass,med)
                            med=''
                        else:
                            med=''
                            write(cond,clas,sclass,med)                                                                        
                else:
                    tags7=tags3.find_elements_by_class_name('monograph')
                    for ts3 in tags7:
                        print("Med "+str(ts3.text))
                        med=med+'; '+str(ts3.text)
                    write(cond,clas,' ',med)
                    med=''
        driver.execute_script('window.close()')
        driver.switch_to_window(driver.window_handles[0])
    driver.close()

if __name__ == "__main__":
    scrap()