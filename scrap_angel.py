import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
urlpage = 'https://angel.co/companies' 


with open(r"D:\WonderlandAI\Angel\search_words.txt") as f:
    content = f.readlines()
keywords = [x.strip() for x in content] 

data = []               
for keyword in keywords: 
    driver = webdriver.Firefox(executable_path = 'geckodriver')
    driver.get(urlpage)
    time.sleep(10)
    driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']")[0].click()
    driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[0].send_keys(keyword)
    driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[0].send_keys(Keys.ENTER)
    time.sleep(10)
    more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
    print(len(more))
    for i in range(20):  
        more[0].click()
        print('Loading more data... (',i,'/20)')
        time.sleep(2)
        more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
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
   
    
    
    for i in range(len(results)):    
        company_name = results[i].text
        location = results_location[i].text
        angel_link = results[i].get_attribute("href")
        website = results_websites[i].text
        employees = results_employees[i].text
        #raised = result_raised[i].text
        data.append({"Company name" : company_name, "Angel link" : angel_link, "Location" : location, "Website" : website, "Number of employees" : employees})#, "Raised" : raised
        
        
    driver.quit()


df = pd.DataFrame(data)
print(df)




df.to_csv('C:/Users/milja/OneDrive/Desktop/Companies.csv')