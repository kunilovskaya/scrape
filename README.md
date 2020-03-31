# scrape
updated: March 25, 2020

collect parallel texts from the web
https://www.bbc.com/russian/ is used as an example

bbc_scraper and process_bbc-scrape are scripts which collect sources and targets from bbc.com/russian/ initial search result for query "Прочитать оригинал"

To get first results page
(1) go to https://www.bbc.co.uk/ws/languages, select your language
(2) test the query for a phrase like 'Read the original/Puede leer el artículo original' in that language
For example for Spanish the start page is https://www.bbc.com/mundo, the query above returns a page with 64 results:
Su búsqueda de "Puede leer el artículo original" dio 64 resultados
For Russian (https://www.bbc.com/russian/): Поиск по запросу "Прочитать оригинал": 1719 результатов

These scripts solve the tasks:
1) iterate search results pages to get the titles of the translations, the links to each of them and the publication dates 
2) from each search result (hit) exptact the link to the source text
3) go to the source text page, and if it is available, extract the source text and the target text
4) add unique identifiers to the text pair (en_207.txt, ru_207.txt) and lose all boilerplate and save the clean texts to the folders
5) create the corpus contents info table that contains:
- source filename
- source title
- source url
- source Year
- target Title
- target url
- translation domain

**How to use**
1. install python libraries: scrapy, pickle, requests, justext, bs4
1. go to [https://www.bbc.co.uk/ws/languages](https://www.bbc.co.uk/ws/languages), select your language
2. test the query for a phrase like 'Read the original/Puede leer el artículo original' in that language
3. supply the link to the search results page to start_urls (line 36 in bbc_scraper.py)
4. run the first script: $ scrapy runspider bbc_scraper.py
5. adjust output folder names in process_bbc-scrape.py (lines 88-90)
6. run the second script: $ python3 process_bbc-scrape.py

partly based on scrapy tutorials
https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
