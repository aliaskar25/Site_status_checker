from django import forms

from .models import Site


class SiteIntervalForm(forms.Form):
    interval_time = forms.IntegerField(help_text="In seconds")