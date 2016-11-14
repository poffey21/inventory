from __future__ import unicode_literals

from django.db import models

# Create your models here.
#  franchise, store, category


class Franchise(models.Model):
    """ all stores with the same name """
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name
        
    def __unicode__(self):
        return self.__str__()


class Store(models.Model):
    franchise = models.ForeignKey('merchant.Franchise')
    number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=2, blank=True)
    
    def __str__(self):
        if self.number:
            return '{} ({}) - {}'.format(self.franchise.name, self.number, self.city)
        else:
            return '{} - {}'.format(self.franchise.name, self.city)
    
    def __unicode__(self):
        return self.__str__()