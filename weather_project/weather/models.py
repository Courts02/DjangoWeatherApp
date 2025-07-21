from django.db import models
from django.utils import timezone

class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.FloatField()
    searched_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-searched_at']
        
    def __str__(self):
        return f"{self.city} - {self.temperature}°C"