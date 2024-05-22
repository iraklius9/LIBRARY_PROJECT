# Generated by Django 5.0.6 on 2024-05-22 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_borrowinghistory_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(choices=[('On loan', 'On loan'), ('Maintenance', 'Maintenance'), ('Reserved', 'Reserved'), ('Returned', 'Returned')], default='On loan', max_length=20),
        ),
    ]