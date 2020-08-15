from BD import *
from SqlDB import MysqlDb

def run_queries(con):
    try:
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Writer(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Penciller(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Inker(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Colorist(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Letterer(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Editor(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Cover Artist(s)")')
        con.execute('INSERT INTO db_comicsf.tbl_Job(Name_of_Job) VALUES("Translator(s)")')
        
        con.execute('INSERT INTO db_comicsf.tbl_Country(Name_Country) VALUES("France")')
        con.execute('INSERT INTO db_comicsf.tbl_Language(Name_Language) VALUES(" Français")')
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":

    print("Press::\n\t1. To initialize Base Tables\n\t2. Scrap Data\n")
    url = "https://www.bedetheque.com/bandes_dessinees_M.html"
    choice=int(input())
    if choice==1:
        db = MysqlDb()
        driver = db.init_driver()
        con = db.init_db_engine()
        run_queries(con)
        driver.close()
    elif choice==2:
        db = MysqlDb()
        driver = db.init_driver()
        con = db.init_db_engine()
        bd=BDscrapper()
        bd.scrap_BD_data(url,con,driver)
        driver.close()