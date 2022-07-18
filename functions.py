import sqlite3
from pprint import pp

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
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        data = con.execute(f"""
                            SELECT title, release_year
                            FROM netflix
                            WHERE release_year BETWEEN '{year1}' AND '{year2}'
                            LIMIT 100
                            """).fetchall()
        for item in data:
            return dict(item)

def get_movie_by_rating(*ratings):
    for rating in ratings:
        with sqlite3.connect("netflix.db") as con:
            con.row_factory = sqlite3.Row
            data = con.execute(f"""
                            SELECT title, rating, description
                            FROM netflix
                            WHERE rating='{rating}'
                            LIMIT 100
                            """).fetchall()
        for item in data:
            return dict(item)

pp(get_movie_by_rating('G'))