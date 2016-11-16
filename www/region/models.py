from __future__ import unicode_literals

from django.db import models

# Create your models here.

class City(models.Model):
    """ city for stores and taxes """


class Tax(models.Model):
    """ percentage by city """

