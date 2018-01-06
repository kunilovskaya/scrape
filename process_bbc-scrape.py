import os, sys
import scrapy
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import requests, justext
import pickle

# this is the second script which finishes the bbc.com scraping job: it (1) reads the binary file with data on all targets created by scraper; (2) increamentally adds data about respective sources and (3) writes texts to files; and (4) creates the corpus description table

def write_txt(fname, url, lang):
    # 1) get text data & 2) write text data to the file
    with open(fname, 'w') as outfile:
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist(lang))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                outfile.write(paragraph.text + '\n')

class item: # create a structure with named fields
    fn_en = ''
    tit_en = ''
    url_en = ''
    dt_en = ''
    tit_ru = ''
    url_ru = ''
    dom_ru = ''

def do_something(lst):
    kk = 0
    try:
        for itm in lst:
            print('itm', kk)

            if itm.url_en is not None and len(itm.url_en)>0:
                continue

            kk += 1
            ru_page = requests.get(itm.url_ru)

            urlsoup = BeautifulSoup(ru_page.content, "html.parser")

            for parag in urlsoup.find_all('p'):
                if "на сайте" in parag.text or "Прочитать оригинал" in parag.text:
                    first_link = parag.find('a', href=True)
                    if first_link:
                        itm.url_en = first_link.get('href')
                        break

            if itm.url_en is None or len(itm.url_en)==0:
                print('url_en is empty')
                continue

            en_page = requests.get(itm.url_en)

            urlsoup1 = BeautifulSoup(en_page.content, "html.parser")

            # <span class="publication-date index-body">13 December 2017</span>
            dt_en = urlsoup1.find('span', attrs={'class': 'publication-date index-body'})
            if dt_en is not None:
                itm.dt_en = dt_en.text

            tit_en = urlsoup1.find('title')
            # print("---------------", tit_en)
            if tit_en is not None:
                itm.tit_en = tit_en.text  # tit_en.replace('<title>','')##.replace('</title>','')

            with open('list.bin', 'wb') as f:
                pickle.dump(lst, f)

    except:
        print('err')

lst = []
with open('list.bin', 'rb') as f:
    lst = pickle.load(f)

print(len(lst))

# находим ссылку на оригинал
do_something(lst)

print("TESTLIST=======================================", len(lst))

with open('_list.txt', 'w') as ofile:
    n = len(lst)
    for k in range(n):
        itm = lst[k]

        if itm.url_en is None or len(itm.url_en) == 0:
            print('url_en is empty')
            continue

        if itm.url_ru is None or len(itm.url_ru) == 0:
            print('url_ru is empty')
            continue

        fname_en = 'en_{0}.txt'.format(k + 207)
        fname_ru = 'ru_{0}.txt'.format(k + 207)

        print("++++++++++++++++++++++++++++++++++++", itm.url_en, '\n')
        try:
            write_txt(fname_ru, itm.url_ru, 'Russian')
            write_txt(fname_en, itm.url_en, 'English')
        except:
            print("BOOOOOOOOOOOOOOOOOOOOOOOOOM", itm.url_en, '\n')
            continue

        s = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(fname_en, itm.tit_en, itm.url_en, itm.dt_en, itm.tit_ru,
                                                       itm.url_ru, itm.dom_ru)
        ofile.write(s + '\n')
print(len(lst))

