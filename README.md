# Autolist
Scraping project using info from autolist

The website being used for this project is www.Autolist.com. It's a website with information about used cars on sale.

The program loops trough ads in the website and saves relevant information to a database.

To use the program, use the command-line interface to determine the scope of search. Use -h for help. 

By default, the file searches for cars in a radius of 50 miles from New York, NY. The parameters that are customizable through the command line interface are as follows:

-b, ---body: Add body type to search. Accepted values: “any”, “convertible”, “coupe”, “crossover”, “hatchback”, “minivan”, “sedan”, “suv”, “passenger_cargo_van”, “truck”, “wagon”

-c, --cat: Add category to search. Accepted values: “any”, “american”, “classic”, “commuter”, “electric”, “family”, “fuel_efficient”, “hybrid”, “large”, “luxury”, “muscle”, “off_road”, “small”, “sport”, “supercar”

-r, --radius: Change radius (in miles) of search. Accepted values: 10, 25, 50, 100, 150, 200, 300, 500, “any”

-pmin, --price_min: Add min price (in thousands of USD) to search. Accepted values: 1 to 100

-pmax, --price_max: Add max price (in thousands of USD) to search. Accepted values: 1 to 100

-ymin, --year_min: Add min year of car to search. Accepted values: 1940 to 2021

-ymax, --year_max: Add max year of car to search. Accepted values: 1940 to 2021

-pg, --page_max: Add max number of pages to scrape. Accepted values: integer

-a, --ads_max: Add max number of ads to scrape. Accepted values: integer
