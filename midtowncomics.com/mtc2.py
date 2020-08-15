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
from SqlDB import MysqlDb

class midTown2:
    error_log_file = 'mtc2' # file name in which all error logs are dumped

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

    def scrap_mtc_data2(self,url,con,driver):
        error_file = open(self.error_log_file, 'a+')
        driver.get(url)
        keys=1
        while keys < 131:
            driver.find_element_by_xpath('//*[@id="pg"]').clear()
            driver.find_element_by_xpath('//*[@id="pg"]').send_keys(str(keys))
            driver.find_element_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span/a/span').click()
            time.sleep(5)
            trs=driver.find_elements_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr')
            i=1
            for tr in trs:
                if i>5:
                    try:
                        link=driver.find_element_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr['+str(i)+']/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/a').get_attribute('href')
                        newTab = 'window.open("' + link + '", "_blank");'
                        driver.execute_script(newTab)
                        driver.switch_to_window(driver.window_handles[1])
                        time.sleep(5)
                        try:
                            avail=driver.find_element_by_xpath('//*[@id="frmPRSeriesTitle"]/table/tbody/tr[1]/td[1]/div').text
                        except:
                            avail=''
                        if 'AVAILABLE IN MULTIPLE COVERS' in avail:
                            trs2=driver.find_elements_by_xpath('//*[@id="frmPRSeriesTitle"]/table/tbody/tr')
                            j=1
                            for tr2 in trs2:
                                if j>1:
                                    try:
                                        driver.find_element_by_xpath('//*[@id="frmPRSeriesTitle"]/table/tbody/tr['+str(j)+']/td[1]/a').click()
                                        time.sleep(6)
                                        try:
                                            title=driver.find_element_by_xpath('//*[@id="title-left"]/div[1]/div/a/h1').text
                                            issue=str(title).split('#')
                                            dlm=str(issue[1])
                                            issue=str(dlm[0:2])
                                            cv=str(dlm).split(issue)
                                            cv=str(cv[1])
                                            cv=str(cv[0:8])
                                            try:
                                                nv=title[title.find(cv):len(title)]
                                                nv=str(nv).split(cv)
                                                nv=str(nv[1])
                                            except:
                                                nv=''
                                            if 'Cover' in nv:
                                                cn=str(nv).split('Cover')
                                                cn=str(cn[0])
                                            else:
                                                cn=nv
                                            try:
                                                titleF=str(title).split('#')
                                                titleF=str(titleF[0])
                                            except:
                                                titleF=title
                                            try:
                                                publisher=driver.find_element_by_xpath('//*[@id="ipd_pub-date"]/a[1]').text
                                            except:
                                                publisher='N/A'
                                            try:
                                                rdate=driver.find_element_by_xpath('//*[@id="ipd_pub-date"]/a[2]').text
                                            except:
                                                rdate='N/A'
                                            try:
                                                if self.check(driver,'//*[@id="description"]/p/span[2]/a')==True:
                                                    driver.find_element_by_xpath('//*[@id="description"]/p/span[2]/a').click()
                                                    synopsis=driver.find_element_by_xpath('//*[@id="description"]/p').text
                                                else:
                                                    synopsis=driver.find_element_by_xpath('//*[@id="description"]/p').text
                                            except:
                                                synopsis='N/A'
                                            try:
                                                upc=driver.find_element_by_xpath('//*[@id="description"]/div').text
                                                upc=str(upc).split('UPC:')
                                                upc=str(upc[1])
                                            except:
                                                upc='N/A'
                                            try:
                                                pic=driver.find_element_by_xpath('//*[@id="SP_ProductImage"]/img').get_attribute('src')
                                            except:
                                                try:
                                                    pic=driver.find_element_by_xpath('//*[@id="SP_ProductImage"]/a/img').get_attribute('src')
                                                except:
                                                    pic='N/A'

                                            try:
                                                mcode=driver.find_element_by_xpath('//*[@id="itemno_container"]').text
                                                mcode=str(mcode).split(':')
                                                mcode=str(mcode[1])
                                            except:
                                                mcode='N/A'
                                            try:
                                                dcode=driver.find_element_by_xpath('//*[@id="diamond_container"]').text
                                            except:
                                                dcode='N/A'
                                            link=driver.current_url
                                            link=str(link).replace('%','')
                                            delim=str(link).split('_')
                                            delim=str(delim[len(delim)-1])
                                            n=self.remspc(delim)
                                            delim=str(delim[n:])

                                            trs3=driver.find_elements_by_xpath('//*[@id="container_grades"]/table/tbody/tr')
                                            try:
                                                k=1
                                                for tr3 in trs3:
                                                    if k>1:
                                                        driver.find_element_by_xpath('//*[@id="container_grades"]/table/tbody/tr['+str(k)+']/td[1]').click()
                                                        time.sleep(10)
                                                        try:
                                                            stock=driver.find_element_by_xpath('//*[@id="dv'+str(delim)+'"]/div[3]/span/img').get_attribute('alt')
                                                            if "Out of Stock" in stock:
                                                                stock='N'
                                                            else:
                                                                stock='N/A'
                                                        except:
                                                            stock='N/A'
                                                        cgn=driver.find_element_by_xpath('//*[@id="container_grades"]/table/tbody/tr['+str(k)+']/td[2]/div').text
                                                        price=driver.find_element_by_xpath('//*[@id="container_grades"]/table/tbody/tr['+str(k)+']/td[3]').text
                                                        now = datetime.datetime.now()
                                                        date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)
                                                        cg=con.execute('SELECT Code_Grade FROM tbl_CGCGrade WHERE Name_Grade="'+str(cgn)+'";').fetchone()[0]
                                                        sql='INSERT INTO tbl_Prices_Floppies(Code_Grade,Price,ID_Website,link,Diamond_Code,Publisher,date,InStock,Midtown_Code) VALUES("'+str(cg)+'","'+price+'","1","'+link+'","'+dcode+'","'+publisher+'","'+date+'","'+stock+'","'+mcode+'")'
                                                        con.execute(sql)
                                                        print(sql)
                                                    k+=1
                                                synopsis=self.remQ(synopsis)
                                                titleF=self.remQ(titleF)
                                                nv=self.remQ(nv)
                                                cv=self.remQ(cv)
                                                cn=self.remQ(cn)
                                                sql='INSERT INTO tbl_Floppy(Title_MTC,Issue_Number,Release_Date,Publisher,Synopsis,ISBN_UPC,Picture,Midtown_Link,Diamond_code,Midtown_code) VALUES("'+str(titleF)+'","'+issue+'","'+rdate+'","'+publisher+'","'+synopsis+'","'+upc+'","'+str(pic)+'","'+str(link)+'","'+str(dcode)+'","'+str(mcode)+'")'
                                                con.execute(sql)
                                                print(sql)

                                                sql='INSERT INTO tbl_Variant(Name_variant,Code_Variant,Midtown_Link,Picture,Cover_Creator_Name) VALUES("'+nv+'","'+cv+'","'+link+'","'+pic+'","'+cn+'")'
                                                con.execute(sql)
                                                print(sql)
                                            except:
                                                traceback.print_exc()
                                                print("SQL Error")
                                                error_file.write('SQL Error '+str(link)+'\n')
                                                pass
                                        except:
                                            traceback.print_exc()
                                            print("Data Scrap Error")
                                            error_file.write('Data Scrap Error '+str(link)+'\n')
                                            pass
                                    except:
                                        pass
                                j+=1

                        else:
                            try:
                                title=driver.find_element_by_xpath('//*[@id="title-left"]/div[1]/div/a/h1').text
                                try:
                                    issue=str(title).split('#')
                                    if len(issue)>1:
                                        issue=issue[len(issue)-1]
                                    else:
                                        issue='N/A'
                                except:
                                    issue='N/A'
                                try:
                                    titleF=str(title).split('#')
                                    titleF=str(titleF[0])
                                except:
                                    titleF=title
                                try:
                                    publisher=driver.find_element_by_xpath('//*[@id="ipd_pub-date"]/a[1]').text
                                except:
                                    publisher='N/A'
                                try:
                                    rdate=driver.find_element_by_xpath('//*[@id="ipd_pub-date"]/a[2]').text
                                except:
                                    rdate='N/A'    
                                try:
                                    if self.check(driver,'//*[@id="description"]/p/span[2]/a')==True:
                                        driver.find_element_by_xpath('//*[@id="description"]/p/span[2]/a').click()
                                        synopsis=driver.find_element_by_xpath('//*[@id="description"]/p').text
                                    else:
                                        synopsis=driver.find_element_by_xpath('//*[@id="description"]/p').text
                                except:
                                    synopsis='N/A'
                                try:
                                    upc=driver.find_element_by_xpath('//*[@id="description"]/div').text
                                    upc=str(upc).split('UPC:')
                                    upc=str(upc[1])
                                except:
                                    upc='N/A'
                                try:
                                    pic=driver.find_element_by_xpath('//*[@id="SP_ProductImage"]/img').get_attribute('src')
                                except:
                                    try:
                                        pic=driver.find_element_by_xpath('//*[@id="SP_ProductImage"]/a/img').get_attribute('src')
                                    except:
                                        pic='N/A'

                                try:
                                    mcode=driver.find_element_by_xpath('//*[@id="itemno_container"]').text
                                    mcode=str(mcode).split(':')
                                    mcode=str(mcode[1])
                                except:
                                    mcode='N/A'
                                try:
                                    dcode=driver.find_element_by_xpath('//*[@id="diamond_container"]').text
                                except:
                                    dcode='N/A'
                                link=driver.current_url
                                link=str(link).replace('%','')
                                delim=str(link).split('_')
                                delim=str(delim[len(delim)-1])
                                n=self.remspc(delim)
                                delim=str(delim[n:])
                                trs3=driver.find_elements_by_xpath('//*[@id="container_grades"]/table/tbody/tr')
                                try:
                                    k=1
                                    for tr3 in trs3:
                                        if k>1:
                                            driver.find_element_by_xpath('//*[@id="container_grades"]/table/tbody/tr['+str(k)+']/td[1]').click()
                                            time.sleep(10)
                                            try:
                                                stock=driver.find_element_by_xpath('//*[@id="dv'+str(delim)+'"]/div[3]/span/img').get_attribute('alt')
                                                if "Out of Stock" in stock:
                                                    stock='N'
                                                else:
                                                    stock='N/A'
                                            except:
                                                stock='N/A'
                                            cgn=driver.find_element_by_xpath('//*[@id="container_grades"]/table/tbody/tr['+str(k)+']/td[2]/div').text
                                            price=driver.find_element_by_xpath('//*[@id="container_grades"]/table/tbody/tr['+str(k)+']/td[3]').text
                                            now = datetime.datetime.now()
                                            date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)
                                            cg=con.execute('SELECT Code_Grade FROM tbl_CGCGrade WHERE Name_Grade="'+str(cgn)+'";').fetchone()[0]
                                            sql='INSERT INTO tbl_Prices_Floppies(Code_Grade,Price,ID_Website,link,Diamond_Code,Publisher,date,InStock,Midtown_Code) VALUES("'+str(cg)+'","'+price+'","1","'+link+'","'+dcode+'","'+publisher+'","'+date+'","'+stock+'","'+mcode+'")'
                                            con.execute(sql)
                                            print(sql)
                                        k+=1
                                    synopsis=self.remQ(synopsis)
                                    titleF=self.remQ(titleF)
                                    sql='INSERT INTO tbl_Floppy(Title_MTC,Issue_Number,Release_Date,Publisher,Synopsis,ISBN_UPC,Picture,Midtown_Link,Diamond_code,Midtown_code) VALUES("'+str(titleF)+'","'+issue+'","'+rdate+'","'+publisher+'","'+synopsis+'","'+upc+'","'+str(pic)+'","'+str(link)+'","'+str(dcode)+'","'+str(mcode)+'")'
                                    con.execute(sql)
                                    print(sql)
                                except:
                                    traceback.print_exc()
                                    print("SQL Error")
                                    error_file.write('SQL Error '+str(link)+'\n')
                                    pass
                            except:
                                traceback.print_exc()
                                print("Data Scrap Error")
                                error_file.write('Data Scrap Error '+str(link)+'\n')
                                pass

                        driver.execute_script('window.close()')
                        driver.switch_to_window(driver.window_handles[0])
                    except:
                        print("Link Error")
                        error_file.write('Link Error '+str(link)+'\n')
                        pass
                i+=1
            keys+=1
        error_file.close()