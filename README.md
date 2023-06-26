# Movies-API

Movies-API is a Python API built using Flask. It provides a series of endpoints that can be used by external entities (like browsers, mobile apps, or manual API calls) to interact with a stored movie database. The application provides various functionalities like querying movie details based on certain criteria, fetching top-rated movies overall and by specific users, and updating the movie ratings given by a user.

## Application Requirements Covered

Based on the source code, the following application requirements are addressed:

1. **Query Movie Data (Api A)**: API endpoint allows consumers to filter and return movie details based on provided criteria. These criteria include:
   - Title or partial title of the movie
   - Year of release
   - Genre(s)
   
   Endpoint responds with the appropriate HTTP status codes: 
   - `404` (if no movie is found based on the criteria)
   - `400` (if invalid/no criteria is given)
   - `200` (OK)

2. **Top 5 Movies Based on Total User Ratings (Api B)**: API endpoint returns the details of the top 5 movies based on the total user average ratings. In case of a rating tie, movies are returned in ascending alphabetical order by title.

3. **Top 5 Movies Rated by Specific User (Api C)**: API endpoint returns the top 5 movies based on the highest ratings given by a specific user. In case of a rating tie, movies are returned in ascending alphabetical order by title.

4. **Add or Update User Rating for a Movie (Api D)**: API endpoint allows consumers to add a rating (an integer between 1 and 5) to a movie for a certain user. If the user already had a rating for that movie, the old rating is updated to the new value. The API responds with appropriate HTTP status codes:
   - `404` (if movie or user is not found)
   - `400` (if rating is an invalid value)
   - `200` (OK)

5. **Average Rating Display**: When returning the average rating associated with a movie, the number is rounded to the nearest 0.5, as per the given requirements.
