from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

movies = [{"movie_id": 1, "title": "Great Expectations", "yearOfRelease": 1998, "genre": "Romantic Drama", "ratings": [{"user_id": 1, "rating": 4},{"user_id": 2, "rating": 4},{"user_id": 3, "rating": 5}]},
          {"movie_id": 2, "title": "Hackers", "yearOfRelease": 1995, "genre": "Thriller", "ratings": [{"user_id": 1, "rating": 2},{"user_id": 2, "rating": 2},{"user_id": 3, "rating": 4}]},
          {"movie_id": 3, "title": "Johnny Mnemonic", "yearOfRelease": 1995, "genre": "Sci-Fi", "ratings": [{"user_id": 1, "rating": 2},{"user_id": 3, "rating": 5}]}]

users = [{"user_id":1, "firstName": "Fotis", "lastName": "Kitsantas"},
         {"user_id":2, "firstName": "Reina", "lastName": "Rapi"},
         {"user_id":3, "firstName": "Spiros", "lastName": "Zamprakos"}]

# API A: Filter movies
class FilterMovies(Resource):
    def get(self):
        movie_id = request.args.get("movie_id")
        title = request.args.get("title")
        yearOfRelease = request.args.get("yearOfRelease")
        genre = request.args.get("genre")
        if not movie_id and not title and not yearOfRelease and not genre:
            return {"error": "At least one filter criteria must be provided."}, 400

        filtered_movies = []
        for movie in movies:
            if movie_id and str(movie_id) != str(movie["movie_id"]):
                continue
            if title and title.lower() not in movie["title"].lower():
                continue
            if yearOfRelease and str(yearOfRelease) != str(movie["yearOfRelease"]):
                continue
            if genre and genre.lower() != movie["genre"].lower():
                continue
            filtered_movies.append(movie)
        return filtered_movies


# API B: Get top 5 movies by average ratings
class Top5Movies(Resource):
    def get(self):
        def calc_average_rating(movie):
            ratings = movie["ratings"]
            return round(sum(rating["rating"] for rating in ratings) / len(ratings) * 2) / 2 if ratings else 0

        sorted_movies = sorted(movies, key=lambda x: calc_average_rating(x), reverse=True)
        top_5 = sorted_movies[:5]
        for movie in top_5:
            movie['average_rating'] = calc_average_rating(movie)
        return top_5