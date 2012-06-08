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
