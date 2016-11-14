from django.shortcuts import render
from django.views import generic
from django.apps import apps

from . import forms


class ReceiptUploadView(generic.CreateView):
    model = apps.get_model('scanner.Receipt')
    form_class = forms.ReceiptForm
    success_url = '/'


class ReceiptListView(generic.ListView):
    model = apps.get_model('scanner.Receipt')

class ExampleFormView(generic.FormView):
    """ lets see what this looks like """
    form_class = forms.ExampleForm
    success_url = '/'
    template_name = 'example_form.html'

