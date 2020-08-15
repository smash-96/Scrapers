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
        file1=open('notFile.txt','a+')
        file2=open('DataLinkNotFound.txt','a+')
        file3=open('PricesLinkNotFound.txt','a+')
        file4=open('NoResults.txt','a+')
        driver.get(url)
        count=con.execute('select count(*) from tbl_Floppy;').fetchone()[0]
        wait=1
        i=101
        while i<=200:
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
                time.sleep(2)
                try:
                    if "Aucun résultat pour" not in driver.page_source:
                        if self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')==True or self.check(driver,'//*[@id="result_0"]/div/div/div/div[2]/div[1]/div[1]/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h5/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/h2/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/h2/a')==True: 
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
                                adate=driver.find_element_by_xpath('//*[@id="title"]/span[3]').text
                                adate=str(adate).split(' ')
                                if str(adate[1]).isdigit():
                                    adate=str(adate[1])
                                else:
                                    adate='N/A'

                                if val10!='' and val10!=' ' and val10!='N/A':
                                    if adate!='N/A':
                                        bdate=str(con.execute('SELECT Release_Date from tbl_Floppy WHERE ISBN="'+str(val10)+'";').fetchone()[0])
                                        bdate=self.myStrip(bdate)
                                        if 'Parution' in bdate:
                                            bdate=str(bdate).split('(')
                                            
                                            if '/' in str(bdate[0]):
                                                bdates=str(bdate[0]).split('/')
                                                
                                                if len(bdates)==2:
                                                    bdate=str(str(adate)+"/"+str(bdate[0]))
                                        else:
                                            if '/' in str(bdate):
                                                bdates=str(bdate).split('/')
                                                if len(bdates)==2:
                                                    bdate=str(str(adate)+"/"+str(bdate))
                                elif val13!='' and val13!=' ' and val13!='N/A':
                                    if adate!='N/A':
                                        bdate=str(con.execute('SELECT Release_Date from tbl_Floppy WHERE ISBN13="'+str(val13)+'";').fetchone()[0])
                                        bdate=self.myStrip(bdate)
                                        if 'Parution' in bdate:
                                            bdate=str(bdate).split('(')
                                            
                                            if '/' in str(bdate[0]):
                                                bdates=str(bdate[0]).split('/')
                                                if len(bdates)==2:
                                                    bdate=str(str(adate)+"/"+str(bdate[0]))
                                        else:
                                            if '/' in str(bdate):
                                                bdates=str(bdate).split('/')
                                                if len(bdates)==2:
                                                    bdate=str(str(adate)+"/"+str(bdate))
                            except:
                                if val10!='' and val10!=' ' and val10!='N/A':
                                    bdate=str(con.execute('SELECT Release_Date from tbl_Floppy WHERE ISBN="'+str(val10)+'";').fetchone()[0])
                                    bdate=self.myStrip(bdate)
                                elif val13!='' and val13!=' ' and val13!='N/A':
                                    bdate=str(con.execute('SELECT Release_Date from tbl_Floppy WHERE ISBN13="'+str(val13)+'";').fetchone()[0])
                                    bdate=self.myStrip(bdate)
                                pass
                            try:
                                pc,dh,dw,dl,i10,i13='','','','','',''
                                lis=driver.find_elements_by_xpath('//*[@id="detail_bullets_id"]/table/tbody/tr/td/div/ul/li')
                                for li in lis:
                                    lit=li.text
                                    lit=str(lit).split(':')
                                    if 'Tankobon broché' in str(lit[0]) or 'Broché' in str(lit[0]) or 'Poche' in str(lit[0]) or 'Relié' in str(lit[0]) or 'Album' in str(lit[0]) or 'Belle reliure' in str(lit[0]):
                                        try:
                                            pc=str(con.execute('SELECT Page_Count from tbl_Floppy WHERE Issue_ID="'+str(i)+'";').fetchone()[0])
                                            if pc=='' or pc==' ':
                                                pc=str(lit[1])
                                        except:
                                            if pc=='' or pc==' ':
                                                pc=str(lit[1])
                                        pc=str(self.myStrip(pc))
                                    elif 'Dimensions du produit' in str(lit[0]) or 'Dimensions du colis' in str(lit[0]):
                                        d=str(lit[1]).split('x')
                                        if len(d)==2:
                                            dh='N/A'
                                            dw=str(d[0])
                                            dl=str(d[1])
                                        elif len(d)==1:
                                            dh='N/A'
                                            dw='N/A'
                                            dl=str(d[0])
                                        else:
                                            dh=str(d[0])
                                            dw=str(d[1])
                                            dl=str(d[2])
                                    elif 'ISBN-10' in str(lit[0]):
                                        i10=str(lit[1])
                                        n=self.remspc(str(i10))
                                        i10=str(i10[n:])
                                    elif 'ISBN-13' in str(lit[0]):
                                        i13=str(lit[1])
                                        i13=str(i13).split('-')
                                        if len(i13)>1:
                                            i13=str(i13[0])+str(i13[1])
                                        else:
                                            i13=str(i13[0])
                                        n=self.remspc(str(i13))
                                        i13=str(i13[n:])  
                                try:
                                    if val10!='' and val10!=' ' and val10!='N/A':
                                        sql='UPDATE tbl_Floppy SET Release_Date="'+str(bdate)+'",Dimension_L="'+str(dl)+'",Dimension_W="'+str(dw)+'",Dimension_H="'+str(dh)+'",Page_Count="'+str(pc)+'",ISBN13="'+str(i13)+'" WHERE ISBN="'+str(val10)+'";'
                                    elif val13!='' and val13!=' ' and val13!='N/A':
                                        sql='UPDATE tbl_Floppy SET Release_Date="'+str(bdate)+'",Dimension_L="'+str(dl)+'",Dimension_W="'+str(dw)+'",Dimension_H="'+str(dh)+'",Page_Count="'+str(pc)+'",ISBN="'+str(i10)+'" WHERE ISBN13="'+str(val13)+'";'
                                    con.execute(sql)
                                    print(sql)
                                except:
                                    error_file.write(str(val)+'\n')
                                    traceback.print_exc()
                                    pass
                            except:
                                error_file.write(str(val)+'\n')
                                traceback.print_exc()
                                pass
                            driver.execute_script('window.close()')
                            driver.switch_to_window(driver.window_handles[0])

                            if 'Actuellement indisponible' not in driver.page_source:
                                try:
                                    if self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[5]/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[3]/div/div[3]/div/a')==True: 
                                        try:
                                            link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/a').get_attribute('href')
                                        except:
                                            try:
                                                link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/a').get_attribute('href')
                                            except:
                                                try:
                                                    link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[5]/a').get_attribute('href')
                                                except:
                                                    try:
                                                        link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/a').get_attribute('href')
                                                    except:
                                                        link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[3]/div/div[3]/div/a').get_attribute('href')
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
                                                        traceback.print_exc()
                                                        pass
                                                    
                                                j+=1
                                        except:
                                            error_file.write(str(val)+'\n')
                                            traceback.print_exc()
                                            pass

                                        driver.execute_script('window.close()')
                                        driver.switch_to_window(driver.window_handles[0])
                                    else:
                                        file3.write(str(val)+'\n')
                                except:
                                    error_file.write(str(val)+'\n')
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
                                    traceback.print_exc()
                                    pass
                        else:
                            file2.write(str(val)+'\n')   
                    else:
                        file4.write(str(val)+'\n')
                except:
                    error_file.write(str(val)+'\n')
                    traceback.print_exc()
                    pass
            time.sleep(2)
            i+=1


        error_file.close()