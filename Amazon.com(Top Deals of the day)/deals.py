from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
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

def write(ASIN ,Product_Name ,Product_Link ,Product_Image ,Active_price ,Old_price ,Percentage_discount ,Review_count ,Reviews_URL ,Customer_Rating ,Sponsored ,Action_button ,Action_button_link ,fn):

    data = []
    data.append(str(ASIN))
    data.append(str(Product_Name).replace('"', '').replace(',', ''))
    data.append(str(Product_Link))
    data.append(str(Product_Image))
    data.append(str(Active_price))
    data.append(str(Old_price))
    data.append(str(Percentage_discount))
    data.append(str(Review_count))
    data.append(str(Reviews_URL))
    data.append(str(Customer_Rating))
    data.append(str(Sponsored))
    data.append(str(Action_button))
    data.append(str(Action_button_link))

    with open('Output/today_deals_' + fn + '.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
        print(data)
    csvFile.close()

    data_new = []
    data_new.append(str(ASIN))
    data_new.append(str(Product_Name).replace('"', '').replace(',', ''))

    with open('Output/Extra_today_deals_' + fn + '.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data_new)
    csvFile.close()


start = time.time()

current_date = datetime.today().strftime('%Y-%m-%d')

products = 0
err = 0


error = open('Errors_deals.txt','w')
report = open('Report_deals.txt','w')

col = ['ASIN','Product_Name','Product_Link','Product_Image','Active_price','Old_price', 'Percentage_discount','Review_count','Reviews_URL','Customer_Rating', 'Sponsored', 'Action_button', 'Action_button_link']

col_new = ['ASIN', 'Product_Title']

with open('Output/today_deals_' + str(current_date) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

with open('Output/Extra_today_deals_' + str(current_date) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col_new)


options=webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("--disable-extensions")
#options.add_argument("--headless")

driver = webdriver.Chrome(executable_path='<Add Path to your chromedriver>', options=options) # CHANGE PATH
driver.wait = WebDriverWait(driver, 10)

try:
    url = "https://www.amazon.com/gp/goldbox/ref=gbps_ftr_s-5_4e18_dls_UPCM?gb_f_deals1=enforcedCategories:2617941011%252C15684181%252C165796011%252C7147444011%252C3760911%252C283155%252C7147443011%252C502394%252C2335752011%252C541966%252C7586165011%252C172282%252C7141123011%252C1063306%252C7147442011%252C11260432011%252C172541%252C3760901%252C1055398%252C667846011%252C228013%252C16310091%252C284507%252C9479199011%252C2619525011%252C679255011%252C7192394011%252C6358539011%252C1040658%252C7147441011%252C11091801%252C1064954%252C2972638011%252C2619533011%252C328182011%252C3375251%252C165793011%252C679337011%252C6358543011%252C1040660%252C7147440011,dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CUPCOMING,dealTypes:DEAL_OF_THE_DAY%252CBEST_DEAL%252CLIGHTNING_DEAL,minRating:3,sortOrder:BY_SCORE,includedAccessTypes:GIVEAWAY_DEAL&pf_rd_p=4a0dd3f9-e36f-4203-83e5-3cbb64324e18&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=Z90W0A6KYPBEPYFAXECH&ie=UTF8"
    driver.get(url)
    driver.maximize_window()

    time.sleep(10)

    pages_len = len(driver.find_elements_by_xpath('//*[@id="FilterItemView_page_pagination"]/div/span/div[2]/ul/li'))
    lcv1 = int(driver.find_element_by_xpath('//*[@id="FilterItemView_page_pagination"]/div/span/div[2]/ul/li['+str(pages_len-1)+']').text)
    
    for i in range(0, lcv1):
        try:
            asin, lnk, img, price, old_price, discount, reviews, r_url, rating, button_txt, button_lnk = '', '', '', '', '', '', '', '', '', '', ''

            p_names = driver.find_elements_by_xpath('//*[@id="dealTitle"]')
            j = 0
            while check(driver, '//*[@id="101_dealView_'+str(j)+'"]/div') == True:

                try:
                    spons = 'No'

                    divs = driver.find_elements_by_xpath('//*[@id="101_dealView_'+str(j)+'"]/div/div[2]/div/div/div')

                    ab = divs[-1]

                    button_txt = ab.text
                    if 'details' in button_txt or 'Learn' in button_txt:
                        button_lnk = ab.find_element_by_tag_name('a').get_attribute('href')
                    else:
                        button_lnk = ''

                    if 'Amazon Prime' not in divs[-2].text:
                        try:
                            reviews = divs[-2].text
                            r_url = divs[-2].find_element_by_tag_name('a').get_attribute('href')

                            rating = str(divs[-2].find_element_by_tag_name('i').get_attribute('class')).split('a-star-')[1]
                            if len(rating) > 1:
                                rating = str(rating).split('-')[0] + '.' + str(rating).split('-')[1]
                        except:
                            reviews = ''
                            r_url = ''
                            rating = ''

                    else:
                        reviews = ''
                        r_url = ''
                        rating = ''


                    for div in divs:
                        if "Sponsored" in str(div.text):
                            spons = 'Yes'
                        elif '$' in str(div.text):
                            try:
                                price = str(div.text).split('\n')[0]
                            except:
                                price = str(div.text)
                            
                            try:
                                old_price = str(div.text).split('\n')[1].split(' ')[1]
                            except:
                                old_price = ''
                            
                            try:
                                discount = str(div.text).split('\n')[1].split('(')[1][:-1]
                            except:
                                discount = ''    
                            break        
                    

                    lnk = p_names[j].get_attribute('href')

                    if '/dp/' in lnk:
                        asin = str(str(str(lnk).split('dp/')[1]).split('/')[0])
                    else:
                        asin = ''

                    img = driver.find_element_by_xpath('//*[@id="101_dealView_'+str(j)+'"]/div/div[2]/div/a/div/div/div[1]/img').get_attribute('src')
                    
                    ## Write to the file
                    write(asin, p_names[j].text, lnk, img, price, old_price, discount, reviews, r_url, rating, spons, button_txt, button_lnk, str(current_date))
                    products += 1

                except:
                    err += 1
                    pass
                j += 1


            if i == 0:
                driver.find_element_by_xpath('//*[@id="FilterItemView_page_pagination"]/div/span/div[2]/ul/li['+str(pages_len)+']/a').click()
                time.sleep(6)
            else:
                pages_len_up = len(driver.find_elements_by_xpath('//*[@id="FilterItemView_page_pagination"]/div/span/div[1]/ul/li'))
                driver.find_element_by_xpath('//*[@id="FilterItemView_page_pagination"]/div/span/div[1]/ul/li['+str(pages_len_up)+']/a').click()
                time.sleep(6)
        except:
            err += 1
            pass

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
report.write("Total Pages Searched -> " + str(lcv1) + '\n')
report.write("Total Products Fetched -> " + str(products) + '\n')
report.write("Total Errors Handled -> " + str(err) + '\n')