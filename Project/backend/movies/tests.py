from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Movie


class MovieViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="strong-pass-123",
        )
        self.movie = Movie.objects.create(
            title="Inception",
            director="Christopher Nolan",
            rating="8.8",
        )

    def test_movie_list_page_renders(self):
        response = self.client.get(reverse("movies:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_create_requires_login(self):
        response = self.client.get(reverse("movies:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_movie_can_be_created(self):
        self.client.login(username="tester", password="strong-pass-123")
        response = self.client.post(
            reverse("movies:create"),
            {"title": "Arrival", "director": "Denis Villeneuve", "rating": "8.1"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Movie.objects.filter(title="Arrival").exists())

    def test_movie_can_be_updated(self):
        self.client.login(username="tester", password="strong-pass-123")
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
        self.client.login(username="tester", password="strong-pass-123")
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

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
