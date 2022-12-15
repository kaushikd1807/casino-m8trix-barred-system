from django.db import models


class PersonalInfo(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    other_name = models.CharField(max_length=100)
    date = models.DateField()
    home_address = models.CharField(max_length=100)
    home_street = models.CharField(max_length=100)
    home_city = models.CharField(max_length=100)
    home_state = models.CharField(max_length=50)
    home_zipcode = models.IntegerField()


