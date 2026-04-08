import django.core.validators
from decimal import Decimal, ROUND_HALF_UP
from django.db import migrations, models


def convert_rating_scale(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")

    for movie in Movie.objects.all():
        if movie.rating and movie.rating > Decimal("5.0"):
            movie.rating = (movie.rating / Decimal("2")).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )
            movie.save(update_fields=["rating"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(blank=True, help_text='Optional link to a movie poster image.', verbose_name='Poster URL'),
        ),
        migrations.RunPython(convert_rating_scale, noop_reverse),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(decimal_places=1, help_text='Enter a score from 0.5 to 5.0.', max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.5')), django.core.validators.MaxValueValidator(Decimal('5.0'))], verbose_name='Rating'),
        ),
    ]
