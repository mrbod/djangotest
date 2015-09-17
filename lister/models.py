from django.db import models

class Entry(models.Model):
    path = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.path

