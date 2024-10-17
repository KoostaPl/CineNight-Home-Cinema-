from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .forms import MovieForm
from django.views import View
from .models import Movie, Genre, Director, MediaType
from django.shortcuts import get_object_or_404


def superuser_required(view_func):
    decorator_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorator_view_func


class MovieListView(View):
    def get(self, request):
        genre_name = request.GET.get("genre", "all")
        search_query = request.GET.get("search", "")
        movies = Movie.objects.all()
        genres = Genre.objects.all()

        if genre_name and genre_name != "all":
            print(f"Фильтруем по жанру:{genre_name}")
            movies = movies.filter(genre__name=genre_name)

        if search_query:
            print(f"Фильтруем по названию: {search_query}")
            movies = movies.filter(title__icontains=search_query)

        print(f"Количество фильмов посл фильтрации: {movies.count()}")

        return render(
            request,
            "movies/movie_list.html",
            {
                "movies": movies,
                "genres": genres,
                "selected_genre": genre_name,
                "search_query": search_query,
            },
        )


class MovieDetailView(View):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        return render(
            request,
            "movies/movie_detail.html",
            {
                "movie": movie,
            },
        )


@method_decorator(superuser_required, name="dispatch")
class MovieCreateView(View):
    def get(self, request):
        form = MovieForm()
        return render(
            request,
            "movies/movie_form.html",
            {
                "form": form,
                "genres": Genre.objects.all(),
                "directors": Director.objects.all(),
                "media_types": MediaType.objects.all(),
            },
        )

    def post(self, request):
        print("POST request received.")

        title = request.POST.get("title")
        description = request.POST.get("description")
        trailer = request.POST.get("trailer")
        year = request.POST.get("year")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")  # Получаем изображение

        # Проверяем, что изображение - это объект, а не список
        if isinstance(image, list):
            print("Image should not be a list.")
            return render(
                request,
                "movies/movie_form.html",
                {
                    "error": "Ошибка загрузки изображения.",
                    "form": MovieForm(request.POST, request.FILES),
                    "genres": Genre.objects.all(),
                    "directors": Director.objects.all(),
                    "media_types": MediaType.objects.all(),
                },
            )

        genres_ids = request.POST.getlist("genres")  # Извлекаем выбранные жанры
        media_types_ids = request.POST.getlist(
            "media_types"
        )  # Извлекаем выбранные медиа типы
        directors_ids = request.POST.getlist(
            "directors"
        )  # Извлекаем выбранных режиссёров
        new_director_name = request.POST.get(
            "new_director"
        )  # Получаем имя нового режиссёра, если оно введено

        # Валидация полей
        if (
            not all([title, description, trailer, year, rating])
            or not genres_ids
            or not media_types_ids
        ):
            print("Validation failed.")
            return render(
                request,
                "movies/movie_form.html",
                {
                    "error": "Пожалуйста, заполните все обязательные поля.",
                    "form": MovieForm(request.POST, request.FILES),
                    "genres": Genre.objects.all(),
                    "directors": Director.objects.all(),
                    "media_types": MediaType.objects.all(),
                },
            )

        # Если введено имя нового режиссера, создаем его в БД
        if new_director_name:
            new_director, created = Director.objects.get_or_create(
                name=new_director_name
            )
            directors_ids.append(new_director.id)  # Добавляем ID нового режиссера

        # Если ни один режиссер не был выбран и новый не введен, возвращаем ошибку
        if not directors_ids and not new_director_name:
            print("No director provided.")
            return render(
                request,
                "movies/movie_form.html",
                {
                    "error": "Выберите режиссера или добавьте нового.",
                    "form": MovieForm(request.POST, request.FILES),
                    "genres": Genre.objects.all(),
                    "directors": Director.objects.all(),
                    "media_types": MediaType.objects.all(),
                },
            )

        # Создание экземпляра Movie
        movie = Movie.objects.create(
            title=title,
            description=description,
            trailer=trailer,
            year=year,
            rating=rating,
            image=image,  # Здесь должно быть одно изображение
        )

        # Привязываем жанры, медиа типы и режиссёров к фильму
        try:
            movie.genres.set(genres_ids)
            movie.media_type.set(media_types_ids)
            movie.directors.set(directors_ids)
        except Exception as e:
            print(f"Error setting relationships: {e}")
            return render(
                request,
                "movies/movie_form.html",
                {
                    "error": "Ошибка при привязке жанров, медиа типов или режиссёров.",
                    "form": MovieForm(request.POST, request.FILES),
                    "genres": Genre.objects.all(),
                    "directors": Director.objects.all(),
                    "media_types": MediaType.objects.all(),
                },
            )

        print(f"Movie created with ID: {movie.pk}")
        return redirect("movie_detail", pk=movie.pk)


