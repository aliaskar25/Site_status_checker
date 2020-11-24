from celery import shared_task

from .models import Site

from random import randint


@shared_task
def hello(*args, **kwargs):
    site = Site.objects.get(id=kwargs['site_id'])
    site.get_response()
