from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import datetime
import os
import csv

def check(driver,x):
    try:
        driver.find_element_by_xpath(x)
    except:
        return False
    return True

def write(Asin, Coupon_image, Coupon_discount, Coupon_name, Coupon_link, fn):

    data=[]
    data.append(str(Asin))
    data.append(str(Coupon_image))
    data.append(str(Coupon_discount).replace('"', '').replace(',', ''))
    data.append(str(Coupon_name).replace('"', '').replace(',', ''))
    data.append(str(Coupon_link))

    with open('Output/today_coupons_' + fn + '.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()

start = time.time()

current_date = datetime.today().strftime('%Y-%m-%d')

products = 0
lnk_cnt = 0
err = 0

control_var = 2 # Control how many times the "Show More Coupons" button will be pressed

error = open('Errors_coupon.txt','w')
report = open('Report_coupon.txt','w')

col=['ASIN', 'Coupon_image', 'Coupon_discount', 'Coupon_name', 'Coupon_link']


with open('Output/today_coupons_' + str(current_date) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)


options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='/Users/maisamshah/Desktop/Scraper/chromedriver', options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)

try:
    url = "https://www.amazon.com/Coupons/b/?ie=UTF8&node=2231352011&ref_=sv_subnav_goldbox_1"
    driver.get(url)
    driver.maximize_window()

    time.sleep(10)

    h3 = driver.find_elements_by_xpath('//*[@id="a-page"]/div[3]/div/div[2]/div/div[2]/div[2]/h3')
    ul = driver.find_elements_by_xpath('//*[@id="a-page"]/div[3]/div/div[2]/div/div[2]/div[2]/ul')

    i = 0
    for h in h3:
        if str(h.text) == "Health & Personal Care" or str(h.text) == "Beauty" or str(h.text) == "Other Categories":
            val = str(h.text)
            elems = ul[i].find_elements_by_tag_name('a')
            for elem in elems:
                lnk = elem.get_attribute('href')

                try:
                    newTab = 'window.open("' + lnk + '", "_blank");'
                    driver.execute_script(newTab)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(10)
                    lnk_cnt += 1

                    try:
                        button = driver.find_element_by_class_name('vpc_coupon_grid_get_more_coupons')
                        driver.implicitly_wait(10)

                        for l in range(0, control_var):
                            ActionChains(driver).move_to_element(button).click().perform()
                            time.sleep(8)
                    except TimeoutException:
                        err += 1
                        print("Timeout Exception -> Connectivity Issue \n Run script again!")
                        pass
                    except NoSuchElementException:
                        err += 1
                        pass
                    except:
                        err += 1
                        print("Button does not exist or is not interactable anymore!")
                        pass
                    
                    try:
                        divs = driver.find_element_by_class_name('vpc_coupon_grid_inner_grid').find_elements_by_xpath('div')
                        for div in divs:

                            d = div.find_elements_by_xpath('div/div/div')
                            
                            img = d[0].find_element_by_tag_name('img').get_attribute('src')
                            c_link = d[0].find_element_by_tag_name('a').get_attribute('href')
                            print(c_link)
                            asin = str(str(c_link).split('Asin=')[1].split('&source')[0])
                            discount = d[1].text
                            c_name = d[2].text

                            if len(discount) == 0 and len(c_name) == 0:
                                break

                            if 'Asin=' in str(c_link):
                                write(asin, img, discount, c_name, c_link, str(current_date))
                                products += 1
                    except:
                        err += 1
                        pass
                
                except TimeoutException:
                    err += 1
                    error.write("Page Crashed for the link -> " + str(lnk) + '\n')
                    print("Timeout Exception -> Connectivity Issue")
                    pass
                except NoSuchElementException:
                    err += 1
                    error.write("Page Crashed for the link -> " + str(lnk) + '\n')
                    print("Element Not Found")
                    pass
                except StaleElementReferenceException as e:
                    err += 1
                    error.write("Page Crashed for the link -> " + str(lnk) + '\n')
                    print("Stale Element Exception")
                    pass
                except:
                    err += 1
                    error.write("Page Crashed for the link -> " + str(lnk) + '\n')
                    print("Unknown Exception")
                    pass

                driver.execute_script('window.close()')
                driver.switch_to.window(driver.window_handles[0])

                if val == "Health & Personal Care" or val == "Beauty":
                    break

        i += 1

except TimeoutException:
    err += 1
    print("Timeout Exception -> Connectivity Issue \n Run script again!")
    pass
except NoSuchElementException:
    err += 1
    print("Element Not Found \n Run script again!")
    pass
except StaleElementReferenceException as e:
    err += 1
    print("Stale Element Exception \n Run script again!")
    pass
except:
    err += 1
    print("Unknown Exception \n Run script again!")
    pass

driver.close()

end = time.time()

report.write("Total Time Elapsed (s) -> " + str(end - start) + '\n')
report.write("Total Links Searched -> " + str(lnk_cnt) + '\n')
report.write("Total Products Fetched -> " + str(products) + '\n')
report.write("Total Errors Handled -> " + str(err) + '\n')