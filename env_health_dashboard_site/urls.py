from django.conf.urls import patterns, include, url

from django.contrib import admin
from env_health_dashboard import views

admin.autodiscover()

ENV_URL_PATTERN = r'^env/(?P<brand>[a-zA-z]{2,4})\.(?P<env>[a-zA-Z_0-9]{3,12})$'
BRAND_PATTERN = r'^brand/?(?P<brand>[a-zA-z]{0,4})$'

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(ENV_URL_PATTERN, views.env_handler, name='env_handler'),
    url(BRAND_PATTERN, views.brand_handler, name='brand_handler'),
    url(r'^admin/', include(admin.site.urls)),
)
