# Autolist
Scraping project using info from autolist

The website being used for this project is www.Autolist.com
It's a website with information about used cars on sale.

We chose as a starting point convertible cars within a 50 miles range 
from New York, NY.

Then we located the parts on the webpage that would allow us to go through
it scrapping.

By analysing the html files, we could get the links to each individual ad.
In every ad page we located all of the useful information to save.
We then located the html element to go to the next page and look for
the links again until there are no more pages with data to search.


After that we wrote functions to allow us to do all of those parts.
	1 - To loop through all the the adds;
	2 - To get the information from each ad;
	3 - To go to the next search page;
	4 - To repeat the process until there's no more pages.