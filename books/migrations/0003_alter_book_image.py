# Generated by Django 5.0.6 on 2024-05-21 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='book_images/2.jpg', null=True, upload_to='book_images'),
        ),
    ]