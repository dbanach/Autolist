import pymysql


class Autolist_DBM:
    """"
    class to create and manage the database to work with Autolist webpage data.
    DBM= DataBase Manager
    """

    def __init__(self):
        newDatabaseName = "Autolist"
        sql_code = "CREATE DATABASE IF NOT EXISTS " + newDatabaseName
        self.sql_command(sql_code)

    def sql_command(self, sql_code):
        cursor, connection = self.connect_to_database()

        try:
            cursorInstance = connection.cursor()
            cursorInstance.execute(sql_code)
        except Exception as e:

            print("Exeception occured:{}".format(e))

    def connect_to_database(self):
        databaseServerIP = "127.0.0.1"
        databaseUserName = "root"
        databaseUserPassword = ""

        charSet = "utf8mb4"  # Character set
        cursor = pymysql.cursors.DictCursor
        connection = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,
                                     charset=charSet, cursorclass=cursor)

        return (cursor, connection)

    def show_db(self):
        sql_code = "SHOW DATABASES"
        self.sql_command(sql_code)

    def create_table_cars(self):
        sql_code = """  CREATE TABLE IF NOT EXISTS Cars(car_id AUTOINCREMENT PRIMARY KEY,
                        sold_by varchar NOT NULL,
                        sale_price float,
                        make varchar,
                        year_of_assembly datetime,
                        model varchar,
                        color varchar,
                        transmission varchar,
                        engine varchar,
                        fuel_type varchar, 
                        condition varchar,
                        mileage float,
                        mile_per_liter float,
                        body_style varchar,
                        
                    FOREIGN KEY (sold_by) REFERENCES SELLERS(Name)) """
        self.sql_command(sql_code)

    def create_table_seller(self):
        sql_code = """ CREATE TABLE IF NOT EXISTS Sellers(Name varchar,
                       phone varchar,
                       address varchar,
                       PRIMARY KEY (Name))
                        
        """
        self.sql_command(sql_code)

    def insert_car_row(self, my_car, seller_name):
        # might be a seller with two identical cars with this features????

        sold_by = seller_name
        sale_price, make, year_of_assembly, model, color, transmission, engine, fuel_type, \
        condition, mileage, mile_per_liter, body_style = my_car.getall()

        sql_code = f"""INSERT IGNORE INTO Cars (sold_by, sale_price, make, year_of_assembly
                    , model, color, transmission, engine, fuel_type, condition
                    , mileage, mile_per_liter, body_style) VALUES ({sold_by},{sale_price},{make}, 
                    {year_of_assembly},{model},{color},{transmission},{engine},{fuel_type},{condition}
                    {mileage},{mile_per_liter},{body_style})
        
        
        """
        self.sql_command(sql_code)

    def insert_seller_row(self, my_seller):
        name, phone, address = my_seller.getall()

        sql_code = f"""INSERT IGNORE INTO Sellers (Name, address,phone)
                        -> VALUES( {name}, {phone}, {address});
        
        
        """
        self.sql_command(sql_code)
