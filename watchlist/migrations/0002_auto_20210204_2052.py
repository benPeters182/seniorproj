# Generated by Django 3.1.5 on 2021-02-05 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
