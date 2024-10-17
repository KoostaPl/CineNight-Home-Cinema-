from .models import Movie
from django import forms


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "trailer",
            "year",
            "rating",
            "media_type",
            "genres",
            "directors",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "trailer": forms.URLInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "rating": forms.TextInput(attrs={"class": "form-control"}),
            "media_type": forms.Select(attrs={"class": "form-control"}),
            "genres": forms.SelectMultiple(attrs={"class": "form-control"}),
            "directors": forms.SelectMultiple(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        help_texts = {
            "year": "Введите год в формате YYYY.",
            "rating": "Введите рейтинг (например, PG-13).",
        }
