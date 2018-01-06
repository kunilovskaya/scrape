#!/usr/bin/python3

# partly based on https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
# this script does scraping per se: starting from the first search-results page for bbc.com for the query "Посмотреть оригинал", it goes to all pages of the search (each has 10 results), collects translations titles, dates and urls and pickles these results into a binary file to be read by the next script which increamentally adds data about respective sources and writes texts to files and creates the corpus description table

import os, sys
import scrapy
import requests
from bs4 import BeautifulSoup
import re
import requests, justext
import pickle

class item: # create a structure with named fields
    fn_en = ''
    tit_en = ''
    url_en = ''
    dt_en = ''
    tit_ru = ''
    url_ru = ''
    dom_ru = ''


class bbcSpider(scrapy.Spider): # зачем-то определяем класс и его методы как в тьюториале по scapy https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
    name = "bbc_spider"
    start_urls = ['http://goo.gl/gYD4nF']  # результаты поиска по сайту (запрос - Прочитать оригинал)
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
    lst_full = []

    def parse(self, response): # непонятно что возврещает этот метод yield; он работает с каждым результатом поиска на странице

        lst = []
        SET_SELECTOR = '.hard-news-unit__body' # why a dot here? it seems it means 'attribute"


        for hit in response.css(SET_SELECTOR): #посмотреть на html -- добавить view-source: перед URL в браузере
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
            # print("=======================================", itm.dom_ru)
            lst.append(itm)

        self.lst_full = self.lst_full + lst
        print(len(self.lst_full))

        # подаем еще страницы резульатов поиска методу parse
        NEXT_PAGE_SELECTOR = '.ws-search-pagination a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract()

        #print("NEXTPAGE=======================================", next_page)
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page[2]),
                callback=self.parse
            )
            # print("Number of translations :", next_page[2].split("=")[2])

    def closed(self, reason):
        print('----------------------- end task')
        lst = self.lst_full
        print(len(lst))

        with open('list.bin', 'wb') as f:
            pickle.dump(lst, f)
