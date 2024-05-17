# Generated by Django 5.0.6 on 2024-05-17 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='irakli', max_length=150, verbose_name='full name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='personal_number',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('^\\d{11}$', 'Personal number must be 11 digits.')]),
        ),
    ]
