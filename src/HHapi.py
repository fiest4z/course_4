import json
import requests
from abc import ABC, abstractmethod


class AbstcractAPI(ABC):
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


class Vacancy:
    """
    Класс для вакансий
    """

    def __init__(self, name: str, employer: str, url: str, description: str, requirements: str, salary):
        self.name = name
        self.employer = employer
        self.url = url
        self.description = description
        self.requirements = requirements
        self.salary_min = None
        self.salary_max = None
        self.compare_salary(salary)

    def __repr__(self):
        return (f"{self.name}\n"
                f"{self.employer}\n"
                f"{self.salary_min}\n"
                f"{self.salary_max}\n"
                f"{self.description}"
                f"{self.url}\n")

    def __str__(self) -> str:
        return (f"Вакансия: {self.name}\n"
                f"Работодатель: {self.employer}\n"
                f"Заработная плата: {self.get_salary()}\n"
                f"Требования: {self.requirements}\n"
                f"Описание: {self.description}\n"
                f"Ссылка на вакансию: {self.url}\n")

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            if self.salary_min and other.salary_min:
                return self.salary_min > other.salary_min
            else:
                return False

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            if self.salary_min and other.salary_min:
                return self.salary_min < other.salary_min
            else:
                return False

    def get_salary(self):
        if self.salary_min:
            if self.salary_max:
                return f"от {self.salary_min} до {self.salary_max} руб."
            else:
                return f"от {self.salary_min}руб."
        if self.salary_max:
            return f"до {self.salary_max} руб."
        return "Данные о заработной плате отсутствуют."

    def compare_salary(self, salary):
        if isinstance(salary, str) and '-' in salary:
            salary_slice = salary.split('-')
            self.salary_min = int(''.join(filter(str.isdigit, salary_slice[0])))
            self.salary_max = int(''.join(filter(str.isdigit, salary_slice[1])))
        elif isinstance(salary, int):
            self.salary_min = salary
            self.salary_max = salary
        elif isinstance(salary, dict):
            self.salary_min = salary.get('from')
            self.salary_max = salary.get('to')
        else:
            self.salary_min = None
            self.salary_max = None


class AbstractFile(ABC):
    """
    Для работы с файлами
    """

    @abstractmethod
    def add_data_to_dict(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def del_data(self):
        pass


class JSONFile(AbstractFile, ABC):
    """
    Класс для работы с json
    """

    def __init__(self, filename: str):
        self.filename = filename

    def add_data_to_dict(self, vacancy: Vacancy):
        with open(self.filename, 'a', encoding='UTF-8') as f:
            json.dump(vacancy.__dict__, f, ensure_ascii=False)
            f.write('/n')

    def get_data(self):
        with open(self.filename, 'r', encoding='UTF-8') as f:
            vacancies = [json.loads(line) for line in f.readlines()]
        return vacancies

    def del_data(self):
        open(self.filename, 'w').close()
