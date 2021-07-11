import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
import argparse
def start_parser():
    """
    Starts parser to get inputs from user
    :return: arguments provided by user
    """
    body_choices = ['any', 'convertible', 'coupe', 'crossover', 'hatchback', 'minivan', 'sedan', 'suv',
                    'passenger_cargo_van', 'truck', 'wagon']
    category_choices = ['any', 'american', 'classic', 'commuter', 'electric', 'family', 'fuel_efficient', 'hybrid',
                        'large',
                        'luxury', 'muscle', 'off_road', 'small', 'sport', 'supercar']
    radius_choices = ['10', '25', '50', '100', '150', '200', '300', '500', 'any']
    parser = argparse.ArgumentParser(description='Retrieves data from autolist.com')
    parser.add_argument('-b', '--body', help='Add body type to search', choices=body_choices, default='any')
    parser.add_argument('-c', '--cat', help='Add category to search', choices=category_choices, default='any')
    parser.add_argument('-r', '--radius', help='Add radius to search', choices=radius_choices, default='50')
    parser.add_argument('-pmin', '--price_min', type=int,
                        help='Add min price (in thousands of USD) to search (1 to 100)',
                        choices=range(0, 101), default=0, metavar='[1-100]')
    parser.add_argument('-pmax', '--price_max', type=int,
                        help='Add max price (in thousands of USD) to search (1 to 100)',
                        choices=range(0, 101), default=100, metavar='[1-100]')
    parser.add_argument('-ymin', '--year_min', type=int, help='Add min year of car to search (1940 to 2021)',
                        choices=range(1939, 2023), default=1939, metavar='[1940-2021]')
    parser.add_argument('-ymax', '--year_max', type=int, help='Add max year of car to search (1940 to 2021)',
                        choices=range(1940, 2023), default=2022, metavar='[1940-2021]')
    parser.add_argument('-pg', '--page_max', type=int, help='Add max number of pages to scrape')
    parser.add_argument('-a', '--ads_max', type=int, help='Add max number of ads to scrape')
    args = parser.parse_args()
    if args.price_min != 'any' and args.price_max != 'any' and args.price_min > args.price_max:
        parser.error('max price must be higher or equal to min price.')
    if args.year_min != 'any' and args.year_max != 'any' and args.year_min > args.year_max:
        parser.error('max year must be higher or equal to min year.')
    return args
def get_param():
    """
    Constructs the autolist.com URL based on user input
    :return: string
    """
    args = start_parser()
    body = '' if args.body == 'any' else f'body_style[]={args.body}&'
    category = '' if args.cat == 'any' else f'category={args.cat}&'
    radius = args.radius
    min_price = '' if args.price_min == 0 else f'price_min={args.price_min * 1000}&'
    max_price = '' if args.price_max == 100 else f'price_max={args.price_max * 1000}&'
    min_year = '' if args.year_min == 1939 else f'price_min={args.year_min}&'
    max_year = '' if args.year_max == 2022 else f'price_min={args.year_max}&'
    url = f'https://www.autolist.com/listings#{min_price}{max_price}{min_year}{max_year}{body}{category}' \
          f'location=New%20York,%20NY&latitude=40.7123&longitude=-74.0068&radius={radius}&page=1'
    return url, args.page_max, args.ads_max
