# Generated by Django 5.1.1 on 2024-10-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kinop", "0005_alter_movie_directors_alter_movie_genres_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="movies/", verbose_name="Изображение"
            ),
        ),
    ]
