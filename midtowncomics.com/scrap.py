from mtc import *
from mtc2 import *
from SqlDB import MysqlDb

def run_queries(con):
    try:
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("10.0","GM","Gem Mint")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("9.9","M","Mint")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("9.8","NM/M","Near Mint/Mint")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("9.6","NM+","Near Mint+")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("9.4","NM","Near Mint")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("9.2","NM-","Near Mint-")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("9.0","VF/NM","Very Fine/Near Mint")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("8.5","VF+","Very Fine+")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("8.0","VF","Very Fine")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("7.5","VF-","Very Fine-")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("7.0","FN/VF","Fine/Very Fine")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("6.5","FN+","Fine+")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("6.0","FN","Fine")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("5.5","FN-","Fine-")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("5.0","VG/FN","Very Good/Fine")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("4.5","VG+","Very Good+")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("4.0","VG","Very Good")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("3.5","VG-","Very Good-")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("3.0","GD/VG","Good/Very Good")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("2.5","GD+","Good+")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("2.0","GD","Good")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("1.8","GD-","Good-")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("1.5","FR/GD","Fair/Good")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("1.0","FR","Fair")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade) VALUES("0.5","PR","Poor")')

        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("NM","Near Mint")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("VF","Very Fine")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("FN","Fine")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("VG","Very Good")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("GD","Good")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("FR","Fair")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Grade,Name_Grade) VALUES("PR","Poor")')


    except Exception:
        traceback.print_exc()

if __name__ == "__main__":

    print("Press::\n\t0. Fill Tables\n\t1. Scrap Collected Data\n\t2. Scrap Floppies Data\n")
    url = "https://www.midtowncomics.com/store/search.asp?cat=62&scat=110&os=1&sh=100&reld=1/1/1900&reld2=1/1/1900&furl=cat=62@@scat=110@@pl=76"
    url2="https://www.midtowncomics.com/store/search.asp?cat=142&scat=145&os=1&sh=100&reld=1/1/1900&reld2=1/1/1900&furl=cat=142@@scat=145@@pl=58"
    choice=int(input())
    if choice==0:
        db = MysqlDb()
        driver = db.init_driver()
        con = db.init_db_engine()
        run_queries(con)
        driver.close()
    elif choice==1:
        db = MysqlDb()
        driver = db.init_driver()
        con = db.init_db_engine()
        mt=midTown()
        mt.scrap_mtc_data(url,con,driver)
        driver.close()
    elif choice==2:
        db = MysqlDb()
        driver = db.init_driver()
        con = db.init_db_engine()
        mt=midTown2()
        mt.scrap_mtc_data2(url2,con,driver)
        driver.close()