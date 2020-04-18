import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def setup():
    try:
        companies = pd.read_csv('Companies.csv')
    except pd.io.common.EmptyDataError:
        print("Companies.csv is empty")

    uniques = companies.iloc[:, 1].to_list()
    with open("cfgs/search_words.txt") as f:
        content = f.readlines()
    keywords = [x.strip() for x in content]
    with open("cfgs/permutators.txt") as f:
        content = f.readlines()
    permutations = [x.strip() for x in content]
    permutation = 2 ** len(permutations) - 1

    return companies, keywords, permutation, permutations, uniques


def main():
    target_url = 'https://angel.co/companies'
    companies, keywords, n_permutations, permutations, uniques = setup()

    for keyword in keywords:
        for permutation in range(1, n_permutations):
            driver = webdriver.Firefox(executable_path='geckodriver')
            driver.maximize_window()
            driver.get(target_url)
            time.sleep(10)
            driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='search-box']")[0].click()
            driver.find_elements_by_xpath(
                "//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[0].send_keys(
                keyword)
            driver.find_elements_by_xpath(
                "//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[0].send_keys(
                Keys.ENTER)

            for j in range(len(permutations)):
                if (1 << j) & permutation:
                    driver.find_elements_by_xpath(
                        "//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[
                        0].send_keys(permutations[j])
                    driver.find_elements_by_xpath(
                        "//*[@class='main_container']//*[@class='search-box']//*[@class='input keyword-input']")[
                        0].send_keys(Keys.ENTER)
                    time.sleep(10)
            more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
            print(len(more))
            if len(more) == 0:
                driver.quit()
                continue
            for i in range(20):
                more[0].click()
                print(f'Loading more data... ({i}/20)')
                time.sleep(3)
                more = driver.find_elements_by_xpath("//*[@class='main_container']//*[@class='more']")
                if len(more) == 0:
                    break

            results = driver.find_elements_by_xpath(
                "//*[@class='main_container']//*[@class='base startup']//*[@class='company column']//*[@class='g-lockup']//*[@class='text']//*[@class='name']//*[@class='startup-link']")
            results_location = driver.find_elements_by_xpath(
                "//*[@class='main_container']//*[@class='base startup']//*[@class='column location']//*[@class='value']")
            results_websites = driver.find_elements_by_xpath(
                "//*[@class='main_container']//*[@class='base startup']//*[@class='column website']//*[@class='value']")
            results_employees = driver.find_elements_by_xpath(
                "//*[@class='main_container']//*[@class='base startup']//*[@class='column company_size']//*[@class='value']")

            for i in range(len(results)):
                company_name = results[i].text
                location = results_location[i].text
                angel_link = results[i].get_attribute("href")
                website = results_websites[i].text
                employees = results_employees[i].text
                if company_name not in uniques:
                    companies.append({
                        "Company name": company_name,
                        "Angel link": angel_link,
                        "Location": location,
                        "Website": website,
                        "Number of employees": employees}, ignore_index=True)
                    uniques.append(company_name)
            driver.quit()
            print('Number of companies extracted:' + str(len(uniques)))
            print(companies)

            companies.to_csv('Companies.csv')


if __name__ == '__main__':
    main()
