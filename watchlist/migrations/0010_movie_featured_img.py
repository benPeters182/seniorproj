# Generated by Django 3.1.5 on 2021-02-28 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0009_auto_20210226_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='featured_img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
