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
time.sleep(15)

more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
print(len(more))
for i in range(20):
    more[0].click()
    time.sleep(5)
#more.click()

#python_button = driver.find_elements_by_xpath("//input[@class='more']") # and @value='Python'
#print(len(python_button))
#for i in range(20):
#    python_button.click()



results = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='company column']//*[@class='g-lockup']//*[@class='text']//*[@class='name']//*[@class='startup-link']")
results_location = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column location']//*[@class='value']")
results_websites = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column website']//*[@class='value']")
results_employees = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column company_size']//*[@class='value']")
#result_raised = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='base startup']//*[@class='column raised hidden_column']//*[@class='value']")


print('Number of results', len(results))
print('Number of results', len(results_location))
print('Number of results', len(results_websites))
print('Number of results', len(results_employees))
#print('Number of results', len(result_raised))




data = []
for i in range(len(results)):    
    company_name = results[i].text
    location = results_location[i]
    angel_link = results[i].get_attribute("href")
    location = location.text
    website = results_websites[i].text
    employees = results_employees[i].text
    #raised = result_raised[i].text
    data.append({"Company name" : company_name, "Angel link" : angel_link, "Location" : location, "Website" : website, "Number of employees" : employees})#, "Raised" : raised
    
    
driver.quit()
df = pd.DataFrame(data)
print(df)




df.to_csv('C:/Users/milja/OneDrive/Desktop/Companies.csv')