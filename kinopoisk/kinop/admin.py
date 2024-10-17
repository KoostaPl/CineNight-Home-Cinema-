from django.contrib import admin
from .models import Movie, Genre, Director, MediaType


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "rating",
        "get_genres",  # Метод для отображения жанров
        "get_directors",  # Метод для отображения режиссеров
        "get_media_types",  # Метод для отображения типов медиа
    )

    search_fields = (
        "title",
        "description",
        "directors__name",  # Поиск по имени режиссера
    )

    list_filter = (
        "genres",  # Используем ManyToMany поле для фильтрации
        "directors",  # Используем ManyToMany поле для фильтрации
        "year",
        "rating",
    )

    ordering = ("-rating", "title")
    actions = ["mark_as_published", "mark_as_featured"]

    def mark_as_published(self, request, queryset):
        queryset.update(status="published")
        self.message_user(request, "Фильмы отмечены как опубликованные.")

    mark_as_published.short_description = "Отметить как опубликованные"

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, "Фильмы отмечены как избранные.")

    mark_as_featured.short_description = "Отметить как избранные"

    def get_genres(self, obj):
        return ", ".join(
            [genre.name for genre in obj.genres.all()]
        )  # Отображение связанных жанров

    get_genres.short_description = "Жанры"

    def get_directors(self, obj):
        return ", ".join(
            [director.name for director in obj.directors.all()]
        )  # Отображение связанных режиссеров

    get_directors.short_description = "Режиссёры"

    def get_media_types(self, obj):
        return ", ".join(
            [media_type.name for media_type in obj.media_type.all()]
        )  # Отображение связанных типов медиа

    get_media_types.short_description = "Тип медиа"


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.site_header = "Управление фильмами"
admin.site.site_title = "Админка кинопоиск"
admin.site.index_title = "Управление контентом"
