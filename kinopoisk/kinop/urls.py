from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    MovieCarouselView,
    MoviesView,
    SeriesView,
    CartoonsView,
)

urlpatterns = [
    path("", MovieListView.as_view(), name="movie_list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movies/create/", MovieCreateView.as_view(), name="movie_create"),
    path("movies/<int:pk>/update/", MovieUpdateView.as_view(), name="movie_update"),
    path("movies/<int:pk>/delete/", MovieDeleteView.as_view(), name="movie_delete"),
    path("movies/", MoviesView.as_view(), name="movies"),
    path("series/", SeriesView.as_view(), name="series"),
    path("cartoon/", CartoonsView.as_view(), name="cartoon"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
