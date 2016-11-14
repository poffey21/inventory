from __future__ import unicode_literals
import json

from django.db import models

# Create your models here.
TAX_CODES = (
    ('FB', 'B-Code'),
    ('NC', 'C-Code'),
)

class Receipt(models.Model):
    """ a receipt from a particular store """

    store_name = models.CharField(max_length=64, blank=True)
    store = models.ForeignKey('merchant.Store', null=True, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    json_data = models.TextField(blank=True)
    
    def __str__(self):
        if self.store and self.timestamp:
            return '{} on {}'.format(self.store.franchise.name, self.timestamp)
        elif self.store:
            return self.store.__str__()
        elif self.json_data:
            try:
                return ' '.join(json.loads(self.json_data)[0]['description'].split('\n')[:5])
            except Exception:
                pass
        return 'Uncategorized'
    
    def __unicode__(self):
        return self.__str__()


class Item(models.Model):
    """ Every item on a receipt """

    name = models.CharField(max_length=32, blank=True)
    given_name = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax_code = models.CharField(max_length=32, blank=True, choices=TAX_CODES)


class Tax(models.Model):
    """ The taxes associated with a receipt """

    name = models.CharField(max_length=32, blank=True, choices=TAX_CODES)
    given_name = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)


class Word(models.Model):
    """ The actual word """

    value = models.CharField(max_length=64)
    item = models.ForeignKey('scanner.Item', null=True, blank=True)
    tax = models.ForeignKey('scanner.Tax', null=True, blank=True)


class Vertex(models.Model):
    """ The bounding polygon for each word """
    
    word = models.ForeignKey('scanner.Word')
    x = models.IntegerField()
    y = models.IntegerField()

