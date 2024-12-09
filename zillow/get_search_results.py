from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import os
import csv

sys.path.append(os.path.join(os.path.abspath(os.curdir), 'lib'))
from urllib.request import urlopen

from fake_useragent import UserAgent

from selenium import webdriver

from zillow import Config
from zillow import Util

# from .Util import *

_url = Config.start_url


def get_webdriver(is_headless=False):
    opts = Util.get_chrome_options(is_headless=is_headless)

    if not is_headless:
        prefs = {"download.default_directory": Config.download_path}
        opts.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=Config.driver_path,
                              chrome_options=opts)

    if is_headless:
        Util.enable_download_in_headless_chrome(driver, Config.download_path)

    return driver


class ZillowSearchOptions(object):
    def __init__(self):
        self.min_rent
        self.max_rent


class Session(object):
    pass


class ZillowSession(Session):
    def __init__(self, is_verbose=True):
        self.listings = []
        self.is_verbose = is_verbose
        self._get_driver()
        # self._setup_search_options()

    def process_all_pages(self):
        # self._get_driver()

        current_page = self.driver.current_url
        print(current_page)

        self._process_page()

        while self.is_have_next_page():
            # self.next_page()
            self._process_page()

    def _get_driver(self):
        self.driver = get_webdriver()
        self.driver.get(Config.start_url)

    def _setup_search_options(self):
        self.driver.find_element_by_xpath('//*[@id="price-exposed-max"]').send_keys('2000')
        self.driver.find_element_by_xpath('//*[@id="listing-type"]').click()

    def _process_page(self):
        if self.is_verbose:
            print('Processing:')
            print(self.driver.current_url)
        page = None
        try:
            self.driver.execute_script("window.scrollTo(0, 10000)")
            page = SearchResultsPage(self.driver)
            results = page.get_results_from_page()

            for result in results:
                self.listings.append(result)

        except Exception as e:
            print('Unable to process page\n{}'.format(e))

        self.driver.implicitly_wait(10)
        try:
            if self.is_have_next_page():
                self.goto_next_page()
        except Exception as e:
            print('Unable to go to next page: {}'.format(e))

    def goto_next_page(self):
        try:
            # self.driver.find_element_by_xpath('//*[@id="mobile-pagination-root"]/div/ol/li[9]').click()
            # buttons = self.driver.find_elements_by_class_name('zsg-pagination')[0].find_elements_by_tag_name('li')
            buttons = self.driver.find_elements_by_class_name('zsg-pagination')[0]
            pagination = buttons.find_elements_by_tag_name('li')
            for b in pagination:
                if b.text.lower() == 'next':

                    b.click()
        except NoSuchElementException:
            pass
        except Exception as e:
            print(e)

    def get_next_button(self):
        try:
            return self.driver.find_element_by_xpath('//*[@id="mobile-pagination-root"]/div/ol/li[8]/a')
        except NoSuchElementException as e:
            pass
        except Exception as e:
            print(e)

    def is_have_next_page(self):
        # BeautifulSoup(self.driver.page_source).find('div', class_='search-pagination').findAll('li')[7].text
        soup = BeautifulSoup(self.driver.page_source)
        pagination = soup.find('div', class_='search-pagination').findAll('li')
        for button in pagination:
            if button.text.strip().lower() == 'next':
                return True

        return False

    def next_page(self):
        try:
            self.get_next_button().click()
        except Exception as e:
            print('Unable to click next button')
            print(e)


class ZillowPage(object):
    pass


