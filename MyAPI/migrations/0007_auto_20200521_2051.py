# Generated by Django 3.0.5 on 2020-05-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAPI', '0006_reddb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reddb',
            name='intent_rasa',
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AlterField(
            model_name='reddb',
            name='ranking_rasa',
            field=models.CharField(blank=True, max_length=180),
        ),
    ]
