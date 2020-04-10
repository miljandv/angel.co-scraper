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

#python_button = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
#for i in range(20):
#    python_button.click()


results = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='company column']//*[@class='g-lockup']//*[@class='text']//*[@class='name']//*[@class='startup-link']")
results_location = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column location']//*[@class='value']//*[@class='tag']")


print('Number of results', len(results))




# create empty array to store data
data = []
# loop over results
for i in range(len(results)):    
    company_name = results[i].text
    #angel_link = result.find_element_by_tag_name('a')
    angel_link = results[i].get_attribute("href")
    location = results_location[i].text 
    data.append({"Company name" : company_name, "Angel link" : angel_link, "Location" : location})
    
    
    
driver.quit()
df = pd.DataFrame(data)
print(df)




df.to_csv('C:/Users/milja/OneDrive/Desktop/Companies.csv')