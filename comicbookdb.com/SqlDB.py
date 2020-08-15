from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import sqlalchemy as sql

class MysqlDb:
    def init_db_engine(self):
        engine = sql.create_engine('mysql://root@localhost/comics?charset=utf8&use_unicode=0', pool_recycle=3600)
        con = engine.connect()
        return con

    def init_driver(self):
        options=webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-extensions")
        #options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path='/home/smash/Desktop/amazon/chromedriver',chrome_options=options)
        driver.wait = WebDriverWait(driver, 0)
        return driver
