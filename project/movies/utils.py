import requests

from project.settings import API_KEY_TMDB

def get_search_list(search_string=None, page=1):
    url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}"
    if search_string != None and search_string != '':
        url = f"https://api.themoviedb.org/3/search/movie?query={search_string}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    result = requests.get(url, headers=headers).json()
    return result