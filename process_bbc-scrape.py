'''
mkunilovskaya
updated: March 25, 2020

this is the second script which finishes the bbc.com scraping job:
(1) it reads the binary file with data on all targets created by scraper;
(2) increamentally adds data about respective sources and
(3) writes texts to files; and
(4) creates the corpus description table

USAGE: python3 process_bbc-scrape.py
Comments:
-- it assumes that the temporary file (list0.bin) produces by bbc_scraper is saved to the same folder as this script (default behavior)
-- if updates the list0.bin and saves another temporary file list1.bin
'''
import os
from bs4 import BeautifulSoup
import requests, justext
import pickle


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

def scrape_it(lst):
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

            with open('list1.bin', 'wb') as f:
                pickle.dump(lst, f)

    except:
        print('err')

#### MAIN CODE ####
lst = []
# create folders for the output
en_outto = 'en/'
os.makedirs(en_outto, exist_ok=True)
ru_outto = 'ru/'
os.makedirs(ru_outto, exist_ok=True)

with open('list0.bin', 'rb') as f:
    lst = pickle.load(f)

print(len(lst))

# find the link to the source
scrape_it(lst)

print("TESTLIST:", len(lst))

with open('corpus_description.tsv', 'w') as ofile:
    n = len(lst)
    for k in range(n):
        itm = lst[k]

        if itm.url_en is None or len(itm.url_en) == 0:
            print('url_en is empty')
            continue

        if itm.url_ru is None or len(itm.url_ru) == 0:
            print('url_ru is empty')
            continue
        # add k + N if you have a continuing collection and need to start counting from 207 for example
        # the can be gaps in the file identifiers due to failures to extract either source or target
        fname_en = 'en_{0}.txt'.format(k)
        fname_ru = 'ru_{0}.txt'.format(k)

        print("+++", itm.url_en, '\n')
        try:
            write_txt(ru_outto + fname_ru, itm.url_ru, 'Russian')
            write_txt(en_outto + fname_en, itm.url_en, 'English')
        except:
            print("BOOOOOOM", itm.url_en, '\n')
            continue

        s = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(fname_en, itm.tit_en, itm.url_en, itm.dt_en, itm.tit_ru,
                                                       itm.url_ru, itm.dom_ru)
        ofile.write(s + '\n')
print(len(lst))

