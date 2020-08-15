from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import csv
import traceback

def conv(n):
    n=int(n)
    res=''
    if n==1:
        res='enero'
    if n==2:
        res='febrero'
    if n==3:
        res='marzo'
    if n==4:
        res='abril'
    if n==5:
        res='mayo'
    if n==6:
        res='junio'
    if n==7:
        res='julio'
    if n==8:
        res='agosto'
    if n==9:
        res='septiembre'
    if n==10:
        res='octubre'
    if n==11:
        res='noviembre'
    if n==12:
        res='diciembre'
    return res

def write(date,college,teacher,figure,area):
    data=[]
    data.append(str(date))
    data.append(str(college))
    data.append(str(teacher))
    data.append(str(figure))
    data.append(str(area))  
        
    with open('test.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()

col=['FECHA','UNIVERSIDAD','PROFESOR','FIGURA','ÁREA']

with open('test.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='/home/smash/Desktop/amazon/chromedriver',chrome_options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)
url='https://www.boe.es/'
driver.get(url)
time.sleep(2)

driver.find_element_by_xpath('//*[@id="diarios"]/div[2]/div[1]/div[1]/div/div/div/ul/li[2]/a/span').click()

words=['titular de Universidad']
for word in words:
    driver.find_element_by_xpath('//*[@id="DOC"]').send_keys(str(word))
    driver.find_element_by_xpath('//*[@id="desdeFP"]').send_keys('01012002')
    driver.find_element_by_xpath('//*[@id="hastaFP"]').send_keys('12312018')
    driver.find_element_by_xpath('//*[@id="mostrar"]/option[5]').click()
    driver.find_element_by_xpath('//*[@id="orden"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="contenido"]/form/div/div/input[1]').click()
    if 'Catedrático' in word:
        cnt=1
        counts=driver.find_elements_by_xpath('//*[@id="contenido"]/div[3]/ul/li')
        while cnt<len(counts):
            if cnt==2:
                nextL=driver.find_element_by_xpath('//*[@id="contenido"]/div[3]/ul/li['+str(cnt)+']/a').get_attribute('href')
                driver.get(nextL)
            elif cnt>2:
                nextL=driver.find_element_by_xpath('//*[@id="contenido"]/div[3]/ul/li['+str(cnt+1)+']/a').get_attribute('href')
                driver.get(nextL)
            cnt+=1

            lis=driver.find_elements_by_xpath('//*[@id="contenido"]/div[4]/ul/li')
            i=1
            for li in lis:
                fecha,coll,prof,fig,area='N/A','N/A','N/A','N/A','N/A'
                linep=li.find_element_by_tag_name('p')
                if 'Profesores Universitarios' not in str(linep.text) and 'profesores titulares' not in str(linep.text).lower():
                    if 'Catedrático' in str(linep.text):               
                        lineh=li.find_element_by_tag_name('h4')
                        lineh=str(lineh.text).split('-')
                        lineh=str(lineh[0]).split(' ')
                        temp=str(lineh[len(lineh)-2])
                        temp=temp.split('/')
                        month=str(conv(temp[1]))
                        day=str(int(temp[0]))
                        fecha=day+' de '+month+' de '+str(temp[2])
                        print(fecha)
                
                        temp=str(linep.text).split('Universidad')
                        if len(temp)>1:
                            temp=str(temp[1]).split(',')
                            temp=str(temp[0])
                            coll=str('Universidad'+temp).replace(',','')
                            print(coll)

                        temp=str(linep.text)
                        temp=temp.split('por la que se nombra')
                        if len(temp)>1:
                            temp=str(temp[1]).split('Catedrático')
                            if str(temp[0])!='' and str(temp[0])!=', ' and str(temp[0])!=',' and str(temp[0])!=' ':
                                prof=str(temp[0]).replace(',','')
                            else:
                                if 'a don ' in str(temp[1]):
                                    temp=str(temp[1]).split('a don ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a Don ' in str(temp[1]):
                                    temp=str(temp[1]).split('a Don ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a doña ' in str(temp[1]):
                                    temp=str(temp[1]).split('a doña ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'Doña ' in str(temp[1]):
                                    temp=str(temp[1]).split('Doña ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a D.' in str(temp[1]):
                                    temp=str(temp[1]).split('a D.')
                                    temp=str(temp[1]).split(',')
                                    prof=str(temp[0]).replace(',','')
                                elif 'Dña.' in str(temp[1]):
                                    temp=str(temp[1]).split('Dña.')
                                    temp=str(temp[1]).split(',')
                                    prof=str(temp[0]).replace(',','')
                            fig='Catedrático de Universidad'
                        else:
                            temp=str(linep.text)
                            temp=temp.split('por la que se')
                            if len(temp)>1:
                                temp=str(temp[1]).split('Catedrático')
                                if str(temp[0])!='' and str(temp[0])!=', ' and str(temp[0])!=',' and str(temp[0])!=' ':
                                    prof=str(temp[0]).replace(',','')
                                else:
                                    if 'a don ' in str(temp[1]):
                                        temp=str(temp[1]).split('a don ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a Don ' in str(temp[1]):
                                        temp=str(temp[1]).split('a Don ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a doña ' in str(temp[1]):
                                        temp=str(temp[1]).split('a doña ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'Doña ' in str(temp[1]):
                                        temp=str(temp[1]).split('Doña ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a D.' in str(temp[1]):
                                        temp=str(temp[1]).split('a D.')
                                        temp=str(temp[1]).split(',')
                                        prof=str(temp[0]).replace(',','')
                                    elif 'Dña.' in str(temp[1]):
                                        temp=str(temp[1]).split('Dña.')
                                        temp=str(temp[1]).split(',')
                                        prof=str(temp[0]).replace(',','')
                            else:
                                temp=str(linep.text)
                                temp=temp.split('se nombra')
                                if len(temp)>1:
                                    temp=str(temp[1]).split('Catedrático')
                                    prof=str(temp[0]).replace(',','')
                            fig='Catedrático de Universidad'
                        
                        if 'don ' in str(prof):
                            prof=str(prof).split('don ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Don ' in str(prof):
                            prof=str(prof).split('Don ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'doña ' in str(prof):
                            prof=str(prof).split('doña ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Doña ' in str(prof):
                            prof=str(prof).split('Doña ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'D.' in str(prof):
                            prof=str(prof).split('D.')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Dña.' in str(prof):
                            prof=str(prof).split('Dña.')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')

                        if len(prof)>4:
                            if 'Área' in prof:
                                prof=str(prof).split('Área')
                                prof=str(prof[0])
                            elif 'área' in prof:
                                prof=str(prof).split('área')
                                prof=str(prof[0])
                        else:
                            prof='N/A'

                        #prof=prof+' ******************** '+str(len(prof))
                        if len(prof)>44 or 'declara desierta una plaza de' in prof:
                            prof='N/A'
                        
                        temp=str(linep.text)
                        if prof=='N/A' and ' doña ' in temp:
                            temp=temp.split(' doña ')
                            if ', ' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif '.' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif 'Catedrático' in temp[1]:
                                temp=str(temp[1]).split('Catedrático')
                                prof=str(temp[0])
                        elif prof=='N/A' and ' don ' in temp:
                            temp=temp.split(' don ')
                            if ', ' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif '.' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif 'Catedrático' in temp[1]:
                                temp=str(temp[1]).split('Catedrático')
                                prof=str(temp[0])
                        
                        prof=str(prof).rstrip()
                        prof=str(str(prof).strip('.')).replace('"','')
                        print(prof)
                        print(fig)
                        if prof!='N/A' and prof!='' and prof!=' ':
                            temp=str(linep.text).lower()
                            if 'área' in temp:
                                temp=temp.split('área')
                                if ' "' in str(temp[1]):
                                    temp=str(temp[1]).split(' "')
                                    if '" ' in temp[1]:
                                        temp=str(temp[1]).split('" ')
                                        area=str(temp[0]).replace(',','')
                                    elif '".' in temp[1]:
                                        temp=str(temp[1]).split('".')
                                        area=str(temp[0]).replace(',','')
                                    elif '",' in temp[1]:
                                        temp=str(temp[1]).split('",')
                                        area=str(temp[0]).replace(',','')
                                elif prof in str(temp[1]):
                                    temp=str(temp[1]).split(prof)
                                    area=str(temp[0]).replace(',','')      
                                else:
                                    area=str(temp[1]).replace(',','')

                            if area=='N/A':
                                lnk=li.find_element_by_tag_name('a').get_attribute('href')
                                newTab = 'window.open("' + lnk + '", "_blank");'
                                driver.execute_script(newTab)
                                driver.switch_to_window(driver.window_handles[1])
                                ps=driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                                for p in ps:
                                    temp=str(p.text).lower()
                                    if str(prof).lower() in temp and 'área' in temp:
                                        temp=str(temp).split('área')
                                        if '«' in str(temp[1]):
                                            temp=str(temp[1]).split('«')
                                            temp=str(temp[1]).split('»')
                                            area=str(temp[0])
                                        elif 'conocimiento' in str(temp[1]):
                                            temp=str(temp[1]).split('conocimiento')
                                            temp=str(temp[1]).split(',')
                                            if len(temp)==1:
                                                temp=str(temp[0]).split('.')
                                            area=str(temp[0])
                                        else:
                                            ind0=ps.index(p)
                                            try:
                                                nextp0=ps[ind0+1]
                                            except:
                                                nextp0=ps[ind0]
                                            nextp0=str(nextp0.text).lower()
                                            if 'conocimiento' in str(nextp0):
                                                nextp0=str(nextp0).split('conocimiento')
                                                nextp0=str(nextp0[1]).split(',')
                                                if len(nextp0)==1:
                                                    nextp0=str(nextp0[0]).split('.')
                                                area=str(nextp0[0])
                                    elif 'área' in temp:
                                        if 'área' in str(p.text):
                                            nt=str(p.text).split('área')
                                        elif 'Área' in str(p.text):
                                            nt=str(p.text).split('Área')
                                        lat=str(nt[1]).lower()
                                        if ' "' in str(nt[1]):
                                            nt=str(nt[1]).split(' "')
                                            if '"' in str(nt[1]):
                                                nt=str(nt[1]).split('"')
                                                area=str(nt[0]).replace(',','')
                                            else:
                                                area=str(nt[1]).replace(',','')
                                        elif 'conocimiento' in lat:
                                            lat=str(lat).split('conocimiento')
                                            if ',' in str(lat[1]):
                                                lat=str(lat[1]).split(',')
                                                area=str(lat[0]).replace(',','')
                                            elif '«' in str(lat[1]):
                                                lat=str(lat[1]).split('«')
                                                lat=str(lat[1]).split('»')
                                                area=str(lat[0])
                                            else:
                                                area=str(lat[1])
                                        else:
                                            ind2=ps.index(p)
                                            try:
                                                nextp2=ps[ind2+1]
                                            except:
                                                nextp2=ps[ind2]
                                            nextp2=nextp2.text
                                            if ' "' in str(nextp2):
                                                nt2=str(nextp2).split(' "')
                                                if '"' in str(nt2[1]):
                                                    nt2=str(nt2[1]).split('"')
                                                    area=str(nt2[0]).replace(',','')
                                                else:
                                                    area=str(nt2[1]).replace(',','')
                                            elif 'conocimiento' in str(nextp2):
                                                lat=str(nextp2).split('conocimiento')
                                                if ',' in str(lat[1]):
                                                    lat=str(lat[1]).split(',')
                                                    area=str(lat[0]).replace(',','')
                                                elif '«' in str(lat[1]):
                                                    lat=str(lat[1]).split('«')
                                                    lat=str(lat[1]).split('»')
                                                    area=str(lat[0])
                                                else:
                                                    area=str(lat[1])
                                                
                                                if area!='N/A':
                                                    t=str(area).replace(' ','')
                                                    if len(t)<=3:
                                                        if ',' in str(nextp2):
                                                            nextp2=str(nextp2).split(',')
                                                            area=str(nextp2[0]).replace(',','')
                                                        elif '«' in str(nextp2):
                                                            nextp2=str(nextp2).split('«')
                                                            nextp2=str(nextp2[1]).split('»')
                                                            area=str(nextp2[0])
                                                        else:
                                                            area=str(nextp2)

                                driver.execute_script('window.close()')
                                driver.switch_to_window(driver.window_handles[0])
                            area=str(area).replace('"','')
                            print(area)
                        if coll!='N/A' and prof!='N/A':
                            write(fecha,coll,prof,fig,area)
                elif 'Profesores Universitarios' in str(linep.text) or 'profesores titulares' in str(linep.text).lower():
                    lineh=li.find_element_by_tag_name('h4')
                    lineh=str(lineh.text).split('-')
                    lineh=str(lineh[0]).split(' ')
                    temp=str(lineh[len(lineh)-2])
                    temp=temp.split('/')
                    month=str(conv(temp[1]))
                    day=str(int(temp[0]))
                    fecha=day+' de '+month+' de '+str(temp[2])
                    print(fecha)
                    
                    lnk=li.find_element_by_tag_name('a').get_attribute('href')
                    newTab = 'window.open("' + lnk + '", "_blank");'
                    driver.execute_script(newTab)
                    driver.switch_to_window(driver.window_handles[1])
                    ps=driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                    txt=driver.find_element_by_xpath('//*[@id="barraSep"]/h3').text
                    if 'de la Universidad' in str(txt):
                        temp=str(txt).split('Universidad')
                        if len(temp)>1:
                            temp=str(temp[1]).split(',')
                            temp=str(temp[0])
                            coll='Universidad'+temp
                            print(coll)
                        for p in ps:
                            temp=p.text
                            if 'Catedrático' in temp:
                                temp=str(temp).split('Catedrático')
                                prof=str(temp[0]).replace(',','')
                                print(prof)
                                ind=ps.index(p)
                                try:
                                    nxtp=ps[ind+1]
                                except:
                                    nxtp=ps[ind]
                                nextp=nxtp.text
                                if 'área' in nextp:
                                    nt=str(nextp).split('área')
                                    if ' "' in str(nt[1]):
                                        nt=str(nt[1]).split(' "')
                                        if '"' in str(nt[1]):
                                            nt=str(nt[1]).split('"')
                                            area=str(nt[0]).replace(',','')
                                        else:
                                            area=str(nt[1]).replace(',','')
                                    else:
                                        ind2=ps.index(nxtp)
                                        nextp2=ps[ind2+1]
                                        nextp2=nextp2.text
                                        if ' "' in str(nextp2):
                                            nt2=str(nextp2).split(' "')
                                            if '"' in str(nt2[1]):
                                                nt2=str(nt2[1]).split('"')
                                                area=str(nt2[0]).replace(',','')
                                            else:
                                                area=str(nt2[1]).replace(',','')
                                        else:
                                            area='N/A'
                                else:
                                    area='N/A'
                                
                                area=str(area).replace('"','')
                                print(area)
                                if coll!='N/A' and prof!='N/A':
                                    write(fecha,coll,prof,'Catedrático de Universidad',area)
                    
                    driver.execute_script('window.close()')
                    driver.switch_to_window(driver.window_handles[0])
    #break
    elif 'Catedrática' in word:
        cnt=1
        counts=driver.find_elements_by_xpath('//*[@id="contenido"]/div[3]/ul/li')
        while cnt<len(counts):
            if cnt==2:
                nextL=driver.find_element_by_xpath('//*[@id="contenido"]/div[3]/ul/li['+str(cnt)+']/a').get_attribute('href')
                driver.get(nextL)
            elif cnt>2:
                nextL=driver.find_element_by_xpath('//*[@id="contenido"]/div[3]/ul/li['+str(cnt+1)+']/a').get_attribute('href')
                driver.get(nextL)
            cnt+=1

            lis=driver.find_elements_by_xpath('//*[@id="contenido"]/div[4]/ul/li')
            i=1
            for li in lis:
                fecha,coll,prof,fig,area='N/A','N/A','N/A','N/A','N/A'
                linep=li.find_element_by_tag_name('p')
                if 'Profesores Universitarios' not in str(linep.text) and 'profesores titulares' not in str(linep.text).lower():
                    if 'Catedrática' in str(linep.text):               
                        lineh=li.find_element_by_tag_name('h4')
                        lineh=str(lineh.text).split('-')
                        lineh=str(lineh[0]).split(' ')
                        temp=str(lineh[len(lineh)-2])
                        temp=temp.split('/')
                        month=str(conv(temp[1]))
                        day=str(int(temp[0]))
                        fecha=day+' de '+month+' de '+str(temp[2])
                        print(fecha)
                
                        temp=str(linep.text).split('Universidad')
                        if len(temp)>1:
                            temp=str(temp[1]).split(',')
                            temp=str(temp[0])
                            coll=str('Universidad'+temp).replace(',','')
                            print(coll)

                        temp=str(linep.text)
                        temp=temp.split('por la que se nombra')
                        if len(temp)>1:
                            temp=str(temp[1]).split('Catedrática')
                            if str(temp[0])!='' and str(temp[0])!=', ' and str(temp[0])!=',' and str(temp[0])!=' ':
                                prof=str(temp[0]).replace(',','')
                            else:
                                if 'a don ' in str(temp[1]):
                                    temp=str(temp[1]).split('a don ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a Don ' in str(temp[1]):
                                    temp=str(temp[1]).split('a Don ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a doña ' in str(temp[1]):
                                    temp=str(temp[1]).split('a doña ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'Doña ' in str(temp[1]):
                                    temp=str(temp[1]).split('Doña ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a D.' in str(temp[1]):
                                    temp=str(temp[1]).split('a D.')
                                    temp=str(temp[1]).split(',')
                                    prof=str(temp[0]).replace(',','')
                                elif 'Dña.' in str(temp[1]):
                                    temp=str(temp[1]).split('Dña.')
                                    temp=str(temp[1]).split(',')
                                    prof=str(temp[0]).replace(',','')
                            fig='Catedrática de Universidad'
                        else:
                            temp=str(linep.text)
                            temp=temp.split('por la que se')
                            if len(temp)>1:
                                temp=str(temp[1]).split('Catedrática')
                                if str(temp[0])!='' and str(temp[0])!=', ' and str(temp[0])!=',' and str(temp[0])!=' ':
                                    prof=str(temp[0]).replace(',','')
                                else:
                                    if 'a don ' in str(temp[1]):
                                        temp=str(temp[1]).split('a don ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a Don ' in str(temp[1]):
                                        temp=str(temp[1]).split('a Don ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a doña ' in str(temp[1]):
                                        temp=str(temp[1]).split('a doña ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'Doña ' in str(temp[1]):
                                        temp=str(temp[1]).split('Doña ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a D.' in str(temp[1]):
                                        temp=str(temp[1]).split('a D.')
                                        temp=str(temp[1]).split(',')
                                        prof=str(temp[0]).replace(',','')
                                    elif 'Dña.' in str(temp[1]):
                                        temp=str(temp[1]).split('Dña.')
                                        temp=str(temp[1]).split(',')
                                        prof=str(temp[0]).replace(',','')
                            else:
                                temp=str(linep.text)
                                temp=temp.split('se nombra')
                                if len(temp)>1:
                                    temp=str(temp[1]).split('Catedrática')
                                    prof=str(temp[0]).replace(',','')
                            fig='Catedrática de Universidad'
                        
                        if 'don ' in str(prof):
                            prof=str(prof).split('don ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Don ' in str(prof):
                            prof=str(prof).split('Don ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'doña ' in str(prof):
                            prof=str(prof).split('doña ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Doña ' in str(prof):
                            prof=str(prof).split('Doña ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'D.' in str(prof):
                            prof=str(prof).split('D.')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Dña.' in str(prof):
                            prof=str(prof).split('Dña.')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')

                        if len(prof)>4:
                            if 'Área' in prof:
                                prof=str(prof).split('Área')
                                prof=str(prof[0])
                            elif 'área' in prof:
                                prof=str(prof).split('área')
                                prof=str(prof[0])
                        else:
                            prof='N/A'

                        #prof=prof+' ******************** '+str(len(prof))
                        if len(prof)>44 or 'declara desierta una plaza de' in prof:
                            prof='N/A'
                        
                        temp=str(linep.text)
                        if prof=='N/A' and ' doña ' in temp:
                            temp=temp.split(' doña ')
                            if ', ' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif '.' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif 'Catedrática' in temp[1]:
                                temp=str(temp[1]).split('Catedrática')
                                prof=str(temp[0])
                        elif prof=='N/A' and ' don ' in temp:
                            temp=temp.split(' don ')
                            if ', ' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif '.' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif 'Catedrática' in temp[1]:
                                temp=str(temp[1]).split('Catedrática')
                                prof=str(temp[0])
                        
                        prof=str(prof).rstrip()
                        prof=str(str(prof).strip('.')).replace('"','')
                        print(prof)
                        print(fig)
                        if prof!='N/A' and prof!='' and prof!=' ':
                            temp=str(linep.text).lower()
                            if 'área' in temp:
                                temp=temp.split('área')
                                if ' "' in str(temp[1]):
                                    temp=str(temp[1]).split(' "')
                                    if '" ' in temp[1]:
                                        temp=str(temp[1]).split('" ')
                                        area=str(temp[0]).replace(',','')
                                    elif '".' in temp[1]:
                                        temp=str(temp[1]).split('".')
                                        area=str(temp[0]).replace(',','')
                                    elif '",' in temp[1]:
                                        temp=str(temp[1]).split('",')
                                        area=str(temp[0]).replace(',','')
                                elif prof in str(temp[1]):
                                    temp=str(temp[1]).split(prof)
                                    area=str(temp[0]).replace(',','')      
                                else:
                                    area=str(temp[1]).replace(',','')

                            if area=='N/A':
                                lnk=li.find_element_by_tag_name('a').get_attribute('href')
                                newTab = 'window.open("' + lnk + '", "_blank");'
                                driver.execute_script(newTab)
                                driver.switch_to_window(driver.window_handles[1])
                                ps=driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                                for p in ps:
                                    temp=str(p.text).lower()
                                    if str(prof).lower() in temp and 'área' in temp:
                                        temp=str(temp).split('área')
                                        if '«' in str(temp[1]):
                                            temp=str(temp[1]).split('«')
                                            temp=str(temp[1]).split('»')
                                            area=str(temp[0])
                                        elif 'conocimiento' in str(temp[1]):
                                            temp=str(temp[1]).split('conocimiento')
                                            temp=str(temp[1]).split(',')
                                            if len(temp)==1:
                                                temp=str(temp[0]).split('.')
                                            area=str(temp[0])
                                        else:
                                            ind0=ps.index(p)
                                            try:
                                                nextp0=ps[ind0+1]
                                            except:
                                                nextp0=ps[ind0]
                                            nextp0=str(nextp0.text).lower()
                                            if 'conocimiento' in str(nextp0):
                                                nextp0=str(nextp0).split('conocimiento')
                                                nextp0=str(nextp0[1]).split(',')
                                                if len(nextp0)==1:
                                                    nextp0=str(nextp0[0]).split('.')
                                                area=str(nextp0[0])
                                    elif 'área' in temp:
                                        if 'área' in str(p.text):
                                            nt=str(p.text).split('área')
                                        elif 'Área' in str(p.text):
                                            nt=str(p.text).split('Área')
                                        lat=str(nt[1]).lower()
                                        if ' "' in str(nt[1]):
                                            nt=str(nt[1]).split(' "')
                                            if '"' in str(nt[1]):
                                                nt=str(nt[1]).split('"')
                                                area=str(nt[0]).replace(',','')
                                            else:
                                                area=str(nt[1]).replace(',','')
                                        elif 'conocimiento' in lat:
                                            lat=str(lat).split('conocimiento')
                                            if ',' in str(lat[1]):
                                                lat=str(lat[1]).split(',')
                                                area=str(lat[0]).replace(',','')
                                            elif '«' in str(lat[1]):
                                                lat=str(lat[1]).split('«')
                                                lat=str(lat[1]).split('»')
                                                area=str(lat[0])
                                            else:
                                                area=str(lat[1])
                                        else:
                                            ind2=ps.index(p)
                                            try:
                                                nextp2=ps[ind2+1]
                                            except:
                                                nextp2=ps[ind2]
                                            nextp2=nextp2.text
                                            if ' "' in str(nextp2):
                                                nt2=str(nextp2).split(' "')
                                                if '"' in str(nt2[1]):
                                                    nt2=str(nt2[1]).split('"')
                                                    area=str(nt2[0]).replace(',','')
                                                else:
                                                    area=str(nt2[1]).replace(',','')
                                            elif 'conocimiento' in str(nextp2):
                                                lat=str(nextp2).split('conocimiento')
                                                if ',' in str(lat[1]):
                                                    lat=str(lat[1]).split(',')
                                                    area=str(lat[0]).replace(',','')
                                                elif '«' in str(lat[1]):
                                                    lat=str(lat[1]).split('«')
                                                    lat=str(lat[1]).split('»')
                                                    area=str(lat[0])
                                                else:
                                                    area=str(lat[1])
                                                
                                                if area!='N/A':
                                                    t=str(area).replace(' ','')
                                                    if len(t)<=3:
                                                        if ',' in str(nextp2):
                                                            nextp2=str(nextp2).split(',')
                                                            area=str(nextp2[0]).replace(',','')
                                                        elif '«' in str(nextp2):
                                                            nextp2=str(nextp2).split('«')
                                                            nextp2=str(nextp2[1]).split('»')
                                                            area=str(nextp2[0])
                                                        else:
                                                            area=str(nextp2)

                                driver.execute_script('window.close()')
                                driver.switch_to_window(driver.window_handles[0])
                            area=str(area).replace('"','')
                            print(area)
                        if coll!='N/A' and prof!='N/A':
                            write(fecha,coll,prof,fig,area)
                elif 'Profesores Universitarios' in str(linep.text) or 'profesores titulares' in str(linep.text).lower():
                    lineh=li.find_element_by_tag_name('h4')
                    lineh=str(lineh.text).split('-')
                    lineh=str(lineh[0]).split(' ')
                    temp=str(lineh[len(lineh)-2])
                    temp=temp.split('/')
                    month=str(conv(temp[1]))
                    day=str(int(temp[0]))
                    fecha=day+' de '+month+' de '+str(temp[2])
                    print(fecha)
                    
                    lnk=li.find_element_by_tag_name('a').get_attribute('href')
                    newTab = 'window.open("' + lnk + '", "_blank");'
                    driver.execute_script(newTab)
                    driver.switch_to_window(driver.window_handles[1])
                    ps=driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                    txt=driver.find_element_by_xpath('//*[@id="barraSep"]/h3').text
                    if 'de la Universidad' in str(txt):
                        temp=str(txt).split('Universidad')
                        if len(temp)>1:
                            temp=str(temp[1]).split(',')
                            temp=str(temp[0])
                            coll='Universidad'+temp
                            print(coll)
                        for p in ps:
                            temp=p.text
                            if 'Catedrática' in temp:
                                temp=str(temp).split('Catedrática')
                                prof=str(temp[0]).replace(',','')
                                print(prof)
                                ind=ps.index(p)
                                try:
                                    nxtp=ps[ind+1]
                                except:
                                    nxtp=ps[ind]
                                nextp=nxtp.text
                                if 'área' in nextp:
                                    nt=str(nextp).split('área')
                                    if ' "' in str(nt[1]):
                                        nt=str(nt[1]).split(' "')
                                        if '"' in str(nt[1]):
                                            nt=str(nt[1]).split('"')
                                            area=str(nt[0]).replace(',','')
                                        else:
                                            area=str(nt[1]).replace(',','')
                                    else:
                                        ind2=ps.index(nxtp)
                                        nextp2=ps[ind2+1]
                                        nextp2=nextp2.text
                                        if ' "' in str(nextp2):
                                            nt2=str(nextp2).split(' "')
                                            if '"' in str(nt2[1]):
                                                nt2=str(nt2[1]).split('"')
                                                area=str(nt2[0]).replace(',','')
                                            else:
                                                area=str(nt2[1]).replace(',','')
                                        else:
                                            area='N/A'
                                else:
                                    area='N/A'
                                
                                area=str(area).replace('"','')
                                print(area)
                                if coll!='N/A' and prof!='N/A':
                                    write(fecha,coll,prof,'Catedrática de Universidad',area)
                    
                    driver.execute_script('window.close()')
                    driver.switch_to_window(driver.window_handles[0])
    elif 'titular' in word:
        cnt=1
        counts=driver.find_elements_by_xpath('//*[@id="contenido"]/div[3]/ul/li')
        while cnt<len(counts):
            if cnt==2:
                nextL=driver.find_element_by_xpath('//*[@id="contenido"]/div[3]/ul/li['+str(cnt)+']/a').get_attribute('href')
                driver.get(nextL)
            elif cnt>2:
                nextL=driver.find_element_by_xpath('//*[@id="contenido"]/div[3]/ul/li['+str(cnt+1)+']/a').get_attribute('href')
                driver.get(nextL)
            cnt+=1

            lis=driver.find_elements_by_xpath('//*[@id="contenido"]/div[4]/ul/li')
            i=1
            for li in lis:
                fecha,coll,prof,fig,area='N/A','N/A','N/A','N/A','N/A'
                linep=li.find_element_by_tag_name('p')
                if 'Profesores Universitarios' not in str(linep.text) and 'profesores titulares' not in str(linep.text).lower():
                    if 'titular' in str(linep.text) or 'Titular' in str(linep.text):
                        if 'Profesor titular' in str(linep.text):
                            cut='Profesor titular'
                        elif 'Profesora titular' in str(linep.text):
                            cut='Profesora titular'
                        elif 'Profesora Titular' in str(linep.text):
                            cut='Profesora Titular'
                        elif 'Profesor Titular' in str(linep.text):
                            cut='Profesor Titular'
                        elif 'Titular' in str(linep.text):
                            cut='Titular'
                        elif 'titular' in str(linep.text):
                            cut='titular'

                        lineh=li.find_element_by_tag_name('h4')
                        lineh=str(lineh.text).split('-')
                        lineh=str(lineh[0]).split(' ')
                        temp=str(lineh[len(lineh)-2])
                        temp=temp.split('/')
                        month=str(conv(temp[1]))
                        day=str(int(temp[0]))
                        fecha=day+' de '+month+' de '+str(temp[2])
                        print(fecha)
                
                        temp=str(linep.text).split('Universidad')
                        if len(temp)>1:
                            temp=str(temp[1]).split(',')
                            temp=str(temp[0])
                            coll=str('Universidad'+temp).replace(',','')
                            print(coll)

                        temp=str(linep.text)
                        temp=temp.split('por la que se nombra')
                        if len(temp)>1:
                            temp=str(temp[1]).split(cut)
                            if str(temp[0])!='' and str(temp[0])!=', ' and str(temp[0])!=',' and str(temp[0])!=' ':
                                prof=str(temp[0]).replace(',','')
                            else:
                                if 'a don ' in str(temp[1]):
                                    temp=str(temp[1]).split('a don ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a Don ' in str(temp[1]):
                                    temp=str(temp[1]).split('a Don ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a doña ' in str(temp[1]):
                                    temp=str(temp[1]).split('a doña ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'Doña ' in str(temp[1]):
                                    temp=str(temp[1]).split('Doña ')
                                    prof=str(temp[1]).replace(',','')
                                elif 'a D.' in str(temp[1]):
                                    temp=str(temp[1]).split('a D.')
                                    temp=str(temp[1]).split(',')
                                    prof=str(temp[0]).replace(',','')
                                elif 'Dña.' in str(temp[1]):
                                    temp=str(temp[1]).split('Dña.')
                                    temp=str(temp[1]).split(',')
                                    prof=str(temp[0]).replace(',','')
                            fig='titular de Universidad'
                        else:
                            temp=str(linep.text)
                            temp=temp.split('por la que se')
                            if len(temp)>1:
                                temp=str(temp[1]).split(cut)
                                if str(temp[0])!='' and str(temp[0])!=', ' and str(temp[0])!=',' and str(temp[0])!=' ':
                                    prof=str(temp[0]).replace(',','')
                                else:
                                    if 'a don ' in str(temp[1]):
                                        temp=str(temp[1]).split('a don ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a Don ' in str(temp[1]):
                                        temp=str(temp[1]).split('a Don ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a doña ' in str(temp[1]):
                                        temp=str(temp[1]).split('a doña ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'Doña ' in str(temp[1]):
                                        temp=str(temp[1]).split('Doña ')
                                        prof=str(temp[1]).replace(',','')
                                    elif 'a D.' in str(temp[1]):
                                        temp=str(temp[1]).split('a D.')
                                        temp=str(temp[1]).split(',')
                                        prof=str(temp[0]).replace(',','')
                                    elif 'Dña.' in str(temp[1]):
                                        temp=str(temp[1]).split('Dña.')
                                        temp=str(temp[1]).split(',')
                                        prof=str(temp[0]).replace(',','')
                            else:
                                temp=str(linep.text)
                                temp=temp.split('se nombra')
                                if len(temp)>1:
                                    temp=str(temp[1]).split(cut)
                                    prof=str(temp[0]).replace(',','')
                            fig='titular de Universidad'
                        
                        if 'don ' in str(prof):
                            prof=str(prof).split('don ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Don ' in str(prof):
                            prof=str(prof).split('Don ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'doña ' in str(prof):
                            prof=str(prof).split('doña ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Doña ' in str(prof):
                            prof=str(prof).split('Doña ')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'D.' in str(prof):
                            prof=str(prof).split('D.')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')
                        elif 'Dña.' in str(prof):
                            prof=str(prof).split('Dña.')
                            if len(prof)>1:
                                prof=str(prof[1]).replace(',','')
                            else:
                                prof=str(prof[0]).replace(',','')

                        if len(prof)>4:
                            if 'Área' in prof:
                                prof=str(prof).split('Área')
                                prof=str(prof[0])
                            elif 'área' in prof:
                                prof=str(prof).split('área')
                                prof=str(prof[0])
                        else:
                            prof='N/A'

                        #prof=prof+' ******************** '+str(len(prof))
                        if len(prof)>44 or 'declara desierta una plaza de' in prof:
                            prof='N/A'
                        
                        temp=str(linep.text)
                        if prof=='N/A' and ' doña ' in temp:
                            temp=temp.split(' doña ')
                            if ', ' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif '.' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif cut in temp[1]:
                                temp=str(temp[1]).split(cut)
                                prof=str(temp[0])
                        elif prof=='N/A' and ' don ' in temp:
                            temp=temp.split(' don ')
                            if ', ' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif '.' in temp[1]:
                                temp=str(temp[1]).split(', ')
                                prof=str(temp[0])
                            elif cut in temp[1]:
                                temp=str(temp[1]).split(cut)
                                prof=str(temp[0])
                        
                        prof=str(prof).rstrip()
                        prof=str(str(prof).strip('.')).replace('"','')
                        print(prof)
                        print(fig)
                        if prof!='N/A' and prof!='' and prof!=' ':
                            temp=str(linep.text).lower()
                            if 'área' in temp:
                                temp=temp.split('área')
                                if ' "' in str(temp[1]):
                                    temp=str(temp[1]).split(' "')
                                    if '" ' in temp[1]:
                                        temp=str(temp[1]).split('" ')
                                        area=str(temp[0]).replace(',','')
                                    elif '".' in temp[1]:
                                        temp=str(temp[1]).split('".')
                                        area=str(temp[0]).replace(',','')
                                    elif '",' in temp[1]:
                                        temp=str(temp[1]).split('",')
                                        area=str(temp[0]).replace(',','')
                                elif prof in str(temp[1]):
                                    temp=str(temp[1]).split(prof)
                                    area=str(temp[0]).replace(',','')      
                                else:
                                    area=str(temp[1]).replace(',','')

                            if area=='N/A':
                                lnk=li.find_element_by_tag_name('a').get_attribute('href')
                                newTab = 'window.open("' + lnk + '", "_blank");'
                                driver.execute_script(newTab)
                                driver.switch_to_window(driver.window_handles[1])
                                ps=driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                                for p in ps:
                                    temp=str(p.text).lower()
                                    if str(prof).lower() in temp and 'área' in temp:
                                        temp=str(temp).split('área')
                                        if '«' in str(temp[1]):
                                            temp=str(temp[1]).split('«')
                                            temp=str(temp[1]).split('»')
                                            area=str(temp[0])
                                        elif 'conocimiento' in str(temp[1]):
                                            temp=str(temp[1]).split('conocimiento')
                                            temp=str(temp[1]).split(',')
                                            if len(temp)==1:
                                                temp=str(temp[0]).split('.')
                                            area=str(temp[0])
                                        else:
                                            ind0=ps.index(p)
                                            try:
                                                nextp0=ps[ind0+1]
                                            except:
                                                nextp0=ps[ind0]
                                            nextp0=str(nextp0.text).lower()
                                            if 'conocimiento' in str(nextp0):
                                                nextp0=str(nextp0).split('conocimiento')
                                                nextp0=str(nextp0[1]).split(',')
                                                if len(nextp0)==1:
                                                    nextp0=str(nextp0[0]).split('.')
                                                area=str(nextp0[0])
                                    elif 'área' in temp:
                                        if 'área' in str(p.text):
                                            nt=str(p.text).split('área')
                                        elif 'Área' in str(p.text):
                                            nt=str(p.text).split('Área')
                                        lat=str(nt[1]).lower()
                                        if ' "' in str(nt[1]):
                                            nt=str(nt[1]).split(' "')
                                            if '"' in str(nt[1]):
                                                nt=str(nt[1]).split('"')
                                                area=str(nt[0]).replace(',','')
                                            else:
                                                area=str(nt[1]).replace(',','')
                                        elif '"' in str(nextp2):
                                            nt2=str(nextp2).split('"')
                                            area=str(nt2[1]).replace(',','')
                                        elif 'conocimiento' in lat:
                                            lat=str(lat).split('conocimiento')
                                            if ',' in str(lat[1]):
                                                lat=str(lat[1]).split(',')
                                                area=str(lat[0]).replace(',','')
                                            elif '«' in str(lat[1]):
                                                lat=str(lat[1]).split('«')
                                                lat=str(lat[1]).split('»')
                                                area=str(lat[0])
                                            else:
                                                area=str(lat[1])
                                        else:
                                            ind2=ps.index(p)
                                            try:
                                                nextp2=ps[ind2+1]
                                            except:
                                                nextp2=ps[ind2]
                                            nextp2=nextp2.text
                                            if ' "' in str(nextp2):
                                                nt2=str(nextp2).split(' "')
                                                if '"' in str(nt2[1]):
                                                    nt2=str(nt2[1]).split('"')
                                                    area=str(nt2[0]).replace(',','')
                                                else:
                                                    area=str(nt2[1]).replace(',','')
                                            elif '"' in str(nextp2):
                                                nt2=str(nextp2).split('"')
                                                area=str(nt2[1]).replace(',','')
                                            elif 'conocimiento' in str(nextp2):
                                                lat=str(nextp2).split('conocimiento')
                                                if ',' in str(lat[1]):
                                                    lat=str(lat[1]).split(',')
                                                    area=str(lat[0]).replace(',','')
                                                elif '«' in str(lat[1]):
                                                    lat=str(lat[1]).split('«')
                                                    lat=str(lat[1]).split('»')
                                                    area=str(lat[0])
                                                else:
                                                    area=str(lat[1])
                                                
                                                if area!='N/A':
                                                    t=str(area).replace(' ','')
                                                    if len(t)<=3:
                                                        if ',' in str(nextp2):
                                                            nextp2=str(nextp2).split(',')
                                                            area=str(nextp2[0]).replace(',','')
                                                        elif '«' in str(nextp2):
                                                            nextp2=str(nextp2).split('«')
                                                            nextp2=str(nextp2[1]).split('»')
                                                            area=str(nextp2[0])
                                                        else:
                                                            area=str(nextp2)
                                    
                                    if area!='N/A':
                                        t=str(area).replace(' ','')
                                        if len(t)<=3:
                                            ind2=ps.index(p)
                                            try:
                                                nextp2=ps[ind2+1]
                                            except:
                                                nextp2=ps[ind2]
                                            nextp2=nextp2.text
                                            if ' "' in str(nextp2):
                                                nt2=str(nextp2).split(' "')
                                                if '"' in str(nt2[1]):
                                                    nt2=str(nt2[1]).split('"')
                                                    area=str(nt2[0]).replace(',','')
                                                else:
                                                    area=str(nt2[1]).replace(',','')
                                            elif '"' in str(nextp2):
                                                nt2=str(nextp2).split('"')
                                                area=str(nt2[1]).replace(',','')
                                            elif 'conocimiento' in str(nextp2):
                                                lat=str(nextp2).split('conocimiento')
                                                if ',' in str(lat[1]):
                                                    lat=str(lat[1]).split(',')
                                                    area=str(lat[0]).replace(',','')
                                                elif '«' in str(lat[1]):
                                                    lat=str(lat[1]).split('«')
                                                    lat=str(lat[1]).split('»')
                                                    area=str(lat[0])
                                                else:
                                                    area=str(lat[1])

                                driver.execute_script('window.close()')
                                driver.switch_to_window(driver.window_handles[0])
                            area=str(area).replace('"','')
                            print(area)
                        if coll!='N/A' and prof!='N/A':
                            write(fecha,coll,prof,fig,area)
                elif 'Profesores Universitarios' in str(linep.text) or 'profesores titulares' in str(linep.text).lower():
                    lineh=li.find_element_by_tag_name('h4')
                    lineh=str(lineh.text).split('-')
                    lineh=str(lineh[0]).split(' ')
                    temp=str(lineh[len(lineh)-2])
                    temp=temp.split('/')
                    month=str(conv(temp[1]))
                    day=str(int(temp[0]))
                    fecha=day+' de '+month+' de '+str(temp[2])
                    print(fecha)
                    
                    lnk=li.find_element_by_tag_name('a').get_attribute('href')
                    newTab = 'window.open("' + lnk + '", "_blank");'
                    driver.execute_script(newTab)
                    driver.switch_to_window(driver.window_handles[1])
                    ps=driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                    txt=driver.find_element_by_xpath('//*[@id="barraSep"]/h3').text
                    if 'de la Universidad' in str(txt):
                        temp=str(txt).split('Universidad')
                        if len(temp)>1:
                            temp=str(temp[1]).split(',')
                            temp=str(temp[0])
                            coll='Universidad'+temp
                            print(coll)
                        for p in ps:
                            temp=p.text
                            if 'profesor titular' in str(temp).lower() or 'profesora titular' in str(temp).lower() or 'profesores titular' in str(temp).lower():
                                temp=str(str(temp).lower()).split('profesor')
                                prof=str(temp[0]).replace(',','')
                                print(prof)
                                ind=ps.index(p)
                                try:
                                    nxtp=ps[ind+1]
                                except:
                                    nxtp=ps[ind]
                                nextp=nxtp.text
                                if 'área' in nextp:
                                    nt=str(nextp).split('área')
                                    if ' "' in str(nt[1]):
                                        nt=str(nt[1]).split(' "')
                                        if '"' in str(nt[1]):
                                            nt=str(nt[1]).split('"')
                                            area=str(nt[0]).replace(',','')
                                        else:
                                            area=str(nt[1]).replace(',','')
                                    else:
                                        ind2=ps.index(nxtp)
                                        nextp2=ps[ind2+1]
                                        nextp2=nextp2.text
                                        if ' "' in str(nextp2):
                                            nt2=str(nextp2).split(' "')
                                            if '"' in str(nt2[1]):
                                                nt2=str(nt2[1]).split('"')
                                                area=str(nt2[0]).replace(',','')
                                            else:
                                                area=str(nt2[1]).replace(',','')
                                        elif '"' in str(nextp2):
                                            nt2=str(nextp2).split('"')
                                            area=str(nt2[1]).replace(',','')
                                        else:
                                            area='N/A'
                                else:
                                    area='N/A'
                                
                                area=str(area).replace('"','')
                                print(area)
                                if coll!='N/A' and prof!='N/A':
                                    write(fecha,coll,prof,'titular de Universidad',area)
                    
                    driver.execute_script('window.close()')
                    driver.switch_to_window(driver.window_handles[0])
driver.close()