def get_data(driver):
    """
    Downloads html data from website
    :param driver: selenium chrome driver
    :return: html data from url as a Beautiful Soup
    """
    soup_check = False
    while not soup_check:
        # wait for page to fully load
        driver.implicitly_wait(50)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        with open('new_soup.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        if soup.find(_class='jsx-2369677278 title') is not None:
            soup_check = True
    return soup
def get_car_info(soup):
    """
    Gets information from autolist car ad
    :param soup: Beautiful Soup html data
    :return: None
    """
    get_basic_info(soup)
    get_buyer_intelligence(soup)
    get_general_info(soup)
    get_key_features(soup)
    get_seller_info(soup)
def get_basic_info(soup):
    """
    Gets car make, year and model
    :param soup: html data from ad
    :return:
    """
    # car name / title of the page
    car_info = {}
    # get the make from the android app url
    make_soup = soup.find('link', href=re.compile(r"^android-app://com.autolist.autolist/autolist/search"))
    print(f'make_soup: {make_soup}')
    make = re.search(r'make=*(\w.*).*&', str(make_soup)).group(1).replace('+', ' ')
    car_info['Make'] = make
    # year and model from the title
    title = soup.find('div', class_='title').text.split(' ')
    car_info['Year'] = title[0]
    model_name_start = make.count(' ') + 2  # how many words / list elements until car name begins
    model = ' '.join(title[model_name_start:])
    car_info['Model'] = model
    print(f'General car info: {car_info}')
def get_buyer_intelligence(soup):
    """
    Gets data from buyer intelligence section of ad
    :param soup: html data from ad
    :return:
    """
    buyer_intelligence = soup.find(id="buyer-intelligence-region")
    buyer_int = {}
    buyer_h3 = buyer_intelligence.findAll('h3')
    buyer_int['Similar Listings'] = buyer_h3[0].text
    buyer_int['Days On Market'] = buyer_h3[1].text
    buyer_int['Price Change'] = buyer_h3[2].text
    print(f'Buyer Intelligence: {buyer_int}')
    if buyer_intelligence.find(string='Full Price History'):
        get_price_history(buyer_intelligence)
def get_price_history(buyer_int):
    """
    Gets price history of ad
    :param buyer_int: html data of buyer intelligence section of ad
    :return:
    """
    price_history = {}
    buyer_prices = buyer_int.findAll('div', class_=re.compile("^jsx-3469215501 price-item price-history-"))
    for index in range(0, len(buyer_prices), 3):
        date = buyer_prices[index].text
        price = buyer_prices[index + 1].text
        delta = buyer_prices[index + 2].text
        price_history[date] = [price, delta]
    print(f'Price History: {price_history}')
def get_general_info(soup):
    """
    Gets general vehicle information from ad
    :param soup: html data from ad
    :return:
    """
    vehicle_information = soup.findAll(class_="vehicle-feature")
    features = {}
    for feature in vehicle_information:
        feature_name = feature.find(class_="feature-block feature-label").text
        feature_value = feature.find(class_="feature-block feature-value").text
        features[feature_name] = feature_value
    print(f'Main Features: {features}')
def get_key_features(soup):
    """
    Gets key features information from ad
    :param soup: html data from ad
    :return:
    """
    key_features = soup.findAll(class_="clean-list spaced-list")
    other_features = []
    for section in key_features:
        for feature in section.findAll('li'):
            other_features.append(feature.text)
    print(f'Other Features: {other_features}')
def get_seller_info(soup):
    """
    Gets seller information from ad
    :param soup: html data from ad
    :return:
    """
    seller = soup.findAll(class_="section -large-gtxs _no-margin", id="seller-info")
    address_and_phone = seller[0].findAll('span')
    seller_info = {}
    seller_info['Dealer Name'] = seller[0].find('b', id="dealer-name").text
    seller_info['Address'] = address_and_phone[0].text
    seller_info['Phone'] = address_and_phone[1].text
    print(f'Seller Info: {seller_info}')
def get_all_car_links_in_page(driver):
    """
    returns a list of specifics ads showed in one page of Autolist
    :param driver: selenium chrome driver
    :return: list of individual car ads html data
    """
    page_load_check = False
    while not page_load_check:
        # wait for page to fully load
        driver.implicitly_wait(5)
        # check if page was loaded
        search_results = driver.find_elements_by_class_name('results-view')[0]
        try:
            url_slice = search_results.find_elements_by_tag_name('a')[0].get_attribute('href')[-4:]
        except StaleElementReferenceException:
            continue
        else:
            if url_slice != 'vin=':
                page_load_check = True
    car_ads = []
    for element in search_results.find_elements_by_tag_name('a'):
        car_ads.append(element)
    return car_ads
def loops_through_ads(driver, ads_left):
    """
    Loops through a list of webpages containing car ads and checks if ad limit was reached
    :param driver: selenium chrome driver
    :param ads_left: ad limit left
    :return: limit reach check and ads left to reach limit
    """
    stop = False
    # loop through ads and use functions from car_ad_data.py to get car info from ads
    for ad in get_all_car_links_in_page(driver):
        ad.click()
        driver.implicitly_wait(500)
        soup = get_data(driver)
        get_car_info(soup)
        if ads_left is not None:
            ads_left -= 1
            if ads_left == 0:
                stop = True
                break
        break
    return stop, ads_left
def next_page(driver, page_increase, url, pages_left):
    """
    function that loads the next ad listing page and checks if there is content
    :param driver: selenium chrome driver
    :param page_increase: int, pages to add to URL
    :param url: current url
    :param pages_left: page limit left
    :return: limit reach check and pages left to reach limit
    """
    # generate new url
    new_page = int(re.search(r'page=(\w*)', url).group(1)) + page_increase
    if pages_left is not None:
        if new_page > pages_left:
            return True, pages_left
    new_url = re.sub(r'page=(\w*)', 'page=' + str(new_page), url)
    driver.get(new_url)
    # check if page has content
    try:
        no_results = driver.find_element_by_xpath("//h3[text()='No Results Found']")
    except NoSuchElementException:
        return False
    else:
        return True, pages_left
def main():
    """ function that runs the program"""
    start_parser()
    url, max_pages, max_ads = get_param()
    driver = webdriver.Chrome()
    driver.get(url)
    loops = 1
    while True:
        car_limit_check, max_ads = loops_through_ads(driver, max_ads)
        if car_limit_check:
            break
        page_limit_check, max_pages = next_page(driver, max_pages, url, max_pages)
        if page_limit_check:
            driver.close()
            break
        loops += 1
if __name__ == '__main__':
    main()