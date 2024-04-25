import requests

from django.shortcuts import render
from django.views.generic import DetailView, ListView


class MoovieListView(ListView):
    template_name = 'movie/movie_list.html'

    def get_queryset(self):
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page']
        url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZTU5NGUzOWZlNGYwZmI0NzcwYzc5OWZkNTUxYzE2ZCIsInN1YiI6IjY2MWVhNDEzM2M0MzQ0MDE3YzAzMjc5NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EHbcVCrBYDitzJskmX2t8LHJ1sxieOBWftpEl2Xr7iI"
        }
        result = requests.get(url, headers=headers).json()['results']
        return result

    def get_context_data(self):
        context = super().get_context_data()
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page']
        context['page'] = page
        context['previous_page'] = page - 1
        context['previous_previous_page'] = page - 2
        context['next_page'] = page + 1
        context['next_next_page'] = page + 2
        return context


class MoovieDetailView(DetailView):
    template_name = 'movie/movie_detail.html'
    context_object_name = 'movie'

    def get_object(self, **kwargs):
        id = self.kwargs['id']

        url_movie = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
        url_actors = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"
        url_trailer = f"https://api.themoviedb.org/3/movie/{id}/videos?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZTU5NGUzOWZlNGYwZmI0NzcwYzc5OWZkNTUxYzE2ZCIsInN1YiI6IjY2MWVhNDEzM2M0MzQ0MDE3YzAzMjc5NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EHbcVCrBYDitzJskmX2t8LHJ1sxieOBWftpEl2Xr7iI"
        }

        movie = requests.get(url_movie, headers=headers).json()
        actors = requests.get(url_actors, headers=headers).json()['cast'][:3]
        videos = requests.get(url_trailer, headers=headers).json()['results']
        trailer = ''
        for video in videos:
            if video['type'] == 'Trailer':
                movie['trailer'] = video
                break
        movie['actors'] = actors
        return movie
