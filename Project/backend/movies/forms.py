from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "director", "rating"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Movie title", "class": "form-control"}
            ),
            "director": forms.TextInput(
                attrs={"placeholder": "Director name", "class": "form-control"}
            ),
            "rating": forms.NumberInput(
                attrs={
                    "min": "1",
                    "max": "10",
                    "step": "0.1",
                    "placeholder": "8.5",
                    "class": "form-control",
                }
            ),
        }

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_director(self):
        return self.cleaned_data["director"].strip()
