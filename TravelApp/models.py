from django.db import models
import calendar
from django.contrib.auth.models import AbstractUser

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class MonthlyCityReview(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    month = models.CharField(max_length=9, choices=MONTH_CHOICES, default='1')

    score = models.IntegerField(default=0)

    def __str__(self):
        return self.city.name + " in " + calendar.month_name[month]


def populateFromFile():
    f = open('static/cities.txt', 'r')
    text = f.read()
    data = [val.strip() for val in text.split('\n') if val]

    for entry in data:
        if "note_ville_" not in entry:
            city, _ = City.objects.get_or_create(name=entry)
            month = 1
        else:
            review, _ = MonthlyCityReview.objects.get_or_create(city=city, month=str(month))
            review.score = int(entry[-1])
            review.save()
            month += 1
    print("Done.")
