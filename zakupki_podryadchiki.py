import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url, pages):
        self.url = url
        self.pages = pages

    def soup_get(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features='html.parser')
        else:
            soup = None

        return soup

    def urls_to_file(self):
        pass

    def get_urls(self):
        pass

    def get_categories(self):
        soup = Parser.soup_get()
        category = BeautifulSoup.find()
        return category

    #Сбор данных о компании
    def get_company(self, id):
        comp_list = []
        self.id = id
        print(self.id)

        companies = self.soup_get()
        companies = (companies.find_all(class_=(self.id)))

        for company in companies:
            comp_list.append(company.text.strip())

        return comp_list

    #возвращает список ссылок на карточки
    def get_urls(self, page_id, pages, url):

        results_list = []

        pages = self.pages
        self.page_id = page_id
        print(self.page_id)

        for page in range(1,pages+1):
            #Подставляем в url номер старницы
            url = (self.url).format(page)

            print(f'page: {page}, url: {url}')
            #получаем список url-ов с 1 страницы
            urls = self.soup_get()

            urls = (urls.find_all(class_=(self.page_id)))

            #перебираем url со страницы и закидываем их в список
            for url in urls:
                results_list.append(url.text.strip())
            # results_list.append()
            return results_list

    #перебирает страницы и присоединяет их результат в список
    def get_pagination(self):
        # result = []
        pages = self.pages
        # for page in range(1, pages + 1):
        #     one_page = Parser.get_urls()
        #     result.append(one_page)
        for page in range(1, pages + 1):
            url = (self.url).format(page)


URL = 'https://zakupki.gov.ru/epz/rkpo/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&sortBy=UPDATE_DATE&pageNumber={}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&active=on&selectedSubjectsIdNameHidden=%7B%7D&rejectReasonIdNameHidden=%7B%7D&customerPlace=5277379'
zakup = Parser(URL, 5)

# print(zakup.url)
# zakup.url = URL

# print(zakup.soup_get())

result = zakup.get_urls('registry-entry__body-href', 5, URL)

print(result)