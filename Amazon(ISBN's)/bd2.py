from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import string, re
import time
from random import randint
from time import sleep
import sqlalchemy as sql
import traceback
import datetime
from SqlDB_bd import MysqlDb_bd

def check(driver,x):
        try:
            driver.find_element_by_xpath(x)
        except:
            return False
        return True

def scrap_weight(driver,con):
    try:
        if check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')==True or check(driver,'//*[@id="result_0"]/div/div/div/div[2]/div[1]/div[1]/a')==True or check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h5/a')==True or check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/h2/a')==True or check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/h2/a')==True: 
            try:
                link=driver.find_element_by_xpath('//*[@id="result_0"]/div/div/div/div[2]/div[1]/div[1]/a').get_attribute('href')
            except:
                try:
                    link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h5/a').get_attribute('href')
                except:
                    try:                                          
                        link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/h2/a').get_attribute('href')
                    except:
                        try:                               
                            link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a').get_attribute('href')
                        except:
                            link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/h2/a').get_attribute('href')
            newTab = 'window.open("' + link + '", "_blank");'
            driver.execute_script(newTab)
            driver.switch_to_window(driver.window_handles[1])
            time.sleep(5)
            try:
                lis=driver.find_elements_by_xpath('//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li')
                for li in lis:
                    lit=li.text
                    lit=str(lit).split(':')
                    if 'Shipping Weight' in str(lit[0]):
                            sw=str(lit[1]).split('(')
                            sw=str(sw[0])
                            break
            except:
                pass
            driver.execute_script('window.close()')
            driver.switch_to_window(driver.window_handles[0])
    except:
        traceback.print_exc()
        pass
    return sw

def remspc(s):
    if s!='':
        i=0
        while s[i] == ' ':
            i+=1 
    return i

if __name__ == "__main__":
    db = MysqlDb_bd()
    driver = db.init_driver()
    con = db.init_db_engine()

    driver.get("https://amazon.com")
    time.sleep(60)
    count=con.execute('select count(*) from tbl_Floppy;').fetchone()[0]
    wait=1
    i=2001
    while i<=2500:
        if wait==50:
            wait=0
            print("Waiting")
            time.sleep(300)
        wait+=1
        try:
            isbn=str(con.execute('select ISBN from tbl_Floppy where Issue_ID="'+str(i)+'";').fetchone()[0],'utf-8')
            isbn13=str(con.execute('select ISBN13 from tbl_Floppy where Issue_ID="'+str(i)+'";').fetchone()[0],'utf-8')
            val=''
            val10=''
            val13=''
            if isbn!='' and isbn!='N/A' and isbn!=' ':
                val=isbn
                val10=isbn
            elif isbn13!='' and isbn13!='N/A' and isbn13!=' ':
                val=isbn13
                val13=isbn13
            if val!='' and val!=' ' and val!='N/A':
                print(val)
                time.sleep(5)
                try:
                    driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
                    driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(str(val))
                    driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
                    time.sleep(2)
                    try:
                        if "No results for" not in driver.page_source:
                            try:
                                sw=scrap_weight(driver,con)
                            except:
                                sw='-1'
                            print(sw)
                            if sw!='' and sw!=' 'and sw!='-1':
                                n=remspc(sw)
                                sw=str(sw[n:])
                                try:
                                    if val10!='' and val10!=' ' and val10!='N/A':
                                        sql='UPDATE tbl_Floppy SET Weight="'+str(sw)+'" WHERE ISBN="'+str(val10)+'";'
                                    elif val13!='' and val13!=' ' and val13!='N/A':
                                        sql='UPDATE tbl_Floppy SET Weight="'+str(sw)+'" WHERE ISBN13="'+str(val13)+'";'
                                    con.execute(sql)
                                    print(sql)
                                except:
                                    traceback.print_exc()
                                    pass
                    except:
                        traceback.print_exc()
                        pass
                except:
                    traceback.print_exc()
                    pass
        except:
            traceback.print_exc()
            pass
        time.sleep(2)
        i+=1
    driver.close()