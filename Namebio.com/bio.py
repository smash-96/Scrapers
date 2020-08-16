# Import the require packages
from selenium import webdriver
import time
import csv

# Initialize the column names list
col = ['Name','Price','Date','Parked_At']

# Write the column name list in the csv file
with open('Domain.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize the browser object
driver = webdriver.Chrome('<Add Path to your chromedriver>', options=chrome_options)

# URL to go to
url = "https://namebio.com/"
# Maximize the browser window
driver.maximize_window()
# Opens the URL in the browser
driver.get(url)

# Counter to traverse through the 10 tables
i = 0

while i < 10:

  #  Get all elements with the table row tag using the xpath method
  trs = driver.find_elements_by_xpath('//*[@id="search-results"]/tbody/tr')

  # Traverse through the rows
  for tr in trs:

    # Split each row to get four values
    tr = str(tr.text).split(' ')
    del tr[2:3]

    # Write the list of values to the csv file
    with open('Domain.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(tr)

    # Close the csv file
    csvFile.close()
  
  # When all rows are read then click the next arrow button to move to next table
  driver.find_element_by_xpath('//*[@id="search-results_next"]/a').click()

  # Give a 2 sec delay for the table to get loaded
  time.sleep(2)

  # Increment the counter
  i+=1

# Close the browser
driver.close()