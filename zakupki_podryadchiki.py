import time
import csv

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

    def data_to_csv(self, data):
        with open('zakupki_podryadchiki.csv', 'a', newline='', encoding='utf-8') as file:
            for line in data:
                for row in line:
                    print(row)
                    file.write(row + ';')
                file.write('\n')

    #Функция для сбора данных
    def get_data(self, urls_list):
        results = []
        print(f'Ссылки: {urls_list}')

        #Словарь со значениями
        results_dict = []

        #Загаловок для csv файла
        csv_headers = \
            'Реестр', \
            'Ссылка на договор', \
            'Заказчик', \
            'ссылка на тендер', \
            'Цена договора', \
            'Дата заключения',\
            'Дата начала', \
            'Дата окончания', \
            'Подрядчик', \
            'Подрядчик ИНН', \
            'Подрядчик КПП', \
            'Подрядчик адрес', \
            'Подрядчик телефон', \
            'Подрядчик email', \
            'Виды работ',

        #Присоединяем заголовок к списку
        results_dict.append(csv_headers)

        #Перебор ссылок из списка ссылок
        for num, url in enumerate(urls_list):

            #Запускаем цикл из нескольких попыток соединения для большей надежности
            for i in range(1, 11):
                print(f'Попытка №: {i}')
                try:
                    soup = self.get_soup(url)
                except:
                    time.sleep(10)
                    continue
                else:
                    break

            #Собираем данные

            #Номер договора в реестре
            reestr_number = soup.find(class_='text-break').find('a').text

            #Название заказчика
            customer = soup.find_all(class_="blockInfo__section")

            #Виды работ
            for tag in customer:
                # если в названии тега есть "Виды работ", то берем его
                if 'Виды работ (услуг)' in tag.text:
                    work_type = tag.find('span', 'section__info').text.strip()

            #Название заказчика
            for tag in customer:
                # если в названии тега есть "Сокращенное наименование заказчика", то берем его
                if 'Сокращенное наименование заказчика' in tag.text:
                    customer = tag.find('span', 'section__info').text.strip()

            #Информация о закупке (тендеру), на основе которого заключили договор
            #пробуем взять ссылку на тендер, если она есть, если нет, то оставляем пустой
            try:
                tender_url = soup.find_all(class_='blockInfo__section')[11].find('a').get('href')
                tender_url = self.domain + tender_url
            except:
                tender_url = ' '

            #Информация в основноб блоке
            main_info = soup.find_all(class_='col')
            for tag in main_info:
                #Сбор блока, где содержится инфа о договоре
                if 'Общая информация о договоре' in tag.text:
                    contract = tag.find_all('span', 'section__info')

                #Сбор блока, где содержится инфа о подрядчике
                elif 'Информация о подрядчике' in tag.text:
                    contractor = tag.find(class_='blockInfo__section')

            # Информация по контракт:

            # Дата заключения договора
            contract_date_conclude = contract[0].text.strip()

            # Дата начала исполнения договора
            contract_date_start = contract[3].text.strip()

            # Дата окончания исполнения договора
            contract_date_end = contract[4].text.strip()

            # Цена договора, руб
            contract_price = contract[2].text.strip()

            #Информация о подрядчике
            #имя подрядчика
            contractor_name = contractor.find_all('span', 'section__info')[0].text.strip()

            #ИНН подрядчика
            contractor_inn = contractor.find_all('span', 'section__info')[1].text.strip()

            #КПП подрядчика
            contractor_kpp = contractor.find_all('span', 'section__info')[2].text.strip()

            #Адрес места нахождения подрядчика
            try:
                for tag in contractor:
                    if 'Адрес места нахождения' in tag.text:
                        contractor_addres = tag.find('span', 'section__info').text.strip()
            except:
                contractor_addres = ' '

            #Контактный телефон подрядчика
            try:
                for tag in contractor:
                    if 'Контактный телефон' in tag.text:
                        contractor_phone = tag.find('span', 'section__info').text.strip()

            except:
                contractor_phone = ' '

            #Электронная почта подрядчика
            try:
                contractor_email = contractor.find_all('span', 'section__info')[6].text.strip()
            except:
                contractor_email = ' '


            #Список полей для печати в консоли списка
            to_save = \
                f'Реестр: {reestr_number}, ' \
                f'Ссылка на договор: {url}, ' \
                f'Заказчик: {customer}, ' \
                f'ссылка на тендер: {tender_url}, ' \
                f'Цена договора: {contract_price}, ' \
                f'Дата заключения: {contract_date_conclude}, ' \
                f'Дата начала: {contract_date_start}, ' \
                f'Дата окончания: {contract_date_end}, ' \
                f'Подрядчик: {contractor_name}, ' \
                f'Подрядчик ИНН: {contractor_inn}, ' \
                f'Подрядчик КПП: {contractor_kpp}, ' \
                f'Подрядчик адрес: {contractor_addres}, ' \
                f'Подрядчик телефон: {contractor_phone}, ' \
                f'Подрядчик email: {contractor_email}, ' \
                f'Виды работ: {work_type}, ' \


            fileds_to_csv = [
                \
                reestr_number,\
                url,\
                customer,\
                tender_url,\
                contract_price,\
                contract_date_conclude,\
                contract_date_start,\
                contract_date_end,\
                contractor_name,\
                contractor_inn,\
                contractor_kpp,\
                contractor_addres,\
                contractor_phone,\
                contractor_email,\
                work_type,\
                ]

            results_dict.append(fileds_to_csv)

            print(to_save)

            #счетчик ссылок
            count = len(urls_list) - num
            print(f'Осталось ссылок: {count}')

            #присоединяем резултат цикла в общий список результатов
            results.append(to_save)
        return results_dict


    #Функция возвращает список ссылок на карточки с заданного кол-ва страниц
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

        return results_list


URL = 'https://zakupki.gov.ru/epz/capitalrepairs/search/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&savedSearchSettingsIdHidden=&contractStage_0=on&contractStage=0&contractNumber=&priceFrom=&priceTo=&sourceOfFinancing=&capitalPurchaseNumber=&selectedSubjectsIdHidden=&selectedSubjectsIdNameHidden=%7B%7D&worktypeIds=&worktypeNames=&worktypeIdsParent=&customerIdOrg=&customerFz94id=&customerTitle=&customerPlace=5277379&customerPlaceCodes=72000000000&subContractNameInn=&capitalDateOfContractConclusionFrom=&capitalDateOfContractConclusionTo=&capitalDateExpiryContractFrom=&capitalDateExpiryContractTo=&capitalDateOfPlacementFrom=&capitalDateOfPlacementTo=&capitalDateOfUpdateFrom=&capitalDateOfUpdateTo=&sortBy=UPDATE_DATE&pageNumber=5&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
pages = 20
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            "Accept-Encoding": "*",
            "Connection": "keep-alive",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",

        }
urls_id = 'registry-entry__header-mid__number'

zakup = Parser(URL, pages, headers, domain='https://zakupki.gov.ru')

print(zakup.headers)

result = zakup.get_urls(urls_id, URL)

data = zakup.get_data(result)

csv_file = zakup.data_to_csv(data)

print(f'DATA: {data}')