import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import csv


def write(Date, Track, Name, t_Time, MGN, s_Split, fn):
    
    data=[]
    data.append(str(Date))
    data.append(str(Track))
    data.append(str(Name))
    data.append(str(t_Time))
    data.append(str(MGN))
    data.append(str(s_Split))

    with open(fn + '.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()


options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
#options.add_argument("--headless")


driver = webdriver.Chrome(executable_path='/Users/maisamshah/Downloads/chromedriver', options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)

filename = 'race' # Enter file name here in which you want to store the data

d_date = '2020-08-13' # Enter date here in the format -> yyyy-mm-dd

if os.path.exists(filename + '.csv') == False:
    col=['Race_Date', 'Track', 'Name','Time','MGN','Split']
    with open(filename + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

driver.get('https://www.thegreyhoundrecorder.com.au/results/')
driver.maximize_window()
try:
    driver.find_element_by_xpath('//*[@id="datePicker"]').send_keys(d_date)
    driver.find_element_by_xpath('//*[@id="searchSubmit"]').click()
    time.sleep(5)
    d_date = d_date.split('-')
    d_date = d_date[0] + '/' + d_date[1] + '/' + d_date[2]

    tr_c = driver.find_elements_by_xpath('//*[@id="mainContainer"]/div[4]/div[1]/div[3]/div/div/table/tbody/tr')
    for i in range(1, len(tr_c)+1):
        track = driver.find_element_by_xpath('//*[@id="mainContainer"]/div[4]/div[1]/div[3]/div/div/table/tbody/tr['+str(i)+']/td[1]').text
        link = driver.find_element_by_xpath('//*[@id="mainContainer"]/div[4]/div[1]/div[3]/div/div/table/tbody/tr['+str(i)+']/td[2]/a').get_attribute('href')

        newTab = 'window.open("' + link + '", "_blank");'
        driver.execute_script(newTab)
        driver.switch_to_window(driver.window_handles[1])
        time.sleep(2)

        j = 1
        lis = driver.find_elements_by_xpath('//*[@id="resultsContainer"]/div[2]/ul/li')
        for li in lis:
            li.click()
            time.sleep(1)
            tr_c2 = driver.find_elements_by_xpath('//*[@id="race-'+str(j)+'"]/table[2]/tbody/tr')
            for k in range(1, len(tr_c2)+1):
                try:
                    name = driver.find_element_by_xpath('//*[@id="race-'+str(j)+'"]/table[2]/tbody/tr['+str(k)+']/td[3]').text
                    name = str(name).split('(')[0]
                    t_time = driver.find_element_by_xpath('//*[@id="race-'+str(j)+'"]/table[2]/tbody/tr['+str(k)+']/td[5]').text
                    mgn = driver.find_element_by_xpath('//*[@id="race-'+str(j)+'"]/table[2]/tbody/tr['+str(k)+']/td[6]').text
                    s_split = driver.find_element_by_xpath('//*[@id="race-'+str(j)+'"]/table[2]/tbody/tr['+str(k)+']/td[7]').text
                    if t_time != '' and mgn != '' and s_split != '':

                        if t_time == '0.00':
                            t_time = ''
                        if s_split == '0.00':
                            s_split = ''
                        write(d_date, track, name, t_time, mgn, s_split, filename)
                except:
                    print(t_time, s_split, "Error")

            j += 1

        driver.execute_script('window.close()')
        driver.switch_to_window(driver.window_handles[0])

    driver.close()
except:
    driver.close()

df = pd.read_csv(filename + '.csv')
df = df.drop_duplicates()
df.to_csv(filename + '.csv', index=False)