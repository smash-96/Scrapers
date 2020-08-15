from web_scrapping import *
from floppy3 import FloppyData
from cf import CollectedFloppy
from SqlDB import MysqlDb
def run_queries(con):
    try:
        con.execute('INSERT INTO tbl_SocialNetworks(Name_Social_Network) VALUES("facebook")')
        con.execute('INSERT INTO tbl_SocialNetworks(Name_Social_Network) VALUES("twitter")')
        con.execute('INSERT INTO tbl_SocialNetworks(Name_Social_Network) VALUES("blog")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Writer(s)")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Penciller(s)")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Inker(s)")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Colorist(s)")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Letterer(s)")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Editor(s)")')
        con.execute('INSERT INTO tbl_Job(Name_of_Job) VALUES("Cover Artist(s)")')
        con.execute('INSERT INTO tbl_Country(Name_Country) VALUES("United States")')
        con.execute('INSERT INTO tbl_Language(Name_Language) VALUES("English")')
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":

    print("Press::\n\t1. To iniialize Base Tables\n\t2. Scrap Everything")
    url = "http://comicbookdb.com/browse.php?search=Publisher&letter=A"
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

        floppyData = FloppyData()
        floppyData.scrap_floppy_data(url, con, driver)

        driver.close()


