from __future__ import print_function
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time, re, os
from datetime import datetime as dt
import pandas as pd
import concurrent.futures as cf


def run_seleniun_and_get_page_source():
    url = 'https://www.ycombinator.com/companies'
    options = webdriver.ChromeOptions()
    options.headless = True
    try:
        path = os.getenv('CHROMEDRIVER_HOME')
        driver = webdriver.Chrome(executable_path=path, chrome_options=options)
    except Exception as e:
        driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)
    time.sleep(10)

    #scroll to the end of the page
    check_page_length = 0
    try:
        while True:
            page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            time.sleep(0.5)

            if check_page_length == page_len:
                break
            check_page_length = page_len
    except:
        driver.close()

    selenium_web_content = BeautifulSoup(driver.page_source, 'lxml')
    get_company_list_block = selenium_web_content.find_all('a', class_='styles-module__company___1UVnl no-hovercard')
    full_location_block = selenium_web_content.find_all('span', class_='styles-module__coLocation___yhKam')

    url_and_location = []
    for i in range(len(get_company_list_block)):
        location = full_location_block[i].text.strip() 
        company_url = get_company_list_block[i]['href']
        info = [company_url, location]
        url_and_location.append(info)

    lenght = len(full_location_block)

    driver.close()
    return url_and_location, lenght


def get_company_info(soup):
    info = {}

    summary = soup.find('div',  class_='space-y-3')
    info['company_name'] = summary.h1.text
    info['link'] = soup.find('div', class_='flex flex-row items-center leading-none px-3').a['href']
    info['short_description'] = summary.find('div',  class_='text-xl').text

    spans = summary.find_all('span',  class_='ycdc-badge')
    info['tags'] = [what.text.replace('Y Combinator Logo', '') for what in spans]
    info['description'] = soup.p.text
    info['company_socials'] = soup.find('div',  class_='space-x-2')
    
    spans = []

    i = 0
    for fact in soup.find('div', class_="space-y-0.5").find_all('span'):
        spans.append(fact.text)
        try:
            key_ = spans[i].lower().replace(' ', '_')[:-1]
            info[key_] = spans[i+1]
            i += 2
        except:
            pass

    info['company_socials'] = [a['href'] for a in soup.find('div',  class_='space-x-2').find_all('a')]

    return info


def get_founders_info(soup):
    founders_info = {}
    try:
        founders = soup.find('div', class_='space-y-5')
        founders_info['active_founders'] = [name.div.text for name in founders.find_all('div', class_='leading-snug')]

        all_about = []
        for what in founders.find_all('div', class_='flex flex-row gap-3 items-start flex-col md:flex-row'):
            about_founder = {}
            name = what.h3.text
            split = name.split(', ')

            about_founder['name'] = name

            if split[0] != split[-1]:
                about_founder['role'] = split[-1]
            else:
                about_founder['role'] = ''

            about_founder['social_media_links'] = [link['href'] for link in what.find('div', class_='mt-1 space-x-2').find_all('a')]
            
            all_about.append(about_founder)

        founders_info['about_founders'] = all_about
        
    except:
        founders = soup.find('div', class_='space-y-4')
        founders_info = {}
        all_about = []
        for founder in founders.find_all('div', class_='leading-snug'):
            about_founder = {}
            name = founder.find('div', class_='font-bold').text
            founders_info['active_founders'] = [name]

            about_founder['name'] = name

            divs = [ what for what in founder.find_all('div')]
            about_founder['role'] = divs[1].text
            about_founder['social_media_links'] = [link['href'] for link in founder.find('div', class_='mt-1 space-x-2').find_all('a')]

            all_about.append(about_founder)
            
        founders_info['about_founders'] = all_about

    return founders_info


def scrape_info(link_and_location):
    main_url = 'https://www.ycombinator.com'
    url = main_url + link_and_location[0]
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    company_all_info = get_company_info(soup)
    company_all_info['full_location'] = link_and_location[1]
    try:
        founder_info = get_founders_info(soup)
    except:
        founder_info = {
            "active_founders":[],
            "about_founders": []
        }
    company_all_info.update(founder_info)

    return company_all_info


def save_to_csv(scraped_info, savepath):
       df = pd.DataFrame(scraped_info)
       df = df[['company_name', 'link', 'short_description', 'tags',
              'company_socials', 'founded', 'team_size', 'full_location', 'location',
              'active_founders', 'about_founders', 'description']]
              
       df.to_csv(savepath, index=False)



if __name__ == "__main__":
    main_url = 'https://www.ycombinator.com'

    start = dt.now()
    url_and_location, lenght = run_seleniun_and_get_page_source()

    m_companies = []
    with cf.ThreadPoolExecutor() as exc:
        results = exc.map(scrape_info, url_and_location)

        for result in results:
            m_companies.append(result)

    save_to_csv(scraped_info=m_companies, savepath='ycombinator.csv')
    runtime_thread = (dt.now() - start).total_seconds()

    print(f'Total runtime - {runtime_thread}')