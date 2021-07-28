import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import argparse
import json
import Car_and_Seller
import Cars_DBM


def start_parser():
    """
    Starts parser to get inputs from user
    :return: arguments provided by user
    """
    body_choices = ['any', 'cargo_van', 'coupe', 'convertible', 'hatchback', 'minivan', 'passenger_van', 'pickup_truck',
                    'suv', 'sedan', 'wagon']
    radius_choices = ['10', '20', '30', '40', '50', '75', '100', '150', '200', '250', '500', 'any']
    condition_choices = ['all', 'new', 'new_cpo', 'used', 'cpo']  # TODO: Describe cpo = certified

    parser = argparse.ArgumentParser(description='Retrieves data from cars.com')

    parser.add_argument('--body', help='Add body type to search', choices=body_choices, default='any')
    parser.add_argument('--cond', help='Add condition to search', choices=condition_choices, default='all')
    parser.add_argument('--radius', help='Add radius to search', choices=radius_choices, default=None)
    parser.add_argument('--price_min', type=int, help='Add min price (in thousands of USD) to search (1 to 2500)',
                        choices=range(0, 2501), default=None, metavar='[1-2500]')
    parser.add_argument('--price_max', type=int, help='Add max price (in thousands of USD) to search (1 to 2500)',
                        choices=range(0, 2501), default=None, metavar='[1-2500]')
    parser.add_argument('--year_min', type=int, help='Add min year of car to search (1900 to 2022)',
                        choices=range(1900, 2023), default=None, metavar='[1900-2022]')
    parser.add_argument('--year_max', type=int, help='Add max year of car to search (1900 to 2022)',
                        choices=range(1900, 2023), default=None, metavar='[1900-2022]')
    parser.add_argument('--ads_max', type=int, help='Add max number of ads to scrape')

    args = parser.parse_args()

    if args.price_min is not None and args.price_max is not None and args.price_min > args.price_max:
        parser.error('max price must be higher or equal to min price.')

    if args.year_min is not None and args.year_max is not None and args.year_min > args.year_max:
        parser.error('max year must be higher or equal to min year.')

    if args.ads_max is not None and args.ads_max < 1:
        parser.error('ads_max must be a positive integer greater than zero.')

    return args


def get_url():
    """
    Constructs the cars.com URL based on user input and the max number of ads to look through
    :return: string with url and in with number of ads
    """
    args = start_parser()

    body = '' if args.body == 'any' else f'body_style_slugs[]={args.body}'
    condition = '' if args.cond == 'all' else args.cond
    radius = 'all' if args.radius == 'any' else args.radius
    min_price = '' if args.price_min is None else str(args.price_min * 1000)
    max_price = '' if args.price_max is None else str(args.price_max * 1000)
    min_year = args.year_min
    max_year = args.year_max

    url = f'https://www.cars.com/shopping/results/?{body}&dealer_id=&list_price_max={max_price}&' \
          f'list_price_min={min_price}&makes[]=&maximum_distance={radius}&mileage_max=&page_size=20&' \
          f'sort=best_match_desc&stock_type={condition}&year_max={max_year}&year_min={min_year}&zip=10001'

    return url, args.ads_max


def go_to_ads(car_driver):
    """
    goes to the first ad in the cars.com search page
    :param car_driver: selenium driver
    :return: None
    """
    first_ad = car_driver.find_element_by_class_name("vehicle-card-link")
    ActionChains(car_driver).click(first_ad).perform()


def next_add(car_driver, ads_left):
    """
    Goes to the cars.com search's next ad and checks if ad limit was reached
    :param car_driver: selenium driver
    :param ads_left: int with number of ads left
    :return: Return True if program should keep going trough ads or False otherwise
    """

    if ads_left == 0:
        return False

    car_driver.implicitly_wait(50)
    next_page_link = car_driver.find_element_by_class_name("srp-carousel-next-link")

    last_page_check = next_page_link.get_attribute('href')[-1]
    if last_page_check == '#':
        return False

    ActionChains(car_driver).click(next_page_link).perform()

    return True


def next_page(car_driver, ads_left, previous_url):
    """
    Goes to the cars.com search's next search page and checks if ad limit was reached
    :param car_driver: selenium driver
    :param ads_left: int with number of ads left
    :param previous_url: url of the previous page
    :return: Return True if program should keep going trough ads or False otherwise
    """
    if ads_left == 0:
        return False

    try:
        current_page = int(re.search(r'page=(\d*)&', url).group(1))
    except ValueError:
        page_index = previous_url.index('/results/?') + len('/results/?')
        new_url = previous_url[:page_index] + 'page=2&' + previous_url[page_index:]
    else:
        new_page = page + 1
        new_url = re.sub(r'page=(\d*)&', f'page={new_page}&', url_target)

    driver.get(new_url)
    car_driver.implicitly_wait(50)

    go_to_ads(driver)
    car_driver.implicitly_wait(50)

    return True


def get_soup(car_driver):
    """
    Downloads html data from website
    :param car_driver: selenium driver
    :return: beautiful soup with html
    """

    html = car_driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    return soup


def get_general_info(soup):
    """
    Gets general information about the car: make, model, trim, year, price, exterior color, interior color, drivetrain,
    fuel type and mileage
    :param soup: html data from ad
    :return: dictionary with features
    """
    filter_keys = ['make', 'model', 'trim', 'year', 'price', 'exterior_color', 'interior_color', 'drivetrain',
                   'fuel_type', 'mileage']
    try:
        basics = soup.findAll('script')
        basics_regex = re.search('"initialActivity"] = (.*})', str(basics)).group(1)
        basics_dict = json.loads(basics_regex)
    except AttributeError:
        print('Could not fetch general information')
        filtered_dict = dict((key, 'NA') for key in filter_keys)
    else:
        if 'trim' not in basics_dict.keys():
            basics_dict['trim'] = 'NA'
        filtered_dict = {key: basics_dict[key] for key in filter_keys}

    return filtered_dict


