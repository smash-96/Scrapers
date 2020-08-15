from bd import *
from mtc import *
from SqlDB_bd import MysqlDb_bd
from SqlDB_mtc import MysqlDb_mtc

def run_queries(con):
    try:
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("10.0","GM","Gem Mint","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("9.9","M","Mint","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("9.8","NM/M","Near Mint/Mint","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("9.6","NM+","Near Mint+","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("9.4","NM","Near Mint","New","Neuf")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("9.2","NM-","Near Mint-","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("9.0","VF/NM","Very Fine/Near Mint","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("8.5","VF+","Very Fine+","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("8.0","VF","Very Fine","Like New","Comme Neuf")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("7.5","VF-","Very Fine-","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("7.0","FN/VF","Fine/Very Fine","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("6.5","FN+","Fine+","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("6.0","FN","Fine","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("5.5","FN-","Fine-","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("5.0","VG/FN","Very Good/Fine","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("4.5","VG+","Very Good+","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("4.0","VG","Very Good","Very Good","Très bon")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("3.5","VG-","Very Good-","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("3.0","GD/VG","Good/Very Good","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("2.5","GD+","Good+","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("2.0","GD","Good","Good","Bon")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("1.8","GD-","Good-","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("1.5","FR/GD","Fair/Good","NULL","NULL")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("1.0","FR","Fair","Acceptable","Acceptable")')
        con.execute('INSERT INTO tbl_CGCGrade(Code_Grade,Name_Short_Grade,Name_Grade,Amazon_US,Amazon_FR) VALUES("0.5","PR","Poor","NULL","NULL")')

        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("NM","Near Mint","New","Neuf")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("VF","Very Fine","Like New","Comme Neuf")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("FN","Fine","Null","Null")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("VG","Very Good","Very Good","Très bon")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("GD","Good","Good","Bon")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("FR","Fair","Acceptable","Acceptable")')
        con.execute('INSERT INTO tbl_Condition(Name_Short_Condition,Name_Condition,NCond_Amazon_US,NCond_Amazon_FR) VALUES("PR","Poor","Null","Null")')

        con.execute('INSERT INTO tbl_Website(ID_Website,Name_Website) VALUES(1,"Midtown Comics")')
        con.execute('INSERT INTO tbl_Website(ID_Website,Name_Website) VALUES(2,"Amazon US")')
        con.execute('INSERT INTO tbl_Website(ID_Website,Name_Website) VALUES(3,"Amazon FR")')
        

    except Exception:
        # print(Exception)
        traceback.print_exc()

if __name__ == "__main__":

    print("Press::\n\t0. Fill Tables\n\t1. Scrap in BD\n\t2. Scrap in MTC\n")
    url = "https://www.amazon.fr/"
    url2 = "https://www.amazon.com"
    choice=int(input())
    if choice==0:
        db = MysqlDb_mtc()
        driver = db.init_driver()
        con = db.init_db_engine()
        run_queries(con)
        driver.close()
    elif choice==1:
        db = MysqlDb_bd()
        driver = db.init_driver()
        con = db.init_db_engine()
        bd=bd()
        bd.fill_bd(url,con,driver)
        driver.close()
    elif choice==2:
        db = MysqlDb_mtc()
        driver = db.init_driver()
        con = db.init_db_engine()
        mt=mtc()
        mt.fill_mtc(url2,con,driver)
        driver.close()