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
from grp2 import group_data
from title import RunTitleData
from fg import FloppyDataG
from web_scrapping import *

class FloppyData:
    error_log_file = 'floppy3' # file name in which all error logs are dumped
    
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

    def dump_variant_data(self, con, comicPageLink,Name, pic_t,pic,fid):
        error_file = open(self.error_log_file, 'a+')
        try:
            sql = 'INSERT INTO tbl_Variant(Issue_ID,Name_variant, Comicbookdb_Link, Picture_Thumbnail, Picture) VALUES('+str(fid)+',"' + Name + '","'+ comicPageLink + '","' + pic_t + '","' + pic + '")' 
            print(sql)
            con.execute(sql)
        except Exception:
            traceback.print_exc()
            error_file.write('Variant error in mysql query '+str(comicPageLink)+' '+str(fid)+'\n')
            pass
        error_file.close()

    def dump_artist_data(self, artist, url, con,job,fiid,u,coll):
        error_file = open(self.error_log_file, 'a+')
        try:
            try:
                id = con.execute('SELECT Creator_ID FROM tbl_Artist WHERE Name_of_Artist="'+artist[0]+'";').fetchone()[0]

            except:
                con.execute('INSERT INTO tbl_Artist(Name_of_Artist, Comicbookdb_Link, Picture, Bio) VALUES("'+artist[0]+'", "'+url+'", "'+artist[3]+'","'+artist[1]+'");')    
                id = con.execute('SELECT Creator_ID FROM tbl_Artist ORDER BY Creator_ID DESC LIMIT 1;').fetchone()[0]

                if artist[4].find('facebook'):
                    con.execute('INSERT INTO tbl_Artist_Websites(Creator_ID, SN_ID, Link_Website) VALUES('+str(id)+', 1, "'+artist[4]+'");')
                if artist[5].find('twitter'):
                    con.execute('INSERT INTO tbl_Artist_Websites(Creator_ID, SN_ID, Link_Website) VALUES('+str(id)+', 2, "'+artist[5]+'");')
                if artist[6].find('.com'):
                    con.execute('INSERT INTO tbl_Artist_Websites(Creator_ID, SN_ID, Link_Website) VALUES('+str(id)+', 3, "'+artist[6]+'");')

                        
            job=str(job).replace(':','')
            jid = con.execute('SELECT ID_Job FROM tbl_Job WHERE Name_of_Job="'+job+'";').fetchone()[0]

            cj=str(jid)+' '+str(id)

            con.execute('INSERT INTO tbl_Artist_Job(Creator_ID, ID_Job,Code_ArtistJob) VALUES('+str(id)+', '+str(jid)+',"'+cj+'")')

            con.execute('INSERT INTO tbl_Floppy_artist(Issue_ID,Code_ArtistJob) VALUES('+str(fiid)+',"'+cj+'")')
            
            if "TPB" in coll or "HC" in coll:
                print(coll)
                cid=con.execute('SELECT Issue_ID FROM tbl_Collected WHERE Comicbookdb_Link="'+u+'";').fetchone()[0]

                con.execute('INSERT INTO tbl_Collected_artist(Issue_ID,Code_ArtistJob) VALUES('+str(cid)+',"'+cj+'")')
        except Exception:
            traceback.print_exc()
            print("Artist error in mysql query")
            error_file.write('Artist error in mysql query '+str(url)+'\n')
            pass
        error_file.close()

    def remQ(self,vname):
        vname=str(vname).replace('"','')
        vname=str(vname).replace('/','')
        vname=str(vname).replace('\\','')
        vname=str(vname).replace('\'','')
        vname=str(vname).replace('%','')
        return vname    
    
    def login(self,driver):
        driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[3]/input').send_keys('smash1996')
        driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[3]/input').send_keys('ZAIN1996')
        driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[3]/input').click()
    
    def scrap_floppy_data(self, url, con, driver):
        error_file = open(self.error_log_file, 'a+')
        pubf=open('pub', 'a+')
        impf=open('imp','a+')
        driver.get(url)
        self.login(driver)
        driver.get(url)
        tablesP=[
            '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td[1]/a',
            '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td[3]/a']
        for tp in tablesP[0:1]:
            linksp=driver.find_elements_by_xpath(tp)
            myway=[]
            mytext=[]
            for xp in linksp:
                myway.append(xp.get_attribute('href'))

            for xp in myway[115:]:
                print(xp)
                time.sleep(2)
                if xp != None:
                    try:
                        pub=PublisherData()
                        pub.scrap_publisher_data(xp, con, driver)
                        pn=driver.find_element_by_class_name("page_subheadline").text
                        pid=con.execute('SELECT ID_Publisher FROM tbl_Publisher WHERE Name_Publisher="'+str(pn)+'";').fetchone()[0]                        
                        try:
                            if 'Imprints:' in driver.page_source:
                                imp=ImprintData()
                                imp.scrap_imprint_data(pid,xp, con, driver)

                            if 'Imprints:' not in driver.page_source:
                                if self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td[1]/a')==True and self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td[3]/a')==True:
                                    tables = [
                                        '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td[1]/a',
                                        '/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td[3]/a'
                                        ]
                                else:
                                    tables = ['/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr/td/a']
                            else:
                                if self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[1]/a')==True and self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[3]/a')==True: 
                                    tables = [
                                        '/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[1]/a', 
                                        '/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td[3]/a'
                                        ]
                                else:
                                    tables = ['/html/body/table/tbody/tr[2]/td[3]/table[1]/tbody/tr/td/table[2]/tbody/tr/td/a']

                            i=0
                            for table in tables:
                                links = driver.find_elements_by_xpath(table)
                                for x in links:
                                    try:
                                        if x.get_attribute('href') != None:
                                            if i==20:
                                                i=0
                                                print("Waiting....")
                                                time.sleep(300)
                                            i=i+1
                                            newTab = 'window.open("' + x.get_attribute('href') + '", "_blank");'
                                            driver.execute_script(newTab)
                                            driver.switch_to_window(driver.window_handles[1])
                                            tName=driver.find_element_by_class_name('page_headline').text
                                            tName=self.remQ(tName)
                                            try:
                                                tid = con.execute('SELECT Title_ID FROM tbl_RunTitle WHERE Name_Run="'+tName+'";').fetchone()[0]
                                            except:
                                                title=RunTitleData()
                                                title.scrap_run_title_data(pid,con,driver)
                                                tid = con.execute('SELECT Title_ID FROM tbl_RunTitle WHERE Name_Run="'+tName+'";').fetchone()[0]
                                            urls = driver.find_elements_by_class_name('page_link')
                                            
                                            result = self.helper(urls, driver, con,tid)
                        
                                    except TimeoutException:
                                        traceback.print_exc()
                                        error_file.write('Title Time Out '+'\n')
                                        print("NoSql")
                                        pass
                                    except NoSuchElementException:
                                        traceback.print_exc()
                                        error_file.write('Title No Element '+'\n')
                                        print("NoSql")
                                        pass
                                    except StaleElementReferenceException as e:
                                        traceback.print_exc()
                                        error_file.write('Title Stale Element '+'\n')
                                        print("NoSql")
                                        pass
                                    except:
                                        traceback.print_exc()
                                        error_file.write('No Title '+'\n')
                                        print("NoSql")
                                        pass
                                    driver.execute_script('window.close()')
                                    driver.switch_to_window(driver.window_handles[0])
                        except:
                            traceback.print_exc()
                            pubf.write('Imprint Insert Error'+str(xp)+'\n')
                            print("Imprint Insert Error")
                            pass                
                    except:
                        traceback.print_exc()
                        pubf.write('Publisher Insert Error'+str(xp)+'\n')
                        print("Publisher Insert Errors")
                        pass   
        error_file.close()
             
    def helper(self, urls, driver, con,tid):
        artist = None
        wait=0
        floppy = []
        error_file = open(self.error_log_file, 'a+')
        for url in urls[1:]:
            if wait==200:
                wait=0
                print("Waiting....")
                time.sleep(300)
            wait=wait+1
            newTab = 'window.open("' + url.get_attribute('href') + '", "_blank");'
            coll=str(url.text)
            u = url.get_attribute('href')
            try:
                driver.execute_script(newTab)
                driver.switch_to_window(driver.window_handles[2])
                time.sleep(4)
                try :
                    try:
                        fid = con.execute('SELECT Issue_ID FROM tbl_Floppy WHERE Comicbookdb_Link="'+u+'";').fetchone()[0]
                    except:
                        lf=FloppyDataG()
                        lf.helper(coll, driver, con,tid)
                        fid = con.execute('SELECT Issue_ID FROM tbl_Floppy WHERE Comicbookdb_Link="'+u+'";').fetchone()[0]

                    ufid=str(fid)
                
                    print("Groups:")
                    if 'Groups:' in driver.page_source:
                        fg=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
                        fg=fg[fg.find('Add/remove groups to this issue'):fg.find('Reviews:')]
                        fg=str(fg).split('\n')
                        if len(fg)>3:
                            n=1
                            while len(fg[n])>1:
                                try:
                                    print(str(fg[n]))
                                    nn=self.remspc(fg[n])
                                    cs=str(fg[n])
                                    cs=cs[nn:]
                                    css=cs
                                    cs=str(cs).replace('"',' ')
                                    cs=str(cs).replace('%','')                                                
                                    gp=driver.find_elements_by_partial_link_text(css)
                                    lnk=''
                                    for ink in gp:
                                        lnk=ink.get_attribute('href')
                                    gpd=group_data()
                                    if lnk!='':
                                        gpd.scrap_group_data(driver,con,lnk)
                                    fgid = con.execute('SELECT ID_Group FROM tbl_Group WHERE Name_Group="'+cs+'";').fetchone()[0]

                                    sql='INSERT INTO tbl_Floppy_Group (Issue_ID,ID_Group) VALUES ('+str(ufid)+','+str(fgid)+');'
                                    print(sql)
                                    con.execute(sql)
                                except:
                                    traceback.print_exc()
                                    error_file.write('Floppy_Group mysql error '+u+' '+str(tid)+' '+lnk+' '+css+'\n')
                                    print("Sql")
                                    pass
                                n+=1

                    t="There are other versions of this issue in the database:"
                    if t in driver.page_source:
                        vd=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[2]/td').text
                        vd=vd[vd.find('There are other versions of this issue in the database:'):vd.find('Story Arc(s):')]
                        vd=str(vd).split('\n')
                        if len(vd)>3:
                            n=1
                            while len(vd[n])>1:
                                try:
                                    print(str(vd[n]))
                                    nn=self.remspc(vd[n])
                                    cs=str(vd[n])
                                    cs=cs[nn:]
                                    css=cs
                                    cs=str(cs).replace('"',' ')
                                    cs=str(cs).replace('%','')                                                         
                                    vr=driver.find_elements_by_partial_link_text(css)
                                    lnk=''
                                    for ink in vr:
                                        lnk=ink.get_attribute('href')
                                    if lnk!='':
                                        driver.get(lnk)
                                        time.sleep(5)
                                        name=str(driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span[2]').text)
                                        name=str(name).replace('"',' ')
                                        name=str(name).replace('%','')
                                        url=driver.current_url
                                        try:
                                            pic_link=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/a[1]').get_attribute('href')
                                        except:
                                            pic_link=' '
                                        try:
                                            pic=driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/a[1]/img').get_attribute('src')
                                        except:
                                            pic=' '
                                        driver.execute_script("window.history.go(-1)")
                                        self.dump_variant_data(con,url,name,pic,pic_link,ufid)
                                except:
                                    traceback.print_exc()
                                    error_file.write('Variant error '+url+' '+str(tid)+' '+str(ufid)+'\n')
                                    pass
                                n+=1

                except Exception:
                    traceback.print_exc()
                    error_file.write('Floppy ID error'+u+' '+str(tid)+'\n')
                    pass
                # --------------artist info------------------- #
                time.sleep(6)                           
                content = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[3]').text
                if content != None:
                    fb = 'none'
                    name = 'none'
                    bio = 'none'
                    twitter = 'none'
                    website = 'none'
                    picture = 'none'
                    dob='none'
                    job='none'
                    alist=[]
                    val=1
                    while self.check(driver,'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[3]/strong['+str(val)+']')==True:
                        alist.append(driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[3]/strong['+str(val)+']').text)
                        val+=1
                    val-=1
                    slist=[]
                    ival=0
                    while ival<val-1:
                        slist.append(content[content.find(str(alist[ival])):content.find(str(alist[ival+1]))])
                        slist[ival]=str(slist[ival]).split('\n')
                        ival+=1                      
                    artist = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table[1]/tbody/tr[1]/td[3]/a')
                    ci=0
                    ii=1
                    for i in range(len(artist)):
                        print(artist[i].get_attribute('href'))
                        url = artist[i].get_attribute('href')

                        if len(slist)!=ci:
                            if str(slist[ci][ii])==str(artist[i].text):
                                job=str(slist[ci][0])
                                ii+=1
                                if len(slist[ci][ii])<=1:
                                    ii=1
                                    ci+=1
                        else:
                            job=str(alist[val-1])

                        try:
                            newTab = 'window.open("' + url + '", "_blank");'
                            driver.execute_script(newTab)
                            driver.switch_to_window(driver.window_handles[3])
                            time.sleep(3)
                            try:
                                content = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/div[1]').text
                            except:
                                content = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td/div[1]').text
                            
                            bio = content[0: content.find("Date of Birth:") - 1].replace('Bio:', '')
                            name = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/span').text
                                                                
                            dob = content[content.find("Date of Birth:"): content.find("Birthplace:")].replace('Date of Birth:', '') 
                            try:
                                picture = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[3]/img').get_attribute('src')
                                social_profile = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/div[1]/a')
                                for x in social_profile[:len(social_profile) - 2]:
                                    if x.get_attribute('href').find('facebook') != -1: 
                                        fb = x.get_attribute('href')
                                    elif x.get_attribute('href').find('twitter') != - 1: 
                                        twitter = x.get_attribute('href')
                                    else:
                                        website = x.get_attribute('href')
                            except NoSuchElementException:
                                picture = ''
                                social_profile = None
                                
                        except TimeoutException:
                            traceback.print_exc()
                            pass
                        except NoSuchElementException:
                            traceback.print_exc()
                            error_file.write('Artist No element found in '+url+ '\n')
                            pass
                        except StaleElementReferenceException as e:
                            traceback.print_exc()
                            pass
                        except:
                            traceback.print_exc()
                            error_file.write('Unknown Artist Error '+url+ '\n')
                            pass
                        
                        driver.execute_script('window.close()')
                        driver.switch_to_window(driver.window_handles[2])

                        name=self.remQ(name)
                        bio=self.remQ(bio)
                        artists = [name, bio, dob, picture, fb, twitter, website]
                        self.dump_artist_data(artists, url, con,job,ufid,u,coll)
               
            except TimeoutException:
                traceback.print_exc()
                error_file.write('Taking to much time to load '+u+ '\n')
                pass
            except NoSuchElementException:
                traceback.print_exc()
                error_file.write('No element found in '+u+ '\n')
                pass
            except StaleElementReferenceException as e:
                traceback.print_exc()
                error_file.write('StateElementReferenceException raised '+u+ '\n')
                pass
            except:
                traceback.print_exc()
                error_file.write('Unknown Error '+u+ '\n')
                pass
                       
            driver.execute_script('window.close()')
            driver.switch_to_window(driver.window_handles[1])    
        error_file.close()
        return artist, floppy