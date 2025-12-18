import requests
from bs4 import BeautifulSoup

import pandas as pd

def collect_films_per_year(year: int) -> list:
    '''
    Collects list of films per year at https://www.kinoafisha.info/rating/movies/

    This function takes an integer representing the year,
    and returns a list of films collected from kinoafisha.
    Function can be extended for genres or country collection from film.

    :param year: The year to collect films for
    :return: List of films in dict format: 'film_name': film_name, 'rating': rating
    ; can to be packed into xlsx format
    '''
    page_num = 1
    data = []

    while True:
        url = f'https://www.kinoafisha.info/rating/movies/{year}/page-{page_num}/'
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('div', class_='movieList_item')

        if len(entries) == 0:
            break

        for entry in entries:
            film_name = entry.find('a', class_='movieItem_title').text
            rating = entry.find('span', class_='movieItem_itemRating').text
            data.append({'film_name': film_name, 'rating': rating})

        page_num += 1

    return data

filter_year = 2024
test_data = collect_films_per_year(filter_year)

df = pd.DataFrame(test_data)
df.to_excel('film_list_2024.xlsx')