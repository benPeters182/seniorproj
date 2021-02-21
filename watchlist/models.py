from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class Movie(models.Model):

    TOWATCH = 'TW'
    WATCHED = 'WD'

    WATCH_STATE_CHOICES = [
        (TOWATCH, 'To watch'),
        (WATCHED, 'Watched')
    ]

    movie_title = models.CharField(max_length=200)

    movie_url = models.CharField(max_length=200, null=True)
    page = models.CharField(max_length=200, null=True)
    synopsis = models.CharField(max_length=200, null=True)

    watch_state = models.CharField(
        choices = WATCH_STATE_CHOICES,
        max_length = 2,
        default = TOWATCH
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
        )

    def __str__(self):
        return self.movie_title

    def rate(self):
        pass

class Show(models.Model):
    TOWATCH = 'TW'
    WATCHING = 'WG'
    WATCHED = 'WD'

    WATCH_STATE_CHOICES = [
        (TOWATCH, 'To watch'),
        (WATCHING, 'Watching'),
        (WATCHED, 'Watched')
    ]

    show_title = models.CharField(max_length=200)
    watch_state = models.CharField(
        choices = WATCH_STATE_CHOICES,
        max_length = 2,
        default = TOWATCH
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.show_title

    def rate(self):
        pass
