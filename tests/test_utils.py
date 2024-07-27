from src import utils, HHapi
import pytest
import os
import json
import os.path


class TestHH:
    @pytest.fixture
    def test_obj(self):
        return HHapi.HeadHunterAPI()

    def test_get_data(self, test_obj):
        test_code = test_obj.get_data(keyword='Разработчик')
        assert type(test_obj.vacancies) == list
        assert isinstance(test_obj.vacancies, list)

    @pytest.fixture
    def formatter_instance(self, test_obj):
        """
            Возвращаем экземпляр класса NewVacancyFormat, используя api_instance.
        :param test_obj:
        :return:
        """
        return utils.formatting_vacancies_to_list(test_obj)

    def test_switch_to_new_format(self, test_obj):
        """
            Проверяется, что возвращенные значения в новом формате
        :param test_obj:
        :return:
        """
        key_word = 'python junior'
        vacancies = test_obj.get_data(key_word)
        assert isinstance(vacancies, list)


@pytest.fixture
def json_file():
    return HHapi.JSONFile('tests/test_data/test_vacancies.json')


def test_add_data_to_dict(json_file):
    vacancy = HHapi.Vacancy("Test", "test_url", "Test Employer",
                            "Test Requirement", "Test Description",
                            "1000-2000")
    json_file.add_data_to_dict(vacancy)

    with open('tests/test_data/test_vacancies.json', 'r', encoding='UTF-8') as test_file:
        vacancies = [json.loads(line) for line in test_file.readlines()]

    assert len(vacancies) == 1
    assert vacancies[0]['name'] == 'Test'


def test_get_data_from_dict(json_file):
    vacancies = json_file.get_data()
    assert len(vacancies) == 1
    assert vacancies[0]['name'] == 'Test'


def test_del_data_dict(json_file):
    json_file.del_data()

    with open('tests/test_data/test_vacancies.json', 'r', encoding='UTF-8') as test_file:
        vacancies = [json.loads(line) for line in test_file.readlines()]

    assert len(vacancies) == 0
    assert os.path.exists('tests/test_data/test_vacancies.json')

    os.remove('tests/test_data/test_vacancies.json')


@pytest.fixture
def test_vacancy():
    vacancies = [
        HHapi.Vacancy(name="Test Title", url="test_url", employer="Test Employer",
                      requirements="Test Requirement", description="Test Description",
                      salary=""),
        HHapi.Vacancy(name="Junior программист Python", employer='ПерилаГлавСнаб',
                      salary="60 000-80 000 руб.", url='https://hh.ru/vacancy/93804724',
                      requirements='Уверенное знание Python. Уверенное знание SQL(PSQL, MSSQL).',
                      description='Поддержка микросервисов. Разработка интеграций.'),
        HHapi.Vacancy(name="Python Developer", url="Google", employer="Test Employer",
                      requirements="Python", description="Write tests",
                      salary={"to": 120000}),

    ]
    return vacancies


def test_init_vacancy(test_vacancy):
    vacancy_2 = test_vacancy[1]
    assert vacancy_2.name == 'Junior программист Python'
    assert vacancy_2.employer == 'ПерилаГлавСнаб'
    assert vacancy_2.salary_min == 60000
    assert vacancy_2.salary_max == 80000
    assert vacancy_2.url == 'https://hh.ru/vacancy/93804724'
    assert vacancy_2.requirements == 'Уверенное знание Python. Уверенное знание SQL(PSQL, MSSQL).'
    assert vacancy_2.description == 'Поддержка микросервисов. Разработка интеграций.'


def test_get_salary(test_vacancy):
    vacancy_1 = test_vacancy[0]
    vacancy_2 = test_vacancy[1]
    vacancy_3 = test_vacancy[2]

    assert vacancy_1.get_salary() == "данные о заработной плате отсутствуют"
    assert vacancy_2.get_salary() == "от 60000 до 80000 руб."
    assert vacancy_3.get_salary() == "до 120000 руб."


def test_check_salary_str(test_vacancy):
    vacancy_2 = test_vacancy[1]
    assert vacancy_2.salary_min == 60000
    assert vacancy_2.salary_max == 80000
