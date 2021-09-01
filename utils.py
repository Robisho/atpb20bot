# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from random import randint


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:79.0) Gecko/20100101 Firefox/79.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4235.0 Safari/537.36', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    ]


def get_html():
    # 'https://www.istu.edu/schedule/?group=459121'  2020/2021
    url = 'https://www.istu.edu/schedule/?group=461943'
    html = requests.get(url, headers=headers[randint(0, 3)])
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


def get_week_info():
    soup = get_html()

    title = soup.find('div', class_='alert-info')
    p_list = title.find_all('p')
    # структура: Институт высоких технологий
    # оставляем второй элемент
    structure_name = p_list[0].text.split(': ')[1]
    # группа: АТПб-20-1
    group_name = p_list[1].text
    # неделя: нечетная
    week_name = p_list[2].text
    # время действия: 12.10.2020 - 18.10.2020
    time_slot = p_list[3].text
    data = (structure_name,
            group_name,
            week_name,
            time_slot)

    return data


def get_main_div():
    soup = get_html()

    if soup.find('div', class_='full-even-week'):
        main_div = soup.find('div', class_='full-even-week')
    elif soup.find('div', class_='full-odd-week'):
        main_div = soup.find('div', class_='full-odd-week')
    return main_div


def get_pair():
    main_div = get_main_div()
    data_list = []

    week_choice = main_div.find_all('h3', class_='day-heading')

    class_lines = main_div.find_all('div', class_='class-lines')

    for i in class_lines:
        day = i.previous_element
        yield '************************'
        # print(day)
        yield day
        yield '************************'

        class_tails = i.find_all('div', class_='class-tails')

        for pair in class_tails:
            # время начала пары
            time_ = pair.find('div', class_='class-time').text
            yield time_

            for p in pair.find_all('div', class_='class-tail'):

                if 'class-all-week' in p.attrs['class']:
                    week = 'Общая неделя'

                elif 'class-even-week' in p.attrs['class']:
                    week = 'Четная неделя'

                elif 'class-odd-week' in p.attrs['class']:
                    week = 'Нечетная неделя'

                if p.text == 'свободно':
                    data = (week, 'Время свободно')

                else:
                    # предмет
                    subject = p.find('div', class_='class-pred').text
                    # аудитория
                    room = p.find('div', class_='class-aud').text
                    # лекция/практика
                    variant = p.find_all('div', class_='class-info')[0].text
                    # преподаватель
                    coach = p.find_all('div', class_='class-info')[-1].find('a').text

                    data = (week, subject, room, variant, coach)

                yield data


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


def main():
    header_list = []
    header = get_week_info()
    for h in header:
        header_list.append(h)

    result_list = []
    result = get_pair()
    for r in result:
        r = str(r)
        r = r.replace("('", '')
        r = r.replace("', '", '  ')
        r = r.replace("')", '')
        result_list.append(r)
    with open('result.txt', 'w', encoding='utf8') as file:
        for header in header_list:
            file.write(header)
            file.write('\n')
        for el in result_list:
            file.write(el)
            file.write('\n')


if __name__ == '__main__':
    main()
