from django.urls import path

from .views import statuses, get_site


urlpatterns = [
    path('', statuses, name='sites_statuses_url'),
    path('<int:pk>/', get_site, name='site_url'),
]