import requests
from flask import Flask, render_template, request


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


@app.route('/anime/<int:id>')
def show_anime(id):
    show_anime = fetch_data(f"anime/{id}/full")
    anime_characters = fetch_data(f"anime/{id}/characters")
    return render_template("show.html", anime=show_anime, anime_characters=anime_characters)

@app.route('/characters', methods=["GET", "POST"])
def characters():
    search_character = request.form['character_name']
    if request.method == "POST":
        characters = fetch_data(f"characters?q={search_character}")
        return render_template('characters.html', characters=characters)

@app.route('/character/<int:id>')
def show_character(id):
    character = fetch_data(f"characters/{id}/full")
    character_pic = fetch_data(f"characters/{id}/pictures")
    return render_template('characterShow.html', character=character, character_pic=character_pic)

@app.route('/characters/top')
def top_characters():
    top_characters = fetch_data("top/characters")
    return render_template('characters.html', characters=top_characters)

if __name__ == '__main__':
    app.run(debug=True)

