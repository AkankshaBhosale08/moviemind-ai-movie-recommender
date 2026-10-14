from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Small built-in catalogue keeps the starter project easy to run and deploy.
# Poster images use TMDB image URLs; an internet connection is needed to load them.
MOVIES = [
    {"id": 1, "title": "Inception", "year": 2010, "genres": ["Sci-Fi", "Thriller"], "rating": 8.8,
     "description": "A skilled thief enters dreams to steal secrets—and is offered one last, unusual job.",
     "poster": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
     "keywords": ["dream", "mind", "heist", "action", "science", "mystery"]},
    {"id": 2, "title": "Interstellar", "year": 2014, "genres": ["Sci-Fi", "Drama"], "rating": 8.7,
     "description": "A team travels beyond Earth in a search for a future for humanity.",
     "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
     "keywords": ["space", "future", "science", "family", "emotional", "adventure"]},
    {"id": 3, "title": "The Dark Knight", "year": 2008, "genres": ["Action", "Crime"], "rating": 9.0,
     "description": "Batman faces a criminal mastermind who pushes Gotham into chaos.",
     "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
     "keywords": ["hero", "crime", "action", "city", "villain", "thriller"]},
    {"id": 4, "title": "Avatar", "year": 2009, "genres": ["Sci-Fi", "Adventure"], "rating": 7.9,
     "description": "On a distant moon, a former marine becomes part of a world unlike his own.",
     "poster": "https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg",
     "keywords": ["space", "nature", "adventure", "fantasy", "science"]},
    {"id": 5, "title": "Titanic", "year": 1997, "genres": ["Romance", "Drama"], "rating": 7.9,
     "description": "Two young people from different worlds meet aboard a famous ocean liner.",
     "poster": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
     "keywords": ["love", "romance", "emotional", "history", "ship"]},
    {"id": 6, "title": "The Avengers", "year": 2012, "genres": ["Action", "Sci-Fi"], "rating": 8.0,
     "description": "A group of heroes must work together to protect the world.",
     "poster": "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
     "keywords": ["hero", "team", "action", "science", "superhero", "adventure"]},
    {"id": 7, "title": "Jumanji: Welcome to the Jungle", "year": 2017, "genres": ["Comedy", "Adventure"], "rating": 6.9,
     "description": "Four students discover a game that turns their world into an adventure.",
     "poster": "https://image.tmdb.org/t/p/w500/pSgXKPU5h6U89ipF7HBYajvYt7j.jpg",
     "keywords": ["fun", "game", "comedy", "adventure", "friends"]},
    {"id": 8, "title": "The Notebook", "year": 2004, "genres": ["Romance", "Drama"], "rating": 7.8,
     "description": "A lifelong love story unfolds through memories and difficult choices.",
     "poster": "https://image.tmdb.org/t/p/w500/rNzQyW4f8B8cQeg7Dgj3n6eT5k9.jpg",
     "keywords": ["love", "romance", "emotional", "relationship"]},
    {"id": 9, "title": "Coco", "year": 2017, "genres": ["Animation", "Family"], "rating": 8.4,
     "description": "A music-loving boy journeys into a colourful world connected to his family history.",
     "poster": "https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg",
     "keywords": ["family", "music", "animation", "emotional", "adventure"]},
    {"id": 10, "title": "Finding Nemo", "year": 2003, "genres": ["Animation", "Adventure"], "rating": 8.2,
     "description": "A worried clownfish crosses the ocean to find his missing son.",
     "poster": "https://image.tmdb.org/t/p/w500/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg",
     "keywords": ["family", "ocean", "animation", "adventure", "comedy"]},
    {"id": 11, "title": "Dangal", "year": 2016, "genres": ["Drama", "Sport"], "rating": 8.3,
     "description": "A former wrestler trains his daughters to compete in wrestling.",
     "poster": "https://image.tmdb.org/t/p/w500/cJRPOLEexI7qp2DKtFfCh7YaaUG.jpg",
     "keywords": ["india", "family", "sport", "inspiration", "drama"]},
    {"id": 12, "title": "3 Idiots", "year": 2009, "genres": ["Comedy", "Drama"], "rating": 8.4,
     "description": "Three engineering students challenge pressure, expectations, and the meaning of success.",
     "poster": "https://image.tmdb.org/t/p/w500/66A9MqXOyVFCssoloscw79z8Tew.jpg",
     "keywords": ["india", "college", "friends", "comedy", "inspiration", "education"]},
    {"id": 13, "title": "Zindagi Na Milegi Dobara", "year": 2011, "genres": ["Drama", "Comedy"], "rating": 8.2,
     "description": "Three friends take a road trip that changes how they see life.",
     "poster": "https://image.tmdb.org/t/p/w500/2uWb0aSm3c9d9B0k8r6s4l8p9Yx.jpg",
     "keywords": ["india", "friends", "travel", "comedy", "life"]},
    {"id": 14, "title": "Drishyam", "year": 2015, "genres": ["Thriller", "Crime"], "rating": 8.2,
     "description": "A family man uses careful planning when his family faces a crisis.",
     "poster": "https://image.tmdb.org/t/p/w500/5l6h3n1z6Z8q3F5J7J9a8w8T4Y.jpg",
     "keywords": ["india", "mystery", "crime", "family", "thriller"]},
    {"id": 15, "title": "Inside Out", "year": 2015, "genres": ["Animation", "Family"], "rating": 8.1,
     "description": "A young girl's emotions navigate the challenges of growing up.",
     "poster": "https://image.tmdb.org/t/p/w500/2H1TmgdfNtsKlU9jKdeNyYL5y8T.jpg",
     "keywords": ["animation", "family", "emotional", "mind", "comedy"]},
    {"id": 16, "title": "Guardians of the Galaxy", "year": 2014, "genres": ["Action", "Sci-Fi", "Comedy"], "rating": 8.0,
     "description": "A band of unlikely space adventurers join forces to save the galaxy.",
     "poster": "https://image.tmdb.org/t/p/w500/r7vmZjiyZw9rpJMQJdXpjgiCOk9.jpg",
     "keywords": ["space", "team", "comedy", "action", "adventure", "science"]},
]

