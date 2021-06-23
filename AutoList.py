from selenium import webdriver
import re
from selenium.common.exceptions import NoSuchElementException
import car_ad_data

URL = 'https://www.autolist.com/listings#page=1&latitude=40.7127753&location=New+York%2C+NY&longitude=-74.0059728&body_style%5B%5D=convertible'


# def get_all_links(driver):
#   links = []
#  elements = driver.find_elements_by_tag_name('a')
# for elem in elements:
#    href = elem.get_attribute("href")
#   links.append(href)
# return links

def get_all_car_links_in_page(driver):
    """
    returns a list of all the links to the specifics adds showed in one page of Autolist
    :return: list of individual car ads
    """
    return driver.find_elements_by_class_name(name='vehicle-item-view')


def loops_through_adds(driver):
    """
    function that receives a driver and loops through a list of webpages
    :param driver: selenium web driver
    :return: None
    """
    driver.implicitly_wait(5)
    for one_add in get_all_car_links_in_page(driver):
        this_add = one_add.find_element_by_tag_name(name='a')
        href = this_add.get_attribute("href")
        soup = car_ad_data.get_data(href)
        car_ad_data.get_car_info(soup)
    print('one loop')


# Here goes code of Ilan taking the info
# might need to adapt and receive something that saves the info


def next_page(driver, page):
    """
    function that checks if there is a next page.
    if there is it clicks on it and returns true, if not does returns false

    """
    new_page = int(re.search(r'page=(\w*)', URL).group(1)) + page
    new_URL = re.sub(r'page=(\w*)', 'page=' + str(new_page), URL)

    driver.get(new_URL)

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

        loops_through_adds(driver)

        val = next_page(driver, loops)

        if not val:
            driver.close()
            break

        loops += 1


if __name__ == '__main__':
    main()
