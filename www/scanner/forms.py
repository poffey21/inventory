from django import forms
from django.apps import apps
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ReceiptForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-lg'))
        
        self.helper.form_class = 'lead'
        self.fields['image'].widget.attrs.update({'display' : 'none'})
    
    image = forms.ImageField(
        label = 'Upload'
    )


    class Meta:
        fields = ['image']
        model = apps.get_model('scanner.Receipt')


class PurchaseListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PurchaseListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    
    class Meta:
        model = apps.get_model('scanner.Receipt')
        fields = ['store']


class PurchaseListItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PurchaseListItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    
    class Meta:
        model = apps.get_model('scanner.Item')
        fields = ['given_name', 'amount']


class ExampleForm(forms.Form):
    """ getting crispy """
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))
    
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )

ItemFormSet = inlineformset_factory(apps.get_model('scanner.Receipt'), apps.get_model('scanner.Item'), form=PurchaseListItemForm)
