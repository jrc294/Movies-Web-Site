import media
import fresh_tomatoes
import urllib
import json

#Constants
API_KEY = ""
IMDB_POSTER_PATH_URL = "http://image.tmdb.org/t/p/w342/"
YOUTUBE_URL = "https://www.youtube.com/watch?v="
IMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie?api_key="
IMDB_SORT_ORDER = "&sort_by=popularity.desc"
IMDB_VIDEO_URL = "http://api.themoviedb.org/3/movie/"
IMDB_VIDEO_SUFFIX = "/videos?api_key="

def get_data(url):

    #Return API response json as defined by the url
    connection = urllib.urlopen(url)
    response = connection.read()
    response_json = json.loads(response)
    connection.close()
    return response_json

def load_movies():
    
    # This function returns a list of six movie objects that contain a movies
    # title, overview, poster path and youtube link

    # Retrieve a list of the most popular movies from IMDB in json format and
    # store in movie_data
    url = IMDB_DISCOVER_URL + API_KEY + IMDB_SORT_ORDER
    movie_data = get_data(url)
    movie_list = []

    # Loop thru the top six results in the json data, and extract the movie
    # title, storyline, poster path and movie id. The movie id will be used in
    # a second api call to the IMDB, that will retrieve a list of associated
    # youtube videos.
    for num in range(0,6):
        # Get the movie title, storyline, poster path and movie id from the
        # json data
        title = movie_data['results'][num]['title']
        storyline = movie_data['results'][num]['overview']
        poster_path = IMDB_POSTER_PATH_URL + movie_data['results'][num]['poster_path']
        movie_id = movie_data['results'][num]['id']

        # Make an api call to the IMDB and retrieve a list of associated youtube
        # videos and store the json response in video_data
        url = IMDB_VIDEO_URL + str(movie_id) + IMDB_VIDEO_SUFFIX + API_KEY
        video_data = get_data(url)

        # Logic to look for the best video to use. As a minimun, the video must
        # be on youtube, but a video with 'trailer' in the name is preferable,
        # and a video of type 'teaser' is even more preferable. The logic
        # should result in a reasonable choice.
        best_match_index = -1
        youtube_video_index = -1
        trailer_video_index = -1
        teaser_video_index = -1
        index = 0
        trailer_youtube_url = ""
        while (index < len(video_data['results'])):
            if (video_data['results'][index]['site'].upper() == "YOUTUBE"):
                youtube_video_index = index
                if (video_data['results'][index]['name'].
                    upper().find("TRAILER") != -1):
                    trailer_video_index = index
                    if (video_data['results'][index]['type'].
                        upper().find("TEASER") != -1):
                        teaser_video_index = index
            index = index + 1
        if (teaser_video_index != -1):
            best_match_index = teaser_video_index
        elif (trailer_video_index != -1):
            best_match_index = trailer_video_index
        elif (youtube_video_index != -1):
            best_match_index = youtube_video_index

        # Add the video URL resulting from the best possible match
        if (best_match_index != -1):
            trailer_youtube_url = YOUTUBE_URL + video_data['results'][best_match_index]['key']

        # Create the movie object and add it to the list
        movie = media.Movie(title, storyline, poster_path, trailer_youtube_url)
        movie_list.append(movie)

    return movie_list             

movies = load_movies()
fresh_tomatoes.open_movies_page(movies)
