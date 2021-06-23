from bs4 import BeautifulSoup
from selenium import webdriver
import re


def get_data(link):
    """
    Downloads html data from website
    :param link: url link
    :return: html data from url as a Beautiful Soup
    """
    browser = webdriver.Chrome()
    browser.get(link)

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    browser.close()

    return soup


def get_car_info(soup):
    """
    Gets information from autolist car ad
    :param soup: Beautiful Soup html data
    :return: None
    """

    # car name / title of the page
    car_info = {}
    # get the make from the android app url
    # from other parts of the html, it is hard to tell the length of the car make, ex: Ford x Alfa Romeo
    # using the android app url there is a clear separation
    make_soup = soup.find('link', href=re.compile(r"^android-app://com.autolist.autolist/autolist/search"))
    make = re.search(r'make=*(\w.*).*&', str(make_soup)).group(1).replace('+', ' ')
    car_info['Make'] = make
    # year and model from the title
    title = soup.find('div', class_='title').text.split(' ')
    car_info['Year'] = title[0]
    model_name_start = make.count(' ') + 2  # how many words / list elements until car name begins
    model = ' '.join(title[model_name_start:])
    car_info['Model'] = model
    print(f'General car info: {car_info}')

    # buyer intelligence section
    buyer_intelligence = soup.find(id="buyer-intelligence-region")
    buyer_int = {}
    buyer_h3 = buyer_intelligence.findAll('h3')
    buyer_int['Similar Listings'] = buyer_h3[0].text
    buyer_int['Days On Market'] = buyer_h3[1].text
    buyer_int['Price Change'] = buyer_h3[2].text
    print(f'Buyer Intelligence: {buyer_int}')

    # price History section (if available)
    if buyer_intelligence.find(string='Full Price History'):
        price_history = {}
        buyer_prices = buyer_intelligence.findAll('div', class_=re.compile("^jsx-3469215501 price-item price-history-"))
        for index in range(0, len(buyer_prices), 3):
            date = buyer_prices[index].text
            price = buyer_prices[index + 1].text
            delta = buyer_prices[index + 2].text
            price_history[date] = [price, delta]
        print(f'Price History: {price_history}')

    # vehicle information section
    vehicle_information = soup.findAll(class_="vehicle-feature")
    features = {}
    for feature in vehicle_information:
        feature_name = feature.find(class_="feature-block feature-label").text
        feature_value = feature.find(class_="feature-block feature-value").text
        features[feature_name] = feature_value
    print(f'Main Features: {features}')

    # Key Features section
    key_features = soup.findAll(class_="clean-list spaced-list")
    other_features = []
    for section in key_features:
        for feature in section.findAll('li'):
            other_features.append(feature.text)
    print(f'Other Features: {other_features}')

    # Seller info section
    seller = soup.findAll(class_="section -large-gtxs _no-margin", id="seller-info")
    address_and_phone = seller[0].findAll('span')
    seller_info = {}
    seller_info['Dealer Name'] = seller[0].find('b', id="dealer-name").text
    seller_info['Address'] = address_and_phone[0].text
    seller_info['Phone'] = address_and_phone[1].text
    print(f'Seller Info: {seller_info}')


if __name__ == "__main__":
    soup = get_data(r'https://www.autolist.com/porsche-cayenne#vin=WP1AA2A25JKA01274')
    get_car_info(soup)
