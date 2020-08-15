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
from lost_ch import lc_data

import sqlalchemy as sql
import traceback
from SqlDB import MysqlDb 

class FloppyDataG:
    error_log_file = 'floppyG' # file name in which all error logs are dumped
    
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
        
    def helper(self, url, driver, con,tid):
        error_file = open(self.error_log_file, 'a+')
        coll=str(url)
        u = driver.current_url
        try:
            try:
                try:
                    issue_num = driver.find_element_by_class_name('page_headline').text.replace("#", "").split(" ")[-1]
                except:
                    try:
                        issue_num=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span/text()').text
                        issue_num=str(issue_num).replace("#","")
                        issue_num=str(issue_num).replace("-","")
                    except:
                        issue_num=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span[1]/text()').text
                        issue_num=str(issue_num).replace("#","")
                        issue_num=str(issue_num).replace("-","")
            except:
                issue_num=''
            if re.match(r'[a-zA-Z]', issue_num):
                issue_num = 0
            issue_num=self.remQ(issue_num)
            try:
                title = str(driver.find_element_by_class_name('page_subheadline').text)
                if title=='Rating':
                    title='None'
                else:
                    title=str(title).replace('"',' ')
            except:
                title=''
            title=self.remQ(title)
            try:
                if 'Cover Date:' in driver.page_source and 'Cover Price:' in driver.page_source:
                    cover_date=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
                    cover_date=cover_date[cover_date.find('Cover Date:'):cover_date.find('Cover Price:')].replace('Cover Date:', '')
                else:
                    if driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td/a[4]').text != 'Add/remove story arcs to this issue':
                        cover_date = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td/a[4]').text
                    else:
                        cover_date = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td/a[3]').text
                cover_date=str(cover_date).replace(' ','')
                cover_date=str(cover_date).replace('\n','')
            except:
                cover_date=''
            cover_date=self.remQ(cover_date)
            try:
                content = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text.split(" ")
                try: 
                    cover_price = content[content.index('$')+1].replace('\n', '')
                    cover_price = re.sub("[a-zA-Z]+", "", cover_price)
                except Exception:
                    cover_price = '0'
                    pass
            except:
                cover_price=''
                
            cover_price=self.remQ(cover_price)
            contents = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text.split("\n")
            try:
                tagline = [content for content in contents if "Issue Tagline:" in content][0].replace("Issue Tagline:", "")
            except:
                tagline='None'
            tagline=self.remQ(tagline)
            x = [content for content in contents if "Format:" in content][0].replace("Format:", "").split(';')
            
            size,pages, color = '','', ''
            try:
                pages = x[2].replace('pages', '').replace(' ', '')
                if len(pages) == 0:
                    pages = pages + "0"
                size=x[1].replace(' ','')
                color = x[0].replace('Color', '')
            except IndexError:
                pages, color = '', '' 
                pass
            pages=self.remQ(pages)
            color=self.remQ(color)
            synopsis = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
            
            if 'Characters:' in driver.page_source:
                synopsis = synopsis[synopsis.find('Synopsis:'):synopsis.find('Characters')].replace('\n', '')
            if 'Plot (Spoilers):' in driver.page_source:
                synopsis = synopsis[synopsis.find('Synopsis:'):synopsis.find('Plot')].replace('\n', '')
            if 'Reprint' in driver.page_source:
                synopsis = synopsis[synopsis.find('Synopsis:'):synopsis.find('Reprint')].replace('\n', '')
            if 'Notes:' in driver.page_source:
                synopsis = synopsis[synopsis.find('Synopsis:'):synopsis.find('Notes')].replace('\n', '')
            
            synopsis=str(synopsis).replace('"',' ')
            synopsis=self.remQ(synopsis)
            if "None entered" in synopsis:
                synopsis="None entered"
            try:    
                picture_thumbnail = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/a[1]/img').get_attribute('src')
            except:
                picture_thumbnail = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/img').get_attribute('src')
            try:
                picture_link = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/a[1]").get_attribute("href")
            except:
                picture_link=' '
            try :
                sql = 'INSERT INTO tbl_Floppy(Title_ID,Issue_Number, Comicbookdb_Link, Title,Cover_Date,Cover_Price, Synopsis, Colour,Size, Issue_Tagline, Page_Count, Picture, Picture_Thumbnail) '
                sql = sql + 'VALUES('+str(tid)+',"'+ str(issue_num)+ '","'+ u + '","' + title + '","'+cover_date+'","'+str(cover_price)+'","' +synopsis + '","'+ color+ '","'+str(size)+'","'+ tagline+ '","'+ str(pages)+'","'+ picture_link+	 '","'+ picture_thumbnail + '");'
                con.execute(sql)
                print(sql)

                fid = con.execute('SELECT Issue_ID FROM tbl_Floppy ORDER BY Issue_ID DESC LIMIT 1;').fetchone()[0]
                ufid=str(fid)
                j=1
                while self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td/span['+str(j)+']/strong')==True:
                    try:
                        name=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td/span['+str(j)+']/strong').text
                        name=str(name).split('"')
                        if len(name)==3:
                            name=name[1]
                        else:
                            name=name[0]
                        name=self.remQ(name)
                        sql='INSERT INTO tbl_Story (Issue_ID,Name_Story) VALUES ('+ufid+',"'+name+'");'
                        print(sql)
                        con.execute(sql)
                    except:
                        traceback.print_exc()
                        error_file.write('mysql Story error '+u+' '+str(tid)+' '+str(j)+'\n')
                        print("Sql")
                        pass
                    j+=1
                if 'Characters:' in driver.page_source:
                    fc=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
                    fc=fc[fc.find('Add/remove characters to this issue'):fc.find('Groups:')]
                    fc=str(fc).split('\n')
                    if len(fc)>3:
                        m=1
                        while len(fc[m])>1:
                            try:
                                print(str(fc[m]))
                                n=self.remspc(fc[m])
                                cs=str(fc[m])
                                cs=cs[n:]
                                css=cs
                                cs=str(cs).replace('"',' ')
                                cs=str(cs).replace('%','')                           
                                try:
                                    fcid = con.execute('SELECT ID_Character FROM tbl_Characters WHERE Name_Character="'+cs+'";').fetchone()[0]
                                except:
                                    lc=driver.find_elements_by_partial_link_text(css)
                                    lnk=''
                                    for ink in lc:
                                        lnk=ink.get_attribute('href')
                                    lostch=lc_data()
                                    if lnk!='':
                                        lostch.scrap_character_data(driver,con,lnk)
                                    fcid = con.execute('SELECT ID_Character FROM tbl_Characters WHERE Name_Character="'+cs+'";').fetchone()[0]
                                sql='INSERT INTO tbl_Floppy_Characters (Issue_ID,ID_Character) VALUES ('+str(ufid)+','+str(fcid)+');'
                                print(sql)
                                con.execute(sql)
                            except:
                                traceback.print_exc()
                                error_file.write('Character mysql error '+u+' '+str(tid)+' '+lnk+' '+css+'\n')
                                print("Sql")
                                pass
                            m+=1
                sname=''
                sa=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
                sa=sa[sa.find('Add/remove story arcs to this issue'):sa.find('Synopsis:')]
                sa=str(sa).split('\n')
                if len(sa)>3:
                    k=1
                    while len(sa[k])>1:
                        chsn=str(sa[k])
                        chsn=str(chsn).replace('"',' ')
                        sname=str(chsn)
                        sname=self.remQ(sname)
                        sql='INSERT INTO tbl_Story_Arc (Story_Arc_Name) VALUES ("'+sname+'");'
                        print(sql)
                        con.execute(sql)
                        usid = con.execute('SELECT ID_StoryArc FROM tbl_Story_Arc ORDER BY ID_StoryArc DESC LIMIT 1;').fetchone()[0]
                        sql='INSERT INTO tbl_Floppy_StoryArc (ID_StoryArc,Floppy_Issue_ID) VALUES ('+str(usid)+','+str(ufid)+');'
                        print(sql)
                        con.execute(sql)
                        k+=1
                if "TPB" in coll or "HC" in coll:
                    cname=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span[1]/a').text
                    cname=str(cname).replace('"',' ')   
                    cname=self.remQ(cname)
                    sql = 'INSERT INTO tbl_Collected(Name_of_Book,Comicbookdb_Link,Title_ID,Story_Arc, Title, Release_Date,Cover_Price,Colour,Size, Page_Count, Summary, Picture, Picture_Thumbnail)'
                    sql = sql + ' VALUES("'+cname+'","'+u+'",'+str(tid)+',"'+sname+'", "'+title+'", "'+cover_date+'", "'+str(cover_price)+'", "'+color+'","'+str(size)+'", "'+str(pages)+'", "'+synopsis+'", "'+picture_link+'", "'+picture_thumbnail+'");'
                    con.execute(sql)
                    print(sql)
            except Exception:
                traceback.print_exc()
                error_file.write('mysql error '+u+' '+str(tid)+'\n')
                print("Sql")
                pass

            
            
        except TimeoutException:
            traceback.print_exc()
            error_file.write('Time Out ' +u+' '+str(tid)+'\n')
            print("NoSql")
            pass
        except NoSuchElementException:
            traceback.print_exc()
            error_file.write('No Element ' +u+' '+str(tid)+'\n')
            print("NoSql")
            pass
        except StaleElementReferenceException as e:
            traceback.print_exc()
            error_file.write('Stale Element ' +u+' '+str(tid)+'\n')
            print("NoSql")
            pass
        except:
            traceback.print_exc()
            error_file.write('Not Working ' +u+' '+str(tid)+'\n')
            print("NoSql")
            pass