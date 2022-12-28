import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import json

host = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

def get_headers():
    return Headers(browser='firefox', os='win').generate()

hh_main = requests.get(host, headers=get_headers()).text
soup = BeautifulSoup(hh_main, features='lxml')

all_content = soup.find(class_='vacancy-serp-content')
all_vacancy = all_content.find_all(class_='serp-item', limit=100)


def search_django_flask():
    searched_vacancy = []
    for vacancy in all_vacancy:
        link = vacancy.find('a', class_='serp-item__title')
        link_relative = link['href']
        vacancy_open = requests.get(link_relative, headers=get_headers()).text
        soup_2 = BeautifulSoup(vacancy_open, features='lxml')
    
        descriptions = soup_2.find(class_='vacancy-section')
        salary = soup_2.find(class_='bloko-header-section-2 bloko-header-section-2_lite').text
        company = soup_2.find(attrs={'class': 'bloko-header-section-2 bloko-header-section-2_lite', 
                                        'data-qa': 'bloko-header-2'}).text
        city = soup_2.select_one('.bloko-text[data-qa=vacancy-serp__vacancy-address]').contents[0]
        pattern = r'django|flask'
        result = re.findall(pattern, descriptions.text, flags=re.I)
        if len(result) > 0:
            searched_vacancy.append({
                'reference': link_relative,
                'salary': ' '.join(salary.split('\xa0')),
                'company': ' '.join(company.split('\xa0')),
                'city': city
            })
    with open("result_django_flask.json", "w", encoding='utf-8') as file:
        json.dump(searched_vacancy, file, ensure_ascii=False, indent=2)

def search_usd():
    searched_vacancy = []
    for vacancy in all_vacancy:
        link = vacancy.find('a', class_='serp-item__title')
        link_relative = link['href']
        vacancy_open = requests.get(link_relative, headers=get_headers()).text
        soup_2 = BeautifulSoup(vacancy_open, features='lxml')

        salary = soup_2.find(class_='bloko-header-section-2 bloko-header-section-2_lite').text
        company = soup_2.find(attrs={'class': 'bloko-header-section-2 bloko-header-section-2_lite', 
                                        'data-qa': 'bloko-header-2'}).text
        city = soup_2.select_one('.bloko-text[data-qa=vacancy-serp__vacancy-address]').contents[0]
        salary_split = salary.lower().split()
        if ['usd'] == [i for i in salary_split if i == 'usd']:
            searched_vacancy.append({
                    'reference': link_relative,
                    'salary': ' '.join(salary.split('\xa0')),
                    'company': ' '.join(company.split('\xa0')),
                    'city': city
                })
    with open("result_usd.json", "w", encoding='utf-8') as file:
            json.dump(searched_vacancy, file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    search_django_flask()
    search_usd()
    