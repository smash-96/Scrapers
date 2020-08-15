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
from SqlDB import MysqlDb 

file1 = open("fu.txt", "w")
file2 = open("cfu.txt", "w")
class CollectedFloppy:
    error_log_file = 'cf' # file name in which all error logs are dumped

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
        
    def scrap_cf_data(self, url, con, driver):
        error_file = open(self.error_log_file, 'a+')
        driver.get(url)
        tables = [
            '/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[1]/a', 
            '/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[3]/a'
        ]

        for table in tables[0:1]:
            links = driver.find_elements_by_xpath(table)
            i=0
            for x in links[2:100]:
                try:
                    if x.get_attribute('href') != None:
                        uu=x.get_attribute('href')
                        if i==50:
                            i=0
                            print("Waiting....")
                            time.sleep(300)
                        i=i+1
                        newTab = 'window.open("' + x.get_attribute('href') + '", "_blank");'
                        driver.execute_script(newTab)
                        driver.switch_to_window(driver.window_handles[1])
                        urls = driver.find_elements_by_class_name('page_link')
                        
                        self.helper(urls, driver, con)
     
                except TimeoutException:
                    traceback.print_exc()
                    error_file.write('Title Time Out '+uu+'\n')
                    print("NoSql")
                    pass
                except NoSuchElementException:
                    traceback.print_exc()
                    error_file.write('Title No Element '+uu+'\n')
                    print("NoSql")
                    pass
                except StaleElementReferenceException as e:
                    traceback.print_exc()
                    error_file.write('Title Stale Element '+uu+'\n')
                    print("NoSql")
                    pass
                except:
                    traceback.print_exc()
                    error_file.write('No Title '+uu+'\n')
                    print("NoSql")
                    pass
                driver.execute_script('window.close()')
                driver.switch_to_window(driver.window_handles[0])
        error_file.close()
             
    def helper(self, urls, driver, con):
        error_file = open(self.error_log_file, 'a+')
        
        alist=["Writer(s):","Penciller(s):","Inker(s):","Colorist(s):","Letterer(s):","Editor(s):","Cover Artist(s):"]
        for url in urls[10:]:
            newTab = 'window.open("' + url.get_attribute('href') + '", "_blank");'
            u = url.get_attribute('href')
            try:
                driver.execute_script(newTab)
                driver.switch_to_window(driver.window_handles[2])
                if 'Reprint' in driver.page_source:
                    cf=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
                    cf=cf[cf.find('Reprint'):cf.find('Characters:')]
                    try:
                        cf=str(cf).split('\n')
                    except:
                        if self.isEnglish(cf)==False:
                            r=''
                            for lat in range(len(cf)-1):
                                if self.isEnglish(cf[lat])==True:
                                    r=r+cf[lat]
                                else:
                                    r=r+'0'
                            cf=r
                        cf=str(cf).split('\n')
                    if len(cf)>3:
                        l=1
                        while len(cf[l])>1:
                            try:
                                nn=self.remspc(cf[l])
                                cs=str(cf[l])
                                cs=cs[nn:]
                                css=cs
                                cs=str(cs).replace('"',' ')
                                cs=str(cs).replace('%','')                           
                                if self.isEnglish(cs)==False:
                                    r=''
                                    for lat in range(len(cs)-1):
                                        if self.isEnglish(cs[lat])==True:
                                            r=r+cs[lat]
                                        else:
                                            r=r+'0'
                                    cs=r                               
                                gp=driver.find_elements_by_partial_link_text(css)
                                lnk=' '
                                for ink in gp:
                                    lnk=ink.get_attribute('href')
                                file1.write(u+ "\n")
                                file2.write(lnk+ "\n")
                                print("f"+u+'\n'+"cf "+lnk)
                            except:
                                traceback.print_exc()
                                error_file.write('Error '+u+' '+css+'\n')
                                print("FILE Error")
                                pass
                            l+=1
                
                j=1
                while self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td/span['+str(j)+']/strong')==True:
                    j+=1
                
                k=1
                if j > 1:
                    contents=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td').text
                    while j > 1:
                        content=contents                    
                        delim=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td/span['+str(k)+']/strong').text
                        content=content[content.find(delim):content.find('Characters:')]
                        content=str(content).split('\n')
                        for c in content:
                            print(c)

                        j-=1
                        k+=1
                        if j>1:
                            delim2=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td/span['+str(k)+']/strong').text                               
                            contents=contents[contents.find(delim2):]

                        delim=str(delim).split('"')
                        if len(delim)==3:
                            delim=delim[1]
                            delim=str(delim)
                        else:
                            delim=delim[0]
                            delim=str(delim)
                        i=4
                        while i < len(content):
                            if content[i]!='\n' and content[i]!='' and content[i]!=' ':
                                if content[i] in alist:
                                    job=str(content[i][0:len(content[i])-1])
                                else: 
                                    try:
                                        artist=str(content[i])
                                        print("con "+str(content[i]))
                                        sid = con.execute('SELECT Story_ID FROM db_comics.tbl_Story WHERE Name_Story="'+delim+'";').fetchone()[0]
                                        sid=str(sid)
                                        print("sid "+str(sid))
                                        aid = con.execute('SELECT Creator_ID FROM db_comics.tbl_Artist WHERE Name_of_Artist="'+artist+'";').fetchone()[0]
                                        aid=str(aid)
                                        print("aid "+str(aid))
                                        jid = con.execute('SELECT ID_Job FROM db_comics.tbl_Job WHERE Name_of_Job="'+job+'";').fetchone()[0]
                                        jid=str(jid)
                                        cj=str(jid)+' '+str(aid)
                                        cj=str(cj)
                                        print("cj "+str(cj))
                                        con.execute('INSERT INTO db_comics.tbl_Story_Artist_Job(Story_ID,Code_ArtistJob) VALUES('+sid+',"'+cj+'")')
                                    except:
                                        traceback.print_exc()
                                        error_file.write('SQL Error '+u+' '+delim+'\n')
                                        print("SQL Error")
                                        pass
                            i+=1

            except Exception:
                traceback.print_exc()
                error_file.write('Code Error '+u+'\n')
                print("Code Error")
                pass
            
            driver.execute_script('window.close()')
            driver.switch_to_window(driver.window_handles[1])