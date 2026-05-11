# Top Movies Collection

A Flask web application to manage a personal top-movies list. Search movies by title using the TMDB API, rate and review them, and they are automatically ranked by your rating.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)

## Features

- Search movies by title via the [TMDB API](https://www.themoviedb.org/documentation/api)
- Store movie data (title, year, poster, description) in a local SQLite database
- Add your own rating and review for each movie
- Automatic ranking sorted by rating
- Delete movies from the collection
- Animated 3D card flip UI to reveal movie details

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-WTF
- **Database:** SQLite with SQLAlchemy ORM (Mapped / DeclarativeBase)
- **Frontend:** Jinja2 templates, Bootstrap 5, CSS 3D transforms
- **External API:** The Movie Database (TMDB) REST API

## Project Structure

```
top-movies/
├── main.py              # App entry point, routes, DB models
├── requirements.txt     # Python dependencies
├── static/
│   └── css/
│       └── styles.css   # Card flip animation and layout
└── templates/
    ├── base.html        # Base template
    ├── index.html       # Movie card grid
    ├── add.html         # Search form
    ├── select.html      # Search results
    └── edit.html        # Rate & review form
```

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/top-movies.git
cd top-movies
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the root directory:
```
TMDB_API_KEY=your_tmdb_api_key
TMDB_API_TOKEN=your_tmdb_read_access_token
SECRET_KEY=your_secret_key
```

**5. Initialize the database**

Uncomment the `db.create_all()` block in `main.py` on first run, then re-comment it.

**6. Run the app**
```bash
python main.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## API Integration

Movies are fetched from the [TMDB API](https://www.themoviedb.org/documentation/api):

- `GET /3/search/movie` — search by title
- `GET /3/movie/{id}` — fetch full movie details (poster, overview, release date)

## Database Model

| Column      | Type    | Description                  |
|-------------|---------|------------------------------|
| id          | Integer | Primary key                  |
| title       | String  | Movie title (unique)         |
| year        | Integer | Release year                 |
| description | String  | Movie overview               |
| rating      | Float   | User rating (0–10)           |
| ranking     | Integer | Auto-calculated from rating  |
| review      | String  | User review                  |
| img_url     | String  | TMDB poster URL              |
