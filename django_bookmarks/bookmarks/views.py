# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.loader import get_template
from django.template import Context


import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>it is now %s.</body></html>" % now
    return HttpResponse(html)

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/account/loggedin/")
    else:
        return HttpResponseRedirect("/account/invalid/")
    
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/loggedout/")

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
