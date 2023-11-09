import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.parse import urljoin, urlparse

def get_full_page_text(soup, exclude_selectors):
    for selector in exclude_selectors:
        for element in soup.select(selector):
            element.extract()
    return ' '.join(soup.stripped_strings)

def scrape_page_to_text(url, exclude_selectors=None):
    if exclude_selectors is None:
        exclude_selectors = ['header', 'nav', '.menu', '.navbar', '.header-menu']
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referrer': 'https://www.google.com',
    }
    
    session = requests.Session()
    response = session.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    page_data = {
        'bodyText': get_full_page_text(soup, exclude_selectors)
    }

    return page_data

