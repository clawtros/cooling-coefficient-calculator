from django.shortcuts import render
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import simplejson

from experiments.models import Experiment, Measurement


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = ['start_time']


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['temperature']


def delete_measurement(request, measurement_id):
    m = Measurement.objects.get(pk=measurement_id)
    e = m.experiment
    m.delete()
    return HttpResponseRedirect(reverse("experiment_detail", kwargs={"experiment_id": e.id}))


def experiment_detail(request, experiment_id):

    e = Experiment.objects.get(pk=experiment_id)

    if request.method == "POST":
        form = MeasurementForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.experiment = e
            m.save()

    form = MeasurementForm()
    
    dataset = []
    for measurement in e.measurement_set.all():
        dataset.append({
            "temperature" : measurement.temperature,
            "t" : measurement.get_t(),
            "estimate": measurement.estimate_at()
        })

    return render(request, 'experiment_detail.html', {
        "experiment":e, 
        "form": form, 
        "jsonset": simplejson.dumps(dataset)
    })


def experiments(request):
    if request.method == "POST":
        form = ExperimentForm(request.POST)
        if form.is_valid():
            e = form.save()
            return HttpResponseRedirect(reverse("experiment_detail", kwargs={"experiment_id": e.id}))
    else:
        form = ExperimentForm()

    return render(request, "experiments.html", {"form":form, "experiments":Experiment.objects.all()})
