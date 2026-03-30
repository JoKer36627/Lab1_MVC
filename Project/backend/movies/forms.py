from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "director", "rating", "poster_url"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Movie title", "class": "form-control"}
            ),
            "director": forms.TextInput(
                attrs={"placeholder": "Director name", "class": "form-control"}
            ),
            "rating": forms.NumberInput(
                attrs={
                    "min": "0.5",
                    "max": "5.0",
                    "step": "0.5",
                    "placeholder": "4.5",
                    "class": "form-control",
                }
            ),
            "poster_url": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com/poster.jpg",
                    "class": "form-control",
                }
            ),
        }

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_director(self):
        return self.cleaned_data["director"].strip()

    def clean_poster_url(self):
        return self.cleaned_data["poster_url"].strip()
