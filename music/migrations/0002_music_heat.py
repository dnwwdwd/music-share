# Generated by Django 4.2.16 on 2024-11-01 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='heat',
            field=models.IntegerField(default=0),
        ),
    ]
