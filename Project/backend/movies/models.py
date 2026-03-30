from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    director = models.CharField(max_length=120, verbose_name="Director")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("0.5")), MaxValueValidator(Decimal("5.0"))],
        verbose_name="Rating",
        help_text="Enter a score from 0.5 to 5.0.",
    )
    poster_url = models.URLField(
        blank=True,
        verbose_name="Poster URL",
        help_text="Optional link to a movie poster image.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "director"]

    def __str__(self):
        return f"{self.title} ({self.director})"

    @property
    def normalized_rating(self):
        return Decimal(self.rating).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    @property
    def star_fill_percent(self):
        return float((self.normalized_rating / Decimal("5.0")) * 100)
