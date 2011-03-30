from django.db import models

class Brewery(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return "%s" % self.name

class BeerType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return "%s" % self.name


class Beer(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    brewery = models.ForeignKey(Brewery)
    type = models.ForeignKey(BeerType, blank=True, null=True)

    def __unicode__(self):
        return "%s -- %s from %s" % (self.name, self.type.name, self.brewery)
