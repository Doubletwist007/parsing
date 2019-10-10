import requests
from bs4 import BeautifulSoup as bs
import re
import csv

"""
код парсит base_url получает (список словарей) и записывает их в CSV файл в табличном виде.
некоторые переменные в цикле комментить смысла нет, старался называть их чтобы было понятно что они делают.
"""
 
headers = {'accept':'*/*', 'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

base_url = 'https://otzovik.com/reviews/bukmekerskaya_kontora_liga_stavok/'

#переменная для очистки данных локации
pattern = 'Россия, \w+'

def pars_page(base_url, headers):
    reviews = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        all_reviews = soup.find_all('div', attrs={'class':"item status4 mshow0"})
        for each_review in all_reviews:
            review = each_review.find('div', attrs={'class': "review-teaser"}).text
            review_time = each_review.find('span', attrs={'class': "tooltip-right"}).text
            #количество "icons icon-star-1" будет равно рейтингу отзыва
            review_mark = len(each_review.find_all('span', attrs={'class': "icons icon-star-1"}))
            review_location = each_review.find('div', attrs={'class': "user-info"}).text
            #т.к. DIV с локацией без атрибутов, то применяем ReDux
            review_locat_re = re.findall(pattern, review_location)[0]
            review_user = each_review.find('span', attrs={'itemprop':"name"}).text
            review_goodpart = each_review.find('div', attrs={'class': "review-plus"}).text
            review_badpart = each_review.find('div', attrs={'class': "review-minus"}).text
            reviews.append({
                'review': review,
                'review_time': review_time,
                'review_mark': review_mark,
                'review_location': review_locat_re,
                'review_user': review_user,
                'review_goodpart': review_goodpart,
                'review_badpart': review_badpart
            })
        return reviews
    else:
        return 'Something went wrong'

final_pars_result = pars_page(base_url, headers)

toSCV = final_pars_result

keys = toSCV[0].keys()

with open('reviews.csv', 'w') as file_pars:
    dict_writer = csv.DictWriter(file_pars, keys)
    dict_writer.writeheader()
    dict_writer.writerows(toSCV)