def get_number_of_features(soup):
    """
    Gets the total number of feature the car has
    :param soup: html data from ad
    :return: int
    """
    feature_list = []
    all_features = soup.findAll('div', class_="all-features-item")
    for feature in all_features:
        feature_list.append(feature.text)

    n_features = len(all_features)

    return n_features


def get_other_info(soup):
    """
    Gets other information about the car: transmission, engine and miles per gallon range
    :param soup: html data from ad
    :return: dictionary with features
    """
    other_info_dict = {}

    other_info = soup.find('dl', class_="fancy-description-list")

    try:
        other_info_dict['transmission'] = re.search(r'Transmission.*\s*<dd>*(.*)<\/', str(other_info)).group(1)
    except AttributeError:
        print('Could not fetch transmission information')
        other_info_dict['transmission'] = 'NA'

    try:
        other_info_dict['engine'] = re.search(r'Engine.*\s*<dd>*(.*)<\/', str(other_info)).group(1)
    except AttributeError:
        print('Could not fetch engine information')
        other_info_dict['engine'] = 'NA'

    try:
        mpg = other_info.find('span', class_="sds-tooltip").find('span').text.split('–')
    except AttributeError:
        print('Could not fetch mpg information')
        other_info_dict['mpg_min'] = 'NA'
        other_info_dict['mpg_max'] = 'NA'
    else:
        other_info_dict['mpg_min'] = mpg[0]
        other_info_dict['mpg_max'] = mpg[1]

    return other_info_dict


def get_car_reviews(soup):
    """
    Gets user car review data
    :param soup: html data from ad
    :return: dictionary with review data
    """
    car_ratings = dict()
    rating_soup = soup.find('section', class_="sds-page-section vehicle-reviews")
    try:
        car_ratings['rating'] = re.search(r'<span class="sds-rating__count">(.*)<', str(rating_soup)).group(1)
    except AttributeError:
        print('Car has no ratings')
        car_ratings['rating'] = 'NA'
        car_ratings['recommended'] = 'NA'
        car_ratings['n_reviews'] = 'NA'
        car_ratings['Comfort'] = 'NA'
        car_ratings['Interior design'] = 'NA'
        car_ratings['Performance'] = 'NA'
        car_ratings['Value for the money'] = 'NA'
        car_ratings['Exterior styling'] = 'NA'
        car_ratings['Reliability'] = 'NA'
    else:
        car_ratings['recommended'] = re.search(r'^(\d*%)', soup.find('div', class_="reviews-recommended").text).group(1)

        rating_breakdown = soup.find('ul', class_="sds-definition-list review-breakdown--list").findAll('li')
        for rating in rating_breakdown:
            car_ratings[rating.find('span', class_="sds-definition-list__display-name").text] = rating.find('span',
                                                                                                            class_="sds-definition-list__value").text
        review_soup = soup.findAll('a', class_="sds-rating__link sds-button-link")
        for review in review_soup:
            if re.search("page-over-page", str(review)):
                car_ratings['n_reviews'] = re.search(r'\((\d*).*r', review.text).group(1)

    return car_ratings


def get_seller_info(soup):
    """
    Gets seller information from ad
    :param soup: html data from ad
    :return: dictionary with seller info
    """

    seller = dict()
    seller['name'] = soup.find('h3', class_="sds-heading--5 heading seller-name").text
    seller['address'] = soup.find('div', class_="dealer-address").text

    rating_soup = soup.find('section', class_="sds-page-section seller-info")
    try:
        seller['rating'] = re.search(r'<span class="sds-rating__count">(.*)<', str(rating_soup)).group(1)
    except AttributeError:
        print('Seller has no reviews')
    else:
        review_soup = soup.findAll('a', class_="sds-rating__link sds-button-link")
        for review in review_soup:
            if re.search("click-vdp-to-dpp-reviews", str(review)):
                seller['n_reviews'] = re.search(r'\((\d*).*r', review.text).group(1)

    return seller


def write_to_db(my_dbm, my_car, my_seller):
    """function that receives a Cars_DBM object and writes with it to the database the information of an add"""
    my_dbm.insert_seller_row(my_seller)
    my_dbm.insert_car_type_row(my_car)
    my_dbm.insert_car_row(my_car, my_seller)


def main():
    """ function that runs the program"""
    # car_dbm = Cars_DBM.Cars_DBM()

    start_parser()
    url, max_ads = get_url()

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(50)

    go_to_ads(driver)
    driver.implicitly_wait(50)

    keep_looping = True
    cars_looped = 0
    while keep_looping:
        car_soup = get_soup(driver)
        general_info = get_general_info(car_soup)
        other_info = get_other_info(car_soup)
        seller_info = get_seller_info(car_soup)
        number_of_features = get_number_of_features(car_soup)
        car_reviews = get_car_reviews(car_soup)
        my_car = Car_and_Seller.Car(general_info, other_info)
        my_seller = Car_and_Seller.Seller(seller_info)

        # TODO: delete or change to logging
        print(general_info)
        print(other_info)
        print(car_reviews)
        print(seller_info)
        print(number_of_features)

        if max_ads is not None:
            max_ads -= 1
        cars_looped += 1
        print(cars_looped)
        if cars_looped == 20:
            new_url = next_page(driver, max_ads, url)
        else:
            keep_looping = next_add(driver, max_ads)

    print('The end')
    driver.close()


if __name__ == '__main__':
    main()
