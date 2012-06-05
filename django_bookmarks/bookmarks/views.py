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
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>it is now %s.</body></html>" % now
    return HttpResponse(html)



@csrf_exempt
def login_page(request):
    if request.method == 'POST':
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
            
@csrf_exempt
def login_page_phone(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # success
                return HttpResponse('1')  
        else:
            # disabled account
            return HttpResponse('0')
    else:
        return render_to_response('registration/login.html') 

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")

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
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form' : form})
    return render_to_response('registration/register.html', variables)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
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

def main_page(request):
    template = get_template('main_page.html')
    variables = Context({'user' : request.user })
    output = template.render(variables)

    return HttpResponse(output)



#def main_page(request):
#    output = '''
#    <html>
#    <head><title>%s</title></head>
#    <body>
#    <h1>%s</h1><p>%s</p>
#    </body>
#    </html>
#    '''%(
#        'django wow',
#        'django',
#        'django3',
#        )
#    return HttpResponse(output)
