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

class midTown:
    error_log_file = 'mtc' # file name in which all error logs are dumped

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
    def Econv(self,s):
        if self.isEnglish(s)==False:
            r=''
            for lat in range(len(s)-1):
                if self.isEnglish(s[lat])==True:
                    r=r+s[lat]
                else:
                    r=r+'e'
            s=r
        return s
    def remQ(self,vname):
        vname=str(vname).replace('"','')
        vname=str(vname).replace('/','')
        vname=str(vname).replace('\\','')
        vname=str(vname).replace('\'','')
        vname=str(vname).replace('%','')
        return vname

    def scrap_mtc_data(self,url,con,driver):
        error_file = open(self.error_log_file, 'a+')
        driver.get(url)
        keys=21
        while keys < 31:
            driver.find_element_by_xpath('//*[@id="pg"]').clear()
            driver.find_element_by_xpath('//*[@id="pg"]').send_keys(str(keys))
            driver.find_element_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span/a/span').click()
            trs=driver.find_elements_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr')
            i=1
            for tr in trs:
                if i>5:
                    try:
                        try:
                            stock=driver.find_element_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr['+str(i)+']/td/table/tbody/tr/td/table/tbody/tr/td[2]').text
                        except:
                            stock=''
                        link=driver.find_element_by_xpath('//*[@id="frmsearchpage"]/div/table/tbody/tr['+str(i)+']/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/a').get_attribute('href')
                        newTab = 'window.open("' + link + '", "_blank");'
                        driver.execute_script(newTab)
                        driver.switch_to_window(driver.window_handles[1])
                        time.sleep(15)
                        Ctitle,Mtitle=' ',' '
                        try:
                            title=driver.find_element_by_xpath('//*[@id="title-left"]/div[1]/div/a/h1').text
                            if ' TP' in title:
                                index=str(title).find(' TP')
                            elif ' HC' in title:
                                index=str(title).find(' HC')
                            size=str(title[index:index+3])
                            if ' Vol' in title:
                                indexV=str(title).find(' Vol')
                                vol=str(title[indexV:indexV+6])
                            else:
                                vol='N/A'
                            if ' Cover' not in title:
                                if ' Vol' in title and ' TP' in title or ' Vol' in title and ' HC' in title:
                                    t=title[title.find(vol):title.find(size)]
                                    t=str(t[len(vol):])
                                    if len(t) < 3:
                                        Ctitle='N/A'
                                    else:
                                        Ctitle=str(t)
                                    Mtitle=str(title).split(vol)
                                    Mtitle=str(Mtitle[0])
                                elif ' Vol' not in title:
                                    t=str(title).split(size)
                                    t=str(t[0])
                                    Ctitle=str(t)
                                    Mtitle=str(t)
                            else:
                                Ctitle=str(title)
                                Mtitle=str(title)
                            try:
                                publisher=driver.find_element_by_xpath('//*[@id="ipd_pub-date"]/a[1]').text
                            except:
                                publisher='N/A'
                            try:
                                rdate=driver.find_element_by_xpath('//*[@id="ipd_pub-date"]/a[2]').text
                            except:
                                rdate='N/A'
                            try:
                                cover_price=driver.find_element_by_xpath('//*[@id="price"]/span[1]/strike').text
                            except:
                                cover_price='N/A'
                            try:
                                if self.check(driver,'//*[@id="description"]/p/span[2]/a')==True:
                                    driver.find_element_by_xpath('//*[@id="description"]/p/span[2]/a').click()
                                    summary=driver.find_element_by_xpath('//*[@id="description"]/p').text
                                else:
                                    summary=driver.find_element_by_xpath('//*[@id="description"]/p').text
                            except:
                                summary='N/A'
                            if 'Collecting' in summary:
                                notes=str(summary).split('Collecting')
                                summary=str(notes[0])
                                notes="Collecting "+str(notes[1])
                            else:
                                notes='N/A'

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
                            try:
                                isbn13=driver.find_element_by_xpath('//*[@id="description"]/div').text
                                isbn13=str(isbn13).split('ISBN:')
                                isbn13=str(isbn13[1])
                                if 'UPC' in isbn13:
                                    isbn13=str(isbn13).split('UPC')
                                    isbn13=str(isbn13[0])
                            except:
                                isbn13='N/A'

                            if 'OUT OF STOCK' in stock:
                                stock='No'
                            else:
                                stock='N/A'
                            try:
                                pic=driver.find_element_by_xpath('//*[@id="SP_ProductImage"]/img').get_attribute('src')
                            except:
                                try:
                                    pic=driver.find_element_by_xpath('//*[@id="SP_ProductImage"]/a/img').get_attribute('src')
                                except:
                                    pic='N/A'
                            
                            try:
                                try:
                                    sql='INSERT INTO tbl_Collected(Title,Title_MTC,Volume_Number,Release_Date,Cover_Price,Size,ISBN13,Summary,Notes,In_Print,Picture,Midtown_Link,Diamond_code,Midtown_code,Publisher) VALUES("'+Ctitle+'","'+Mtitle+'","'+vol+'","'+rdate+'","'+cover_price+'","'+size+'","'+isbn13+'","'+summary+'","'+notes+'","'+stock+'","'+pic+'","'+link+'","'+dcode+'","'+mcode+'","'+publisher+'")'
                                    con.execute(sql)
                                    print(sql)
                                except:
                                    try:
                                        Ctitle=self.remQ(Ctitle)
                                        Mtitle==self.remQ(Mtitle)
                                        summary=self.remQ(summary)
                                        notes=self.remQ(notes)
                                        link=str(link).replace('%','')
                                        sql='INSERT INTO tbl_Collected(Title,Title_MTC,Volume_Number,Release_Date,Cover_Price,Size,ISBN13,Summary,Notes,In_Print,Picture,Midtown_Link,Diamond_code,Midtown_code,Publisher) VALUES("'+Ctitle+'","'+Mtitle+'","'+vol+'","'+rdate+'","'+cover_price+'","'+size+'","'+isbn13+'","'+summary+'","'+notes+'","'+stock+'","'+pic+'","'+link+'","'+dcode+'","'+mcode+'","'+publisher+'")'
                                        con.execute(sql)
                                        print(sql)                               
                                    except:
                                        summary=self.Econv(summary)
                                        notes=self.Econv(notes)
                                        sql='INSERT INTO tbl_Collected(Title,Title_MTC,Volume_Number,Release_Date,Cover_Price,Size,ISBN13,Summary,Notes,In_Print,Picture,Midtown_Link,Diamond_code,Midtown_code,Publisher) VALUES("'+Ctitle+'","'+Mtitle+'","'+vol+'","'+rdate+'","'+cover_price+'","'+size+'","'+isbn13+'","'+summary+'","'+notes+'","'+stock+'","'+pic+'","'+link+'","'+dcode+'","'+mcode+'","'+publisher+'")'
                                        con.execute(sql)
                                        print(sql)

                                now = datetime.datetime.now()
                                date=str(now.second)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.day)+':'+str(now.month)+':'+str(now.year)

                                sql='INSERT INTO tbl_Prices_Collected(Price,ID_Website,link,Diamond_Code,date,InStock,Midtown_Code) VALUES("'+cover_price+'","1","'+link+'","'+dcode+'","'+date+'","'+stock+'","'+mcode+'")'
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