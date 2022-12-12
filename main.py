from flask import Flask, jsonify
from utils import get_movie_by_title, get_movies_by_period, get_movies_by_rating, get_movies_by_genre

app = Flask(__name__)
app.config['app.json.ensure_ascii'] = False


@app.route("/movie/<title>/")
def movie_page(title):
    result = get_movie_by_title(title)
    return jsonify(result)


@app.route("/movie/<int:year1>/to/<int:year2>/")
def movies_by_period_page(year1, year2):
    result = get_movies_by_period(year1, year2)
    return jsonify(result)


@app.route("/rating/<rating>/")
def movies_by_rating_page(rating):
    result = get_movies_by_rating(rating)
    return jsonify(result)


@app.route("/genre/<genre>/")
def movies_by_genre_page(genre):
    result = get_movies_by_genre(genre)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
