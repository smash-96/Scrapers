# -*- coding: utf-8 -*-
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
from SqlDB_mtc import MysqlDb_mtc

class mtc:
    error_log_file = 'mtc.txt' # file name in which all error logs are dumped

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


    def fill_mtc(self,url,con,driver):
        error_file = open(self.error_log_file, 'a+')
        file1=open('DataLinkNotFound.txt','a+')
        file2=open('NoResults.txt','a+')
        file3=open('Stockless.txt','a+')
        driver.get(url)
        count=con.execute('select count(*) from tbl_Collected;').fetchone()[0]

        q2="select ISBN13 from tbl_Collected;"
        r2=con.execute(q2).fetchall()
       
        wait=1
        i=400
        while i<=410:
            if wait==50:
                wait=0
                print("Waiting")
                time.sleep(300)
            wait+=1
            
            isbn13=str(r2[i])
            
            val=''
            val13=''
            if 'N/A' not in isbn13:
                isbn13=str(isbn13[3:16])
                print(isbn13)

                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
                driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(str(isbn13))
                driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
                time.sleep(2)
                try:
                    if "No results for" not in driver.page_source:
                        try:
                            if "comiXology" in driver.page_source:
                                form=driver.find_elements_by_partial_link_text('Kindle & comiXology')
                                lnk=''
                                for fm in form:
                                    lnk=fm.get_attribute('href')
                                    if lnk!='None':
                                        break
                                newTab = 'window.open("' + lnk + '", "_blank");'
                                driver.execute_script(newTab)
                                driver.switch_to_window(driver.window_handles[1])
                                time.sleep(5)
                                try:
                                    asin=''
                                    lis=driver.find_elements_by_xpath('//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li')
                                    for li in lis:
                                        lit=li.text
                                        lit=str(lit).split(':')
                                        if 'ASIN' in str(lit[0]):
                                            asin=str(lit[1])
                                            break
                                    
                                    if asin!='':
                                        sql='UPDATE tbl_Collected SET ASIN_V="'+str(asin)+'", On_Comixology="Yes" WHERE ISBN13="'+str(isbn13)+'";'
                                        con.execute(sql)
                                        print(sql)
                                except:
                                    error_file.write("Comixology Page Error "+str(isbn13)+'\n')
                                    traceback.print_exc()
                                    pass

                                driver.execute_script('window.close()')
                                driver.switch_to_window(driver.window_handles[0])
                        except:
                            error_file.write("Comixology Link Error "+str(isbn13)+'\n')
                            traceback.print_exc()
                            pass

                        time.sleep(2)
                        sz=str(con.execute('SELECT Size from tbl_Collected WHERE ISBN13="'+str(isbn13)+'";').fetchone()[0])

                        if "TP" in sz or "HC" in sz:
                            if "TP" in sz:
                                sz="Paperback"
                            elif "HC" in sz:
                                sz="Hardcover"

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
                                mdate=str(con.execute('SELECT Release_Date from tbl_Collected WHERE ISBN13="'+str(isbn13)+'";').fetchone()[0])
                                mdate=self.myStrip(mdate)
                                ck=str(mdate).split('/')
                                if len(ck) < 3:
                                    adate=driver.find_element_by_xpath('//*[@id="title"]/span[3]').text
                                
                                USlink=driver.current_url
                                pc,dh,dw,dl,i10,wt='','','','','',''
                                lis=driver.find_elements_by_xpath('//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li')
                                for li in lis:
                                    lit=li.text
                                    lit=str(lit).split(':')

                                    if 'Paperback' in str(lit[0]) or 'Hardcover' in str(lit[0]):
                                        pc=str(lit[1])
                                    elif 'Product Dimensions' in str(lit[0]):
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
                                    elif 'Shipping Weight' in str(lit[0]):
                                        wt=str(lit[1])
                                        if '(' in wt:
                                            wt=str(wt).split('(')
                                            wt=str(wt[0])

                                sql='UPDATE tbl_Collected SET Weight="'+str(wt)+'",AmazonUS_Link="'+str(USlink)+'", Dimension_L="'+str(dl)+'",Dimension_W="'+str(dw)+'",Dimension_H="'+str(dh)+'",Page_Count="'+str(pc)+'",ISBN_Number="'+str(i10)+'" WHERE ISBN13="'+str(isbn13)+'";'
                                con.execute(sql)
                                print(sql)
                            except:
                                error_file.write("Main Page Data Error "+str(isbn13)+'\n')
                                traceback.print_exc()
                                pass   

                            driver.execute_script('window.close()')
                            driver.switch_to_window(driver.window_handles[0])

                            time.sleep(2)
                            try:
                                if self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[5]/a')==True or self.check(driver,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/a')==True: 
                                    try:
                                        link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/a').get_attribute('href')
                                    except:
                                        try:
                                            link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/a').get_attribute('href')
                                        except:
                                            try:
                                                link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[5]/a').get_attribute('href')
                                            except:
                                                link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[4]/a').get_attribute('href')

                                    newTab = 'window.open("' + link + '", "_blank");'
                                    driver.execute_script(newTab)
                                    driver.switch_to_window(driver.window_handles[1])
                                    time.sleep(5)
                                    try:
                                        if self.check(driver,'//*[@id="raw-platform-refinement-div"]/fieldset/ul/li/span/span/div/label/input')==True:
                                            j=1
                                            while j<=4:
                                                driver.find_element_by_xpath('//*[@id="raw-platform-refinement-div"]/fieldset/ul/li/span/ul/span['+str(j)+']/div/label/input').click()
                                                time.sleep(1)
                                                if 'There are currently no listings for this search. Try a different' not in driver.page_source:
                                                    break
                                                j+=1
                                        else:
                                            driver.find_element_by_xpath('//*[@id="raw-platform-refinement-div"]/fieldset/ul/span/div/label/input').click()
                                            time.sleep(1)
                                        

                                        lnk=driver.current_url
                                        lnk=str(lnk).replace('%','%%')
                                        now = datetime.datetime.now()
                                        date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)
                                        cnt=driver.find_elements_by_xpath('//*[@id="olpOfferList"]/div/div/div')
                                        j=2
                                        while j<=len(cnt):
                                            check=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[4]/p/a/b').text
                                            check=str(check).split('%')
                                            check=int(str(check[0]))
                                            if check>=80:
                                                price=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[1]/span').text
                                                cgn=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[2]/div[1]/span').text
                                                cgn=str(cgn).split('-')
                                                if len(cgn)>1:
                                                    cgn=str(cgn[1])
                                                else:
                                                    cgn=str(cgn[0])
                                                n=self.remspc(cgn)
                                                cgn=str(cgn[n:])
                                                cg=con.execute('SELECT Name_Short_Condition FROM tbl_Condition WHERE NCond_Amazon_US="'+str(cgn)+'";').fetchone()[0]
                                                cg=self.myStrip(str(cg))
                                            
                                                sql='INSERT INTO tbl_Prices_Collected(Name_Short_Condition,Price,ID_Website,link,date,InStock,ISBN13) VALUES("'+str(cg)+'","'+price+'",2,"'+lnk+'","'+date+'","Yes","'+str(isbn13)+'")'
                                                con.execute(sql)
                                                print(sql)
                                            j+=1
                                    except:
                                        error_file.write("Prices Page Data Error "+str(isbn13)+'\n')
                                        traceback.print_exc()
                                        pass
                                    driver.execute_script('window.close()')
                                    driver.switch_to_window(driver.window_handles[0])
                                else:
                                    content=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]').text
                                    temp=content[content.find(sz):content.find(')')]
                                    if 'left in stock' not in temp:
                                        content=content[content.find(sz):content.find(')')]
                                        content=str(content).split(' (')
                                        content=str(content[1])
                                        newl=driver.find_elements_by_partial_link_text(content)
                                        lnk=''
                                        for l in newl:
                                            lnk=l.get_attribute('href')
                                            if lnk!='None':
                                                break
                                        newTab = 'window.open("' + lnk + '", "_blank");'
                                        driver.execute_script(newTab)
                                        driver.switch_to_window(driver.window_handles[1])
                                        time.sleep(5)
                                        try:
                                            if self.check(driver,'//*[@id="raw-platform-refinement-div"]/fieldset/ul/li/span/span/div/label/input')==True:
                                                j=1
                                                while j<=4:
                                                    driver.find_element_by_xpath('//*[@id="raw-platform-refinement-div"]/fieldset/ul/li/span/ul/span['+str(j)+']/div/label/input').click()
                                                    time.sleep(1)
                                                    if 'There are currently no listings for this search. Try a different' not in driver.page_source:
                                                        break
                                                    j+=1
                                            else:
                                                driver.find_element_by_xpath('//*[@id="raw-platform-refinement-div"]/fieldset/ul/span/div/label/input').click()
                                                time.sleep(1)
                                            

                                            lnk=driver.current_url
                                            lnk=str(lnk).replace('%','%%')
                                            now = datetime.datetime.now()
                                            date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)
                                            cnt=driver.find_elements_by_xpath('//*[@id="olpOfferList"]/div/div/div')
                                            j=2
                                            while j<=len(cnt):
                                                check=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[4]/p/a/b').text
                                                check=str(check).split('%')
                                                check=int(str(check[0]))
                                                if check>=80:
                                                    price=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[1]/span').text
                                                    cgn=driver.find_element_by_xpath('//*[@id="olpOfferList"]/div/div/div['+str(j)+']/div[2]/div[1]/span').text
                                                    cgn=str(cgn).split('-')
                                                    if len(cgn)>1:
                                                        cgn=str(cgn[1])
                                                    else:
                                                        cgn=str(cgn[0])
                                                    n=self.remspc(cgn)
                                                    cgn=str(cgn[n:])
                                                    cg=con.execute('SELECT Name_Short_Condition FROM tbl_Condition WHERE NCond_Amazon_US="'+str(cgn)+'";').fetchone()[0]
                                                    cg=self.myStrip(str(cg))
                                                
                                                    sql='INSERT INTO tbl_Prices_Collected(Name_Short_Condition,Price,ID_Website,link,date,InStock,ISBN13) VALUES("'+str(cg)+'","'+price+'",2,"'+lnk+'","'+date+'","Yes","'+str(isbn13)+'")'
                                                    con.execute(sql)
                                                    print(sql)
                                                j+=1
                                        except:
                                            error_file.write("Prices Page Data Error "+str(isbn13)+'\n')
                                            traceback.print_exc()
                                            pass
                                        driver.execute_script('window.close()')
                                        driver.switch_to_window(driver.window_handles[0])
                                    else:
                                        file3.write(str(isbn13)+'\n')
                                    
                            except:
                                error_file.write("Prices Link Error "+str(isbn13)+'\n')
                                traceback.print_exc()
                                pass
                        else:
                            file1.write(str(isbn13)+'\n')
                    else:
                        file2.write(str(isbn13)+'\n')
                except:
                    error_file.write("Unknown Error "+str(isbn13)+'\n')
                    traceback.print_exc()
                    pass
            time.sleep(2)
            i+=1
        
