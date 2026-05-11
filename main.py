from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_SEARCH_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
API_MOVIE_ENDPOINT = "https://api.themoviedb.org/3/movie/"
API_TOKEN = os.getenv("TMDB_API_TOKEN")
API_KEY = os.getenv("TMDB_API_KEY")

api_headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {API_TOKEN}"
            }

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_collection.db"
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# with app.app_context():
#     db.create_all()

class EditMovieForm(FlaskForm):
    rating = StringField("Your Rating out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    # with app.app_context():
    #     new_movie = Movie(
    #         title="Avatar The Way of Water",
    #         year=2022,
    #         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #         rating=7.3,
    #         ranking=9,
    #         review="I liked the water.",
    #         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    #     )
    #     db.session.add(new_movie)
    #     db.session.commit(
    result = db.session.execute(db.select(Movie).order_by(desc(Movie.rating)))
    all_movies = result.scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = i + 1

    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = EditMovieForm()
    with app.app_context():
        movie_to_edit = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        if form.validate_on_submit():
            movie_to_edit.rating = request.form.get("rating")
            movie_to_edit.review = request.form.get("review")
            db.session.commit()

            return redirect(url_for('home'))
        else:
            return render_template("edit.html", movie=movie_to_edit, form=form)

@app.route("/delete/<id>")
def delete(id):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()

        return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    with app.app_context():
        if form.validate_on_submit():
            params = {
                "query": request.form['title'],
                "include_adult": "false",
                "languaje": "en-US",
            }
            response = requests.get(url=API_SEARCH_ENDPOINT, headers=api_headers, params=params)
            response.raise_for_status()
            movie_data = response.json()['results']
            return render_template("select.html", movies=movie_data)
        else:
            return render_template("add.html", form=form)

@app.route("/select/<id>", methods=["GET", "POST"])
def select(id):
    with app.app_context():
        params = {"movie_id": id}
        response = requests.get(url=f"{API_MOVIE_ENDPOINT}{id}", headers=api_headers)
        response.raise_for_status()
        data = response.json()

        new_movie = Movie(
            title = data['title'],
            description = data['overview'],
            img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
            year = int((data['release_date'])[:4]),
            review = "",
            rating = 0,
            ranking = 10
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('edit', id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
