import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import car_ad_data

URL = 'https://www.autolist.com/listings#page=1&latitude=40.7127753&location=New+York%2C+NY&longitude=-74.0059728&body_style%5B%5D=convertible'


def get_all_car_links_in_page(driver):
    """
    returns a list of all the links to the specifics adds showed in one page of Autolist
    :return: list of individual car ads
    """
    return driver.find_elements_by_class_name(name='vehicle-item-view')


def loops_through_ads(driver):
    """
    function that receives a driver and loops through a list of webpages containing car ads
    :param driver: selenium web driver
    :return: None
    """
    # wait for page to fully load
    driver.implicitly_wait(5)

    # loop through ads and use functions from car_ad_data.py to get car info from ads
    for one_ad in get_all_car_links_in_page(driver):
        this_ad = one_ad.find_element_by_tag_name(name='a')
        href = this_ad.get_attribute("href")
        soup = car_ad_data.get_data(href)
        car_ad_data.get_car_info(soup)
    print('one loop')


def next_page(driver, page_increase):
    """
    function that loads the next ad listing page and checks if there is content
    :param driver: selenium web driver
    :param page_increase: int, pages to add to URL
    :return: True if page exists, False if it doesn't
    """
    # generate new url
    new_page = int(re.search(r'page=(\w*)', URL).group(1)) + page_increase
    new_URL = re.sub(r'page=(\w*)', 'page=' + str(new_page), URL)

    driver.get(new_URL)

    # check if page has content
    try:
        no_results = driver.find_element_by_xpath("//h3[text()='No Results Found']")
    except NoSuchElementException:
        return True
    else:
        return False


def main():
    """ function that runs the program"""
    global driver
    driver = webdriver.Chrome()
    driver.get(URL)

    loops = 1
    while True:

        loops_through_ads(driver)

        val = next_page(driver, loops)

        if not val:
            driver.close()
            break

        loops += 1


if __name__ == '__main__':
    main()
