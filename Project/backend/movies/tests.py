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
            rating="4.5",
            poster_url="https://example.com/inception.jpg",
        )

    def test_movie_list_page_renders(self):
        response = self.client.get(reverse("movies:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "Rating: 4.5/5.0")
        self.assertContains(response, "inception.jpg")

    def test_create_requires_login(self):
        response = self.client.get(reverse("movies:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_movie_can_be_created(self):
        self.client.login(username="tester", password="strong-pass-123")
        response = self.client.post(
            reverse("movies:create"),
            {
                "title": "Arrival",
                "director": "Denis Villeneuve",
                "rating": "4.0",
                "poster_url": "https://example.com/arrival.jpg",
            },
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
                "rating": "5.0",
                "poster_url": "https://example.com/inception-new.jpg",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(str(self.movie.rating), "5.0")

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
            rating="4.5",
        )

        response = self.client.get(reverse("movies:list"), {"q": "wach"})

        self.assertContains(response, "The Matrix")
        self.assertNotContains(response, "Inception")

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_rating_must_fit_new_five_star_scale(self):
        self.client.login(username="tester", password="strong-pass-123")
        response = self.client.post(
            reverse("movies:create"),
            {"title": "Invalid", "director": "Nobody", "rating": "5.5", "poster_url": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value is less than or equal to 5.0")
