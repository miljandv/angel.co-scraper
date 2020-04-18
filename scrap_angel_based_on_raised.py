import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
urlpage = 'https://angel.co/companies'
normal_form_raised = 'https://angel.co/companies?raised[min]=low&raised[max]=high'

read = pd.read_csv('Companies.csv')
uniques = read.iloc[:,1].astype(str).values.tolist()

with open("cfgs/search_words.txt") as f:
    content = f.readlines()
keywords = [x.strip() for x in content]

with open("cfgs/raised.txt") as f:
    content = f.readlines()
raised = [x.strip() for x in content]
raised_normalized = []
for i in range(len(raised)):
    for j in range(i+1,len(raised)):
        raised_normalized.append(normal_form_raised.replace('low',raised[i]).replace('high',raised[j]))
        break
data = []    
for keyword in keywords: 
    for curr_raise in raised_normalized:      
        driver = webdriver.Firefox(executable_path = 'geckodriver')
        driver.get(curr_raise)
        time.sleep(10)
        driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']")[0].click()
        driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[0].send_keys(keyword)
        driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[0].send_keys(Keys.ENTER)
        time.sleep(10)
        more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
        print(len(more))
        if len(more)!=0:
            for i in range(20):  
                more[0].click()
                print('Loading more data... (',i,'/20)')
                time.sleep(3)
                more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
                if len(more)==0:
                    break
        
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
            if not company_name in uniques:
                data.append({"Company name" : company_name, "Angel link" : angel_link, "Location" : location, "Website" : website, "Number of employees" : employees})#, "Raised" : raised
                uniques.append(company_name)
        driver.quit()
        print('Number of companies extracted:' + str(len(uniques)))
        df = pd.DataFrame(data)
        print(data)
        df.to_csv('Companies.csv',header=False)
             
df = pd.DataFrame(data)
print(df)




df.to_csv('Companies.csv', header=False)





