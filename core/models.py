from django.db import models

from django.contrib.auth.models import User

class Challenge(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    creator = models.ForeignKey(User)

    def __unicode__(self):
        return "%s" % self.name