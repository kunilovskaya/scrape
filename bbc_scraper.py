'''
kunilovskaya
updated: March 25, 2020
partly based on https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
this script does scraping per se: starting from the first search-results page for bbc.com for the query "Посмотреть оригинал" (See source), it goes to all pages of the search (each has 10 results),
collects translations titles, dates and urls and pickles these results into a binary file to be read by the next script which increamentally adds data about respective sources and writes texts to files and creates the corpus description table

to get first results page
(1) go to https://www.bbc.co.uk/ws/languages, select your language
(2) test the query for a phrase like 'Read the original/Puede leer el artículo original' in that language
For example for Spanish the start page is https://www.bbc.com/mundo, the query above returns a page with 64 results:
Su búsqueda de "Puede leer el artículo original" dio 64 resultados
For Russian (https://www.bbc.com/russian/): Поиск по запросу "Прочитать оригинал": 1719 результатов

USAGE: scrapy runspider bbc_scraper.py
(explanation: Scrapy comes with its own command line interface to streamline the process of starting a scraper.)
'''


import scrapy
import pickle

class item: # create a structure with named fields
    fn_en = ''
    tit_en = ''
    url_en = ''
    dt_en = ''
    tit_ru = ''
    url_ru = ''
    dom_ru = ''


class bbcSpider(scrapy.Spider):
    name = "bbc_spider"
    # the page https://www.bbc.com/russian/ with initial search results for query "See source":
    start_urls = ['https://www.bbc.com/russian/search?q=%D0%9F%D1%80%D0%BE%D1%87%D0%B8%D1%82%D0%B0%D1%82%D1%8C+%D0%BE%D1%80%D0%B8%D0%B3%D0%B8%D0%BD%D0%B0%D0%BB']
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
    lst_full = []
    

    def parse(self, response):
        lst = []
        SET_SELECTOR = '.hard-news-unit__body'


        for hit in response.css(SET_SELECTOR):
            link_SELECTOR = 'h3 a ::attr(href)'
            # fetch href attribute within <a> tag see <a class="hard-news-unit__headline-link" href="http://www.bbc.co.uk/russian/vert-cap-42438945">
            title_SELECTOR = 'h3 a ::text'
            date_SELECTOR = 'div ::attr(data-datetime)'

            # to write these results to a file run: scrapy runspider scraper.py -o items.csv
            yield {
                'title': hit.css(title_SELECTOR).extract_first(),
                'link': hit.css(link_SELECTOR).extract_first(),
                'date': hit.css(date_SELECTOR).extract_first(),
            }

            itm = item()
            itm.tit_ru = hit.css(title_SELECTOR).extract_first()
            itm.url_ru = hit.css(link_SELECTOR).extract_first()
            itm.dt_ru = hit.css(date_SELECTOR).extract_first()
            itm.dom_ru = itm.url_ru.split('/')[2]  # extracts domain
            # print("===", itm.dom_ru)
            lst.append(itm)

        self.lst_full = self.lst_full + lst
        print(len(self.lst_full))

        # feeding more pages to parse
        NEXT_PAGE_SELECTOR = '.ws-search-pagination a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract()
        # print("NEXTPAGE=====", next_page)
        
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page[2]),
                callback=self.parse
            )
            print("Number of search results:", next_page[2].split("=")[2])

    def closed(self, reason):
        print('--- end task ---')
        lst = self.lst_full
        print(len(lst))

        with open('list0.bin', 'wb') as f: # the output is saved to the working folder, i.e. the folder from which you start the script
            pickle.dump(lst, f)
