"""
forms.py module
"""
from django import forms


class UrlForm(forms.Form):
    """
    This class creates a form
    """
    url = forms.URLField(
        label='',
        widget=forms.URLInput(
            attrs={'class': 'url-field'},
        )
    )
