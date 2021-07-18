class Car:
    """
    class that simulates a car object with the relevant information that's useful that we get from autolist

    """

    def __init__(self, general_dict, other_dict):
        """
        Constructor of the class.

        """
        self.car_dict = {}
        for key, item in general_dict.items():
            self.car_dict[key] = item

        for key, item in other_dict.items():
            self.car_dict[key] = item

    def getall(self):
        """
        method that returns all the parameters as a tuple
        :return:
        """

        return (self.get_saleprice(), self.get_make(), self.get_model(), self.get_year(), self.get_trim(),
                self.get_transmission(), self.get_drivetrain(), self.get_mileage(),
                self.get_engine(), self.get_fueltype(), self.get_int_color(), self.get_ext_color(),
                self.get_mile_per_galon_min(), self.get_mile_per_galon_max())

    def get_mile_per_galon_min(self):
        """
        returns the mile_per_galon min (in city) parameter
        :return:
        """
        return self.car_dict['mile_per_galon_min']

    def get_mile_per_galon_max(self):
        """
        returns the mile_per_galon max (in highway) parameter
        :return:
        """
        return self.car_dict['mile_per_galon_max']

    def get_mileage(self):
        """
        returns the mileage parameter
        :return:
        """
        return self.car_dict['mileage']

    def get_ext_color(self):
        """
        returns exterior color parameter
        :return:
        """
        return self.car_dict['ext_color']

    def get_int_color(self):
        """
        returns interior color parameter
        :return:
        """
        return self.car_dict['int_color']

    def get_fueltype(self):
        """
        returns fueltype parameter
        :return:
        """
        return self.car_dict['fuel_type']

    def get_engine(self):
        """
        return engine parameter
        :return:
        """

        return self.car_dict['engine']

    def get_transmission(self):
        """
        returns transmission parameter
        :return:
        """

        return self.car_dict['transmission']

    def get_model(self):
        """
        returns model parameter
        :return:
        """
        return self.car_dict['model']

    def get_saleprice(self):
        """
        returns salesprice parameter
        :return:
        """
        return self.car_dict['sale_price']

    def get_make(self):
        """
        returns make parameter
        :return:
        """
        return self.car_dict['make']

    def get_year(self):
        """
        returns year_of_assembly parameter
        :return:
        """
        return self.car_dict['year']

    def get_drivetrain(self):
        """
        get the parameter drivetrain
        :return:
        """
        return self.car_dict['drivetrain']

    def get_trim(self):
        """
        returns trim parameter (details of specific version of model)
        :return:
        """
        return self.car_dict['trim']

    def get_car_dict(self):
        return self.car_dict

class Seller:
    """
    class that simulates a Car seller with the relevant information

    """

    def __init__(self, seller_dict):
        """
        constructor of the class
        :param name:
        :param phone:
        :param address:
        """
        self.seller_dict = {}
        self.cars = []
        for key, item in seller_dict.items():
            self.seller_dict[key] = item

    def get_cars(self):
        """
        gets the cars that the seller has for sale
        :return:
        """

        return self.cars

    def add_car(self, new_car):
        """
        adds a car to the list of cars of a seller
        :param new_car:
        :return:
        """

        self.cars.append(new_car)

    def popcar(self, my_car):
        """Simulates a sale. eliminates a car from the list of cars of a particular seller. """

        for i, car in enumerate(self.cars):
            if car == my_car:
                self.cars.pop(i)

    def getname(self):
        """ gets the name of a seller"""

        return self.seller_dict['name']

    def getrating(self):
        """
        gets the rating of the seller
        :return:
        """

        return self.seller_dict['rating']

    def getadress(self):
        """ gets the adress of a seller"""

        return self.seller_dict['address']

    def getall(self):
        """
        gets all of the parameters of the seller

        :return:
        """
        return (self.getname(), self.getadress(), self.getrating())
