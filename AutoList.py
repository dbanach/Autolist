from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import car_ad_data
URL = 'https://www.autolist.com/listings#page=1&latitude=32.0668&location=Tel+Aviv%2C+TA&longitude=34.7649&radius=any'


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
    :return:
    """
    return driver.find_elements_by_class_name(name='vehicle-item-view')


def loops_through_adds(driver):
    """
    function that receives a driver and loops through a list of webpages
    :param driver:
    :return:
    """

    for one_add in get_all_car_links_in_page(driver):
        this_add = one_add.find_element_by_tag_name(name='a')
        href = this_add.get_attribute("href")
        soup = car_ad_data.get_data(href)
        car_ad_data.get_car_info(soup)



    print('one loop')


# Here goes code of Ilan taking the info
# might need to adapt and receive something that saves the info


def next_page(driver):
    """
    function that checks if there is a next page.
    if there is it clicks on it and returns true, if not does returns false

    """

    possible_next = driver.find_element_by_id(id_='pagination-region').find_element_by_tag_name(
        name='div').find_element_by_tag_name(name='ul').find_elements_by_tag_name(name='li')[-1]

    if possible_next.text == 'Next':
        webdriver.ActionChains(driver).move_to_element(possible_next).click(possible_next).perform()
        # possible_next.find_element_by_tag_name(name='a').click()
        return True
    else:
        return False


def main():
    """ function that runs the program"""
    global driver
    driver = webdriver.Chrome()
    driver.get(URL)

    int1 = 1
    while True:
        loops_through_adds(driver)

        val = next_page(driver)

        int1+= 1

        if not val:
            break

        if int1 ==5:
            break

if __name__ == '__main__':
    main()
