# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
# specify the url
urlpage = 'https://angel.co/companies' 
print(urlpage)
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox(executable_path = 'geckodriver')

# get web page
driver.get(urlpage)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(30)
# driver.quit()




#results = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='company column']//*[@class='g-lockup']//*[@class='text']//*[@class='name']//*[@class='startup-link']")


results = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='company column']//*[@class='g-lockup']//*[@class='text']//*[@class='name']")
print('Number of results', len(results))




# create empty array to store data
data = []
# loop over results
for result in results:    
    product_name = result.text
    #angel_link = result.find_element_by_tag_name('a')
    angel_link = result.get_attribute("href")
    data.append({"product" : product_name, "link" : angel_link})
    
    
    
driver.quit()
df = pd.DataFrame(data)
print(df)




df.to_csv('C:/Users/milja/OneDrive/Desktop/Companies.csv')