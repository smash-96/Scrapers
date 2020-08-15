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
from SqlDB import MysqlDb

class BDscrapper:
    error_log_file = 'bd' # file name in which all error logs are dumped
    artist_error_file = 'artist'

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

    def dump_artist(self, driver, con, job, artist,fid):
        error_file=open(self.artist_error_file, 'a+')
        try:
            try:
                id = con.execute('SELECT Creator_ID FROM db_comicsf.tbl_Artist WHERE Name_of_Artist="'+artist+'";').fetchone()[0]
            except:
                if '<' not in artist:
                    atr=' '
                    try:
                        new=str(artist).split(' ')
                        if len(new) > 1:
                            new[1]=str(new[1])+', '
                            atr=str(str(new[1])+str(new[0]))

                        else:
                            atr=str(new[0])

                        l=driver.find_elements_by_partial_link_text(atr)
                        for ink in l:
                            atr=ink.get_attribute('href')
                    except:
                        atr='N/A'
                else:
                    atr='N/A'
                sql='INSERT INTO db_comicsf.tbl_Artist(Name_of_Artist,Comicbookdb_Link) VALUES("'+artist+'","'+str(atr)+'");'
                con.execute(sql)
                print(sql)
                id = con.execute('SELECT Creator_ID FROM db_comicsf.tbl_Artist WHERE Name_of_Artist="'+artist+'";').fetchone()[0]

            job=str(job).replace(':','')
            job=str(job).replace(' ','')
            if job=='Scénario':
                ejob='Writer(s)'
            elif job=='Dessin':
                ejob='Penciller(s)'
            elif job=='Encreur':
                ejob='Inker(s)'
            elif job=='Couleurs':
                ejob='Colorist(s)'
            elif job=='Lettrage':
                ejob='Letterer(s)'
            elif job=='Editeur':
                ejob='Editor(s)'
            elif job=='Artiste de Couverture':
                ejob='Cover Artist(s)'
            elif job=='Traducteur':
                ejob='Translator(s)'
            jid = con.execute('SELECT ID_Job FROM db_comicsf.tbl_Job WHERE Name_of_Job="'+ejob+'";').fetchone()[0]
            cj=str(jid)+' '+str(id)
            sql='INSERT INTO db_comicsf.tbl_Floppy_artist(Issue_ID,Code_ArtistJob) VALUES('+str(fid)+',"'+cj+'")'
            con.execute(sql)
            print(sql)
            sql='INSERT INTO db_comicsf.tbl_Artist_Job(Creator_ID, ID_Job,Code_ArtistJob) VALUES('+str(id)+', '+str(jid)+',"'+cj+'");'
            con.execute(sql)
            print(sql)
        except:
            traceback.print_exc()
            print("Artist Not in Database")
            error_file.write('Artist Error '+str(job)+' '+str(artist)+'\n')
            pass
        error_file.close()


    def conv(self,s):
        ss=str(s).split(',')
        if len(ss)>1:
            s=str(str(ss[1])+' '+str(ss[0]))
            num=self.remspc(s)
            s=s[num:]
            return s
        else:
            return s

    def scrap_BD_data(self,url,con,driver):
        error_file = open(self.error_log_file, 'a+')
        driver.get(url)
        driver.maximize_window()
        
        i=1
        while self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/div[4]/div/div/ul/li['+str(i)+']')==True:
            try:
                link=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/div[4]/div/div/ul/li['+str(i)+']')
                img=link.find_element_by_css_selector('img').get_attribute('src')
                if "France" in img:
                    nlink=link.find_element_by_css_selector('a').get_attribute('href')
                    print(str(nlink)+' '+str(img))
                    newTab = 'window.open("' + nlink + '", "_blank");'
                    driver.execute_script(newTab)
                    driver.switch_to_window(driver.window_handles[1])

                    try:
                        if self.check(driver,'//*[@id="adult-overlay"]/div[2]/form')==True:
                            try:
                                driver.find_element_by_xpath('//*[@id="adult-overlay"]/div[2]/form/div[3]/input').click()
                            except:
                                pass
                        #Runtitle Scraping
                        gen,par,tome,idf,org,synopsis=' ',' ',' ',' ',' ',' '
                        j=1 
                        while self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li['+str(j)+']')==True:
                            data=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li['+str(j)+']')
                            tdata  = data.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li['+str(j)+']/label').text
                            if "Genre" in tdata:
                                gen=data.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li[1]/span').text
                            elif "Parution" in tdata:
                                par=data.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li[2]/span').text
                            elif "Tome" in tdata:
                                tome=data.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li[3]').text
                                tome=str(tome).split(':')
                                tome=str(tome[1])
                            elif "Identifiant" in tdata:
                                idf=data.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li[4]').text
                                idf=str(idf).split(':')
                                idf=str(idf[1])
                            elif "Origine" in tdata:
                                org=data.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/ul/li[5]').text
                                org=str(org).split(':')
                                org=str(org[1])
                                break
                            j+=1
                        try:
                            synopsis=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/article/div[1]/p').text

                            synopsis=str(synopsis).replace('"',' ')
                            synopsis=str(synopsis).replace('%',' ')

                            gen=str(gen).replace('"',' ')
                            gen=str(gen).replace('%',' ')

                            par=str(par).replace('"',' ')
                            par=str(par).replace('%',' ')
                            
                            org=str(org).replace('"',' ')
                            org=str(org).replace('%',' ')
                            
                            tome=str(tome).replace('"',' ')
                            tome=str(tome).replace('%',' ')
                            
                            idf=str(idf).replace('"',' ')
                            idf=str(idf).replace('%',' ')
                        except:
                            synopsis='N/A'
                        


                        if self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/ul/li[1]')==False:
                            name=' '
                            try:
                                name=driver.find_element_by_xpath('/html/body/div[7]/div[2]/article/div[1]/div/h1/a').text
                            except:
                                try:
                                    name=driver.find_element_by_xpath('/html/body/div[8]/div[2]/article/div[1]/div/h1/a').text
                                except:
                                    name='N/A'
                            name=str(name).replace('"','')
                            name=str(name).replace('/','')
                            name=str(name).replace('\\','')
                            name=str(name).replace('\'','')
                            name=str(name).replace('%','')
                            
                            try:
                                sql='INSERT INTO db_comicsf.tbl_RunTitle (Name_Run,ID_Country,ID_Language,Bdtheque_Link,Synopsis,Origin,Genre,Bdtheque_ID,Ongoing_Title,Number_of_Books) VALUES ("'+name+'",2,2,"'+str(driver.current_url)+'","'+synopsis+'","'+org+'","'+gen+'","'+idf+'","'+par+'","'+tome+'");'
                                print(sql)
                                con.execute(sql)
                            except:
                                if self.isEnglish(synopsis)==False:
                                    r=''
                                    for lat in range(len(synopsis)-1):
                                        if self.isEnglish(synopsis[lat])==True:
                                            r=r+synopsis[lat]
                                        else:
                                            r=r+'e'
                                    synopsis=r
                                sql='INSERT INTO db_comicsf.tbl_RunTitle (Name_Run,ID_Country,ID_Language,Bdtheque_Link,Synopsis,Origin,Genre,Bdtheque_ID,Ongoing_Title,Number_of_Books) VALUES ("'+name+'",2,2,"'+str(driver.current_url)+'","'+synopsis+'","'+org+'","'+gen+'","'+idf+'","'+par+'","'+tome+'");'
                                print(sql)
                                con.execute(sql)
                        try:
                            #Artist and Collected Scraping
                            checks=0
                            k=1
                            while self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']')==True:
                                dataf=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']')
                                title=dataf.find_element_by_css_selector('h3').text
                                try:
                                    ll=driver.find_elements_by_partial_link_text(str(title))
                                    for ink in ll:
                                        f_link=ink.get_attribute('href')
                                except:
                                    f_link='N/A'
                                f_link=str(f_link).replace('%','%%')
                                issue=str(title).split('.')
                                issue=str(issue[0]).replace(' ','')
                                try:
                                    issue=str(int(issue))
                                except:
                                    issue='N/A'

                                title=str(title).split('.')
                                if len(title)>1:
                                    title=str(title[1])
                                else:
                                    title=str(title[0])
                                
                                title=str(title).replace('"','')
                                title=str(title).replace('/','')
                                title=str(title).replace('\\','')
                                title=str(title).replace('\'','')
                                title=str(title).replace('%','')

                                BD_ID, release_D, P_Name, I_Name, I_Link, size, isbn, isbn13, pages, dim, artist=' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '
                                job=[]
                                art=[]
                                art1,art2,art3,art4,art5,art6,art7=' ',' ',' ',' ',' ',' ',' '
                                l=1
                                while self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[2]/ul/li['+str(l)+']')==True:
                                    ac=dataf.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[2]/ul/li['+str(l)+']').text
                                    ac=str(ac).split('\n')
                                    
                                    if len(ac)==1:
                                        if 'Identifiant' not in str(ac[0]) and 'Scénario' not in str(ac[0]) and 'Dessin' not in str(ac[0]) and 'Couleurs' not in str(ac[0]) and 'Dépot légal' not in str(ac[0]) and 'Editeur' not in str(ac[0]) and 'Collection' not in str(ac[0]) and 'Format' not in str(ac[0]) and 'ISBN' not in str(ac[0]) and 'Planches' not in str(ac[0]):
                                            num=self.remspc(str(ac[0]))
                                            ea=str(ac[0])
                                            ea=str(ea[num:])
                                            ea=self.conv(ea)
                                            job.append(artist)
                                            art.append(ea)

                                    else:
                                        if "Identifiant" in str(ac[0]):
                                            BD_ID=str(ac[1])
                                        elif "Scénario" in str(ac[0]):
                                            artist=str(ac[0])
                                            art1=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art1)
                                        elif "Dessin" in str(ac[0]):
                                            artist=str(ac[0])
                                            art2=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art2)
                                        elif "Couleurs" in str(ac[0]):
                                            artist=str(ac[0])
                                            art3=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art3)
                                        elif "Lettrage" in str(ac[0]):
                                            artist=str(ac[0])
                                            art4=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art4)
                                        elif "Artiste de Couverture" in str(ac[0]):
                                            artist=str(ac[0])
                                            art5=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art5)
                                        elif "Traducteur" in str(ac[0]):
                                            artist=str(ac[0])
                                            art6=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art6)
                                        elif "Encreur" in str(ac[0]):
                                            artist=str(ac[0])
                                            art6=self.conv(str(ac[1]))
                                            job.append(artist)
                                            art.append(art6)
                                        elif "Dépot légal" in str(ac[0]):
                                            release_D=str(ac[1])
                                        elif "Editeur" in str(ac[0]):
                                            P_Name=str(ac[1])
                                            P_Name=str(P_Name).replace('%','%%')
                                        elif "Collection" in str(ac[0]):
                                            I_Name=str(ac[1])
                                            try:
                                                ll=driver.find_elements_by_partial_link_text(I_Name)
                                                for ink in ll:
                                                    I_Link=ink.get_attribute('href')
                                                I_Link=str(I_Link).replace('%','%%')
                                            except:
                                                I_Link='N/A'
                                            I_Name=str(I_Name).replace('%','%%')
                                        elif "Format" in str(ac[0]):
                                            size=str(ac[1])
                                        elif "ISBN" in str(ac[0]):
                                            isbn=str(ac[1]).replace('-','')
                                            ilen=len(str(isbn))
                                            if ilen > 10:
                                                isbn13=isbn
                                                isbn='N/A'
                                            else:
                                                visbn13='N/A'
                                        elif "Planches" in str(ac[0]):
                                            pages=str(ac[1])
                                            break
                                    
                                    l+=1
                                try:
                                    notes=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[2]/div[2]/p').text
                                    notes=str(notes).split('tion :')
                                    notes=str(notes[1])
                                    notes=str(notes).replace('"','')
                                    notes=str(notes).replace('/','')
                                    notes=str(notes).replace('\\','')
                                    notes=str(notes).replace('\'','')
                                    notes=str(notes).replace('%','')
                                except:
                                    try:
                                        notes=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[2]/div[2]/p[1]').text
                                        notes=str(notes).split('tion :')
                                        notes=str(notes[1])
                                        notes=str(notes).replace('"','')
                                        notes=str(notes).replace('/','')
                                        notes=str(notes).replace('\\','')
                                        notes=str(notes).replace('\'','')
                                        notes=str(notes).replace('%','')

                                    except:
                                        notes=' '
                                
                                try:
                                    pic_t=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[1]/div[1]/a/img').get_attribute('src')
                                except:
                                    pic_t='N/A'
                                try:
                                    pic_l=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[1]/div[1]/a').get_attribute('href')
                                except:
                                    pic_l='N/A'
                                
                                try:
                                    if checks==0:
                                        if P_Name != ' ' and P_Name != '' and P_Name != '\n':
                                            try:
                                                pid = con.execute('SELECT ID_Publisher FROM db_comicsf.tbl_Publisher WHERE Name_Publisher="'+P_Name+'";').fetchone()[0]
                                                sql='INSERT INTO db_comicsf.tbl_Imprint(ID_Publisher,Bedetheque_Link,Name_Imprint) VALUES('+str(pid)+',"'+str(I_Link)+'","'+str(I_Name)+'");'
                                                con.execute(sql)
                                                print(sql)
                                                iid = con.execute('SELECT ID_Imprint FROM db_comicsf.tbl_Imprint WHERE Name_Imprint="'+I_Name+'";').fetchone()[0]
                                            except:
                                                sql='INSERT INTO db_comicsf.tbl_Publisher(Name_Publisher) VALUES("'+P_Name+'");'
                                                con.execute(sql)
                                                print(sql)
                                                pid = con.execute('SELECT ID_Publisher FROM db_comicsf.tbl_Publisher WHERE Name_Publisher="'+P_Name+'";').fetchone()[0]
                                                if I_Name != '' and I_Name != ' ' and I_Name != '\n':
                                                    sql='INSERT INTO db_comicsf.tbl_Imprint(ID_Publisher,Bedetheque_Link,Name_Imprint) VALUES('+str(pid)+',"'+str(I_Link)+'","'+str(I_Name)+'");'
                                                    con.execute(sql)
                                                    print(sql)
                                                    iid = con.execute('SELECT ID_Imprint FROM db_comicsf.tbl_Imprint WHERE Name_Imprint="'+I_Name+'";').fetchone()[0]
                                                else:
                                                    iid=0
                                        
                                        name=' '
                                        try:
                                            name=driver.find_element_by_xpath('/html/body/div[7]/div[2]/article/div[1]/div/h1/a').text
                                        except:
                                            try:
                                                name=driver.find_element_by_xpath('/html/body/div[8]/div[2]/article/div[1]/div/h1/a').text
                                            except:
                                                name='N/A'
                                        name=str(name).replace('"','')
                                        name=str(name).replace('/','')
                                        name=str(name).replace('\\','')
                                        name=str(name).replace('\'','')
                                        name=str(name).replace('%','')
                                        try:
                                            sql='INSERT INTO db_comicsf.tbl_RunTitle (Name_Run,ID_Country,ID_Language,Bdtheque_Link,Synopsis,Origin,Genre,Bdtheque_ID,Ongoing_Title,Number_of_Books) VALUES ("'+name+'",2,2,"'+str(driver.current_url)+'","'+synopsis+'","'+org+'","'+gen+'","'+idf+'","'+par+'","'+tome+'");'
                                            print(sql)
                                            con.execute(sql)
                                        except:
                                            if self.isEnglish(synopsis)==False:
                                                r=''
                                                for lat in range(len(synopsis)-1):
                                                    if self.isEnglish(synopsis[lat])==True:
                                                        r=r+synopsis[lat]
                                                    else:
                                                        r=r+'e'
                                                synopsis=r
                                            sql='INSERT INTO db_comicsf.tbl_RunTitle (Name_Run,ID_Country,ID_Language,Bdtheque_Link,Synopsis,Origin,Genre,Bdtheque_ID,Ongoing_Title,Number_of_Books) VALUES ("'+name+'",2,2,"'+str(driver.current_url)+'","'+synopsis+'","'+org+'","'+gen+'","'+idf+'","'+par+'","'+tome+'");'
                                            print(sql)
                                            con.execute(sql)
                                        
                                        checks=1
                                    
                                    try:
                                        tid = con.execute('SELECT Title_ID FROM db_comicsf.tbl_RunTitle ORDER BY Title_ID DESC LIMIT 1;').fetchone()[0]
                                        try:
                                            sql='INSERT INTO db_comicsf.tbl_Floppy(Title_ID,Issue_Number,Title,Bedetheque_Link,Bedetheque_ID,Release_Date,Size,Page_Count,Notes,ISBN,ISBN13,Picture_Thumbnail,Picture) VALUES('+str(tid)+',"'+issue+'","'+title+'","'+str(f_link)+'","'+BD_ID+'","'+release_D+'","'+size+'","'+pages+'","'+str(notes)+'","'+isbn+'","'+isbn13+'","'+str(pic_t)+'","'+str(pic_l)+'");'
                                            con.execute(sql)
                                            print(sql)
                                        except:
                                            if self.isEnglish(notes)==False:
                                                r=''
                                                for lat in range(len(notes)-1):
                                                    if self.isEnglish(notes[lat])==True:
                                                        r=r+notes[lat]
                                                    else:
                                                        r=r+'e'
                                                notes=r
                                            sql='INSERT INTO db_comicsf.tbl_Floppy(Title_ID,Issue_Number,Title,Bedetheque_Link,Bedetheque_ID,Release_Date,Size,Page_Count,Notes,ISBN,ISBN13,Picture_Thumbnail,Picture) VALUES('+str(tid)+',"'+issue+'","'+title+'","'+str(f_link)+'","'+BD_ID+'","'+release_D+'","'+size+'","'+pages+'","'+str(notes)+'","'+isbn+'","'+isbn13+'","'+str(pic_t)+'","'+str(pic_l)+'");'
                                            con.execute(sql)
                                            print(sql)

                                        fid = con.execute('SELECT Issue_ID FROM db_comicsf.tbl_Floppy ORDER BY Issue_ID DESC LIMIT 1;').fetchone()[0]
                                        cnt=0
                                        while cnt < len(art):
                                            self.dump_artist(driver,con,str(job[cnt]),str(art[cnt]),fid)
                                            cnt+=1
                                    except:
                                        traceback.print_exc()
                                        print("Floppy MySql Error")
                                        error_file.write('Floppy MySql Error '+str(i)+' '+str(k)+' '+str(nlink)+'\n')
                                        pass
                                except:
                                    traceback.print_exc()
                                    print("Title MySql Error")
                                    error_file.write('Title MySql Error '+str(i)+' '+str(nlink)+'\n')
                                    pass

                                # Variant Scraping
                                try:                                    
                                    var=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(k)+']/div[2]/div[2]/p[2]/a').get_attribute('href')
                                    newTab = 'window.open("' + var + '", "_blank");'
                                    driver.execute_script(newTab)
                                    driver.switch_to_window(driver.window_handles[2])
                                    visbn,visbn13,vpages,reprint,vnotes=' ',' ',' ',' ',' '
                                    try:
                                        m=2
                                        while self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(m)+']') == True:
                                            vname=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(m)+']/div[2]/h3').text
                                            vname=str(vname).replace('"','')
                                            vname=str(vname).replace('/','')
                                            vname=str(vname).replace('\\','')
                                            vname=str(vname).replace('\'','')
                                            vname=str(vname).replace('%','')
                                                                                      
                                            n=1
                                            while self.check(driver,'/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(m)+']/div[2]/ul/li['+str(n)+']') == True:
                                                vdata=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(m)+']/div[2]/ul/li['+str(n)+']').text
                                                vdata=str(vdata).split('\n')
                                                if 'ISBN' in str(vdata[0]):
                                                    if len(vdata)>1:
                                                        visbn=str(vdata[1])
                                                        visbn=visbn.replace('-','')
                                                        ilen=len(str(visbn))
                                                        if ilen > 10:
                                                            visbn13=visbn
                                                            visbn='N/A'
                                                        else:
                                                            visbn13='N/A'
                                                    else:
                                                        visbn='N/A'
                                                        visbn13='N/A'
                                                elif 'Planches' in str(vdata[0]):
                                                    if len(vdata)>1:
                                                        vpages=str(vdata[1])
                                                    else:
                                                        vpages='N/A'
                                                elif 'Dépot légal' in str(vdata[0]):
                                                    if len(vdata)>1:
                                                        vRdate=str(vdata[1])
                                                        vRdate=vRdate.split('(')
                                                        vRdate=str(vRdate[0])
                                                        vRdate=vRdate.replace(' ','')
                                                        temp=release_D.split('(')
                                                        temp=str(temp[0])
                                                        temp=temp.replace(' ','')
                                                        if vRdate==temp:
                                                            reprint='N'
                                                        else:
                                                            reprint='Y'
                                                    else:
                                                        reprint='N/A'                               
                                                n+=1

                                            try:
                                                vnotes=driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[2]/div[1]/ul/li['+str(m)+']/div[2]/div/p').text
                                                vnotes=str(vnotes).split('tion :')
                                                vnotes=str(vnotes[1])
                                                vnotes=str(vnotes).replace('"','')
                                                vnotes=str(vnotes).replace('/','')
                                                vnotes=str(vnotes).replace('\\','')
                                                vnotes=str(vnotes).replace('\'','')
                                                vnotes=str(vnotes).replace('%','')
                                            except:
                                                vnotes=' '
                                            try:
                                                sql='INSERT INTO db_comicsf.tbl_Variant(Issue_ID,Name_Variant,Bedetheque_Link,Reprint,Release_Date,size,Page_Count,Notes,ISBN,ISBN13) VALUES('+str(fid)+',"'+vname+'","'+str(driver.current_url)+'","'+reprint+'","'+vRdate+'","'+size+'","'+vpages+'","'+vnotes+'","'+visbn+'","'+visbn13+'");'
                                                con.execute(sql)
                                                print(sql)
                                            except:
                                                if self.isEnglish(vnotes)==False:
                                                    r=''
                                                    for lat in range(len(vnotes)-1):
                                                        if self.isEnglish(vnotes[lat])==True:
                                                            r=r+vnotes[lat]
                                                        else:
                                                            r=r+'e'
                                                    vnotes=r
                                                sql='INSERT INTO db_comicsf.tbl_Variant(Issue_ID,Name_Variant,Bedetheque_Link,Reprint,Release_Date,size,Page_Count,Notes,ISBN,ISBN13) VALUES('+str(fid)+',"'+vname+'","'+str(driver.current_url)+'","'+reprint+'","'+vRdate+'","'+size+'","'+vpages+'","'+vnotes+'","'+visbn+'","'+visbn13+'");'
                                                con.execute(sql)
                                                print(sql)
                                            m+=1
                                    except:
                                        traceback.print_exc()
                                        print("Variant Error")
                                        error_file.write('Variant Error '+str(i)+' '+str(k)+' '+str(nlink)+' '+str(var)+'\n')
                                        pass
                                    driver.execute_script('window.close()')
                                    driver.switch_to_window(driver.window_handles[1])
                                except:
                                    print("No Variant")
                                    pass                               
                                # Variant End
                                k+=1
                        except:
                            traceback.print_exc()
                            print("Floppy Scrape Error")
                            error_file.write('Floppy Scrape Error '+str(i)+' '+str(k)+' '+str(nlink)+'\n')
                            pass
                    except:
                        traceback.print_exc()
                        print("Title Scrape Error")
                        error_file.write('Title Scrape Error '+str(i)+' '+str(nlink)+'\n')
                        pass

                    driver.execute_script('window.close()')
                    driver.switch_to_window(driver.window_handles[0])
            except:
                traceback.print_exc()
                print("Link Error")
                error_file.write('Link Error '+str(i)+'\n')
                pass

            i+=1
        error_file.close()