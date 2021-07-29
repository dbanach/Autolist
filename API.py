import requests
import config
import Cars_DBM
import pandas as pd


# might need to check if there's info requested from the api that is not there


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
    if response.text == '':
        return ''

    new_text = response.text[response.text.index("type"):]
    types = new_text[7:new_text.index('}') - 1]
    return types


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
    return df


def gets_all_types(dataframe):
    """
    function that gets all of the types of car of the cars in the car_type table in the database
    :dataframe: pandas dataframe with make and model columns
    :return: list of types for each respective row fo dataframe
    """
    types_list = []
    for index in range(0, len(dataframe.index)):
        types_list.append(api_query(dataframe['make'].iloc[index], dataframe['model'].iloc[index]))

    return types_list


def update_type_in_db(my_cars_dbm):
    """
    function that updates all the information from the Api into the database
    :param my_cars_dbm:
    :return:
    """

    df = get_info_to_search(my_cars_dbm)
    types = gets_all_types(df)

    for index in range(df.shape[0]):
        if types(index)!='':
            make = df.loc[index, 'make']
            model = df.loc[index, 'model']

            my_cars_dbm.update_car_type(make, model, types(index))