class SearchResultsPage(ZillowPage):
    def __init__(self,
                 driver: webdriver):
        self.driver = webdriver
        self.soup = BeautifulSoup(driver.page_source, 'html.parser')

    def get_results_from_page(self):
        zillow_listings = []
        search_results = self.soup.findAll('article', class_='list-card list-card-short list-card_not-saved')
        for result in search_results:
            try:
                beds = result.find('ul', class_='list-card-details').findAll('li')[0].text
                baths = result.find('ul', class_='list-card-details').findAll('li')[1].text
                size = result.find('ul', class_='list-card-details').findAll('li')[2].text
                address = result.find('h3', class_='list-card-addr').text
                url = result.find('a', class_='list-card-link list-card-img').attrs['href']
                company = result.find('div', class_='list-card-type').text

                listing = ZillowListing()
                listing.beds = beds
                listing.baths = baths
                listing.size = size
                listing.address = address
                listing.url = url
                listing.company = company

                # print(listing)
                zillow_listings.append(listing)


            except Exception as e:
                print('Unable to add listing')
                print(', '.join((beds, baths, size, address, url, company)))
                print(e)

        return zillow_listings

    def is_have_next_page(self):
        try:
            elem = self.driver.find_element_by_xpath('//*[@id="mobile-pagination-root"]/div/ol/li[9]')
            return True
        except NoSuchElementException as e:
            return False

    def is_captcha_page(self):
        try:
            elem = self.driver.find_element_by_xpath('/html/body/main/div/div/h5')
            return True
        except NoSuchElementException:
            return False

    # def goto_next_page(self):
    #     try:
    #         # self.driver.find_element_by_xpath('//*[@id="mobile-pagination-root"]/div/ol/li[9]').click()
    #         # buttons = self.driver.find_elements_by_class_name('zsg-pagination')[0].find_elements_by_tag_name('li')
    #         buttons = self.driver.find_elements_by_class_name('zsg-pagination')[0]
    #         pagination = buttons.find_elements_by_tag_name('li')
    #         print(len(pagination))
    #         for b in pagination:
    #             print(b.text)
    #             if b.text.lower() == 'next':
    #
    #                 b.click()
    #     except NoSuchElementException:
    #         pass
    #     except Exception as e:
    #         print(e)


class ZillowListing(object):
    def __init__(self):
        self._beds = None
        self._baths = None
        self._size = None
        self._address = None
        self._url = None
        self._company = None

    @staticmethod
    def return_empty_string(val: str):
        if val == None:
            return ' '
        else:
            return val.strip()

    @property
    def beds(self):
        return ZillowListing.return_empty_string(self._beds)

    @beds.setter
    def beds(self, val):
        self._beds = ZillowListing.return_empty_string(val)

    @property
    def baths(self):
        return ZillowListing.return_empty_string(self._baths)

    @baths.setter
    def baths(self, val):
        self._baths = ZillowListing.return_empty_string(val)

    @property
    def size(self):
        return ZillowListing.return_empty_string(self._size)

    @size.setter
    def size(self, val):
        self._size = ZillowListing.return_empty_string(val)


    @property
    def address(self):
        return ZillowListing.return_empty_string(self._address)

    @address.setter
    def address(self, val):
        self._address = ZillowListing.return_empty_string(val)

    @property
    def url(self):
        return ZillowListing.return_empty_string(self._url)

    @url.setter
    def url(self, val):
        self._url = ZillowListing.return_empty_string(val)

    @property
    def company(self):
        return ZillowListing.return_empty_string(self._company)

    @company.setter
    def company(self, val):
        self._company = ZillowListing.return_empty_string(val)


class ZillowListingsCollection(object):
    def __init__(self,
                 listings: []):
        self.listings = []
        for listing in listings:
            self.listings.append(listing)

    def as_csv(self, output_file: str):
        if not output_file:
            return
        header = ('company', 'beds', 'baths', 'size', 'address', 'url')
        with open(output_file, 'w+') as f:
            # writer = csv.writer(f)
            # writer.writerows(header)
            f.write(','.join(header))
            f.write('\n')


            for listing in self.listings:
                try:
                    row = (
                        listing.company,
                        listing.beds,
                        listing.baths,
                        listing.size,
                        listing.address,
                        listing.url
                    )
                    # strRow = ','.join(row)
                    # print(strRow)
                    # writer.writerows(row)
                    f.write('{}\n'.format(','.join(row)))
                except Exception as e:
                    print('Failed to write row to CSV: \n{}'.format(e))


