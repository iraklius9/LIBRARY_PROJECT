# Generated by Django 5.0.6 on 2024-05-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowinghistory',
            name='borrowing_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]