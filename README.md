# Autolist
Scraping project using info from autolist

The website being used for this project is www.Autolist.com
It's a website with information about used cars on sale.

We choose as a starting point a search that included all of the makes of
cars, not minding how far it is to the location of the user.

Then we located the parts on the webpage that would allow us to go through
it scrapping.

We located the html elements of all adds, getting the webpage for it.
We then located the html element to go to the next page.
In every add page we located all of the useful information to save.

After that we wrote functions to allow us to do all of those parts.
	1 - To loop through all the the adds.
	2 - To click on them and get the information
	3 - To go to the next page.
	4 - To repeat the process until there's no more pages.

