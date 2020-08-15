# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import string, re
from time import sleep
import time
import sqlalchemy as sql
import traceback
from SqlDB import MysqlDb


Character_file = 'lost_char'

class lc_data:
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

    def scrap_character_data(self,driver, con,lnk):
        logs = open(Character_file, 'a+')
        newTab = newTab = 'window.open("' + lnk + '", "_blank");'
        driver.execute_script(newTab)
        driver.switch_to_window(driver.window_handles[3])
        time.sleep(3)

        try:
            link = lnk
            try:
                contents = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td').text.split("\n")
            except:
                contents = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]').text.split("\n")

            real_name = contents[1].replace("Real Name:", "")
            bio, weakness, notes = '', '', ''

            try:
                power = contents[contents.index("Powers:")+1]
            except ValueError:
                power = ''
            try:
                bio = contents[contents.index("Bio:")+1]
            except ValueError:
                bio = ''
            try:
                weakness = contents[contents.index("Weaknesses:")+1]
            except ValueError:
                weakness = ''
            try:
                notes = contents[contents.index("Notes:")+1]
            except ValueError:
                notes = ''
            
            try:
                first_appearence = [content for content in contents if "First Appearance:" in content][0].replace("First Appearance:", "")
            except:
                first_appearence=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/a[2]').text
            
            ch_name=driver.find_element_by_class_name('page_headline').text
            ch_pic=''
            if self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[3]/img')==True:
                ch_pic=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[3]/img').get_attribute('src')
            
            bio=str(bio).replace('"',' ')
            bio=str(bio).replace('%','')

            notes=str(notes).replace('"',' ')
            notes=str(notes).replace('%','')

            weakness=str(weakness).replace('"',' ')
            weakness=str(weakness).replace('%','')

            power=str(power).replace('"',' ')
            power=str(power).replace('%','')

            
            real_name=str(real_name).replace('"',' ')
            real_name=str(real_name).replace('%','')
            
            ch_name=str(ch_name).replace('"',' ')
            ch_name=str(ch_name).replace('%','')

            link=driver.current_url
            self.dump_characters_data(driver,con, link, ch_name, real_name,power,weakness, bio, notes, first_appearence,str(ch_pic))
            
        except StaleElementReferenceException as e:
            pass
        except:
            traceback.print_exc()
            logs.write('Not Working ' +link+'\n')
            print("NoSql")
            pass
            
        driver.execute_script('window.close()')
        driver.switch_to_window(driver.window_handles[2])
        logs.close()
            

    def dump_characters_data(self,driver, con, Link, ch_name, Real_name,power,weakness, Bio, Notes, First_appearence,pic):
        logs = open(Character_file, 'a+')
        try:
            sql = 'INSERT INTO tbl_Characters(Comicbookdb_Link,Name_Character, Real_Name,Powers,Weaknesses, Bio, Notes, First_Appearance) VALUES("'+ Link + '","'+ch_name+'","' + Real_name + '","'+power+'","'+weakness+'","' + Bio + '","' + Notes + '","' + First_appearence + '");' 
            print(sql)
            con.execute(sql)
            
            cid = con.execute('SELECT ID_Character FROM tbl_Characters ORDER BY ID_Character DESC LIMIT 1;').fetchone()[0]                
            sql = 'INSERT INTO tbl_Character_Pictures(ID_Character,Picture) VALUES('+str(cid)+',"'+ pic + '");' 
            print(sql)
            con.execute(sql)

        except Exception:
            traceback.print_exc()
            logs.write('mysql error '+Link+'\n')
            print("Sql")
            pass
        
        logs.close()

