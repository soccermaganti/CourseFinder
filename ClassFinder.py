import os
from pydoc import doc
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import selenium
# Selenium => Had to reinstall the virtual enviroment (delete it and remake it)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

i = 1
def checker(url):
   global i
   try:

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # soup = BeautifulSoup(content, "html.parser")

    #https://stackoverflow.com/questions/26704309/python-how-to-scrape-tr-td-table-data-using-requests-beautifulsoup
    texts = soup.find_all('td')
    # print(texts)
    with open('results.txt', 'at', encoding='utf8') as file:
        locationBool = False
        seasonBool = False
        for text in texts:
            text = text.get_text().strip()
            # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
            if text is not None and "Canterbury" in text:
                # file.write(text.get_text("\n", strip=True) + '\n')
                # file.write(url + '\n')
                locationBool = True
            if text is not None and "Autumn Term" in text:
                seasonBool = True
        # print([locationBool, seasonBool])
        if locationBool and seasonBool:
            classTitle = soup.find('h1').get_text()
            file.write("Class name: " + classTitle + ". The URL to this is: " + url + '\n')

    file.close()
    print(f"Website {i} Completed")
    i += 1
   except Exception as e:
        print(f'Error: {e}')
        return
   


def traversal(url):
    # https://scrapfly.io/blog/scraping-using-browsers/
    # The course module website is dynamically loading meaning that I can't scrape the basic HTML as it is empty.
    # Needed a tool that can scrape dynamic pages => Selenium is a great tool for this (Opens a web browser like a regular user would)
    browser = webdriver.Chrome()
    browser.get(url) 

    title = (
        WebDriverWait(driver=browser, timeout=5)
        .until(visibility_of_element_located((By.CSS_SELECTOR, "h2")))
        .text
    )
    # retrieve fully rendered HTML content
    content = browser.page_source
    # browser.close()

    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # }
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.content, 'html.parser')

    soup = BeautifulSoup(content, "html.parser")

    # This finds all elements that are ul in this class
    classList = soup.find('ul', class_='search-filters__listing')
    if classList:
        # This finds all the classes by only retreiving the li elements
        classes = classList.find_all('li')
        # print(list_items)
        print(len(classes))
        for course in classes:
            # getting the href and putting my conditions on it (regex)
            courseLink = course.find('a', href=True)
            if courseLink:
                if re.search(r'\b[A-Z]{4}3[0-9]{3}\b', courseLink['href']):
                    checker(courseLink['href'])

    browser.close()

            


if __name__ == "__main__":
    start = time.time()

    base_url = "https://www.kent.ac.uk/courses/modules"
    traversal(base_url)
    # checker("https://www.kent.ac.uk/courses/modules/module/COMP8740")

    end = time.time()
    print(end-start)
