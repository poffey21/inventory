from django.apps import apps
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from . import forms


class ReceiptUploadView(generic.CreateView):
    model = apps.get_model('scanner.Receipt')
    form_class = forms.UploadReceiptForm
    success_url = '/'
    
    
class ReceiptUpdateView(generic.FormView):
    queryset = None
    model = apps.get_model('scanner.Item')
    success_url = '/'
    template_name = 'scanner/receipt_form.html'
    form_class = modelformset_factory(model, forms.UpdateReceiptForm, extra=0)
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'queryset': self.get_queryset(),
            'prefix': self.get_prefix(),
        }
        return kwargs
    
    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        #ordering = self.get_ordering()
        #if ordering:
        #    if isinstance(ordering, six.string_types):
        #        ordering = (ordering,)
        #    queryset = queryset.order_by(*ordering)
        return queryset.filter(receipt__pk=self.kwargs['pk'])


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

