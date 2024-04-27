from django.urls import path

from .views import MoovieListView, MoovieDetailView

urlpatterns = [
    path('', MoovieListView.as_view(), name='movie-list'),
    path('<int:page>', MoovieListView.as_view(), name='movie-list-page'),
    path('detail/<int:id>', MoovieDetailView.as_view(), name='movie-detail'),
]
