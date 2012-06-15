from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from bookmarks.users import *

class MoneyUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = self.MoneyUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.MoneyUser.objects.get(username=username):
            return None

    def get_user(self, user_id):
        try:
            return self.MoneyUser.objects.get(pk=user_id)
        except self.MoneyUser.DoesNotExist:
            return None
        
    @property
    def MoneyUser(self):
        if not hasattr(self, '_MoneyUser'):
            #self._MoneyUser = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            self._MoneyUser = get_model('bookmarks', 'MoneyUser')
            if not self._MoneyUser:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._MoneyUser

    def users(self):
        return self.MoneyUser.objects.all()

