import requests

from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.

class MooviewListView(ListView):
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