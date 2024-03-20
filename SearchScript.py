import requests
import time
from selenium import webdriver

from fake_useragent import UserAgent
from selenium_stealth import stealth
from bs4 import BeautifulSoup


def process_data(site, code, class_title, class_url, class_price, market, *args, timeout):
    url = f'{site}'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent={UserAgent.random}')
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\dimae\PycharmProjects\SearchProducts\drivers\chromedriver.exe',
    )

    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine"
            )
    url = f'{url}'
    driver.get(url=url)
    time.sleep(timeout)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    titles = soup.find_all(class_=f"{class_title}")
    urls = soup.find_all(class_=f"{class_url}")
    # file = open('page.html', 'w', encoding='utf-8').write(page)
    prices = soup.find_all(class_=f"{class_price}")
    driver.close()
    driver.quit()
    for title, url_product, price in zip(titles, urls, prices):
        if f"{code}" in title.text:
            if title == None or url_product == None or price == None:
                return None
            return {"market": market,
                    "title": title.text.strip(),
                    "url": f"{str(*args)}" + url_product['href'].strip(),
                    "price": price.text.strip()}


process_data('https://www.wildberries.ru/catalog/0/search.aspx?search=55QNED816RA', '55QNED816RA', 'product-card__name',
             'product-card__link j-card-link j-open-full-product-card', 'product-card__price price', 'Wildberries:',
             timeout=2)
process_data('https://www.citilink.ru/search/?text=55QNED816RA', '55QNED816RA', 'app-catalog-9gnskf e1259i3g0',
             'app-catalog-9gnskf e1259i3g0', 'e1j9birj0 e106ikdt0 app-catalog-56qww8 e1gjr6xo0', 'Citilink:',
             'https://www.citilink.ru', timeout=2)
process_data('https://www.mvideo.ru/product-list-page?q=55qned816ra', '55QNED816RA',
             'product-title__text product-title--clamp', 'product-title__text product-title--clamp',
             'price__main-value', 'Mvideo:', 'https://www.mvideo.ru', timeout=2)
process_data('https://www.vseinstrumenti.ru/search/?what=BELMASH%20RG-55', 'RA127A', '-dp5Dd clamp-3 buZF02',
             '-dp5Dd clamp-3 buZF02', 'typography heading v5 -no-margin R34yPj ACNQm3', 'Vseinstrumenti:', timeout=2)

process_data('https://www.pulscen.ru/search/price?q=55QNED816RA', '55QNED816RA',
             'product-listing__product-title',
             'aui-link product-listing__product-name js-bp-title js-bp-title-online-store js-ga-link js-catalogue-ecommerce js-conversion-event',
             'bp-price fsn', 'Pulscen:', timeout=2)