@method_decorator(superuser_required, name="dispatch")
class MovieUpdateView(View):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        genres = Genre.objects.all()
        directors = Director.objects.all()
        media_types = MediaType.objects.all()

        return render(
            request,
            "movies/update.html",
            {
                "movie": movie,
                "genres": genres,
                "directors": directors,
                "media_types": media_types,
            },
        )

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        # Обновляем поля фильма
        movie.title = request.POST.get("title")
        movie.description = request.POST.get("description")
        movie.trailer = request.POST.get("trailer")
        movie.year = request.POST.get("year")
        movie.rating = request.POST.get("rating")

        genre_id = request.POST.get("genre")
        media_type_id = request.POST.get("media_type")

        # Получаем новый режиссер: либо существующий, либо новый
        director_name = request.POST.get("director_name")  # Имя нового режиссера
        director_id = request.POST.get("director")  # ID выбранного режиссера

        # Обработка жанров
        genre = get_object_or_404(Genre, id=genre_id)
        movie.genres.clear()  # Удаляем старые жанры
        movie.genres.add(genre)  # Добавляем новый жанр

        # Обработка медиа типов
        media_type = get_object_or_404(MediaType, id=media_type_id)
        movie.media_type.clear()
        movie.media_type.add(media_type)

        # Обработка режиссеров
        if director_id:
            director = get_object_or_404(Director, id=director_id)
            movie.directors.clear()
            movie.directors.add(director)
        elif director_name:  # Если имя нового режиссера передано
            director, created = Director.objects.get_or_create(name=director_name)
            movie.directors.clear()
            movie.directors.add(director)

        # Сохраняем изменения
        movie.save()

        return redirect("movie_detail", pk=movie.pk)


@method_decorator(superuser_required, name="dispatch")
class MovieDeleteView(View):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        return render(request, "movies/movie_confirm_delete.html", {"movie": movie})

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
        return redirect("movie_list")


class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=1)
        return render(request, "menu/movies.html", {"movies": movies})


class SeriesView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=2)
        return render(request, "menu/series.html", {"movies": movies})


class DocumentaryView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=3)
        return render(request, "menu/documentary.html", {"movies": movies})


class CartoonsView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=4)
        return render(request, "menu/cartoon.html", {"movies": movies})


class AnimatedSeriesView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=5)
        return render(request, "menu/animated_series.html", {"movies": movies})


class MiniSeriesView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=6)
        return render(request, "menu/mini_series.html", {"movies": movies})


class WebSeriesView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=7)
        return render(request, "menu/web_series.html", {"movies": movies})


class TVShowView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=8)
        return render(request, "menu/tv_show.html", {"movies": movies})


class RealityShowView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=9)
        return render(request, "menu/reality_show.html", {"movies": movies})


class ShortFilmView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=10)
        return render(request, "menu/short_film.html", {"movies": movies})


class AnimatedShowView(View):
    def get(self, request):
        movies = Movie.objects.filter(media_type_id=11)
        return render(request, "menu/animated_show.html", {"movies": movies})


class MovieCarouselView(View):
    def get(self, request):
        movies = Movie.objects.all()  # Получаем все фильмы из базы данных
        return render(request, "./movies/movie_list.html", {"movies": movies})
