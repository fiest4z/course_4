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
    data = HeadHunterAPI().get_data(keyword=keyword)
    vacancies = []
    for vacancy in data:
        snippet = vacancy['snippet']
        salary = vacancy['salary']
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


def user_interaction():

    json_file = JSONFile('data/vacancies.json')
    platforms = ['HeadHunter']

    search_query = input('Введите поисковый запрос: ')
    vacancies_list = formatting_vacancies_to_list(search_query)
    filter_words = str(input('Введите ключевые слова для фильтрации вакансий по описанию: ').split())
    filtered_vacancies = filtering_vacancies(vacancies_list, filter_words)

    if not filtered_vacancies:
        print('Вакансии не найдены')
        return None

    print("Найдены вакансии по запросу: \n")
    for idx, vacancy in enumerate(filtered_vacancies, start=1):
        print(f'{idx}. {vacancy}')
        json_file.add_data_to_dict(vacancy)

    top_n = int(input('Введите количество вакансий для вывода: '))
    vacancies_with_salary = [vacancy for vacancy in filtered_vacancies if vacancy.salary_min is not None
                             or vacancy.salary_max is not None]
    ranged_vacancies = sorted(vacancies_with_salary, key=lambda x: x.salary_min if x.salary_min is not None else float(
        'inf'), reverse=True)
    print(f'\nТоп-{top_n} вакансий по зарплате: \n')
    for idx, vacancy in enumerate(ranged_vacancies[:top_n], start=1):
        print(f'{idx}. {vacancy}')

    clean_data = input("Очистить список? y/n: ")
    if clean_data.lower() == 'y':
        json_file.del_data()

    run_again = input("Повторить поиск? y/n: ")
    if run_again.lower() == 'y':
        user_interaction()
