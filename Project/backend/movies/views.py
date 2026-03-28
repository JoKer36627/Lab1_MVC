from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MovieForm
from .models import Movie


def movie_list(request):
    query = request.GET.get("q", "").strip()
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(
            Q(title__icontains=query) | Q(director__icontains=query)
        )

    context = {
        "movies": movies,
        "query": query,
        "movie_count": movies.count(),
    }
    return render(request, "movies/movie_list.html", context)


def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie added successfully.")
            return redirect("movies:list")
    else:
        form = MovieForm()

    return render(
        request,
        "movies/movie_form.html",
        {"form": form, "page_title": "Add Movie", "submit_label": "Create"},
    )


def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie updated successfully.")
            return redirect("movies:list")
    else:
        form = MovieForm(instance=movie)

    return render(
        request,
        "movies/movie_form.html",
        {
            "form": form,
            "movie": movie,
            "page_title": "Edit Movie",
            "submit_label": "Save changes",
        },
    )


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        movie.delete()
        messages.success(request, "Movie deleted successfully.")
        return redirect("movies:list")

    return render(request, "movies/movie_confirm_delete.html", {"movie": movie})
