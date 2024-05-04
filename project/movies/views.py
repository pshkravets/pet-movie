import requests

from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .forms import SearchMovieForm
from .utils import get_search_list
from project.settings import API_KEY_TMDB


class MoovieListView(ListView):
    template_name = 'movie/movie_list.html'

    def get_queryset(self):
        search = self.request.GET.get('search_field')
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page']
        response = get_search_list(search_string=search, page=page)
        return response['results']

    def get_context_data(self):
        context = super().get_context_data()
        context['pagination'] = True
        if self.request.GET.get('search_field') != None and self.request.GET.get('search_field') != '':
            context['pagination'] = False
        page = 1
        if 'page' in self.kwargs:
            page = self.kwargs['page']
        context['page'] = page
        context['previous_page'] = page - 1
        context['previous_previous_page'] = page - 2
        context['next_page'] = page + 1
        context['next_next_page'] = page + 2
        context['form'] = SearchMovieForm(self.request.GET)
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
