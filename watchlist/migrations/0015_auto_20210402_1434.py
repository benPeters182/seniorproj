# Generated by Django 3.1.5 on 2021-04-02 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0014_actor_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
