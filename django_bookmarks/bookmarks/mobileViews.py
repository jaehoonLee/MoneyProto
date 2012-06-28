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
from bookmarks.uidDef import *
from bookmarks.exceptionHandler import *
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
            return exception_handler(EC_AUTHENTICATION_FAIL)
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

            if user == EC_USERNAME_EXISTS:
                return HttpResponse(EC_USERNAME_EXISTS)
            
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
def bank_account(request, uid):
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
        uidV = uuidTable.objects.get(uid = uid)
        if(uidV == EC_UID_DOES_NOT_EXISTS) :
            return HttpResponse(EC_UID_DOES_NOT_EXISTS)
        type = uidV.type
        
        if(type == MONEYUSER_TYPE):
            user = uidV.moneyuser
        else:
            return HttpResponse(EC_NOT_MONEYUSER_TYPE_ACCOUNT)
            
        bankAccounts = user.bankaccount_set.all()
        serial_data = user_bankaccount(bankAccounts)
        #serializer method for json
        '''
        response = HttpResponse()
        json_serializer = serializers.get_serializer("json")() 
        json_serializer.serialize(bankAccounts, ensure_ascii=False, stream = response)
        '''
        
        #easy method with simplejson
        '''
        bankAccountList = []
        for bankAccount in bankAccounts:
            return_data = {'accountID': bankAccount.accountID,
                           'accountType' : bankAccount.accountType,
                           'bankCompany' : bankAccount.bankCompany,
                           'ownerName' : bankAccount.ownerName,
                           'title' : bankAccount.title,
                           'success': 1}
            bankAccountList.append(return_data)
        serial_data = simplejson.dumps(bankAccountList, ensure_ascii = False)
        '''
    return HttpResponse(serial_data, content_type = 'application/json; charset=utf-8')


def cash(request, uid):
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
    else:
        uidV = uuidTable.objects.get(uid = uid)
        if(uidV == EC_UID_DOES_NOT_EXISTS) :
            return HttpResponse(EC_UID_DOES_NOT_EXISTS)
        type = uidV.type
        
        if(type == MONEYUSER_TYPE):
            user = uidV.moneyuser
        else:
            return HttpResponse(EC_NOT_MONEYUSER_TYPE_ACCOUNT)
            
        cashs = user.cash_set.all()
        serial_data = user_cash(cashs)
        
    return HttpResponse(serial_data)

def credit_card(request, uid):
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
    else:
        uidV = uuidTable.objects.get(uid = uid)
        if(uidV == EC_UID_DOES_NOT_EXISTS) :
            return HttpResponse(EC_UID_DOES_NOT_EXISTS)
        type = uidV.type
        
        if(type == MONEYUSER_TYPE):
            user = uidV.moneyuser
        else:
            return HttpResponse(EC_NOT_MONEYUSER_TYPE_ACCOUNT)

        creditCards = user.creditcard_set.all()
        serial_data = user_creditcard(creditCards)
        
    return HttpResponse(serial_data)

def stock_account(request, uid):
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
    else:
        uidV = uuidTable.objects.get(uid = uid)
        if(uidV == EC_UID_DOES_NOT_EXISTS) :
            return HttpResponse(EC_UID_DOES_NOT_EXISTS)
        type = uidV.type
        
        if(type == MONEYUSER_TYPE):
            user = uidV.moneyuser
        else:
            return HttpResponse(EC_NOT_MONEYUSER_TYPE_ACCOUNT)

        stockAccounts = user.stockaccount_set.all()
        serial_data = user_stockaccount(stockAccounts)
        
    return HttpResponse(serial_data)

def uid_request(request, uid):
    uidV = uuidTable.objects.get(uid = uid)
    if(uidV == EC_UID_DOES_NOT_EXISTS) :
        return HttpResponse(EC_UID_DOES_NOT_EXISTS)
    type = uidV.type
    
    uidDefs = {MONEYUSER_TYPE : money_user_uid,
               BANKACCOUNT_TYPE : bankaccount_uid,
               CASH_TYPE : cash_uid,
               CREDITCARD_TYPE : creditcard_uid,
               STOCKACCOUNT_TYPE : stockaccount_uid,
               BANKACCOUNTHISTORY_TYPE : bankaccounthis_uid,
               CASHHISTORY_TYPE : cashhis_uid,
               CREDITCARDHISTORY_TYPE : creditcardhis_uid,
               SASSET_TYPE : sasset_uid,
               }
    
    if type == MONEYUSER_TYPE :
        parameter = uidV.moneyuser
    elif type == BANKACCOUNT_TYPE :
        parameter = uidV.bankaccount
    elif type == CASH_TYPE :
        parameter = uidV.cash
    elif type == CREDITCARD_TYPE :
        parameter = uidV.creditcard
    elif type == STOCKACCOUNT_TYPE :
        parameter = uidV.stockaccount
    elif type == BANKACCOUNTHISTORY_TYPE :
        parameter = uidV.bankaccounthistory
    elif type == CASHHISTORY_TYPE :
        parameter = uidV.cashhistory
    elif type == CREDITCARDHISTORY_TYPE :
        parameter = uidV.creditcardhistory
    elif type == SASSET_TYPE :
        parameter = uidV.sasset

    return HttpResponse(uidDefs.get(type)(parameter), content_type = 'application/json; charset=utf-8')

def histories_request(request, uid):
    uidV = uuidTable.objects.get(uid = uid)
    if(uidV == EC_UID_DOES_NOT_EXISTS) :
        return HttpResponse(EC_UID_DOES_NOT_EXISTS)
    type = uidV.type
    
    if type == BANKACCOUNT_TYPE :
        histories = uidV.bankaccount.bankaccounthistory_set.all()
        serial_data = bankaccount_history(histories)
    elif type == CASH_TYPE :
        histories = uidV.cash.cashhistory_set.all()
        serial_data = cash_history(histories)
    elif type == CREDITCARD_TYPE :
        histories = uidV.creditcard.creditcardhistory_set.all()
        serial_data = creditcard_history(histories)
    elif type == STOCKACCOUNT_TYPE :
        histories = uidV.stockaccount.sasset_set.all()
        serial_data = sasset_history(histories)
    else :
        HttpResponse(NOT_ACCOUNT_TYPE_HISTORY)
        
    return HttpResponse(serial_data, content_type = 'application/json; charset=utf-8')
    





