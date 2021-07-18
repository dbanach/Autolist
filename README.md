# Cars.Com
Scraping project using info from cars.com

The website used for this project is www.cars.com. It's a website with information about cars on sale in the USA.

The program goes through ads in the website and saves relevant information to a database.

To use the program, use the command-line interface to determine the scope of search. Use -h for help. 

The parameters that are customizable through the command line interface are as follows:

---body:
**Definition**: Adds body type to search results.
**Accepted values**: "any", "cargo_van", "coupe", "convertible", "hatchback", "minivan", "passenger_van", "pickup_truck", "suv", "sedan" and "wagon"
**Default value**: "any"

--cond: 
**Definition**: Adds condition to search results. 
**Accepted values**: "all", "new", "new_cpo", "used", "cpo".
**Default value**: "all"
"cpo" is a Certified Pre-Owned car, which is a used car with quality certified by the website. 
"new_cpo" will output both new and cpo cars.

--radius: 
**Definition**: Change radius (in miles) of search. 
**Accepted values**: "10", "20", "30", "40", "50", "75", "100", "150", "200", "250", "500", "any"
**Default value**: "any"

--price_min: 
**Definition**: Add min price (in thousands of USD) to search. 
**Accepted values**: 0 to 2500
**No default value**

--price_max: 
**Definition**: Add max price (in thousands of USD) to search. 
**Accepted values**: 0 to 2500
**No default value**

--year_min:
**Definition**: Add min year of car to search. 
**Accepted values**: 1900 to 2022
**No default value**

--year_max:
**Definition**: Add max year of car to search. 
**Accepted values**: 1900 to 2022
**No default value**

--ads_max:
**Definition**: Add max number of ads to scrape.
**Accepted values**: integer greater than 0
**Default value**: By default the program will loop through all available ads in the search
