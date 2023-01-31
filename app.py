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

# API C: Get top 5 movies rated by a specific user
class Top5UserRatedMovies(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return {"error": "User ID must be provided."}, 400

        if user_id not in [user["user_id"] for user in users]:
            return {"error": "User with ID {} not found."}, 404

        user_ratings = []
        for movie in movies:
            movie_ratings = movie.get("ratings", [])
            for rating in movie_ratings:
                if rating["user_id"] == user_id:
                    user_ratings.append({"movie": movie, "rating": rating["rating"]})
                    break

        sorted_movies = sorted(user_ratings, key=lambda x: x["rating"], reverse=True)

        top_5 = sorted_movies[:5]
        return top_5


# API D: Add or update a rating for a movie by a user
class AddUpdateRating(Resource):
    def post(self):
        user_id = request.json.get("user_id")
        movie_id = request.json.get("movie_id")
        rating = request.json.get("rating")
        if not user_id or not movie_id or not rating:
            return {"error": "User ID, movie ID, and rating must be provided."}, 400

        movie = next((movie for movie in movies if movie["movie_id"] == movie_id), None)
        if not movie:
            return {"error": f"Movie with ID {movie_id} not found."}, 404

        user = next((user for user in users if user["user_id"] == user_id), None)
        if not user:
            return {"error": f"User with ID {user_id} not found."}, 404

        rating_found = next((rating for rating in movie["ratings"] if rating["user_id"] == user_id), None)
        if rating_found:
            rating_found["rating"] = rating
        else:
            movie["ratings"].append({"user_id": user_id, "rating": rating})

        return {"message": "Rating updated successfully."}, 200