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
        '''
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username only available for Alphabet, Number, _')
        '''
        user =  MoneyUser.objects.get(username=username)
        if EC_USERNAME_DOES_NOT_EXISTS == user:
            return username
        else :
            raise forms.ValidationError('Username already exists.')
         

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField()


class phoneRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    firstname = forms.CharField()

#Money Info Forms
class BankAccountForm(forms.Form):
    accountID = forms.CharField(label='accountID')
    accountType = forms.IntegerField(label='accountType')
    bankCompany = forms.IntegerField(label='bankCompany')
    ownerName = forms.CharField(label='ownerName')
    title = forms.CharField(label='title')
#    userName = forms.CharField(label='userName(MoneyUser)') # accessToken
    
class CashForm(forms.Form):
    cashID = forms.CharField(label='cashID')
    desc = forms.CharField(label='desc')
    user = forms.CharField(label='user')

class CreditCardForm(forms.Form):
    cardCompany = forms.IntegerField(label='cardCompany')
    cardID = forms.CharField(label='cardID')
    personPNO = forms.CharField(label='personPNO')
    smsPNO = forms.CharField(label='smsPNO')
    title = forms.CharField(label='title')
    type = forms.IntegerField(label='type')
    uID = forms.CharField(label='uID')
    uPWD = forms.CharField(label='uPWD')
    userName = forms.CharField(label='userName')
    thisMonthAmount = forms.FloatField(label='thisMonthAmount')

class StockAccountForm(forms.Form):
    accountID = forms.CharField(label='accountID')
    owner = forms.CharField(label='owner')

#Money History Forms
class BankAccountHistoryForm(forms.Form):
    amount = forms.FloatField(label='amount')
    date = forms.CharField(label='date')
    desc = forms.CharField(label='desc')
    historyID = forms.CharField(label='historyID')
    receiverName = forms.CharField(label='receiverName')
    senderName = forms.CharField(label='senderName')
    type = forms.IntegerField(label='type')

class CashHistoryForm(forms.Form):
    amount = forms.FloatField(label='amount')
    createdDate = forms.CharField(label='createdDate')
    desc = forms.CharField(label='desc')
    historyID = forms.CharField(label='historyID')
    spentDate = forms.CharField(label='spentDate')

    storeName = forms.CharField(label='storeName')
    storePNO = forms.CharField(label='storePNO')
    storeID = forms.CharField(label='storeID')
    longtitude = forms.FloatField(label='longtitude')
    latitude = forms.FloatField(label='latitude')
    storeAddress = forms.CharField(label='storeAddress')
    
class CreditCardHistoryForm(forms.Form):
    amount = forms.FloatField(label='amount')
    createdDate = forms.CharField(label='createdDate')
    desc = forms.CharField(label='desc')
    historyID = forms.CharField(label='historyID')

    storeName = forms.CharField(label='storeName')
    storePNO = forms.CharField(label='storePNO')
    storeID = forms.CharField(label='storeID')
    longtitude = forms.FloatField(label='longtitude')
    latitude = forms.FloatField(label='latitude')
    storeAddress = forms.CharField(label='storeAddress')
    
class SAssetForm(forms.Form):
    assetID = forms.CharField(label='assetID')

