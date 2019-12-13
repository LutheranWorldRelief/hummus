import datetime
from django import forms
from .models import LWRRegion, Country
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, User


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class FilterDashboardForm(forms.Form):
    start_date = forms.DateField(
        label=_('From'),
        widget=forms.DateField.widget(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'value': datetime.date.today(),
                'max': datetime.date.today(),
            }
        )
    )

    end_date = forms.DateField(
        label=_('To'),
        widget=forms.DateField.widget(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'value': datetime.date.today(),
                'max': datetime.date.today(),
            }
        )
    )

    region = forms.ModelChoiceField(
        queryset=LWRRegion.objects.all(),
        widget=forms.ModelChoiceField.widget(
            attrs={'class': 'form-control'}
        )
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.ModelChoiceField.widget(
            attrs={'class': 'form-control'}
        )
    )
