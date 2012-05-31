from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# -*- coding: utf-8 -*-
class RegistrationForm(forms.Form):
    username = forms.CharField(label='UserName', max_length=30)
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password(Check)', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Not Equal Password.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username only available for Alphabet, Number, _')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username already exists.')
            

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField()