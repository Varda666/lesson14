import sqlite3
from pprint import pp
import json
from collections import Counter

def get_movie_by_title(titl):
    """ Возвращает фильмы по названию"""
    with sqlite3.connect("netflix.db") as con:
        data = con.execute(f"""
                    SELECT title, country, release_year, description
                    FROM netflix
                    WHERE title LIKE '%{titl}%'
                    ORDER BY release_year DESC
                    LIMIT 1
                    """).fetchone()
        new_dict = {}
        new_dict['title'] = data[0]
        new_dict['country'] = data[1]
        new_dict['release_year'] = data[2]
        new_dict['description'] = data[3]

        return new_dict

def get_movie_by_rel_year():
        with sqlite3.connect("netflix.db") as con:
            cur = con.cursor()
            cur.execute("""
                        SELECT title, country, release_year, description
                        FROM netflix
                        WHERE release_year = 1997
                        """)
            data = list(cur.fetchall())
            return data

def get_movie_between_rel_year(year1, year2):
    '''Возвращает фильмы за определенный период'''
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        data = con.execute(f"""
                            SELECT title, release_year
                            FROM netflix
                            WHERE release_year BETWEEN '{year1}' AND '{year2}'
                            ORDER BY release_year
                            LIMIT 100
                            """).fetchall()
        result = []
        for item in data:
            result.append(dict(item))
        return result

def get_movie_by_rating(*ratings):
    """ Возвращает фильмы по рейтингу"""
    for rating in ratings:
        with sqlite3.connect("netflix.db") as con:
            con.row_factory = sqlite3.Row
            data = con.execute(f"""
                            SELECT title, rating, description
                            FROM netflix
                            WHERE rating='{rating}'
                            LIMIT 100
                            """).fetchall()
        result = []
        for item in data:
            result.append(dict(item))
        return json.dumps(result)

def get_movie_by_listed_in(list_in):
    """Возвращает фильмы по жанру"""
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        data = con.execute(f"""
                        SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{list_in}%'
                        ORDER BY release_year DESC
                        LIMIT 10
                        """).fetchall()
        result = []
        for item in data:
           result.append(dict(item))
        return json.dumps(result)


def get_actor_in_couple(actor1, actor2):
    """Возвращает актеров играющих в паре с заданными актерами более 2х раз"""
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        data = con.execute(f"""
                        SELECT title, netflix.cast
                        FROM netflix
                        WHERE netflix.cast LIKE '%{actor1}%'
                        OR netflix.cast LIKE '%{actor2}%'
                        ORDER BY '%{actor2}%' 
                        """).fetchall()
        names_list = []
        for item in data:
            names = set(item['cast'].split(', ')) - set([actor1, actor2])
            for name in names:
                names_list.append(name)
        counter = Counter(names_list)
        new_names_list = []
        for k,v in dict(counter).items():
            if v >= 2:
                new_names_list.append(k)
        print(new_names_list)



def get_movie_by_type_listed_in_and_release_year(type_=None, listed_in_=None, release_year_=None):
    """Возвращает фильмы по типу, году выпуска и жанру"""
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        data = con.execute(f"""
                        SELECT title, description
                        FROM netflix
                        WHERE type = '{type_}'
                        AND listed_in LIKE '%{listed_in_}%'
                        AND release_year = '{release_year_}'
                        """).fetchall()
        result = []
        for item in data:
            result.append(dict(item))
        return json.dumps(result)


pp(get_movie_between_rel_year(2019, 2020))


