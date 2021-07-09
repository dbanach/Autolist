class Car:

    def __init__(self, sale_price,make, year, model, transmission, engine, fuel_type, ext_color, condition, mileage,
                 mile_per_liter, body_style):
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
        return (self.get_saleprice(),self.get_make(),self.get_year(),self.get_model(), self.get_transmission(),
                self.get_engine(), self.get_fueltype(), self.get_color(), self.get_condition(), self.get_mileage()
                , self.get_mileperliter(), self.get_bodystyle())


    def get_bodystyle(self):
        return self.body_style

    def get_mileperliter(self):
        return self.mile_per_liter

    def get_mileage(self):
        return self.mileage

    def get_condition(self):
        return self.condition

    def get_color(self):
        return self.color

    def get_fueltype(self):
        return self.fuel_type


    def get_engine(self):
        self.engine


    def get_transmission(self):
        return self.transmission

    def get_model(self):
        return self.model

    def get_saleprice(self):
        return self.sale_price

    def get_make(self):
        return self.make

    def get_year(self):
        return self.year




    def how_old(self):

        pass



class Seller:

    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address
        self.cars = []

    def get_cars(self):
        return self.cars

    def add_car(self,new_car):
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



