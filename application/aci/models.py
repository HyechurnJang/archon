from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Domain(models.Model):
    name = models.CharField(max_length=64)
    controllers = models.CharField(max_length=64)
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class EPTracker(models.Model):
    mac = models.CharField(max_length=18)
    ip = models.CharField(max_length=16)
    domain = models.CharField(max_length=64)
    tenant = models.CharField(max_length=100)
    app = models.CharField(max_length=100)
    epg = models.CharField(max_length=100)
    intf = models.CharField(max_length=2048)
    start = models.CharField(max_length=24)
    stop = models.CharField(max_length=24)
    
    def __str__(self):
        return self.mac