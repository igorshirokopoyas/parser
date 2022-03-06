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
            comp_list.append(company)

        return comp_list

    def pagination(self):
        pass

URL = 'https://zakupki.gov.ru/epz/rkpo/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&active=on&selectedSubjectsIdNameHidden=%7B%7D&rejectReasonIdNameHidden=%7B%7D&customerPlace=5277379'
zakup = Parser(URL, 39)

print(zakup.url)
# zakup.url = URL

# print(zakup.soup_get())

result = zakup.get_company('registry-entry__body-href')

print(result)