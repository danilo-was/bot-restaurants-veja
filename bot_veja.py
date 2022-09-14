#%%
import requests
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

veja_data = pd.read_csv('assets\csv\Restaurantes restaurants II - Sheet1.csv')

options = Options()
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(
    options=options, 
    # executable_path=r"assets\chromedriver.exe",
)
veja_critical = []
for link in veja_data['Link veja']:
    # -*- coding: utf-8 -*-
    print(link)
    browser.get(link)
    page_content = browser.page_source
    soup = BeautifulSoup(page_content,'html.parser')
    critical = soup.find('h4').text
    section = soup.find('section')

    if section != None: 
        print(len(section.find_all('p')))
        if len(section.find_all('p')) > 17:
            text = section.find_all('p')[-4].text
        elif len(section.find_all('p')) > 16:
            text = section.find_all('p')[-3].text
        else:
            text = section.find_all('p')[-2].text
    else:
        section = soup.find("div", { "class" : "establishment-content row" })
        text = section.find_all('p')[-2].text

    veja_critical.append([critical,text])

veja_critical_df= pd.DataFrame(veja_critical, columns=['Critico','texto'])
veja_data = pd.concat([veja_data,veja_critical_df],axis=1)
veja_data.to_csv('veja_data.csv')
# %%
