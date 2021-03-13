from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class WatchList(models.Model):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return self.name

class Movie(models.Model):

    TOWATCH = 'TW'
    WATCHED = 'WD'

    WATCH_STATE_CHOICES = [
        (TOWATCH, 'To watch'),
        (WATCHED, 'Watched')
    ]

    list = models.ForeignKey(WatchList, on_delete=models.CASCADE, null=True, blank=True)
    movie_title = models.CharField(max_length=200)

    synopsis = models.CharField(max_length=200, null=True)
    featured_img = models.ImageField(null=True)

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
