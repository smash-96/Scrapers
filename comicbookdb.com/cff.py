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

file1 = 'cfu.txt'
file2 = 'fu.txt'  
lines1=[]
lines2=[]

with open(file1) as fp1:  
   line = fp1.readline()
   while line:
       lines1.append(line.strip())
       line = fp1.readline()

with open(file2) as fp2:  
   line = fp2.readline()
   while line:
       lines2.append(line.strip())
       line = fp2.readline()


db = MysqlDb()
con = db.init_db_engine()

i=0
while i<len(lines1):
    clink=str(lines1[i])
    flink=str(lines2[i])
    if clink!='' and clink!=' ':
        try:
            flinkID=con.execute('SELECT Issue_ID FROM db_comics.tbl_Floppy WHERE Comicbookdb_Link="'+flink+'";').fetchone()[0]
            flinkID=unicode(str(flinkID),"utf-8")
            clinkID=con.execute('SELECT Issue_ID FROM db_comics.tbl_Collected WHERE Comicbookdb_Link="'+clink+'";').fetchone()[0]
            clinkID=unicode(str(clinkID),"utf-8")
            print(str(flinkID)+'    '+str(clinkID))
            con.execute('INSERT INTO db_comics.tbl_Collected_Floppy(Floppy_ID,Collected_ID) VALUES('+flinkID+','+clinkID+')')
        except:
            print("Error")
            pass
    i+=1



























