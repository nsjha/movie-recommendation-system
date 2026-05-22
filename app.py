import joblib
from pathlib import Path

import pandas as pd
import requests
from flask import Flask, jsonify, render_template_string, request

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

# =========================================================
# TMDB API
# =========================================================

TMDB_API_KEY = "210321c1a96b9647a15f08baace43cdf"

TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie/{}"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500{}"

# =========================================================
# LOAD DATA
# =========================================================

movies = pd.DataFrame(
    joblib.load(BASE_DIR / "movies_dict.pkl")
)

similarity = joblib.load(
    BASE_DIR / "similarity.pkl"
)

movie_titles = sorted(
    movies["title"].dropna().unique()
)

# =========================================================
# FETCH POSTER
# =========================================================

def fetch_poster(movie_id):

    try:

        response = requests.get(
            TMDB_MOVIE_URL.format(movie_id),
            params={
                "api_key": TMDB_API_KEY
            },
            timeout=10
        )

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:

            return TMDB_IMAGE_URL.format(
                poster_path
            )

        return None

    except:
        return None

# =========================================================
# SEARCH MOVIES
# =========================================================

def search_movies(query):

    query = query.lower().strip()

    results = []

    # Startswith results first
    for title in movie_titles:

        if title.lower().startswith(query):

            results.append(title)

    # Partial results
    for title in movie_titles:

        if query in title.lower():

            if title not in results:

                results.append(title)

    return results[:8]

# =========================================================
# BEST MATCH
# =========================================================

def get_best_match(user_input):

    user_input = user_input.lower().strip()

    # Exact
    for title in movie_titles:

        if title.lower() == user_input:

            return title

    # Startswith
    for title in movie_titles:

        if title.lower().startswith(user_input):

            return title

    # Partial
    for title in movie_titles:

        if user_input in title.lower():

            return title

    return None

# =========================================================
# RECOMMENDATION FUNCTION
# =========================================================

def recommend(movie_name):

    matched_movie = get_best_match(movie_name)

    if not matched_movie:

        return []

    movie_index = movies[
        movies["title"] == matched_movie
    ].index[0]

    distances = similarity[movie_index]

    recommended_movies = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for movie in recommended_movies:

        index = movie[0]

        title = movies.iloc[index]["title"]

        movie_id = movies.iloc[index]["movie_id"]

        poster = fetch_poster(movie_id)

        recommendations.append({

            "title": title,
            "poster": poster

        })

    return recommendations

# =========================================================
# HTML UI
# =========================================================

HTML = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Movie Recommendation System</title>

<link rel="preconnect"
href="https://fonts.googleapis.com">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap"
rel="stylesheet">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Poppins',sans-serif;
}