if __name__ == '__main__':
    # r = requests.get(_url)
    # soup = BeautifulSoup(r.text, 'html.parser')
    #
    # print(soup)

    # driver = get_webdriver()
    # driver.get(Config.start_url)
    #
    # print(driver.name)

    # driver = webdriver.Chrome(executable_path=Config.driver_path)
    # driver = webdriver.Firefox(executable_path=Config.firefox_driver_path)
    # driver.get('http://wwww.google.com')

    # ua = UserAgent()
    # print(ua.chrome)
    # header = {'User-Agent': str(ua.chrome)}
    # r = requests.get(url=Config.start_url, headers=header)
    # page = urlopen(r).read()
    # print(page)
    # soup = BeautifulSoup(page, 'html.parser')
    #
    # print(r.text)

    # driver = webdriver.Chrome(executable_path=Config.driver_path)
    # driver.get(Config.start_url)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)
    #
    # # soup.find('ul', class_='photo-cards photo-cards_wow photo-cards_short').findAll('li')[2].text
    # cards = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('div',class_='list-card-price').text
    #
    # beds = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('ul', class_='list-card-details').findAll('li')[0].text
    # baths = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('ul', class_='list-card-details').findAll('li')[1].text
    # size = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('ul', class_='list-card-details').findAll('li')[2].text
    # address = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('h3', class_='list-card-addr').text
    # url = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('a', class_='list-card-link list-card-img').attrs['href']
    # company = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')[0].find('div', class_='list-card-type').text
    #
    # zillow_listings = []
    # search_results = soup.findAll('article', class_='list-card list-card-short list-card_not-saved')
    # for result in search_results:
    #     try:
    #         beds = result.find('ul', class_='list-card-details').findAll('li')[0].text
    #         baths = result.find('ul', class_='list-card-details').findAll('li')[1].text
    #         size = result.find('ul', class_='list-card-details').findAll('li')[2].text
    #         address = result.find('h3', class_='list-card-addr').text
    #         url = result.find('a', class_='list-card-link list-card-img').attrs['href']
    #         company = result.find('div', class_='list-card-type').text
    #
    #         listing = ZillowListing()
    #         listing.beds = beds
    #         listing.baths = baths
    #         listing.size = size
    #         listing.address = address
    #         listing.url = url
    #         listing.company = company
    #
    #         zillow_listings.append(listing)
    #     except Exception as e:
    #         print(e)
    #
    # driver.find_element_by_xpath('//*[@id="mobile-pagination-root"]/div/ol/li[9]').click()


    # driver = get_webdriver()
    # driver.get(Config.start_url)
    # driver.implicitly_wait(10)
    #
    # # driver.find_element_by_xpath('//*[@id="price"]').click()
    # # driver.find_element_by_xpath('//*[@id="price-exposed-max"]').send_keys('2000')
    # # driver.find_element_by_xpath('//*[@id="search-page-react-content"]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/button').click()
    #
    # driver.find_element_by_xpath('//*[@id="listing-type"]').click()
    #
    # print(driver.name)




    listings = []
    session = ZillowSession(True)
    session.process_all_pages()
    listings = session.listings
    collection = ZillowListingsCollection(listings)
    collection.as_csv(Config.csv_output)

    # caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "normal"  #  complete
    # caps["pageLoadStrategy"] = "eager"  # interactive

    # driver = webdriver.Chrome(executable_path=Config.driver_path)

    # driver.get('C:\\Users\\tomku\\Downloads\\Cheap Apartments For Rent _ Zillow.html')
    # driver.implicitly_wait(3)
    # driver.execute_script("window.stop();")
    #
    # results = SearchResultsPage(driver)
    # listings = results.get_results_from_page()
    # collection = ZillowListingsCollection(listings)
    # collection.as_csv(Config.csv_output)
    # driver.implicitly_wait(100)