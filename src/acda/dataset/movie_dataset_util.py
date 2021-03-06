'''
Utility module for working on the movielens dataset
'''

import pandas as pd
import sklearn.model_selection as ms

RATINGS_FILE = "../../../dataset/movielens/ratings.csv"
RATINGS_CONTEXT_FILE = "../../../dataset/movielens/rating_context.csv"
RATINGS_SCORE_CONTEXT_FILE = "../../../dataset/movielens/rating_score_context.csv"
MOVIES_FILE = "../../../dataset/movielens/movies.csv"
TAGS_FILE = "../../../dataset/movielens/tags.csv"


def generate_movie_dataset():
    ratings = pd.read_csv(RATINGS_FILE)
    movies = pd.read_csv(MOVIES_FILE)
    ratings_context = pd.merge(ratings, movies, on='movieId', how='left')
    ratings_context.to_csv(RATINGS_CONTEXT_FILE, index=False)

    
def update_movie_dataset():
    ratings = pd.read_csv(RATINGS_SCORE_CONTEXT_FILE)
    ratings.loc[ratings['score'] >= 5.0, 'rating'] = 1
    ratings.loc[ratings['score'] < 5.0, 'rating'] = 0
    ratings.to_csv(RATINGS_CONTEXT_FILE, index=False)

    
def perform_train_test_split():
    RATINGS_TRAIN_FILE = "../../../dataset/movielens/ratings_train.csv"
    RATINGS_TEST_FILE = "../../../dataset/movielens/ratings_test.csv"
    
    ratings = pd.read_csv(RATINGS_FILE)
    ratings.loc[ratings['score'] >= 5.0, 'rating'] = 1
    ratings.loc[ratings['score'] < 5.0, 'rating'] = 0
    ratings_sorted = ratings.sort_values(['timestamp'], ascending=True)
    # perform the train-test split
    train_ratings, test_ratings = ms.train_test_split(ratings_sorted, test_size=0.2, random_state=42)
    # split again to generate CV set
    train_ratings, cv_ratings = ms.train_test_split(train_ratings, test_size=0.25, random_state=42)
    train_ratings_set = train_ratings[['userId', 'movieId', 'rating']]
    test_ratings_set = test_ratings[['userId', 'movieId', 'rating']]

    train_ratings_set.to_csv(RATINGS_TRAIN_FILE, index=False)
    test_ratings_set.to_csv(RATINGS_TEST_FILE, index=False)


def generate_librec_rating_file():
    train_file = "../../../dataset/rsvp_chicago_train.csv"
    train_rating_file = "../../../dataset/rsvp_chicago_train_rating.csv"
    test_file = "../../../dataset/rsvp_chicago_test.csv"
    test_rating_file = "../../../dataset/rsvp_chicago_test_rating.csv"
    
    train_events = pd.read_csv(train_file)
    train_events_ratings = train_events[['memberId', 'eventId', 'rsvpRating']]
    
    test_events = pd.read_csv(test_file)
    test_events_ratings = test_events[['memberId', 'eventId', 'rsvpRating']]
        
    train_events_ratings.to_csv(train_rating_file, index=False)
    test_events_ratings.to_csv(test_rating_file, index=False)


def print_ratings_data(file_name):
    ratings = pd.read_csv(file_name)
    print("Total Ratings", len(ratings))
    print("Users:", len(ratings['userId'].unique()))
    print("Events:", len(ratings['movieId'].unique()))
    print("Positive Ratings:", len(ratings[ratings['rating'] == 1]))
    print("Negative Ratings:", len(ratings[ratings['rating'] == 0]))


def main():
    print("Main method")
    # perform_train_test_split()
    print_ratings_data(RATINGS_CONTEXT_FILE)
    print("Main method complete")


if __name__ == '__main__':
    main()