def recommend_movies(movie_id, limit=6):
    """Content-based recommendation using genre and keyword overlap."""
    selected = next((movie for movie in MOVIES if movie["id"] == movie_id), None)
    if not selected:
        return []

    scored = []
    for movie in MOVIES:
        if movie["id"] == movie_id:
            continue
        shared_genres = set(selected["genres"]) & set(movie["genres"])
        shared_keywords = set(selected["keywords"]) & set(movie["keywords"])
        # Genres carry more weight than descriptive keywords.
        score = len(shared_genres) * 3 + len(shared_keywords)
        if score > 0:
            scored.append((score, movie["rating"], movie))

    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [
        {**movie, "match": min(99, round(55 + score * 5))}
        for score, _, movie in scored[:limit]
    ]

@app.route("/")
def index():
    genres = sorted({genre for movie in MOVIES for genre in movie["genres"]})
    return render_template("index.html", movies=MOVIES, genres=genres)

@app.route("/api/movies")
def api_movies():
    query = request.args.get("q", "").strip().lower()
    genre = request.args.get("genre", "").strip()
    filtered = [
        movie for movie in MOVIES
        if (not query or query in movie["title"].lower()
            or query in movie["description"].lower()
            or any(query in keyword for keyword in movie["keywords"]))
        and (not genre or genre in movie["genres"])
    ]
    return jsonify(filtered)

@app.route("/api/recommend/<int:movie_id>")
def api_recommend(movie_id):
    return jsonify(recommend_movies(movie_id))

if __name__ == "__main__":
    app.run(debug=True)
