# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import re
import time
import os
import re
import requests
import urllib
import traceback

def wait_for_internet_connection():
    url = 'http://www.google.com/'
    timeout = 5
    while True:
        try:
            _ = requests.get(url, timeout=timeout)
            return
        except requests.ConnectionError:
            print("...")
            pass

def check(driver,x):
    try:
        driver.find_element_by_xpath(x)
    except:
        return False
    return True

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

cat=[]
name=[]
add=[]
contract=[]
town=[]
pc=[]
email=[]
phone=[]
links=[]
fax=[]
site=[]
perf=''
catg=''
tno=''
regex = re.compile('[@]')
url = "https://healthatlas.gov.gr/HealthCare#!/"
options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(executable_path='<Add Path to your chromedriver>',chrome_options=options)
driver.implicitly_wait(10)
driver.get(url)
gk=driver.find_element_by_xpath('//*[@id="culture-en-US"]')
gk.click()
time.sleep(8)
driver.maximize_window()
dd3 = driver.find_element_by_xpath('//*[@id="filterContract"]/option[2]')
hover = ActionChains(driver).move_to_element(dd3)

for i in range(53):
    if i > 1:
        dd1 = driver.find_element_by_xpath('//*[@id="divFilterPanel"]/div/div[1]/div[1]/div[1]/select/option[2]')
        perf = dd1.text
        p1 = perf.split('\n')
        p2 = p1[0].split(' ')
        perf = p2[len(p2) - 1]
        dd1.click()
        for j in range(16):
            if j > 1:
                dd2 = driver.find_element_by_xpath('//*[@id="divFilterPanel"]/div/div[1]/div[1]/div[2]/select/option[2]')
                catg = dd2.text
                p1 = catg.split('\n')
                p2 = p1[0].split(' ')
                catg = p2[len(p2) - 4] + p2[len(p2) - 3] + p2[len(p2) - 2] + ' ' + p2[len(p2) - 1]
                dd2.click()
                if dd3.is_displayed():
                    hover.perform()
                btn = driver.find_element_by_id('btLoadData')
                btn.click()
                time.sleep(10)
                tns = driver.find_element_by_xpath('//*[@id="siteDataStats"]').text
                tns = str(tns).split(' ')
                tno = tns[1]
                col = "Νομός" + '\t' + "Κατηγορία" + '\t' + "Βρέθηκαν εγγραφές" + '\t' + "Σύμβαση" + '\t' + "Κατηγορία" + '\t' + "Όνομα" + '\t' + "Διεύθυνση" + '\t' + "Town" + '\t' + "Postal Code" + '\t' + "Fax" + '\t' + "Website" + '\t' + "E-mail" + '\t' + "Τηλέγωνο" + '\t' + "Links"
                file = open("feg.txt", "w", encoding='utf-8')
                file.write(str(col) + "\n")
                val = 0
                cnt = 0
                try:
                    for iii in range(int(tno)):
                        print(cnt)
                        loop = False
                        while loop==False:
                            try:
                                aflag = False
                                if val == 31:
                                    scrl = driver.find_element_by_xpath(
                                        '//*[@id="divList"]/div[' + str(val + 1) + ']/div/div[2]/div/a/span')
                                    driver.execute_script("return arguments[0].scrollIntoView();", scrl)
                                    val -= 4

                                if val == 0:
                                    driver.find_element_by_xpath(
                                        '//*[@id="divList"]/div[' + str(val + 2) + ']/div/div[2]/div/a/span').click()
                                    time.sleep(1)
                                    driver.find_element_by_xpath(
                                        '//*[@id="divForm"]/form-buttons-back/div/button').click()
                                time.sleep(2)

                                driver.find_element_by_xpath(
                                    '//*[@id="divList"]/div[' + str(val + 2) + ']/div/div[2]/div/a/span').click()
                                time.sleep(5)
                                if driver.find_element_by_xpath('//*[@id="divSiteMap"]/div').get_attribute(
                                        'class') != 'site-nodata-warning':
                                    try:
                                        driver.find_element_by_xpath('//*[@id="gmimap' + str(cnt) + '"]/area').click()
                                    except:
                                        time.sleep(3)
                                        cnt += 1
                                        driver.find_element_by_xpath('//*[@id="gmimap' + str(cnt) + '"]/area').click()
                                    temp1= driver.find_element_by_xpath('//*[@id="bodyContent"]/div[3]/a').get_attribute(
                                            "href") #link
                                    cnt += 1
                                    aflag = True
                                else:
                                    temp1=' '
                                tcat=driver.find_element_by_xpath('//*[@id="divForm"]/form-div-header/div/table/tbody/tr/td/div/span').text
                                tname=driver.find_element_by_xpath('//*[@id="site-fields-container"]/div[1]/div/div').text
                                try:
                                    tcontract=driver.find_element_by_xpath('//*[@id="site-fields-container"]/div[3]/div/div/span').text
                                except:
                                    tcontract=driver.find_element_by_xpath('//*[@id="site-fields-container"]/div[2]/div/div/span').text
                                try:
                                    atp = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[5]/div/div').text
                                    temail = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[11]/div/div').text
                                    tphone = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[7]/div/div').text
                                    tfax = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[9]/div/div').text
                                    tsite = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[13]/div/div/a').text
                                except:
                                    atp = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[4]/div/div').text
                                    temail = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[10]/div/div').text
                                    tphone = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[6]/div/div').text
                                    tfax = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[8]/div/div').text
                                    tsite = driver.find_element_by_xpath(
                                        '//*[@id="site-fields-container"]/div[12]/div/div/a').text
                                driver.find_element_by_xpath('//*[@id="divForm"]/form-buttons-back/div/button').click()

                                links.append(temp1)
                                cat.append(tcat)
                                name.append(tname)
                                contract.append(tcontract)
                                email.append(temail)
                                phone.append(tphone)
                                fax.append(tfax)
                                site.append(tsite)

                                atp = str(atp).split(',')
                                atp.reverse()
                                tp = atp[0]
                                tp = str(tp).split(' ')
                                if len(tp) == 2:
                                    if tp[1].isdigit():
                                        town.append(' ')
                                        pc.append(str(tp[1]))
                                    else:
                                        town.append(str(tp[1]))
                                        pc.append(' ')
                                else:
                                    if len(atp) == 1:
                                        wc = 0
                                    else:
                                        wc = 1
                                    tn = ''
                                    while tp[wc].isdigit() == False:
                                        tn = tn + tp[wc] + ' '
                                        wc += 1
                                        if wc == len(tp):
                                            break
                                    town.append(str(tn))
                                    pcd = ''
                                    while wc < len(tp):
                                        pcd = pcd + tp[wc] + ' '
                                        wc += 1
                                    pc.append(pcd)
                                if len(atp) > 1:
                                    ad = atp[len(atp) - 1]
                                    for ct in range(1, len(atp) - 1):
                                        ad = ad + atp[len(atp) - (ct + 1)]
                                    add.append(ad)
                                else:
                                    add.append(' ')

                                val += 1
                                loop=True
                                file.write(perf + "\t")
                                file.write(catg + "\t")
                                file.write(tno + "\t")
                                file.write(contract[iii] + "\t")
                                file.write(cat[iii] + "\t")
                                file.write(name[iii] + "\t")
                                file.write(add[iii] + "\t")
                                file.write(town[iii] + "\t")
                                file.write(pc[iii] + "\t")
                                file.write(fax[iii] + "\t")
                                file.write(site[iii] + "\t")
                                file.write(email[iii] + "\t")
                                file.write(phone[iii] + "\t")
                                file.write(links[iii] + "\t")
                                file.write("\n")
                            except:
                                print("NO")
                                traceback.print_exc()
                                if iii==int(tno)-2:
                                    loop=True
                                if check_internet()!=True:
                                    if check(driver, '//*[@id="divForm"]/div') == True:
                                        if aflag==False:
                                            cnt+=1
                                        driver.find_element_by_xpath('//*[@id="divForm"]/form-buttons-back/div/button').click()
                                    wait_for_internet_connection()

                    file.close()
                    print("Done1")
                    driver.close()
                    time.sleep(30000)
                except:
                    file.close()
                    print("Done2")
                    driver.close()
                    time.sleep(30000)


