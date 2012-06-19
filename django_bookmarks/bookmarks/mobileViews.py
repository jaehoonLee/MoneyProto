# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import *
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.loader import get_template
from django.template import *
from django.contrib.auth import logout
from bookmarks.forms import *
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.forms.util import ErrorList
from django.core import serializers
from django.utils import simplejson
from bookmarks.models import *
from django.utils.encoding import *

@csrf_exempt
def login_page_phone(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                #data = serializers.serialize("json", user);
                # success
                return_data = {'ID': user.username, 'PW' : user.password}
                serial_data = simplejson.dumps(return_data)
                return HttpResponse(serial_data)  
        else:
            # disabled account
            return HttpResponse('0')
    else:
        return render_to_response('registration/login.html') 


@csrf_exempt
def register_page_phone(request):
    if request.method == 'POST':
        form = phoneRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            user.first_name = form.cleaned_data['firstname'];
            user.save()

            return_data = {'ID': user.username, 'FirstName' : user.first_name, 'success': 1}
            serial_data = simplejson.dumps(return_data)
            
            return HttpResponse(serial_data)
        else:
            
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

            return HttpResponse('0')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form' : form})
    return render_to_response('registration/register.html', variables)


#User Infomation set Method
def bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            user = MoneyUser.objects.get(username=request.POST['username'])
            bankAccount = BankAccount.objects.create(
                accountID=form.cleaned_data['accountID'],
                accountType=form.cleaned_data['accountType'],
                bankCompany=form.cleaned_data['bankCompany'],
                ownerName=form.cleaned_data['ownerName'],
                title=form.cleaned_data['title'],
                moneyAccount=user
                )
            bankAccount.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

        return HttpResponse(serial_data)
    else:
        user = MoneyUser.objects.get(username=request.GET['username'])
        bankAccounts = user.bankaccount_set.all()
        serial_data = serializers.serialize("json", bankAccounts)


        #serializer method for json
        response = HttpResponse()
        json_serializer = serializers.get_serializer("json")() 
        json_serializer.serialize(bankAccounts, ensure_ascii=False, stream = response)
    
        #easy method with simplejson
        for bankAccount in bankAccounts:
            return_data = {'accountID': bankAccount.accountID,
                           'accountType' : bankAccount.accountType,
                           'bankCompany' : bankAccount.bankCompany,
                           'ownerName' : bankAccount.ownerName,
                           'title' : bankAccount.title,
                           'success': 1}
            serial_data = simplejson.dumps(return_data, ensure_ascii = False)
           
        
    print serial_data
    print response.content
    #return response
    return HttpResponse(serial_data, content_type = 'application/json; charset=utf-8')


def cash(request):
    if request.method == 'POST':
        form = CashForm(request.POST)
        if form.is_valid():
            moneyUser = MoneyUser.objects.get(username=request.POST['username'])
            cash = Cash.objects.create(
                cashID=form.cleaned_data['cashID'],
                desc=form.cleaned_data['desc'],
                user=form.cleaned_data['user'],
                moneyAccount=moneyUser
                )
            cash.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)
    return HttpResponse(serial_data)

def credit_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            user = MoneyUser.objects.get(username=request.POST['username'])
            creditcard = CreditCard.objects.create(
                cardCompany=form.cleaned_data['cardCompany'],
                cardID=form.cleaned_data['cardID'],
                personPNO=form.cleaned_data['personPNO'],
                smsPNO=form.cleaned_data['smsPNO'],
                title=form.cleaned_data['title'],
                type=form.cleaned_data['type'],
                uID=form.cleaned_data['uID'],
                uPWD=form.cleaned_data['uPWD'],
                userName=form.cleaned_data['userName'],
                moneyAccount=user
                )
            creditcard.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)
    return HttpResponse(serial_data)

def stock_account(request):
    if request.method == 'POST':
        form = StockAccountForm(request.POST)
        if form.is_valid():
            user = MoneyUser.objects.get(username=request.POST['username'])
            stockaccount = StockAccount.objects.create(
                accountID=form.cleaned_data['cashID'],
                owner=form.cleaned_data['owner'],
                moneyAccount=user
                )
            stockaccount.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)
    return HttpResponse(serial_data)
