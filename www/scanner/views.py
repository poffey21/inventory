from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from . import forms


class ReceiptUploadView(generic.CreateView):
    model = apps.get_model('scanner.Receipt')
    form_class = forms.ReceiptForm
    success_url = '/'


class ReceiptCreateView(generic.CreateView):
    template_name = 'scanner/receipt_add.html'
    model = apps.get_model('scanner.Receipt')
    form_class = forms.PurchaseListForm
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = forms.ItemFormSet()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                item_form=item_form,
            )
        )
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = forms.ItemFormSet(self.request.POST)
        if (form.is_valid() and item_form.is_valid() and
            item_form.is_valid()):
            return self.form_valid(form, item_form)
        else:
            return self.form_invalid(form, item_form)
    
    def form_valid(self, form, item_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        item_form.instance = self.object
        item_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, item_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(
                form=form,
                item_form=item_form,
            )
        )

class ReceiptListView(generic.ListView):
    model = apps.get_model('scanner.Receipt')

class ExampleFormView(generic.FormView):
    """ lets see what this looks like """
    form_class = forms.ExampleForm
    success_url = '/'
    template_name = 'example_form.html'

