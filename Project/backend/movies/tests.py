from django.test import TestCase
from django.urls import reverse

from .models import Movie


class MovieViewsTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            director="Christopher Nolan",
            rating="8.8",
        )

    def test_movie_list_page_renders(self):
        response = self.client.get(reverse("movies:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_movie_can_be_created(self):
        response = self.client.post(
            reverse("movies:create"),
            {"title": "Arrival", "director": "Denis Villeneuve", "rating": "8.1"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Movie.objects.filter(title="Arrival").exists())

    def test_movie_can_be_updated(self):
        response = self.client.post(
            reverse("movies:update", args=[self.movie.pk]),
            {
                "title": "Inception",
                "director": "Christopher Nolan",
                "rating": "9.0",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(str(self.movie.rating), "9.0")

    def test_movie_can_be_deleted(self):
        response = self.client.post(
            reverse("movies:delete", args=[self.movie.pk]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

    def test_movie_search_filters_results(self):
        Movie.objects.create(
            title="The Matrix",
            director="The Wachowskis",
            rating="8.7",
        )

        response = self.client.get(reverse("movies:list"), {"q": "wach"})

        self.assertContains(response, "The Matrix")
        self.assertNotContains(response, "Inception")
