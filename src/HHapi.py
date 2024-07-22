import json
import requests
from abc import ABC, abstractmethod

class  AbstcractAPI(ABC):
    """
    Абстрактный класс для работы с API
    """
    @abstractmethod
    def get_data(self, keyword):
        pass

class HeadHunterAPI(AbstcractAPI, ABC):
"""
Класс для работы с API
"""
    def __init__(self, area=113) -> None:
        self.url = ''
        self.headers = {'User-Agent': 'HH-User_Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 5}
        self.vacancies = []
        self.area = area

    def get_data(self, keyword):
        print(f"Поиск вакансий по ключевому слову...")
        self.params['text'] = keyword
        self.params['area'] = self.area
        while self.params.get('page') != 5:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies


