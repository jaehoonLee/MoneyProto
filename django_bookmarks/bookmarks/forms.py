from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from bookmarks.models import *

SEX_SELECTION = ((0,'male'),(1,'female'))
# -*- coding: utf-8 -*-
class RegistrationForm(forms.Form):
    username = forms.EmailField(label='UserName')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password(Check)', widget=forms.PasswordInput())
    sex = forms.ChoiceField(label = 'sex', choices = SEX_SELECTION)
    age = forms.DecimalField(label = 'age')
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Not Equal Password.')

    def clean_sex(self):
        return self.cleaned_data['sex']

    def clean_age(self):
        return self.cleaned_data['age']

    def clean_username(self):
        username = self.cleaned_data['username']
        print 'hello'
        '''
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username only available for Alphabet, Number, _')
        '''
        try:
            MoneyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username already exists.')
         

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField()


class phoneRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    firstname = forms.CharField()

#Money Info Forms
class BackAccountForm(forms.Form):
    accountID = forms.CharField()
    accountType = forms.IntegerField()
    bankCompany = forms.IntegerField()
    ownerName = models.CharField()
    title = models.CharField()
    
class CashForm(forms.Form):
    cashID = models.CharField()
    desc = models.CharField()
    user = models.CharField()

class CreditCardForm(forms.Form):
    cardCompany = models.IntegerField()
    cardID = models.CharField()
    personPNO = models.CharField()
    smsPNO = models.CharField()
    title = models.CharField()
    type = models.IntegerField()
    uID = models.CharField()
    uPWD = models.CharField()
    userName = models.CharField()

class StockAccountForm(forms.Form):
    accountID = models.CharField()
    owner = models.CharField()
   

