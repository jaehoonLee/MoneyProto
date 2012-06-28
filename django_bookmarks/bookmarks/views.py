# Create your views here.
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
import datetime
from bookmarks.mobileViews import *
from bookmarks.models import *

@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        user = MoneyUser.objects.get(username=request.POST['username'])
        if user is not EC_USERNAME_DOES_NOT_EXISTS:
            if user.check_password(request.POST['password']):
                request.session['userID'] = user.username;
                return HttpResponseRedirect('/')
            else:
                form = LoginForm(request.POST)
                stats = "your password is wrong"
        else:
            form = LoginForm(request.POST)
            stats = "username doesn't exist"

        return render_to_response('registration/login.html', {'form' : form, 'stats' : stats})

        #formal login method using django login system
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # success
                return HttpResponseRedirect('/')
            
        else:
            # disabled account
            form = LoginForm(request.POST)
            stats = "Your username and password doesn't exist"
            return render_to_response('registration/login.html', {'form' : form, 'stats' : stats})
        
        
    else:
        # invalid login
        #if request.user is not None:
        #    return HttpResponseRedirect('/')
        #else:
            return render_to_response('registration/login.html')

def logout_page(request):
    #logout(request)
    del request.session['userID']
    return HttpResponseRedirect("/")

def register_page(request):
    if request.method == 'POST':
        print "Hello3"
        form = RegistrationForm(request.POST)
        print "Hello2"
        if form.is_valid():
            print "Hello"
            user = MoneyUser.objects.create_MoneyUser(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                sex = form.cleaned_data['sex'],
                age = form.cleaned_data['age'],
                )
            print "User" + user.username
            request.session['userID'] = user.username;
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form' : form})
    return render_to_response('registration/register.html', variables)
    
def template_test(request):
    t = get_template('test1.html');
    html = t.render(Context({'message' : "adding message"}))
    return HttpResponse(html)

def my_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/>next=%s' % request.path)

@csrf_exempt
def main_page(request):
    if 'userID' in request.session:
        username = request.session['userID']
        user = MoneyUser.objects.get(username='jaehoonlee88@gmail.com')
        template = get_template('main_page.html')
        variables = Context({'user' : username, 'uid': user.uidT.uid})
        output = template.render(variables)
        return HttpResponse(output)
    else:
        return HttpResponseRedirect('/accounts/login/')

#Money Info Form
def bank_account_page(request, uid):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            #user = MoneyUser.objects.get(username=request.POST['username'])
            uidV = uuidTable.objects.get(uid = uid)
            user = uidV.moneyuser
            bankAccount = BankAccount.objects.create(
                form.cleaned_data['accountID'],
                form.cleaned_data['accountType'],
                form.cleaned_data['bankCompany'],
                form.cleaned_data['ownerName'],
                form.cleaned_data['title'],
                user
                )
            bankAccount.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

        return HttpResponse(serial_data)
    else:
        form = BankAccountForm()
        variables = RequestContext(request, {'form' : form})
        return render_to_response('registration/bankaccountform.html', variables)


def cash_page(request, uid):
    if request.method == 'POST':
        form = CashForm(request.POST)
        if form.is_valid():
            #user = MoneyUser.objects.get(username=request.POST['username'])
            uidV = uuidTable.objects.get(uid = uid)
            user = uidV.moneyuser
            cash = Cash.objects.create(
                form.cleaned_data['cashID'],
                form.cleaned_data['desc'],
                form.cleaned_data['user'],
                user
                )
            cash.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

        return HttpResponse(serial_data)
    else:
        form = CashForm()
        variables = RequestContext(request, {'form' : form})
        return render_to_response('registration/bankaccountform.html', variables)


def credit_card_page(request, uid):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            #user = MoneyUser.objects.get(username=request.POST['username'])
            uidV = uuidTable.objects.get(uid = uid)
            user = uidV.moneyuser
            creditCard = CreditCard.objects.create(
                form.cleaned_data['cardCompany'],
                form.cleaned_data['cardID'],
                form.cleaned_data['personPNO'],
                form.cleaned_data['smsPNO'],
                form.cleaned_data['title'],
                form.cleaned_data['type'],
                form.cleaned_data['uID'],
                form.cleaned_data['uPWD'],
                form.cleaned_data['userName'],
                form.cleaned_data['thisMonthAmount'],
                user
                )
            creditCard.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

        return HttpResponse(serial_data)
    else:
        form = CreditCardForm()
        variables = RequestContext(request, {'form' : form})
        return render_to_response('registration/bankaccountform.html', variables)

