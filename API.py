import requests
import config
import Cars_DBM
import pandas as pd


def api_query(make, model):
    """
    function that receives a make and model of a car and looks in API car data (https://rapidapi.com/principalapis/api/car-data/)
    for the type of car that it is and returns it
    :param make:
    :param model:
    :return:
    """
    querystring = {"limit": "01", "page": "0", "make": make, "model": model}

    headers = {
        'x-rapidapi-key': "655dea5783msh29937912634411cp162c35jsn19fd9b903e44",
        'x-rapidapi-host': "car-data.p.rapidapi.com"
    }

    response = requests.request("GET", config.API_URL, headers=headers, params=querystring)

    new_text = response.text[response.text.index("type"):]
    car_type = new_text[7:new_text.index('}') - 1]
    return car_type


def get_info_to_search(my_cars_dbm):
    """
    function that connects to the database and asks for
    all of the make_model rows in the table car_type and
    returns it as a dataframe instance
    :param my_cars_dbm:
    :return:
    """

    result = my_cars_dbm.get_all_make_model()
    df = pd.DataFrame(result)
    df.columns = ['make', 'model']
    df['type'] = gets_all_types(df)
    return df


def gets_all_types(dataframe):
    """
    function that gets all of the types of car of the cars in the car_type table in the database
    :dataframe: pandas dataframe with make and model columns
    :return: list of types for each respective row fo dataframe
    """
    types_list = []
    for index in range(0, len(dataframe.index)):
        types_list.append(api_query(df['make'].iloc[index], df['model'].iloc[index]))

    return types_list
