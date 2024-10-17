import json
from django.core.management.base import BaseCommand
from kinop.models import Genre, Director, Movie, MediaType


class Command(BaseCommand):
    help = "Загружает фильмы, жанры и режиссёров из JSON файлов"

    def handle(self, *args, **kwargs):
        # Загрузка жанров
        with open("kinop_json/genre.json", "r", encoding="utf-8") as genre_file:
            genres = json.load(genre_file)
            for genre_data in genres:
                genre, created = Genre.objects.get_or_create(name=genre_data["name"])
                if created:
                    self.stdout.write(
                        self.style.SUCCESS('Жанр "%s" был создан.' % genre.name)
                    )

        # Загрузка медиаполей
        with open("kinop_json/mediatype.json", "r", encoding="utf-8") as media_file:
            media_types_data = json.load(media_file)
            for media_data in media_types_data:
                media, created = MediaType.objects.get_or_create(
                    name=media_data["name"]
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS('Media "%s" был создан.' % media.name)
                    )

        # Загрузка режиссёров
        with open("kinop_json/director.json", "r", encoding="utf-8") as director_file:
            directors = json.load(director_file)
            for director_data in directors:
                director, created = Director.objects.get_or_create(
                    name=director_data["name"]
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS('Режиссёр "%s" был создан.' % director.name)
                    )

        # Загрузка фильмов
        with open("kinop_json/movie.json", "r", encoding="utf-8") as movie_file:
            movies = json.load(movie_file)
            for movie_data in movies:
                director_ids = movie_data.get("director_ids", [])
                if isinstance(director_ids, int):
                    director_ids = [director_ids]
                directors = Director.objects.filter(id__in=director_ids)

                media_type_ids = movie_data.get("media_type_ids", [])
                if isinstance(media_type_ids, int):
                    media_type_ids = [media_type_ids]

                movie = Movie(
                    title=movie_data["title"],
                    description=movie_data["description"],
                    trailer=movie_data["trailer"],
                    year=movie_data["year"],
                    rating=movie_data["rating"],
                    external_image_url=movie_data["external_image_url"],
                )
                movie.save()

                # Установка связей
                movie.directors.set(directors)
                media_types = MediaType.objects.filter(id__in=media_type_ids)
                movie.media_type.set(media_types)

                genre_ids = movie_data.get("genre_ids", [])
                if isinstance(genre_ids, int):
                    genre_ids = [genre_ids]
                genres = Genre.objects.filter(id__in=genre_ids)
                movie.genres.set(genres)

                self.stdout.write(
                    self.style.SUCCESS('Фильм "%s" был создан.' % movie.title)
                )
