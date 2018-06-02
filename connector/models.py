from django.db import models

# Create your models here.

class Website(models.Model):
    website_name = models.CharField(max_length=50)
    website_url = models.CharField(max_length=100)

    def __str__(self):
        return self.website_name

class Result(models.Model):
    website_name = models.ForeignKey(Website, on_delete=models.CASCADE)
    ping_time = models.DateTimeField('time pinged')
    ping_result = models.DecimalField(max_digits=7, decimal_places=3)
    ping_success = models.PositiveSmallIntegerField()
    ping_total = models.PositiveSmallIntegerField()
