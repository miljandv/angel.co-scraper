# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
urlpage = 'https://angel.co/companies' 
print(urlpage)
driver = webdriver.Firefox(executable_path = 'geckodriver')

driver.get(urlpage)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(30)

#python_button = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
#for i in range(20):
#    python_button.click()



results = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='company column']//*[@class='g-lockup']//*[@class='text']//*[@class='name']//*[@class='startup-link']")
results_location = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column location']//*[@class='value']")
results_websites = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column website']//*[@class='value']//*[@class='website']")
results_employees = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column company_size hidden_column']//*[@class='value']")

print('Number of results', len(results))
print('Number of results', len(results_location))
print('Number of results', len(results_employees))




# create empty array to store data
data = []
# loop over results
for i in range(len(results)):    
    print(i)
    company_name = results[i].text
    location = results_location[i]
    angel_link = results[i].get_attribute("href")
    location = location.text
    website = results_websites[i].text
    employees = results_employees[i].text
    data.append({"Company name" : company_name, "Angel link" : angel_link, "Location" : location, "Website" : website, "Number of employees" : employees})
    
    
    
driver.quit()
df = pd.DataFrame(data)
print(df)




df.to_csv('C:/Users/milja/OneDrive/Desktop/Companies.csv')