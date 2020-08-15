from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bd2 import *
import string, re
import time
from random import randint
from time import sleep
import sqlalchemy as sql
import traceback
import datetime
from SqlDB_bd import MysqlDb_bd

class bd:
    error_log_file = 'bd' # file name in which all error logs are dumped

    def check(self,driver,x):
        try:
            driver.find_element_by_xpath(x)
        except:
            return False
        return True

    def isEnglish(self,s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def remspc(self,s):
        if s!='':
            i=0
            while s[i] == ' ':
                i+=1 
        return i
    
    def remQ(self,vname):
        vname=str(vname).replace('"','')
        vname=str(vname).replace('/','')
        vname=str(vname).replace('\\','')
        vname=str(vname).replace('\'','')
        vname=str(vname).replace('%','')
        return vname

    def myStrip(self,z):
        z=str(z).rstrip("'")
        z=str(z[2:])
        return z


    def fill_bd(self,url,con,driver):
        error_file = open(self.error_log_file, 'a+')
        file1=open('notFile','a+')
        file2=open('LnknotFile','a+')
        file3=open('err2File','a+')
        driver.get(url)
        count=con.execute('select count(*) from tbl_Floppy;').fetchone()[0]
        wait=1
        i=15000
        while i<=16000:
            if wait==50:
                wait=0
                print("Waiting")
                time.sleep(300)
            wait+=1
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
                driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
                driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(str(val))
                driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
                try:
                    if 'Actuellement indisponible' not in driver.page_source:
                        try:
                            if self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[5]/a')==True: 
                                try:
                                    link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/a').get_attribute('href')
                                except:
                                    try:
                                        link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/a').get_attribute('href')
                                    except:
                                        link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[5]/a').get_attribute('href')
                                
                                newTab = 'window.open("' + link + '", "_blank");'
                                driver.execute_script(newTab)
                                driver.switch_to_window(driver.window_handles[1])
                                time.sleep(4)
                                try:
                                    if self.check(driver,'//*[@id="raw-platform-refinement-div"]/fieldset[2]/ul/li/span/span/div/label/input')==True:
                                        j=1
                                        while j<=4:
                                            driver.find_element_by_xpath('//*[@id="raw-platform-refinement-div"]/fieldset[2]/ul/li/span/ul/span['+str(j)+']/div/label/input').click()
                                            time.sleep(1)
                                            if 'a actuellement pas de produits répondant à ces critères. Essayez de changer les filtres' not in driver.page_source:
                                                break
                                            j+=1
                                        print(j)
                                    else:
                                        driver.find_element_by_xpath('//*[@id="raw-platform-refinement-div"]/fieldset[2]/ul/span/div/label/input').click()
                                        time.sleep(1)
                                    
                                    lnk=driver.current_url
                                    lnk=str(lnk).replace('%','%%')
                                    now = datetime.datetime.now()
                                    date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)
                                    cnt=driver.find_elements_by_xpath('//*[@id="olpOfferList"]/div/div/div')
                                    j=2
                                    while j<=len(cnt):
                                        check=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[3]/p/a/b').text
                                        check=str(check).split('%')
                                        check=int(str(check[0]))
                                        if check>=80:
                                            try:
                                                price=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[1]/span').text
                                                cgn=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[2]/div[1]/span').text
                                                cgn=str(cgn).split('-')
                                                if len(cgn)>1:
                                                    cgn=str(cgn[1])
                                                else:
                                                    cgn=str(cgn[0])
                                                n=self.remspc(cgn)
                                                cgn=str(cgn[n:])
                                                cg=con.execute('SELECT Code_Grade FROM tbl_CGCGrade WHERE Amazon_FR="'+str(cgn)+'";').fetchone()[0]
                                                cg=self.myStrip(str(cg))
                                            
                                                sql='INSERT INTO tbl_Prices_Floppies(Issue_ID,Code_Grade,Price,ID_Website,link,date,InStock) VALUES('+str(i)+',"'+str(cg)+'","'+price+'",3,"'+lnk+'","'+date+'","Yes")'
                                                con.execute(sql)
                                                print(sql)
                                            except:
                                                error_file.write(str(val)+'\n')
                                                file3.write("Insert SQL Error"+'\n')
                                                traceback.print_exc()
                                                pass
                                        j+=1
                                except:
                                    error_file.write(str(val)+'\n')
                                    file3.write("Price link Error"+'\n')
                                    traceback.print_exc()
                                    pass

                                driver.execute_script('window.close()')
                                driver.switch_to_window(driver.window_handles[0])
                            else:
                                file2.write(str(val)+'\n')
                        except:
                            error_file.write(str(val)+'\n')
                            file3.write("Second click link Error"+'\n')
                            traceback.print_exc()
                            pass
                    elif 'Actuellement indisponible' in driver.page_source:
                        file1.write(str(val)+'\n')
                        lnk=driver.current_url
                        lnk=str(lnk).replace('%','%%')
                        now = datetime.datetime.now()
                        date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)
                        try:
                            sql='INSERT INTO tbl_Prices_Floppies(Issue_ID,ID_Website,link,date,InStock) VALUES('+str(i)+',3,"'+lnk+'","'+date+'","No")'
                            con.execute(sql)
                            print(sql)
                        except:
                            error_file.write(str(val)+'\n')
                            file3.write("Insert Error"+'\n')
                            traceback.print_exc()
                            pass
                        
                except:
                    error_file.write(str(val)+'\n')
                    file3.write("First click link Error"+'\n')
                    traceback.print_exc()
                    pass
            i+=1


        error_file.close()