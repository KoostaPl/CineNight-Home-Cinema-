# Generated by Django 5.1.1 on 2024-10-11 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kinop", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="raiting",
            new_name="rating",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="director",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="genre",
        ),
        migrations.AddField(
            model_name="movie",
            name="directors",
            field=models.ManyToManyField(to="kinop.director", verbose_name="Режиссёры"),
        ),
        migrations.AddField(
            model_name="movie",
            name="genres",
            field=models.ManyToManyField(to="kinop.genre", verbose_name="Жанры"),
        ),
    ]
