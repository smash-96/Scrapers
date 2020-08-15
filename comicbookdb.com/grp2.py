# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import string, re
from time import sleep
from lost_chg import lcg_data
import time
import sqlalchemy as sql
import traceback
from SqlDB import MysqlDb


Group_file = 'Group'

class group_data:  
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

    def remQ(self,vname):
        vname=str(vname).replace('"','')
        vname=str(vname).replace('/','')
        vname=str(vname).replace('\\','')
        vname=str(vname).replace('\'','')
        vname=str(vname).replace('%','')
        return vname

    def scrap_group_data(self, driver, con,lnk):
        logs = open(Group_file, 'a+')
        newTab = newTab = 'window.open("' + lnk + '", "_blank");'
        driver.execute_script(newTab)
        driver.switch_to_window(driver.window_handles[3])
        time.sleep(3)

        try:
            link = lnk
            content = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]').text.split("\n")
            bio = ''.join(content[content.index('Bio:')+1: content.index('Members:')])
            bio=self.remQ(bio)
            members = content[content.index('Members:') + 1: content.index('Appearances:')]
            
            members = members[:members.index('')]
            g_name=driver.find_element_by_class_name('page_headline').text

            bio=str(bio).replace('"',' ')
            bio=str(bio).replace('%','')
            g_name=str(g_name).replace('"',' ')
            g_name=str(g_name).replace('%','')
            g_name=self.remQ(g_name)
            link=driver.current_url
            self.dump_group_data(con, bio, members, link,str(g_name),driver)
            
        except StaleElementReferenceException as e:
            pass
        except:
            logs.write('Not Working ' +link+'\n')
            print("NoSql")
            pass
        
        driver.execute_script('window.close()')
        driver.switch_to_window(driver.window_handles[2])
        logs.close()
            

    def dump_group_data(self, con, bio, members, link,name,driver):
        logs = open(Group_file, 'a+')
        try:  
            sql = 'INSERT INTO tbl_Group(Comicbookdb_Link, Bio,Name_Group) VALUES("'+ link + '","' + bio + '","' + name + '");' 
            print(sql)
            con.execute(sql)
            if len(members)>=1:
                gid = con.execute('SELECT ID_Group FROM tbl_Group ORDER BY ID_Group DESC LIMIT 1;').fetchone()[0]     
                i=0
                while i<len(members):
                    try:
                        member=''
                        try:
                            gcid = con.execute('SELECT ID_Character FROM tbl_Characters WHERE Name_Character="'+str(members[i])+'";').fetchone()[0]
                        except:
                            lc=driver.find_elements_by_partial_link_text(str(members[i]))
                            lnk=''
                            for ink in lc:
                                lnk=ink.get_attribute('href')
                            lostch=lcg_data()
                            if lnk!='':
                                lostch.scrap_character_data(driver,con,lnk)
                            gcid = con.execute('SELECT ID_Character FROM tbl_Characters WHERE Name_Character="'+str(members[i])+'";').fetchone()[0]

                        sql = 'INSERT INTO tbl_Group_Characters(ID_Group,ID_Character) VALUES('+str(gid)+','+ str(gcid) + ');' 
                        print(sql)
                        con.execute(sql)
                    except:
                        traceback.print_exc()
                        logs.write('Group_Characters error '+str(members[i])+' '+link+'\n')
                        print("Sql")
                        pass
                    i+=1

        except Exception:
            traceback.print_exc()
            logs.write('mysql error '+link+'\n')
            print("Sql")
        logs.close()

