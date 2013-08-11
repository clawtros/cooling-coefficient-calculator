"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime
from django.test import TestCase
from experiments.models import *

class KTest(TestCase):
    def test_sane_k_values(self):
        now = datetime.datetime.now()
        e = Experiment(name="test",
                       ambient_temperature=20.0,
                       original_temperature=80.0,
                       start_time=now)
        data = Measurement(time_taken=datetime.datetime.fromtimestamp(time.mktime(now.timetuple()) + 1000 * 3600),
                           experiment=e,
                           temperature=70
            )
        print data.get_k()
        
    def test_generated_function_range(self):
        now = datetime.datetime.now()
        e = Experiment.objects.create(name="test",
                       ambient_temperature=20.0,
                       original_temperature=80.0,
                       start_time=now)
        data = Measurement.objects.create(time_taken=datetime.datetime.fromtimestamp(time.mktime(now.timetuple()) + 1000 * 3600),
                           experiment=e,
                           temperature=70
        )
        cfunc = e.get_average_cooling_function()
        for i in range(10, 1000):
            self.assertTrue(cfunc(i * 1000 * 3600) >= e.ambient_temperature)
            self.assertTrue(cfunc(i * 1000 * 3600) <= e.original_temperature)
