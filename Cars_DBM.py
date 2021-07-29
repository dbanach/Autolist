import pymysql
import config


class Cars_DBM:
    """"
    class to create and manage the database to work with Autolist webpage data.
    DBM= DataBase Manager
    """

    def __init__(self):
        """
        the constructor of the class. It creates the Database if it does not exist and creates the tables.
        """

        sql_code = "CREATE DATABASE IF NOT EXISTS " + config.DATABASENAME
        self.sql_command(sql_code)
        sql_code = "USE " + config.DATABASENAME
        self.sql_command(sql_code)
        self.create_table_sellers()
        self.create_table_cars()
        self.create_table_car_type()

    def sql_command(self, sql_code, _return=0):
        """
        method that executes sql code
        :param sql_code:
        :return:
        """
        cursor, connection = self.connect_to_database()

        try:
            cursorInstance = connection.cursor()
            if 'CREATE DATABASE' not in sql_code:
                cursorInstance.execute('USE CARS')

            cursorInstance.execute(sql_code)
        except Exception as e:
            print(sql_code)
            print("Exeception occured:{}".format(e))
        if _return == 1:
            return cursor.fetchone()
        elif _return== 2:
            return cursor.fetchall()

    def connect_to_database(self):
        """
        method that connects to database
        :return:
        """
        cursor = pymysql.cursors.DictCursor
        connection = pymysql.connect(host=config.DB_IP, user=config.DB_USER, password=config.DB_PASS,
                                     charset=config.CHARSET, cursorclass=cursor)

        return (cursor, connection)

    def use_database(self):
        pass

    def show_db(self):
        """
        shows current databases
        :return:
        """

        sql_code = "SHOW DATABASES"
        self.sql_command(sql_code)

    def create_table_cars(self):
        """ method that creates the table CARS"""

        sql_code = """  CREATE TABLE IF NOT EXISTS CARS (car_id int AUTO_INCREMENT
                        ,car_type_id int NOT NULL
                        ,sold_by int NOT NULL
                        ,sale_price float
                        ,ext_color varchar(30)
                        ,int_color varchar(30)                       
                        ,transmission varchar(30)
                        ,mileage float          
                    ,PRIMARY KEY (car_id)    
                    ,FOREIGN KEY (sold_by) REFERENCES SELLERS(seller_id)
                    ,FOREIGN KEY (car_type_id) REFERENCES CAR_TYPE(car_type_id))"""
        self.sql_command(sql_code)

    def create_table_sellers(self):
        """ method that creates table sellers"""
        sql_code = """ CREATE TABLE IF NOT EXISTS SELLERS(seller_id int AUTO_INCREMENT
         , name varchar(50) ,address varchar(50),rating float,PRIMARY KEY (seller_id))"""
        self.sql_command(sql_code)

    def create_table_car_type(self):
        """ method that creates table car_type"""

        sql_code = """  CREATE TABLE IF NOT EXISTS CAR_TYPE(
                        car_type_id int AUTO_INCREMENT PRIMARY KEY,
                        make varchar(50),
                        model varchar(30),
                        year datetime,
                        miles_per_galon_min float,
                        miles_per_galon_max float,
                        trim varchar(30),
                        drivetrain varchar(30),
                        fuel_type varchar(20),
                        engine varchar(20))                        
                   """
        self.sql_command(sql_code)

    def insert_car_row(self, my_car, my_seller):
        """ method that inserts a row in table cars"""

        sold_by = my_seller.getname()

        my_dict = my_car.get_car_dict()

        sql_code = f"""SELECT car_type_id FROM CAR_TYPE WHERE make= {my_dict['make']} AND 
                        model = {my_dict['model']} AND year = {my_dict['year']} 
                        
                    """
        car_type_id = int(self.sql_command(sql_code, 1)['car_type_id'])

        sql_code = f"""INSERT IGNORE INTO Cars (car_type_id,sold_by, sale_price, ext_color,int_color, transmission, mileage)
         VALUES ({car_type_id},{sold_by},{my_dict['sale_price']},{my_dict['ext_color']},{my_dict['int_color']}
         ,{my_dict['transmission']},{my_dict['mileage']})
        
        
        """
        self.sql_command(sql_code)

    def insert_seller_row(self, my_seller):
        """ method that inserts a row in sellers table"""

        name, address, ratings = my_seller.getall()

        sql_code = f"""INSERT IGNORE INTO Sellers (Name, address,phone)
                        -> VALUES( {name},  {address},{ratings});
        
        
        """
        self.sql_command(sql_code)

    def insert_car_type_row(self, my_car):
        """
        method that inserts new row in car_type table
        """

        my_dict = my_car.get_car_dict()

        sql_code = f"""INSERT IGNORE INTO CAR_TYPE (make,model, year,miles_per_galon_min, miles_per_galon_max
                    ,trim, drivetrain, fuel_type,engine) VALUES ({my_dict['make']},{my_dict['model']},{my_dict['year']}
                    ,{my_dict['miles_per_galon_min']},{my_dict['miles_per_galon_max']},{my_dict['trim']},{my_dict['drivetrain']},
                    {my_dict['fuel_type']},{my_dict['engine']})"""

        self.sql_command(sql_code)

    def drop_database(self):
        """
        method to drop the database
        :return:
        """

        sql_code = f""" DROP DATABASE {config.DATABASENAME} """

    def test_data(self):

        sql_code = "SELECT car_id,mileage FROM CARS"
        data = self.sql_command(sql_code,_return=2)

        for d in data:
            print(d['car_id'])