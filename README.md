# scrape
collect parallel texts from the web

bbc_scraper and process_bbc-scrape are scripts which collect sources and targets from bbc.com
start page
http://www.bbc.com/russian/ искать по фразе Прочитать оригинал 
goo.gl/gYD4nF

These scripts solve the tasks:
1) найти и сохранить название перевода, ссылку на него со страницы результатов поиска и дату 
2) перейти на след страницу результатов (находит 351 перевод) 

3) из каждого результата поиска (hit) извлечь <p> содержащий ссылку на оригинал
4) перейти на страницу оригинала, если она доступна и извлечь текст оригинала и соответствующий текст перевода, 
присвоив им уникальные имена, начиная с en_207ж сохранить в папку проекта

5) напечатать таблицу, содержащую
Source filename
Source title
Source url
Source Year
Target Title
Target url
Translation Domain

based on scrapy tutorials
https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
