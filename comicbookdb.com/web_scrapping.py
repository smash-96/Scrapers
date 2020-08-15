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

Publisher_file = 'pub'
Imprint_file = 'imp'
Title_file = 'titlt'
Character_file = 'charS'
Group_file = 'grp'

class PublisherData:
    def dump_publisher_data(self, con, comicPageLink, website, publisherName, notes):
        logs = open(Publisher_file, 'a+')
        try:
            pid=con.execute('SELECT ID_Publisher FROM tbl_Publisher WHERE Name_Publisher="'+str(publisherName)+'";').fetchone()[0]
        except:
            try:
                sql = 'INSERT INTO tbl_Publisher(Comicbookdb_Link, Website, Notes, Name_Publisher) VALUES("'+ comicPageLink + '","' + website + '","' + notes + '","' + publisherName + '")' 
                print(sql)
                con.execute(sql)
            except Exception:
                logs.write('mysql error\n')
                traceback.print_exc()
        logs.close
        
    def scrap_publisher_data(self, url, con, driver):
        logs = open(Publisher_file, 'a+')
        try:
            comicPageLink = url
            driver.get(comicPageLink)
            publisherName = driver.find_element_by_class_name("page_subheadline").text        
            website = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/a[2]").text
            parent = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td").text
            
            try:
                notes = ""
                start = parent.find("Notes:") + len("Notes:") + 1
                end = None

                # below check is for ID=4 url
                if url[-1] == "4":
                    end = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/b").text
                else:
                    end = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/strong[3]").text
                end = parent.find(end)
                
                while(start < end):
                    notes += parent[start]
                    start += 1
            except:
                notes=""
            self.dump_publisher_data(con, comicPageLink, website, publisherName, notes)

        except TimeoutException:
            print("{url} taking too much time to load")
            logs.write(' taking too much time to load\n')
        except NoSuchElementException:
            traceback.print_exc()
            logs.write('no element found in '+str(comicPageLink))
            print("no element found in", comicPageLink, " page\n")
        logs.close()

class ImprintData:

    def check(self,driver,x):
        try:
            driver.find_element_by_xpath(x)
        except:
            return False
        return True
    def dump_imprint_data(self, con,pid, comicPageLink, website, imprintName, notes):
        logs = open(Imprint_file, 'a+')
        try:
            impID=con.execute('SELECT ID_Imprint FROM tbl_Imprint WHERE Name_Imprint="'+str(imprintName)+'";').fetchone()[0]
        except:
            try:
                sql = 'INSERT INTO tbl_Imprint(ID_Publisher,Comicbookdb_Link, Website, Notes, Name_Imprint) VALUES('+str(pid)+',"'+ comicPageLink + '","' + website + '","' + notes + '","' + imprintName + '")' 
                print(sql)
                con.execute(sql)
            except Exception:
                logs.write('mysql error'+ str(comicPageLink)+'\n')
                traceback.print_exc()
        logs.close

    def scrap_imprint_data(self, pid,url, con, driver):
        logs = open(Imprint_file, 'a+')
        links = []
        names=[]
        if self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[1]')==True and self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[2]')==True and self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[3]')==True:
            for c in range(3):
                td = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[' + str(c + 1) + ']')
                name=str(td.text)
                name=name.split('\n')
                for n in name:
                    print(n)
                    names.append(str(n))
                hrefs = td.find_elements_by_xpath(".//a")
                for h in hrefs:
                    print(h.get_attribute('href'))
                    links.append(str(h.get_attribute('href')))
        elif self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[1]')==True and self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[2]')==True:
            for c in range(2):
                td = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td[' + str(c + 1) + ']')
                name=str(td.text)
                name=name.split('\n')
                for n in name:
                    print(n)
                    names.append(str(n))
                hrefs = td.find_elements_by_xpath(".//a")
                for h in hrefs:
                    print(h.get_attribute('href'))
                    links.append(str(h.get_attribute('href')))
        elif self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr/td[1]')==True and self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr/td[2]')==True:
            for c in range(2):
                td = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr/td[' + str(c + 1) + ']')
                name=str(td.text)
                name=name.split('\n')
                for n in name:
                    print(n)
                    names.append(str(n))
                hrefs = td.find_elements_by_xpath(".//a")
                for h in hrefs:
                    print(h.get_attribute('href'))
                    links.append(str(h.get_attribute('href')))
        else:
            td = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[1]/tbody/tr/td')
            name=str(td.text)
            name=name.split('\n')
            for n in name:
                print(n)
                names.append(str(n))
            hrefs = td.find_elements_by_xpath(".//a")
            for h in hrefs:
                print(h.get_attribute('href'))
                links.append(str(h.get_attribute('href')))

        print(len(links))
        for i in range(len(links)):
            self.help(pid,links[i], names[i], con, driver)
            driver.execute_script("window.history.go(-1)")

        del links[:]
        del names[:]
        time.sleep(4)
        logs.close()

    def help(self,pid,url,name,con,driver):
        logs = open(Imprint_file, 'a+')
        try:
            comicPageLink = url
            driver.get(comicPageLink)
            imprintName = name
            website = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/a[2]").text
            parent = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td").text

            notes = ""
            start = parent.find("Notes:") + len("Notes:") + 1
            end = None

            try:
                end = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/strong[3]").text
            except:
                end = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/p/strong[1]").text
            end = parent.find(end)

            while (start < end):
                notes += parent[start]
                start += 1
            notes=str(notes).replace('"',' ')
            self.dump_imprint_data(con, pid,comicPageLink, website, imprintName, notes)

        except TimeoutException:
            print(comicPageLink, " taking too much time to load")
            logs.write(str(comicPageLink)+' taking to much time to load')
            pass
        except NoSuchElementException:
            print("no element found in {comicPageLink} page")
            logs.write('no element found in'+ str(comicPageLink)+'\n')
            pass