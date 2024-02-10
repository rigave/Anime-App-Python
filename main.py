import requests
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

BASE_URL = 'https://api.jikan.moe/v4'


# class SearchForm(FlaskForm):
#     anime_title = StringField("Enter Anime Title", validators=[DataRequired()])
#     search = SubmitField("Search")


def fetch_data(url):
    response = requests.get(f'{BASE_URL}/{url}')
    if response.status_code == 200:
        data = response.json()
        all_data = data['data']
        return all_data
    else:
        print("Something went wrong!")


@app.route('/', methods=['GET', 'POST'])
def home():
    popular_anime = fetch_data("top/anime?filter=bypopularity")
    return render_template("index.html", animes=popular_anime)


@app.route('/search', methods=["GET", "POST"])
def search():
    title = request.form['title']
    if request.method == "POST":
        search_anime = fetch_data(f'anime?q={title}')
        return render_template('index.html', animes=search_anime)

@app.route('/upcoming')
def upcoming():
    upcoming_anime = fetch_data("top/anime?filter=upcoming")
    return render_template("index.html", animes=upcoming_anime)


@app.route('/airing')
def airing():
    airing_anime = fetch_data("top/anime?filter=airing")
    return render_template('index.html', animes=airing_anime)


@app.route('/favorite')
def favorite():
    favorite_anime = fetch_data("top/anime?filter=favorite")
    return render_template ('index.html', animes=favorite_anime)

@app.route('/anime/<int:id>', methods=["GET", "POST"])
def show_anime(id):
    show_anime = fetch_data(f"anime/{id}/full")
    return render_template("show.html", anime=show_anime)


if __name__ == '__main__':
    app.run(debug=True)

