class Car:
    """
    class that simulates a car object with the relevant information that's useful that we get from autolist

    """
    def __init__(self, sale_price,make, year, model, transmission, engine, fuel_type, ext_color, condition, mileage,
                 mile_per_liter, body_style):
        """
        Constructor of the class.

        """

        self.sale_price = sale_price
        self.make = make
        self.year = year
        self.model = model
        self.transmission = transmission
        self.engine = engine
        self.fuel_type = fuel_type
        self.color = ext_color
        self.condition = condition
        self.mileage = mileage
        self.mile_per_liter = mile_per_liter
        self.body_style = body_style

    def getall(self):
        """
        method that returns all the parameters as a tuple
        :return:
        """

        return (self.get_saleprice(),self.get_make(),self.get_year(),self.get_model(), self.get_transmission(),
                self.get_engine(), self.get_fueltype(), self.get_color(), self.get_condition(), self.get_mileage()
                , self.get_mileperliter(), self.get_bodystyle())


    def get_bodystyle(self):
        """
        returns the bodystyle of the car instance
        :return:
        """

        return self.body_style

    def get_mileperliter(self):
        """
        returns the mile_per_liter parameter
        :return:
        """
        return self.mile_per_liter

    def get_mileage(self):
        """
        returns the mileage parameter
        :return:
        """
        return self.mileage

    def get_condition(self):
        """
        returns condition parameter
        :return:
        """
        return self.condition

    def get_color(self):
        """
        returns color parameter
        :return:
        """
        return self.color

    def get_fueltype(self):
        """
        returns fueltype parameter
        :return:
        """
        return self.fuel_type


    def get_engine(self):
        """
        return engine parameter
        :return:
        """

        self.engine


    def get_transmission(self):
        """
        returns transmission parameter
        :return:
        """

        return self.transmission

    def get_model(self):
        """
        returns model parameter
        :return:
        """
        return self.model

    def get_saleprice(self):
        """
        returns salesprice parameter
        :return:
        """
        return self.sale_price

    def get_make(self):
        """
        returns make parameter
        :return:
        """
        return self.make

    def get_year(self):
        """
        returns year_of_assembly parameter
        :return:
        """
        return self.year






class Seller:
    """
    class that simulates a Car seller with the relevant information

    """
    def __init__(self, name, phone, address):
        """
        constructor of the class
        :param name:
        :param phone:
        :param address:
        """

        self.name = name
        self.phone = phone
        self.address = address
        self.cars = []

    def get_cars(self):
        """
        gets the cars that the seller has for sale
        :return:
        """

        return self.cars

    def add_car(self,new_car):
        """
        
        :param new_car:
        :return:
        """

        self.cars.append(new_car)

    def popcar(self,my_car):
        # think how to make car unique
        for i,car in enumerate(self.cars):
            if car == my_car:
                self.cars.pop(i)

    def getname(self):
        return self.name

    def getphone(self):
        return self.phone

    def getadress(self):
        return self.address

    def getall(self):
        return (self.getname(),self.getphone(),self.getadress())



