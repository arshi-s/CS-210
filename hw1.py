# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO AUTOLAB

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    movie_ratings=defaultdict(list)
    with open(f, 'r') as file:
        for line in file:
            line_part = line.strip().split('|') #separate line into parts
            movie = line_part[0]  #movie title and year
            rating = float(line_part[1]) 

            movie_ratings[movie].append(rating)  #append movie rating to list
    return dict(movie_ratings)
    

# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    movie_genres={}
    with open(f, "r") as file:
        for line in file:
            line_part = line.strip().split('|')
            genre = line_part[0] #genre
            movie = line_part[2] #movie and year

            movie_genres[movie] = genre
    return movie_genres

# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    genre_to_movie = defaultdict(list)
    for movie, genre in d.items():
        genre_to_movie[genre].append(movie)
    return dict(genre_to_movie)

    
# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    movie_to_average = {}
    for movie,ratings in d.items():
        movie_to_average[movie] = sum(ratings) / len(ratings)
    return movie_to_average    
    
# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    sorted_movies_by_rating = sorted(d.items(), key=lambda x: x[1], reverse=True)
    top_movies_from_ratings = dict(sorted_movies_by_rating[:n])
    return top_movies_from_ratings
    
# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    filtered_movies = {movie: rating for movie, rating in d.items() if rating>=thres_rating}
    return filtered_movies
    
# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    movies_in_genre = genre_to_movies.get(genre, [])
    genre_movie_ratings = {movie: movie_to_average_rating[movie] for movie in movies_in_genre if movie in movie_to_average_rating}
    sorted_movies = dict(sorted(genre_movie_ratings.items(), key = lambda item: item[1], reverse=True))
    return dict(list(sorted_movies.items())[:n])
    
# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    movies_in_genre = genre_to_movies.get(genre, [])
    rated_movies = [movie_to_average_rating[movie] for movie in movies_in_genre if movie in movie_to_average_rating]
    if len(rated_movies)==0:
        return 0
    return sum(rated_movies)/len(rated_movies)  
    
# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    genre_avg_ratings = {
        genre: get_genre_rating(genre, genre_to_movies, movie_to_average_rating)
        for genre in genre_to_movies
    }
    sorted_genres = sorted(genre_avg_ratings.items(), key = lambda x: x[1], reverse=True)
    return dict(sorted_genres[:n])

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    user_ratings_to_movies = {}
    with open(f, "r") as file:
        for line in file:
            movie, rating, user_id = line.strip().split("|")
            rating = float(rating)
            user_id = int(user_id)

            if user_id not in user_ratings_to_movies:
                user_ratings_to_movies[user_id] = []
            user_ratings_to_movies[user_id].append((movie, rating))
    return user_ratings_to_movies
    
# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    genre_ratings = {}
    for movie, rating in user_to_movies[user_id]:
        if movie in movie_to_genre:
            genre = movie_to_genre[movie]
            if genre not in genre_ratings:
                genre_ratings[genre] = [0,0]
            genre_ratings[genre][0] += rating
            genre_ratings[genre][1] += 1

    top_user_genre = max(genre_ratings, key=lambda g: genre_ratings[g][0]/genre_ratings[g][1]) 
    return top_user_genre
    
# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    genre_movies = {movie for movie, genre in movie_to_genre.items() if genre==top_genre}
    user_rated_movies = {movie for movie, _ in user_to_movies.get(user_id, [])}
    unrated_movies = genre_movies - user_rated_movies
    ratings_unrated_movies = {movie: movie_to_average_rating[movie] for movie in unrated_movies if movie in movie_to_average_rating}
    top_recs = dict(sorted(ratings_unrated_movies.items(), key=lambda x: x[1], reverse=True)[:3])
    return top_recs

# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading

    #ratings=read_ratings_data("movie_ratings.txt")  #test read_ratings_data
    #print("Movie Ratings Dictionary:", ratings)

    #genres=read_movie_genre("movie_genres.txt")  #test read_movie_genre
    #print("Movie Genres Dictionary:", genres)

    """d = {"Toy Story (1995)": "Adventure", #test create_genre_dict
    "Golden Eye (1995)": "Action",
    "Jumanji (1995)": "Adventure"}
    print(create_genre_dict(d))"""

    """movie_ratings = {    #test calculate_average_rating
    "Spider-Man (2002)": [3, 2, 4, 5],
    "Titanic (1997)": [5, 4, 5, 3, 4],}
    print(calculate_average_rating(movie_ratings))"""

    """movie_ratings = {    #test get_popular_movies
    "Spider-Man (2002)": 3.5,
    "Titanic (1997)": 4.2,
    "The Godfather (1972)": 4.9,
    "Inception (2010)": 4.8,
    "The Dark Knight (2008)": 4.7,
    "Forrest Gump (1994)": 4.6}
    print(get_popular_movies(movie_ratings, 3))"""

    """movie_ratings = {    #test filter_movies
    "Spider-Man (2002)": 3.5,
    "Titanic (1997)": 4.2,
    "The Godfather (1972)": 4.9,
    "Inception (2010)": 4.8,
    "The Dark Knight (2008)": 4.7,
    "Forrest Gump (1994)": 4.6}
    print(filter_movies(movie_ratings, 3.5))"""

    #test get_popular_in_genre, get_genre_rating, genre_popularity
    """genre_to_movies = {
        "Action": ["Mad Max: Fury Road (2015)", "Die Hard (1988)", "John Wick (2014)"],
        "Drama": ["The Shawshank Redemption (1994)", "Forrest Gump (1994)", "Titanic (1997)"],
        "Sci-Fi": ["Inception (2010)", "Interstellar (2014)", "The Matrix (1999)"]
    }
    movie_ratings = {
        "Mad Max: Fury Road (2015)": 4.8,
        "Die Hard (1988)": 4.5,
        "John Wick (2014)": 4.3,
        "The Shawshank Redemption (1994)": 4.9,
        "Forrest Gump (1994)": 4.6,
        "Titanic (1997)": 4.2,
        "Inception (2010)": 4.8,
        "Interstellar (2014)": 4.7,
        "The Matrix (1999)": 4.6
    }"""
    #print(get_popular_in_genre("Action", genre_to_movies, movie_ratings, 2)) 
    #print(get_genre_rating("Drama", genre_to_movies, movie_ratings))
    #print(genre_popularity(genre_to_movies, movie_ratings, n=3))

    #test read_user_ratings
    """user_ratings = read_user_ratings("movie_ratings.txt")
    for user, movies in list(user_ratings.items())[:3]:  
        print(f"User {user}: {movies}")"""
    
    # test get_user_genre
    """user_to_movies = {
        1: [("Toy Story (1995)", 4.0), ("Heat (1995)", 4.0)],
        6: [("Jumanji (1995)", 4.0), ("GoldenEye (1995)", 3.0), ("Father of the Bride Part II (1995)", 5.0)]
    }
    movie_to_genre = {
        "Toy Story (1995)": "Animation",
        "Heat (1995)": "Action",
        "Jumanji (1995)": "Fantasy",
        "GoldenEye (1995)": "Action",
        "Father of the Bride Part II (1995)": "Comedy"
    }
    top_genre_user6 = get_user_genre(6, user_to_movies, movie_to_genre) # Find top genre for user 6
    print(f"User 6's top genre: {top_genre_user6}")"""

    #test reccomend_movies
    """user_to_movies = {
        1: [("Toy Story (1995)", 4.0), ("Heat (1995)", 4.0)],
        6: [("Jumanji (1995)", 4.0), ("GoldenEye (1995)", 3.0), ("Father of the Bride Part II (1995)", 5.0)]
    }
    movie_to_genre = {
        "Toy Story (1995)": "Animation",
        "Heat (1995)": "Action",
        "Jumanji (1995)": "Fantasy",
        "GoldenEye (1995)": "Action",
        "Father of the Bride Part II (1995)": "Comedy",
        "Shrek (2001)": "Animation",
        "Finding Nemo (2003)": "Animation",
        "The Incredibles (2004)": "Animation",
        "Die Hard (1988)": "Action",
        "Mad Max: Fury Road (2015)": "Action"
    }
    movie_to_avg_rating = {
        "Toy Story (1995)": 4.3,
        "Heat (1995)": 4.0,
        "Jumanji (1995)": 3.5,
        "GoldenEye (1995)": 3.0,
        "Father of the Bride Part II (1995)": 4.2,
        "Shrek (2001)": 4.4,
        "Finding Nemo (2003)": 4.6,
        "The Incredibles (2004)": 4.5,
        "Die Hard (1988)": 4.7,
        "Mad Max: Fury Road (2015)": 4.8
    }
    recommendations_user1 = recommend_movies(1, user_to_movies, movie_to_genre, movie_to_avg_rating)
    print(f"Recommended movies for User 1: {recommendations_user1}")"""

    


    
# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions
    
# program will start at the following main() function call
# when you execute hw1.py
main()

    
