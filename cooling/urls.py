from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'experiments.views.experiments', name='index'),
    url(r'^experiment/(?P<experiment_id>\d+)/$', 'experiments.views.experiment_detail', name='experiment_detail'),
    url(r'^delete-measurement/(?P<measurement_id>\d+)/$', 'experiments.views.delete_measurement', name='delete_measurement'),
    # Examples:
    # url(r'^$', 'cooling.views.home', name='home'),
    # url(r'^cooling/', include('cooling.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
