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


Title_file = 'title'


class RunTitleData:

    def dump_title_data(self, con,pid,name, comicPageLink, year, fr, lr, notes,impID):
        logs = open(Title_file, 'a+')
        try:
            sql = 'INSERT INTO tbl_RunTitle(Name_Run,Comicbookdb_Link, Year, First_Release, Last_Release,ID_Publisher,ID_Imprint,ID_Country,ID_Language,Notes) VALUES("'+ name + '","'+ comicPageLink + '","' + str(year) + '","' + str(fr) + '","' + str(lr) + '",'+str(pid)+','+str(impID)+',1,1,"'+str(notes)+'")' 
            print(sql)
            con.execute(sql)
        except Exception:
            logs.write('mysql error '+ str(comicPageLink)+'\n')
            traceback.print_exc()
        logs.close
    
    def remQ(self,vname):
        vname=str(vname).replace('"','')
        vname=str(vname).replace('/','')
        vname=str(vname).replace('\\','')
        vname=str(vname).replace('\'','')
        vname=str(vname).replace('%','')
        return vname

    def scrap_run_title_data(self,pid,con,driver2):
        logs = open(Title_file, 'a+')
        # newTab = 'window.open("' + url + '", "_blank");'
        # driver2.execute_script(newTab)
        # driver2.switch_to_window(driver2.window_handles[1])
        try:
            comicbook_link=driver2.current_url
            run_name = driver2.find_element_by_class_name('page_headline').text
            run_name=self.remQ(run_name)
            year = driver2.find_elements_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td/strong[1]")[1].text.replace('(','').replace(')', '')                   
            #year=unicode(str(year),"utf-8")
            x = driver2.find_elements_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr/td")
            contents = x[7].text.split("\n")
            
            dates = [content for content in contents if "Publication Date: " in content][0]
            dates = dates.replace("Publication Date: ", '')
            dates=str(dates).split('-')
            if len(dates)==2:
                fr=dates[0]
                lr=dates[1]
            else:
                fr=dates
                lr='NULL'
            #fr=unicode(str(fr),"utf-8")
            #lr=unicode(str(lr),"utf-8")

            language = [content for content in contents if "Language:" in content][0]
            language = language.replace("Language:", '')
            
            country = [content for content in contents if "Country:" in content][0]
            country = country.replace("Country:", '')
            
            notes = ''
            if contents[contents.index('Notes:') + 1] != '':
                notes = contents[contents.index('Notes:') + 1]
            notes=str(notes).replace('"',' ')
            notes=str(notes).replace('%','')
            # if self.isEnglish(notes)==False:
            #     r=''
            #     for lat in range(len(notes)-1):
            #         if self.isEnglish(notes[lat])==True:
            #             r=r+notes[lat]
            #         else:
            #             r=r+'0'
            #     notes=r
            run_name=str(run_name).replace('"',' ')
            # if self.isEnglish(run_name)==False:
            #     r=''
            #     for lat in range(len(run_name)-1):
            #         if self.isEnglish(run_name[lat])==True:
            #             r=r+run_name[lat]
            #         else:
            #             r=r+'0'
            #     run_name=r    
            impID=0
            txt=str(driver2.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/a[2]').text)
            pc=con.execute('SELECT Name_Publisher FROM tbl_Publisher WHERE ID_Publisher='+str(pid)+';').fetchone()[0]
            if txt!=pc:
                try:
                    impID=con.execute('SELECT ID_Imprint FROM tbl_Imprint WHERE Name_Imprint="'+txt+'";').fetchone()[0]
                except:
                    impID=0            
            #impID=unicode(str(impID), "utf-8")
            self.dump_title_data(con,pid,run_name, comicbook_link, year, fr, lr, notes,impID)

        except TimeoutException:
            print(comicbook_link, " taking too much time to load")
            logs.write(str(comicbook_link)+" taking too much time to load")
            pass
        except NoSuchElementException:
            print("no element found in", comicbook_link, " page")
            logs.write("no element found in "+ comicbook_link+ " page")
            pass
        except StaleElementReferenceException as e:
            logs.write("staleStateElementException raised")
            pass
        except:
            logs.write(comicbook_link+ " page")
            pass
