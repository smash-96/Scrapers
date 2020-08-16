from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import os
import csv
import traceback

fresh=0

def check(driver,x):
    try:
        driver.find_element_by_xpath(x)
    except:
        return False
    return True

def write(Handle,title,desc,vendor,types,tag,cn,cv,sn,sv,un,uv,wn,wv,item,price,image,oos):
    if types=='' or types==' ':
        types='N/A'
    data=[]
    soup = BeautifulSoup(desc)
    for a in soup.findAll('a'):
        a.replaceWithChildren()
    data.append(str(Handle))
    data.append(str(title))
    data.append(str(soup))
    data.append(str(vendor))
    data.append(str(types))
    data.append(str(tag))
    data.append(str(cn))
    data.append(str(cv))
    data.append(str(sn))
    data.append(str(sv))
    data.append(str(un))
    data.append(str(uv))
    data.append(str(wn))
    data.append(str(wv))
    data.append(str(item))
    data.append(str(price))
    data.append(str(image))


    with open('Info.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()

def extract(driver,mainC):
    global fresh
    if fresh==10:   # CHANGE NUMBER OF PRODUCTS TO BE SCRAPED BEFORE REFRESH HERE..!!
        print("Refreshing...")
        fresh=0
        time.sleep(20)
        fresh=0
    else:
        fresh+=1
    #try:
    t=2
    tag=''
    while check(driver,'//*[@id="product-form"]/div/ol/li['+str(t)+']/a/span')==True:
        tagM=str(driver.find_element_by_xpath('//*[@id="product-form"]/div/ol/li['+str(t)+']/a/span').text)+', '
        tag=str(tag)+tagM
        t+=1
    try:
        bname=driver.find_element_by_xpath('//*[@id="product-form"]/div/div[1]/div[2]/a/small').text
    except:
        bname=driver.find_element_by_xpath('//*[@id="product-form"]/div[1]/div[2]/a/small').text
    try:
        pname=driver.find_element_by_xpath('//*[@id="product-form"]/div/div[1]/div[2]/h1/span').text
    except:
        pname=driver.find_element_by_xpath('//*[@id="product-form"]/div[1]/div[2]/h1/span').text
    tag=str(tag)+str(bname)    
    price=driver.find_element_by_xpath('//*[@id="product-price"]/h2/span').text
    price=str(price).split('$')
    price=str(price[1])
    desc=driver.find_element_by_xpath('//*[@id="description"]/span').get_attribute("outerHTML")
    item=''
    stock=''
    previtem='p'
    time.sleep(5)
    if check(driver,'//*[@id="stand_color"]')==False and check(driver,'//*[@id="color"]')==False and check(driver,'//*[@id="units"]')==False and check(driver,'//*[@id="size"]')==False and check(driver,'//*[@id="watts"]')==False:
        item=driver.find_element_by_xpath('//*[@id="product-id"]').text
        time.sleep(2)
        if "Out of Stock" in driver.page_source:
            stock='Yes'
        img=1
        image=''
        if check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
            while check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                try:
                    driver.find_element_by_xpath('//*[@id="product-image"]/div/ol/li['+str(img)+']/img').click()
                    time.sleep(2)
                    imaget=str(driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div['+str(img)+']/a/div/img').get_attribute('src'))+'; '
                    image=str(image)+imaget
                except:
                    pass
                img+=1
        else:
            image=driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div[1]/a/div/img').get_attribute('src')
        write(pname,pname,desc,bname,mainC,tag,'','','','','','','','',item,price,image,stock)
    elif check(driver,'//*[@id="stand_color"]')==True:
        num=len(driver.find_elements_by_xpath('//*[@id="stand_color"]/option'))
        i=2
        while i <= num:
            driver.find_element_by_xpath('//*[@id="stand_color"]/option['+str(i)+']').click()
            color=driver.find_element_by_xpath('//*[@id="stand_color"]/option['+str(i)+']').text
            flag=False
            stock=''
            while flag==False:
                item=driver.find_element_by_xpath('//*[@id="product-id"]').text
                if 'Please make a selection' not in item and item !=previtem:
                    previtem=item
                    flag=True
                    if "Out of Stock" in driver.page_source:
                        stock='Yes'
                    #if "Out of Stock" not in driver.page_source:
                    try:
                        time.sleep(5)
                        img=1
                        image=''
                        if check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                            while check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                                try:
                                    driver.find_element_by_xpath('//*[@id="product-image"]/div/ol/li['+str(img)+']/img').click()
                                    time.sleep(2)
                                    imaget=str(driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div['+str(img)+']/a/div/img').get_attribute('src'))+'; '
                                    image=str(image)+imaget
                                except:
                                    pass
                                img+=1
                        else:
                            image=driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div[1]/a/div/img').get_attribute('src')
                    except:
                        image='N/A'
                    price=driver.find_element_by_xpath('//*[@id="product-price"]/h2/span').text
                    price=str(price).split('$')
                    price=str(price[1])
                    if i==2:
                        write(pname,pname,desc,bname,mainC,tag,'Color',color,'','','','','','',item,price,image,stock)
                        #write(mainC,tag,bname,pname,item,price,image,color,'N/A','N/A',desc)
                    else:
                        write(pname,'','','',mainC,tag,'Color',color,'','','','','','',item,price,image,stock)
                        #write(mainC,tag,' ',' ',item,price,image,color,'N/A','N/A',' ')
            i+=1
    elif check(driver,'//*[@id="color"]')==True:
        num=len(driver.find_elements_by_xpath('//*[@id="color"]/option'))
        i=2
        while i <= num:
            driver.find_element_by_xpath('//*[@id="color"]/option['+str(i)+']').click()
            color=driver.find_element_by_xpath('//*[@id="color"]/option['+str(i)+']').text
            flag=False
            stock=''
            while flag==False:
                item=driver.find_element_by_xpath('//*[@id="product-id"]').text
                if 'Please make a selection' not in item and item !=previtem:
                    previtem=item
                    flag=True
                    if "Out of Stock" in driver.page_source:
                        stock='Yes'
                    #if "Out of Stock" not in driver.page_source:
                    try:
                        time.sleep(5)
                        img=1
                        image=''
                        if check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                            while check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                                try:
                                    driver.find_element_by_xpath('//*[@id="product-image"]/div/ol/li['+str(img)+']/img').click()
                                    time.sleep(2)
                                    imaget=str(driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div['+str(img)+']/a/div/img').get_attribute('src'))+'; '
                                    image=str(image)+imaget
                                except:
                                    pass
                                img+=1
                        else:
                            image=driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div[1]/a/div/img').get_attribute('src')
                    except:
                        image='N/A'
                    price=driver.find_element_by_xpath('//*[@id="product-price"]/h2/span').text
                    price=str(price).split('$')
                    price=str(price[1])
                    if i==2:
                        write(pname,pname,desc,bname,mainC,tag,'Color',color,'','','','','','',item,price,image,stock)
                        #write(mainC,tag,bname,pname,item,price,image,color,'N/A','N/A',desc)
                    else:
                        write(pname,'','','',mainC,tag,'Color',color,'','','','','','',item,price,image,stock)
                        #write(mainC,tag,' ',' ',item,price,image,color,'N/A','N/A',' ')
            i+=1
    elif check(driver,'//*[@id="units"]')==True:
        num=len(driver.find_elements_by_xpath('//*[@id="units"]/option'))
        i=2
        while i <= num:
            driver.find_element_by_xpath('//*[@id="units"]/option['+str(i)+']').click()
            unit=driver.find_element_by_xpath('//*[@id="units"]/option['+str(i)+']').text
            flag=False
            stock=''
            while flag==False:
                item=driver.find_element_by_xpath('//*[@id="product-id"]').text
                if 'Please make a selection' not in item and item !=previtem:
                    previtem=item
                    flag=True
                    if "Out of Stock" in driver.page_source:
                        stock='Yes'
                    #if "Out of Stock" not in driver.page_source:
                    try:
                        time.sleep(5)
                        img=1
                        image=''
                        if check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                            while check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                                try:
                                    driver.find_element_by_xpath('//*[@id="product-image"]/div/ol/li['+str(img)+']/img').click()
                                    time.sleep(2)
                                    imaget=str(driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div['+str(img)+']/a/div/img').get_attribute('src'))+'; '
                                    image=str(image)+imaget
                                except:
                                    pass
                                img+=1
                        else:
                            image=driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div[1]/a/div/img').get_attribute('src')
                    except:
                        image='N/A'
                    price=driver.find_element_by_xpath('//*[@id="product-price"]/h2/span').text
                    price=str(price).split('$')
                    price=str(price[1])
                    if i==2:
                        write(pname,pname,desc,bname,mainC,tag,'','','','','Units',unit,'','',item,price,image,stock)
                        #write(mainC,tag,bname,pname,item,price,image,'N/A','N/A',unit,desc)
                    else:
                        write(pname,'','','',mainC,tag,'','','','','Units',unit,'','',item,price,image,stock)
                        #write(mainC,tag,' ',' ',item,price,image,'N/A','N/A',unit,' ')
            i+=1
    elif check(driver,'//*[@id="size"]')==True:
        num=len(driver.find_elements_by_xpath('//*[@id="size"]/option'))
        i=2
        while i <= num:
            driver.find_element_by_xpath('//*[@id="size"]/option['+str(i)+']').click()
            size=driver.find_element_by_xpath('//*[@id="size"]/option['+str(i)+']').text
            flag=False
            stock=''
            while flag==False:
                item=driver.find_element_by_xpath('//*[@id="product-id"]').text
                if 'Please make a selection' not in item and item !=previtem:
                    previtem=item
                    flag=True
                    if "Out of Stock" in driver.page_source:
                        stock='Yes'
                    #if "Out of Stock" not in driver.page_source:
                    try:
                        time.sleep(5)
                        img=1
                        image=''
                        if check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                            while check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                                try:
                                    driver.find_element_by_xpath('//*[@id="product-image"]/div/ol/li['+str(img)+']/img').click()
                                    time.sleep(2)
                                    imaget=str(driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div['+str(img)+']/a/div/img').get_attribute('src'))+'; '
                                    image=str(image)+imaget
                                except:
                                    pass
                                img+=1
                        else:
                            image=driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div[1]/a/div/img').get_attribute('src')
                    except:
                        image='N/A'
                    price=driver.find_element_by_xpath('//*[@id="product-price"]/h2/span').text
                    price=str(price).split('$')
                    price=str(price[1])
                    if i==2:
                        write(pname,pname,desc,bname,mainC,tag,'','','Size',size,'','','','',item,price,image,stock)
                        #write(mainC,tag,bname,pname,item,price,image,'N/A',size,'N/A',desc)
                    else:
                        write(pname,'','','',mainC,tag,'','','Size',size,'','','','',item,price,image,stock)
                        #write(mainC,tag,' ',' ',item,price,image,'N/A',size,'N/A',' ')
            i+=1
    elif check(driver,'//*[@id="watts"]')==True:
        num=len(driver.find_elements_by_xpath('//*[@id="watts"]/option'))
        i=2
        while i <= num:
            driver.find_element_by_xpath('//*[@id="watts"]/option['+str(i)+']').click()
            watt=driver.find_element_by_xpath('//*[@id="watts"]/option['+str(i)+']').text
            flag=False
            stock=''
            while flag==False:
                item=driver.find_element_by_xpath('//*[@id="product-id"]').text
                if 'Please make a selection' not in item and item !=previtem:
                    previtem=item
                    flag=True
                    if "Out of Stock" in driver.page_source:
                        stock='Yes'
                    #if "Out of Stock" not in driver.page_source:
                    try:
                        time.sleep(5)
                        img=1
                        image=''
                        if check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                            while check(driver,'//*[@id="product-image"]/div/ol/li['+str(img)+']/img')==True:
                                try:
                                    driver.find_element_by_xpath('//*[@id="product-image"]/div/ol/li['+str(img)+']/img').click()
                                    time.sleep(2)
                                    imaget=str(driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div['+str(img)+']/a/div/img').get_attribute('src'))+'; '
                                    image=str(image)+imaget
                                except:
                                    pass
                                img+=1
                        else:
                            image=driver.find_element_by_xpath('//*[@id="product-image"]/div/div/div[1]/a/div/img').get_attribute('src')
                    except:
                        image='N/A'
                    price=driver.find_element_by_xpath('//*[@id="product-price"]/h2/span').text
                    price=str(price).split('$')
                    price=str(price[1])
                    if i==2:
                        write(pname,pname,desc,bname,mainC,tag,'','','','','','','Watt',watt,item,price,image,stock)
                        #write(mainC,tag,bname,pname,item,price,image,'N/A',size,'N/A',desc)
                    else:
                        write(pname,'','','',mainC,tag,'','','','','','','Watt',watt,item,price,image,stock)
                        #write(mainC,tag,' ',' ',item,price,image,'N/A',size,'N/A',' ')
            i+=1
    # except:
    #     pass

#col=['Handle','Main Category','tags','Brand Name','Product Name','Item #','Product Price','Product Picture','Color','Size','Unit','Product Description']
col=['Handle','Title','Body','Vendor','Type','Tags','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Option4 Name','Option4 Value','Variant SKU','Variant Price','Image Src','Out of Stock']
with open('Info.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)


options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
#options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='<Add Path to your chromedriver>',chrome_options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)
urls=[
    'https://www.marinedepot.com/aquarium-lights',
    'https://www.marinedepot.com/additives-supplements',
    'https://www.marinedepot.com/aeration',
    'https://www.marinedepot.com/co2-injection',
    'https://www.marinedepot.com/aquariums',
    'https://www.marinedepot.com/reactors',
    'https://www.marinedepot.com/heaters-chillers',
    'https://www.marinedepot.com/filter-media',
    'https://www.marinedepot.com/filters',
    'https://www.marinedepot.com/fish-coral-food',
    'https://www.marinedepot.com/aquarium-maintenance',
    'https://www.marinedepot.com/fragging-supplies',
    'https://www.marinedepot.com/salt-mix',
    'https://www.marinedepot.com/merchandise',
    'https://www.marinedepot.com/uv-sterilizers-ozone',
    'https://www.marinedepot.com/aquarium-plumbing',
    'https://www.marinedepot.com/aquarium-pumps',
    'https://www.marinedepot.com/ato-dosing-pumps',
    'https://www.marinedepot.com/protein-skimmers',
    'https://www.marinedepot.com/reverse-osmosis',
    'https://www.marinedepot.com/sand-and-gravel',
    'https://www.marinedepot.com/rock-wood-and-plants',
    'https://www.marinedepot.com/water-testing',
    'https://www.marinedepot.com/controllers-timers',
    'https://www.marinedepot.com/education',
    'https://www.marinedepot.com/live-goods']

for url in urls:
    driver.get(url)
    mainC=str(driver.title)
    mainC=str(mainC).split('-')
    mainC=str(mainC[0])
    if check(driver,'//*[@id="verada"]/div/div[2]/h3')==True and str(driver.find_element_by_xpath('//*[@id="verada"]/div/div[2]/h3').text)=="Categories":
        if check(driver,'//*[@id="verada"]/div')==True:
            elem1=driver.find_elements_by_xpath('//*[@id="verada"]/div/div[2]/div')
            if len(elem1) > 0:
                for e1 in elem1:
                    link=e1.find_element_by_tag_name('a').get_attribute('href')
                    newTab = 'window.open("' + link + '", "_blank");'
                    driver.execute_script(newTab)
                    driver.switch_to_window(driver.window_handles[1])
                                    
                    if check(driver,'//*[@id="verada"]/div/div[2]/h3')==True and str(driver.find_element_by_xpath('//*[@id="verada"]/div/div[2]/h3').text)=="Categories":
                        if check(driver,'//*[@id="verada"]/div')==True:
                            elem2=driver.find_elements_by_xpath('//*[@id="verada"]/div/div[2]/div')
                            if len(elem2) > 0:
                                for e2 in elem2:
                                    link2=e2.find_element_by_tag_name('a').get_attribute('href')
                                    time.sleep(1)
                                    newTab = 'window.open("' + link2 + '", "_blank");'
                                    driver.execute_script(newTab)
                                    driver.switch_to_window(driver.window_handles[2])
                                    
                                    elem3=driver.find_elements_by_xpath('//*[@id="products"]/div')
                                    for e3 in elem3:
                                        try:
                                            link3=e3.find_element_by_tag_name('a').get_attribute('href')
                                            time.sleep(1)
                                            newTab = 'window.open("' + link3 + '", "_blank");'
                                            driver.execute_script(newTab)
                                            driver.switch_to_window(driver.window_handles[3])
                                            time.sleep(5)
                                            extract(driver,mainC)
                                        except:
                                            pass
                                        
                                        driver.execute_script('window.close()')
                                        driver.switch_to_window(driver.window_handles[2])

                                    driver.execute_script('window.close()')
                                    driver.switch_to_window(driver.window_handles[1])

                            driver.execute_script('window.close()')
                            driver.switch_to_window(driver.window_handles[0])
                    else:
                        subcatg=''
                        elem3=driver.find_elements_by_xpath('//*[@id="products"]/div')
                        for e3 in elem3:
                            try:
                                link3=e3.find_element_by_tag_name('a').get_attribute('href')
                                time.sleep(1)
                                newTab = 'window.open("' + link3 + '", "_blank");'
                                driver.execute_script(newTab)
                                driver.switch_to_window(driver.window_handles[2])
                                time.sleep(5)
                                extract(driver,mainC)
                            except:
                                pass
                            
                            driver.execute_script('window.close()')
                            driver.switch_to_window(driver.window_handles[1])

                        driver.execute_script('window.close()')
                        driver.switch_to_window(driver.window_handles[0])
    else:
        catg,subcatg='',''
        elem3=driver.find_elements_by_xpath('//*[@id="products"]/div')
        for e3 in elem3:
            try:
                link3=e3.find_element_by_tag_name('a').get_attribute('href')
                time.sleep(1)
                newTab = 'window.open("' + link3 + '", "_blank");'
                driver.execute_script(newTab)
                driver.switch_to_window(driver.window_handles[1])
                time.sleep(5)
                extract(driver,mainC)
            except:
                pass
            
            driver.execute_script('window.close()')
            driver.switch_to_window(driver.window_handles[0])
    #driver.close()