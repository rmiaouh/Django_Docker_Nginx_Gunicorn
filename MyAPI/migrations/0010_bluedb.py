# Generated by Django 3.0.5 on 2020-05-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAPI', '0009_pinkdb'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlueDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_mar', models.CharField(max_length=180)),
                ('output_mar', models.CharField(blank=True, max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
