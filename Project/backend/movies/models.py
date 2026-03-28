from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    director = models.CharField(max_length=120, verbose_name="Director")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Rating",
        help_text="Enter a score from 1.0 to 10.0.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "director"]

    def __str__(self):
        return f"{self.title} ({self.director})"
