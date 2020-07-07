from django.db import models

# Create your models here.


class Task(models.Model):
    message_babel = models.CharField(max_length=1000)
    langue_babel = models.CharField(max_length=3, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_babel


class OrangeDB(models.Model):
    message_date = models.CharField(max_length=1000)
    dim_date = models.CharField(max_length=10, blank=True)
    text_date = models.CharField(max_length=180, blank=True)
    value_date = models.CharField(max_length=180, blank=True)
    color_date = models.CharField(max_length=10, blank=True)
    output_date = models.CharField(max_length=5000, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_date


class RedDB(models.Model):
    message_rasa = models.CharField(max_length=1000)
    intent_rasa = models.CharField(max_length=180, blank=True)
    confidence_rasa = models.CharField(max_length=180, blank=True)
    entity_rasa = models.CharField(max_length=180, blank=True)
    ranking_rasa = models.CharField(max_length=180, blank=True)
    output_rasa = models.CharField(max_length=5000, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_rasa


class YellowDB(models.Model):
    message_ortho = models.CharField(max_length=1000)
    output_ortho = models.CharField(max_length=5000, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_ortho


class PinkDB(models.Model):
    message_feel = models.CharField(max_length=1000)
    output_feel = models.CharField(max_length=5000, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_feel


class BlueDB(models.Model):
    message_mar = models.CharField(max_length=1000)
    output_mar = models.CharField(max_length=5000, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_mar


class GreenDB(models.Model):
    message_lieux = models.CharField(max_length=1000)
    output_lieux = models.CharField(max_length=5000, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message_lieux