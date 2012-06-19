from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)

from bookmarks.users import *
from django.core.validators import *

class Link(models.Model):
    url = models.URLField(unique=True)

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)

#Real DB For Money    
#class Subscriber(models.Model):
#    user = models.CharField(max_length = 10)
    
class Card(models.Model):
    cardID = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    pno = models.CharField(max_length=20)
    uid = models.CharField(max_length=20)

class MoneyProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # additional info
    sex = models.CharField(max_length = 2)
    pno = models.AutoField(primary_key=True)
    age = models.IntegerField()


#Money User

class MoneyUserManager(models.Manager):
    @classmethod    
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email
    
    def create_MoneyUser(self, username, password=None, sex=0, age=0):
        """
        Creates and saves a User with the given username, email and password.
        """
        #now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        username = MoneyUserManager.normalize_email(username)
        user = self.model(username=username, sex=sex, age=age)
        user.set_password(password)
        user.save()
        return user

    def get(self, username):
        query = self.filter(username=username)
        if query.count() == 0 :
            return None
        else :
            return query.get(username=username)

        
class MoneyUser(models.Model):
    #required
    username = models.EmailField(max_length = 30, unique=True)
    password = models.CharField(max_length = 255) 
    sex = models.IntegerField()
    #pno = models.AutoField(primary_key=True)
    #pno = models.CharField(max_length = 20) 
    age = models.IntegerField()
    objects = MoneyUserManager()
    
    def __unicode__(self):
        return self.username
    #optional
    #objects = UserManager()
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)

class MoneyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'sex', 'age')
admin.site.register(MoneyUser, MoneyUserAdmin)

#User Information for Money
class BankAccount(models.Model):
    accountID = models.CharField(max_length = 30)
    accountType = models.IntegerField()
    bankCompany = models.IntegerField()
    ownerName = models.CharField(max_length = 20)
    title = models.CharField(max_length = 20)
    moneyAccount = models.ForeignKey(MoneyUser)

class Cash(models.Model):
    cashID = models.CharField(max_length = 20)
    desc = models.CharField(max_length = 40)
    #subscriber = models.CharField(max_length = 20)
    user = models.CharField(max_length = 20)
    moneyAccount = models.ForeignKey(MoneyUser)

class CreditCard(models.Model):
    cardCompany = models.IntegerField()
    cardID = models.CharField(max_length = 20)
    personPNO = models.CharField(max_length = 20)
    smsPNO = models.CharField(max_length = 20)
    title = models.CharField(max_length = 20)
    type = models.IntegerField()
    uID = models.CharField(max_length = 20)
    uPWD = models.CharField(max_length = 20)
    userName = models.CharField(max_length = 20)
    moneyAccount = models.ForeignKey(MoneyUser)

class StockAccount(models.Model):
    accountID = models.CharField(max_length = 20)
    owner = models.CharField(max_length = 20)
    #subscriber = models.CharField(max_length = 20)
    moneyAccount = models.ForeignKey(MoneyUser)