body{

    background:
    radial-gradient(circle at top left,
    #0f172a,
    #020617 60%);

    color:white;

    min-height:100vh;

    overflow-x:hidden;
}

/* ========================================= */
/* CONTAINER */
/* ========================================= */

.container{

    width:min(1450px,94%);

    margin:auto;

    padding:40px 0 70px;
}

/* ========================================= */
/* HERO */
/* ========================================= */

.hero{

    margin-bottom:50px;
}

.heading{

    font-size:clamp(52px,9vw,120px);

    font-weight:800;

    line-height:0.95;

    background:linear-gradient(
        to right,
        #ffffff,
        #93c5fd,
        #60a5fa
    );

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

    letter-spacing:-4px;

    margin-bottom:25px;

    animation:fadeUp 1s ease;
}

.heading span{

    display:block;
}

.subtitle{

    color:#94a3b8;

    font-size:clamp(16px,2vw,24px);

    max-width:850px;

    line-height:1.7;

    animation:fadeUp 1.3s ease;
}

/* ========================================= */
/* SEARCH */
/* ========================================= */

.search-wrapper{

    position:relative;

    margin-top:45px;

    margin-bottom:20px;
}

input{

    width:100%;

    padding:24px 28px;

    border-radius:22px;

    border:2px solid rgba(96,165,250,0.5);

    background:rgba(30,41,59,0.92);

    backdrop-filter:blur(10px);

    color:white;

    font-size:clamp(18px,2vw,24px);

    outline:none;

    transition:0.3s;
}

input::placeholder{

    color:#7c8aa0;
}

input:focus{

    border-color:#60a5fa;

    box-shadow:
    0 0 25px rgba(59,130,246,0.35);

    transform:scale(1.01);
}

/* ========================================= */
/* SUGGESTIONS */
/* ========================================= */

.suggestions{

    position:absolute;

    width:100%;

    background:#172033;

    border-radius:18px;

    overflow:hidden;

    margin-top:10px;

    z-index:999;

    border:1px solid #334155;

    box-shadow:0 20px 40px rgba(0,0,0,0.45);
}

.suggestion-item{

    padding:18px 24px;

    cursor:pointer;

    font-size:18px;

    transition:0.25s;

    border-bottom:1px solid #273449;
}

.suggestion-item:hover{

    background:#243041;

    padding-left:32px;
}

/* ========================================= */
/* MOVIES GRID */
/* ========================================= */

.movies-grid{

    display:grid;

    grid-template-columns:
    repeat(auto-fit,minmax(240px,1fr));

    gap:30px;

    margin-top:55px;
}

/* ========================================= */
/* CARD */
/* ========================================= */

.movie-card{

    background:rgba(23,32,51,0.95);

    border-radius:24px;

    overflow:hidden;

    border:1px solid rgba(71,85,105,0.5);

    transition:0.35s;

    display:flex;

    flex-direction:column;

    height:100%;
}

.movie-card:hover{

    transform:
    translateY(-10px)
    scale(1.02);

    box-shadow:
    0 25px 45px rgba(0,0,0,0.5);
}

/* ========================================= */
/* IMAGE */
/* ========================================= */

.movie-card img{

    width:100%;

    aspect-ratio:2/3;

    object-fit:cover;

    display:block;
}

.poster-placeholder{

    width:100%;

    aspect-ratio:2/3;

    display:flex;

    align-items:center;

    justify-content:center;

    background:#334155;

    color:#cbd5e1;

    font-size:18px;
}

/* ========================================= */
/* INFO */
/* ========================================= */

.movie-info{

    padding:22px;

    flex-grow:1;

    display:flex;

    align-items:flex-start;
}

.movie-title{

    font-size:clamp(20px,2vw,30px);

    font-weight:600;

    line-height:1.35;
}

.error{

    color:#f87171;

    font-size:20px;

    margin-top:15px;
}

/* ========================================= */
/* ANIMATION */
/* ========================================= */

@keyframes fadeUp{

    from{

        opacity:0;

        transform:translateY(30px);
    }

    to{

        opacity:1;

        transform:translateY(0);
    }
}

/* ========================================= */
/* TABLET */
/* ========================================= */

@media(max-width:992px){

    .movies-grid{

        grid-template-columns:
        repeat(2,1fr);

        gap:24px;
    }

    .heading{

        letter-spacing:-2px;
    }
}

/* ========================================= */
/* MOBILE */
/* ========================================= */

@media(max-width:600px){

    .container{

        width:92%;

        padding-top:30px;
    }

    .movies-grid{

        grid-template-columns:1fr;

        gap:22px;
    }

    input{

        padding:18px 20px;

        border-radius:16px;
    }

    .movie-info{

        padding:18px;
    }

    .suggestion-item{

        font-size:16px;

        padding:15px 18px;
    }

    .heading{

        line-height:1;

        margin-bottom:18px;
    }

    .subtitle{

        line-height:1.5;
    }
}

</style>

</head>

<body>

<div class="container">

<!-- HERO -->

<div class="hero">

<h1 class="heading">

<span>Movie Recommendation</span>

<span>System</span>

</h1>

<p class="subtitle">

Search any movie and instantly discover top 5 similar recommendations with beautiful movie posters and smart autocomplete search.

</p>

</div>

<!-- SEARCH -->

<form id="movieForm" method="POST">

<div class="search-wrapper">

<input
    type="text"
    id="movieInput"
    name="movie"
    placeholder="Type movie name like Harry Potter..."
    autocomplete="off"
    value="{{selected_movie}}"
/>

<div class="suggestions"
id="suggestions"></div>

</div>

</form>

{% if error %}

<div class="error">
{{error}}
</div>

{% endif %}

<!-- MOVIES -->

{% if recommendations %}

<div class="movies-grid">

{% for movie in recommendations %}

<div class="movie-card">

{% if movie.poster %}

<img src="{{movie.poster}}"
alt="{{movie.title}}">

{% else %}

<div class="poster-placeholder">
Poster unavailable
</div>

{% endif %}

<div class="movie-info">

<div class="movie-title">
{{movie.title}}
</div>

</div>

</div>

{% endfor %}

</div>

{% endif %}

</div>

<script>

const input =
document.getElementById("movieInput");

const suggestions =
document.getElementById("suggestions");

const form =
document.getElementById("movieForm");

/* ========================================= */
/* AUTOCOMPLETE */
/* ========================================= */

input.addEventListener("keyup", async () => {

    const query = input.value.trim();

    if(query.length === 0){

        suggestions.innerHTML = "";

        return;
    }

    const response =
    await fetch(`/search?q=${query}`);

    const data =
    await response.json();

    suggestions.innerHTML = "";

    data.forEach(movie => {

        const div =
        document.createElement("div");

        div.classList.add(
        "suggestion-item"
        );

        div.innerText = movie;

        div.onclick = () => {

            input.value = movie;

            suggestions.innerHTML = "";

            form.submit();
        };

        suggestions.appendChild(div);
    });
});

/* ========================================= */
/* ENTER KEY */
/* ========================================= */

input.addEventListener(
"keypress",
function(event){

    if(event.key === "Enter"){

        event.preventDefault();

        form.submit();
    }
});

/* ========================================= */
/* HIDE SUGGESTIONS */
/* ========================================= */

document.addEventListener(
"click",
function(event){

    if(
    !event.target.closest(
    ".search-wrapper"
    )){

        suggestions.innerHTML = "";
    }
});

</script>

</body>
</html>

"""

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []

    selected_movie = ""

    error = None

    if request.method == "POST":

        selected_movie = request.form.get(
            "movie",
            ""
        ).strip()

        recommendations = recommend(
            selected_movie
        )

        if not recommendations:

            error = (
            "Movie not found. "
            "Try another movie."
            )

    return render_template_string(

        HTML,

        recommendations=recommendations,

        selected_movie=selected_movie,

        error=error
    )

# =========================================================
# SEARCH ROUTE
# =========================================================

@app.route("/search")
def search():

    query = request.args.get("q", "")

    results = search_movies(query)

    return jsonify(results)

# =========================================================
# HEALTH ROUTE
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status":"ok"
    })

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8000,

        debug=True
    )
