from selenium import webdriver
from bs4 import BeautifulSoup
import time
import io
import numpy as np
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv
from fake_useragent import UserAgent

#insert the path of the geckodriver in your local machine
geckodriver_path = ""

final_data = pd.read_csv("../data/initial_datasets/Business_Analytics/data/technology_nan",delimiter = '|')
crunchbase_dataset = pd.read_excel('../data/initial_datasets/crunchbase_monthly_export_d43b4klo2ade53.xlsx',sheet_name = 'Companies')
crunchbase_dataset1 = crunchbase_dataset.rename(columns = {'name':'company_name'})

merged = pd.merge(final_data,crunchbase_dataset1, on = 'company_name').loc[:,['company_name','permalink']]

links = merged.loc[:,'permalink']
driver = webdriver.Firefox(executable_path=geckodriver_path)
with io.open('../data/initial_datasets/descriptions_scraped/Descriptions.csv','a',newline='',encoding="utf-8") as csvfile:
    write = csv.writer(csvfile, delimiter = '|')
    for i in range(939,1004):
        new_url = 'https://www.crunchbase.com/{0}'.format(links[i])
        driver.get(new_url)
        time.sleep(np.random.randint(1,3))
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        captcha_code = soup.find("div", class_="page-title")
        if captcha_code != None:
            driver.quit()
            i -= 1
            driver = webdriver.Firefox(executable_path=geckodriver_path)
            continue
        try:
            cerca = driver.find_element_by_xpath("/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/entity/page-layout/div[2]/div/div[2]/div/div[1]/entity-section[1]/section-layout/mat-card/div[2]/description-card/a")
            cerca.click()
        except:
            pass
        description_code = soup.find("div", class_="cb-display-inline")
        if description_code == None:
            continue
        description = description_code.get_text()
        name_code = soup.find("div", class_="component--image-with-text-card")
        name = name_code.find('span',class_="ng-star-inserted").get_text()
        write.writerow([name,description])
        csvfile.flush()
