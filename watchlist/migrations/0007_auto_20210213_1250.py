# Generated by Django 3.1.5 on 2021-02-13 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0006_movie_movie_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='page',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='synopsis',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
