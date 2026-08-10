import os
from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/movie", methods=['GET', 'POST'])
def movie():
    user_search = request.form.get("movie_name")
    if not user_search:
        return redirect(url_for('home'))
        
    user_search = user_search.strip()
    api_key = os.getenv("OMDB_API_KEY")
    
    api_url = "http://www.omdbapi.com/"
    query_parameters = {
        "t": user_search,
        "apikey": api_key
    }
    
    reponse = requests.get(api_url, params=query_parameters)
    data = reponse.json()
    
    if data.get("Response") == "False":
        return f"movie not found please try again"
    
    movie_name = data["Title"]
    director_name = data["Director"]
    year_date = data["Year"]
    rating_review = data["imdbRating"]
    movie_plot = data.get("Plot", "No description available.")
    movie_poster = data.get("Poster", "N/A")

    return render_template("movies.html", movie=movie_name, director=director_name, year=year_date, rating=rating_review, plot=movie_plot, poster=movie_poster)

if __name__ == '__main__':
    app.run(debug=True)
