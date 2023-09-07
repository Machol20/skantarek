from django import forms
from django.core.validators import FileExtensionValidator

from wyszukiwarka_ulic.models import Salesman, Offer


class StreetSearchForm(forms.Form):
    """
    Search for street by its name.
    """
    search_query = forms.CharField(label='Search Street', max_length=200)


class StreetServicesForm(forms.Form):
    """
    Search for street by services it provides.
    """
    has_internet = forms.BooleanField(label='Internet', required=False)
    has_television = forms.BooleanField(label='Television', required=False)
    has_phone = forms.BooleanField(label='Phone', required=False)


class SalesmenForm(forms.Form):
    """
    Search for sales by salesman.
    """
    salesman = forms.ModelChoiceField(Salesman.objects.all())


class OffersForm(forms.Form):
    """
    Search for streets by offer.
    """
    offers = forms.ModelMultipleChoiceField(Offer.objects.all())


class ImportExcelForm(forms.Form):
    """
    Import data from excel file.
    """
    file = forms.FileField(label='Select Excel File', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])
    truncate = forms.BooleanField(label='Truncate', required=False)
