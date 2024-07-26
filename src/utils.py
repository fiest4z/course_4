from src.HHapi import *


def filtering_vacancies(vacancies_list, filter_words):
    """
    Фильтр по названию
    """
    filtered_vacancies = []
    for vacancy in vacancies_list:
        if vacancy.description:
            exclude = False
            for word in filter_words:
                try:
                    if word.lower() in vacancy.title.lower() or word.lower() in vacancy.description.lower():
                        exclude = True
                    break
                except AttributeError:
                    continue
            if not exclude:
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def formatting_vacancies_to_list(keyword):
    """
    Форматирование по з/п
    """
    data = HeadHunterAPI.get_data(keyword=keyword)
    vacancies = []
    for vacancy in data:
        snippet = vacancy['snippet']
        salary = vacancies['salary']
        if salary:
            s_from = salary.get('from')
            s_to = salary.get('to')
            if s_from:
                if s_to:
                    s_range = f'{s_from} - {s_to} руб.'
                else:
                    s_range = f'от {s_from} руб.'
            else:
                if s_to:
                    s_range = f'до {s_to} руб.'
                else:
                    f'Данные о заработной плате отсутствуют'
            vacancy = Vacancy(
                name=vacancy['name'],
                url=vacancy['alternate_url'],
                employer=vacancy['employer']['name'],
                requirements=snippet.get('requirement', ''),
                description=snippet.get('responsibility', ''),
                salary=s_range
            )
            vacancies.append(vacancy)
    return vacancies
