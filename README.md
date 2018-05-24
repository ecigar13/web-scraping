# web-scraping-truyenyy.com
Using python3-bs4 to scrape truyenyy.com so I can read it offline. 

***

This program uses BeautifulSoup4 to get all the chapters of a certain series on truyenyy.com. The URL is built-in to the program. You only need to supply the following to main():

 1. Name of the story to construct the URL e.g. "quan-than" as in https://truyenyy.com/truyen/quan-than/chuong-1830.html. 
 2. Name of the file to save to (preferably HTML)
 3. Also change the search parameter in extractTitle and extractContent to get those items. They change based on the page source and client you use. Your browser might show one thing but the program might show another thing. Just print out the soup on line 142 to see what's in it.

I might add more scrapers to other sites if time permits.

The URL and html tag might change so you will need to modify the parameter of find() function to get the correct data.

***



