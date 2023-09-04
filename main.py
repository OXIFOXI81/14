
import requests
import bs4
import fake_headers
import time
import json
from pprint import pprint


def connect():
 url="https://hh.ru/search/vacancy"
 params={"text": "python django flask москва санкт-перербург"}
 headers={'User-Agent': 'Mozilla'}
 response = requests.get("https://hh.ru/search/vacancy", params=params ,headers=headers, proxies={},  verify=False)
 return (response)

def data_fill(response):
  vacancy_from_hh = []
  if response.status_code == 200:
    main_html = response.text
    main_soup = bs4.BeautifulSoup(main_html, 'lxml')
    vacancies = main_soup.find_all(class_="serp-item")

    for vacancy in vacancies:
       link= vacancy.find('a', attrs={"data-qa": 'serp-item__title'})['href']
       vacancy_name=vacancy.find('a',class_='serp-item__title').text
       salary = vacancy.find('span',attrs={"data-qa":'vacancy-serp__vacancy-compensation'})
       if salary is  None:
         salary_ = 'оплата не указана'
       else:
         salary_ = salary.text.replace(u'\u202f', u' ')
       city =vacancy.find('div',attrs={"data-qa": 'vacancy-serp__vacancy-address'}).text.replace(u'\xa0', u' ')
       company = vacancy.find('a', attrs={"data-qa": 'vacancy-serp__vacancy-employer'}).text.replace(u'\xa0', u' ')
       vacancy_from_hh.append({
           'link': link,
           'company': company,
           'city': city,
           'salary': salary_
       })
  else:
      print('Ошибка при выполнении соединения.')
  return(vacancy_from_hh)


if __name__ == '__main__':
  response=connect()
  vacancy_from=data_fill(response)
  pprint(vacancy_from)
  with open('vacancies_hh.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_from, file, ensure_ascii=False, indent=3)

  print('Парсинг завершен. Результаты сохранены в файле vacancies_hh.json.')
