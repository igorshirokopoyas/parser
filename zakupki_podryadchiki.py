import time

import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url, pages, headers, domain=None):
        self.url = url
        self.pages = pages
        self.headers = headers
        self.domain = domain

    def get_soup(self, url):
        #импортируем заголовки браузера
        headers = self.headers

        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features='html.parser')
        else:
            print(f'Error status code: {response.status_code}')
            soup = None
        return soup

    def urls_to_file(self):
        pass

    def get_data(self, urls_list):
        results = []
        print(f'Ссылки: {urls_list}')
        for num, url in enumerate(urls_list):

            #Запускаем цикл из нескольких попыток
            for i in range(1, 11):
                print(f'Попытка №: {i}')
                try:
                    soup = self.get_soup(url)
                except:
                    time.sleep(10)
                    continue
                else:
                    break

            # print(f'SOUP: {soup}')
            reestr_number = soup.find(class_='text-break').find('a').text
            # print(f'Реестровый номер: {reestr_number}')
            customer = soup.find_all(class_='registry-entry__body-value')[1].text.strip()
            print(f'Номер реестра: {reestr_number}, заказчик: {customer}')
            count = len(urls_list) - num
            print(f'Осталось ссылок: {count}')

        return results


    #возвращает список ссылок на карточки
    def get_urls(self, urls_id, url):
        results_list = []

        pages = self.pages
        self.urls_id = urls_id

        #Пагинация, переход по страницам, просто перебираем циклом и в конце присоединяем к списку
        for page in range(1,pages+1):

            #Получаем url из атрибута экземпляра класса и подставляем в url номер старницы
            url = (self.url).format(page)

            #Печатаем текущую страницу
            print(f'page: {page}, url: {url}')

            #получаем список url-ов с одной страницы
            urls_list = self.get_soup(url)

            #Забираем требуемый параметр с помощью атрибута urls_id
            urls_list = (urls_list.find_all(class_=(self.urls_id)))
            # print(f'Список ссылок: {urls_list}')

            #Вытаскиваем ссылку
            for tag in urls_list:
                res_url = tag.find('a').get('href')
                results_list.append(self.domain + res_url)

            #перебираем сслыки со страницы, обрабатываем их и закидываем в список
            for link in urls_list:
                pass
            # results_list.append()
        return results_list

    #перебирает страницы и присоединяет их результат в список
    def get_pagination(self):
        # result = []
        pages = self.pages
        for page in range(1, pages + 1):
            url = (self.url).format(page)


URL = 'https://zakupki.gov.ru/epz/capitalrepairs/search/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&savedSearchSettingsIdHidden=&contractStage_0=on&contractStage=0&contractNumber=&priceFrom=&priceTo=&sourceOfFinancing=&capitalPurchaseNumber=&selectedSubjectsIdHidden=&selectedSubjectsIdNameHidden=%7B%7D&worktypeIds=&worktypeNames=&worktypeIdsParent=&customerIdOrg=&customerFz94id=&customerTitle=&customerPlace=5277379&customerPlaceCodes=72000000000&subContractNameInn=&capitalDateOfContractConclusionFrom=&capitalDateOfContractConclusionTo=&capitalDateExpiryContractFrom=&capitalDateExpiryContractTo=&capitalDateOfPlacementFrom=&capitalDateOfPlacementTo=&capitalDateOfUpdateFrom=&capitalDateOfUpdateTo=&sortBy=UPDATE_DATE&pageNumber=5&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
pages = 5
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            "Accept-Encoding": "*",
            "Connection": "keep-alive",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",

        }
urls_id = 'registry-entry__header-mid__number'

zakup = Parser(URL, pages, headers, domain='https://zakupki.gov.ru')

print(zakup.headers)

# print(zakup.url)
# zakup.url = URL

# print(zakup.soup_get())

result = zakup.get_urls(urls_id, URL)

data = zakup.get_data(result)

print(data)