from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask, IntervalSchedule

import requests
import json

from datetime import datetime


class Site(models.Model):
    url = models.URLField(max_length=128)
    interval_check = models.IntegerField(verbose_name='in seconds', null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    last_request = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.url

    def get_or_create_interval_check(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.interval_check,
            period=IntervalSchedule.SECONDS
        )
        return schedule

    def create_task(self) -> None:
        PeriodicTask.objects.create(
            interval=self.get_or_create_interval_check(),
            name=self.url,
            task='apps.sites.tasks.hello',
            kwargs=json.dumps({
                'site_id': self.id
            })
        )

    def get_response(self):
        self.status = requests.get(self.url).status_code
        self.last_request = datetime.now()
        self.save()


@receiver(post_save, sender=Site)
def create_site_task_(sender, instance, created, *args, **kwargs):
    task = PeriodicTask.objects.filter(name=instance.url).first()
    if not task:
        instance.create_task()
    else:
        task.interval = instance.get_or_create_interval_check()
        task.save()