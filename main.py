import sqlite3
from flask import Flask, jsonsify, jsonify
import functions

con = sqlite3.connect("netflix.db")
app = Flask(__name__)

@app.route("/")
def page():
    return "я главная"

@app.route("/movie/<titl>")
def page_movie(titl):
    return functions.get_movie_by_title(titl=titl)

@app.route("/movie/<year1>/<year2>")
def page_list_movie(year1,year2):
    return jsonify(functions.get_movie_between_rel_year(year1=year1, year2=year2))


@app.route("/rating/children")
def page_list_movie_children():
    return jsonify(functions.get_movie_by_rating('G'))

@app.route("/rating/family")
def page_list_movie_family():
    return jsonify(functions.get_movie_by_rating('G', 'PG', 'PG-13'))

@app.route("/rating/adult")
def page_list_movie_adult():
    return jsonify(functions.get_movie_by_rating('R', 'NC-17'))



if __name__ == "__main__":
	app.run()

