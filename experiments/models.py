import time
import math
import datetime

from django.db import models


class Experiment(models.Model):
    name = models.CharField(max_length=255)
    ambient_temperature = models.FloatField()
    original_temperature = models.FloatField()
    start_time = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def get_average_k(self):
        if self.measurement_set.count() < 1:
            return False

        return sum([row.get_k() for row in self.measurement_set.all()]) / self.measurement_set.count()


    def get_average_cooling_function(self):
        k = self.get_average_k()
        def cooling_function(t):
            return (self.ambient_temperature + (self.original_temperature - self.ambient_temperature) * math.e ** (-t * k))
        return cooling_function
        

class Measurement(models.Model):
    experiment = models.ForeignKey(Experiment)
    time_taken = models.DateTimeField(default=datetime.datetime.now, blank=True)
    temperature = models.FloatField()

    def get_t(self):
        return time.mktime(self.time_taken.timetuple()) - time.mktime(self.experiment.start_time.timetuple())

    def estimate_at(self):
        return self.experiment.get_average_cooling_function()(self.get_t())

    def get_k(self):
        return -(math.log(((self.temperature - self.experiment.ambient_temperature) / float(self.experiment.original_temperature - self.experiment.ambient_temperature))) / self.get_t())