def stock_account_page(request, uid):
    if request.method == 'POST':
        print request.POST
        form = StockAccountForm(request.POST)
        if form.is_valid():
            #user = MoneyUser.objects.get(username=request.POST['username'])
            uidV = uuidTable.objects.get(uid = uid)
            user = uidV.moneyuser
            stockAccount = StockAccount.objects.create(
                form.cleaned_data['accountID'],
                form.cleaned_data['owner'],
                user
                )
            stockAccount.save()

            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

        return HttpResponse(serial_data)
    else:
        form = StockAccountForm()
        variables = RequestContext(request, {'form' : form})
        return render_to_response('registration/bankaccountform.html', variables)

def account_get(uidV, type):
    if type == BANKACCOUNT_TYPE :
        account = uidV.bankaccount
    elif type == CASH_TYPE :
        account = uidV.cash
    elif type == CREDITCARD_TYPE :
        account = uidV.creditcard
    elif type == STOCKACCOUNT_TYPE :
        account = uidV.stockaccount
    return account

def account_form_get(type, dict = None):
    if type == BANKACCOUNT_TYPE :
        form = BankAccountHistoryForm(dict)
    elif type == CASH_TYPE :
        form = CashHistoryForm(dict)
    elif type == CREDITCARD_TYPE :
        form = CreditCardHistoryForm(dict)
    elif type == STOCKACCOUNT_TYPE :
        form = SAssetForm(dict)
    else :
        print "error"
    return form
 
def account_history_create(form, uidV, type):
    account = account_get(uidV, type)
    if type == BANKACCOUNT_TYPE :
        history = BankAccountHistory.objects.create(
            form.cleaned_data['amount'],
            form.cleaned_data['date'],
            form.cleaned_data['desc'],
            form.cleaned_data['historyID'],
            form.cleaned_data['receiverName'],
            form.cleaned_data['senderName'],
            form.cleaned_data['type'],
            account
            )
    elif type == CASH_TYPE :
        history = CashHistory.objects.create(
            form.cleaned_data['amount'],
            form.cleaned_data['createdDate'],
            form.cleaned_data['desc'],
            form.cleaned_data['historyID'],
            form.cleaned_data['spentDate'],
            form.cleaned_data['storeName'],
            form.cleaned_data['storePNO'],
            form.cleaned_data['storeID'],
            form.cleaned_data['longtitude'],
            form.cleaned_data['latitude'],
            form.cleaned_data['storeAddress'],
            account
            )
    elif type == CREDITCARD_TYPE :
        history = CreditCardHistory.objects.create(
            form.cleaned_data['amount'],
            form.cleaned_data['createdDate'],
            form.cleaned_data['desc'],
            form.cleaned_data['historyID'],
            form.cleaned_data['storeName'],
            form.cleaned_data['storePNO'],
            form.cleaned_data['storeID'],
            form.cleaned_data['longtitude'],
            form.cleaned_data['latitude'],
            form.cleaned_data['storeAddress'],
            account
            )
    elif type == STOCKACCOUNT_TYPE :
        history = SAsset.objects.create(
            form.cleaned_data['assetID'],
            account
            )
    else :
        print "error"
    history.save()

def history_page(request, uid):
    uidV = uuidTable.objects.get(uid = uid)
    type = uidV.type
    
    if request.method == 'POST':
        form = account_form_get(type, request.POST)        
        if form.is_valid():
            account_history_create(form, uidV, type)
            return_data = {'success': 1}
            serial_data = simplejson.dumps(return_data)
        else:
            return_data = {'success': 0}
            serial_data = simplejson.dumps(return_data)

        return HttpResponse(serial_data)
    else:
        form = account_form_get(type)        
        variables = RequestContext(request, {'form' : form})
        return render_to_response('registration/bankaccountform.html', variables)







    
