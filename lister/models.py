from django.db import models

class Entry(models.Model):
    path = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)

    def __cmp__(self, other):
        if self.path < other.path:
            return -1
        if self.path > other.path:
            return 1
        return 0

    def __unicode__(self):
        return self.path

