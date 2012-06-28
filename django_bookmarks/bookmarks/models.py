from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import *
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from bookmarks.users import *
from django.core.validators import *
from bookmarks.uidDef import *
from bookmarks.exceptionHandler import *
import uuid

class Link(models.Model):
    url = models.URLField(unique=True)

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)

#Real DB For Money    
#class Subscriber(models.Model):
#    user = models.CharField(max_length = 10)


#Money User
class UuidManager(models.Manager):
    def create_uuid(self, type):
        uuid_value = str(uuid.uuid4())
        uuid_value = uuid_value.replace("-", "")
        search_uid = self.filter(uid = uuid_value)
        if search_uid.count() != 0:
            self.create_uuid()
        else:
            uidV = self.model(uid = uuid_value, type = type)
        return uidV

    def get(self, uid=None):
        if uid is not None:
            query = self.filter(uid=uid)
            if query.count() == 0 :
                #raise ObjectDoesNotExist
                return EC_UID_DOES_NOT_EXISTS
            else :
                return query.get(uid=uid)    

class uuidTable(models.Model):
    uid = models.CharField(max_length = 64, primary_key = True,  editable=False)
    type = models.IntegerField()
    objects = UuidManager()
    
class uuidTableAdmin(admin.ModelAdmin):
    list_display = ('uid', 'type')
    #def get_type(self, obj):
    #    return obj.moneyobject.moneyuser.username
admin.site.register(uuidTable, uuidTableAdmin)
    
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
    
    def get(self, username=None, id=None):
        if username is not None:
            query = self.filter(username=username)
            if query.count() == 0 :
                #raise ObjectDoesNotExist
                return EC_USERNAME_DOES_NOT_EXISTS
            else :
                return query.get(username=username)

        if id is not None:
            query = self.filter(id=id)
            if query.count() == 0 :
                #raise ObjectDoesNotExist
                return EC_ID_DOES_NOT_EXISTS
            else :
                return query.get(id=id)

    def create_MoneyUser(self, username, password=None, sex=0, age=0):
        """
        Creates and saves a User with the given username, email and password.
        """
        #now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        else :
            query = self.filter(username=username)
            if query.count() > 0 :
                return EC_USERNAME_EXISTS

        username = MoneyUserManager.normalize_email(username)
        uidTable = uuidTable.objects.create_uuid(MONEYUSER_TYPE)
        user = self.model(username=username, sex=sex, age=age)
        user.set_password(password)
        user.uidT = uidTable
        user.save()
        uidTable.save()
        return user
                
class MoneyUser(models.Model):
    #required
    username = models.EmailField(max_length = 30, unique=True)
    password = models.CharField(max_length = 255) 
    sex = models.IntegerField()
    #pno = models.AutoField(primary_key=True)
    #pno = models.CharField(max_length = 20) 
    age = models.IntegerField()
    objects = MoneyUserManager()
    uidT = models.OneToOneField(uuidTable)
    
    def __unicode__(self):
        return self.username
    #optional
    #objects = UserManager()

    def __type__():
        return MONEYUSER_TYPE
    
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
    list_display = ('username', 'password', 'sex', 'age', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
admin.site.register(MoneyUser, MoneyUserAdmin)

#User Information for Money
class BankAccountManager(models.Manager):    
    def create(self, accountID, accountType, bankCompany, ownerName, title, moneyAccount):
        uidTable = uuidTable.objects.create_uuid(BANKACCOUNT_TYPE)
        uidTable.save()
        bankaccount = self.model(accountID=accountID, accountType=accountType, bankCompany=bankCompany, ownerName=ownerName, title=title)
        bankaccount.uidT = uidTable
        bankaccount.save()
        bankaccount.moneyAccount.add(moneyAccount) # do it after save. 
        return bankaccount

class BankAccount(models.Model):
    accountID = models.CharField(max_length = 30)
    accountType = models.IntegerField()
    bankCompany = models.IntegerField()
    ownerName = models.CharField(max_length = 20)
    title = models.CharField(max_length = 20)
    moneyAccount = models.ManyToManyField(MoneyUser)
    uidT = models.OneToOneField(uuidTable) 
    
    objects = BankAccountManager()
        
    def __type__(self):
        return BANKACCOUNT_TYPE 

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('accountID', 'accountType', 'bankCompany', 'ownerName', 'title', 'get_moneyaccount', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_moneyaccount(self, obj):
        users = ""
        for user in obj.moneyAccount.all():
            if users == "":
                users = user.username
            else:
                users = users + ", " +  user.username
        return users
admin.site.register(BankAccount, BankAccountAdmin)

class CashManager(models.Manager):    
    def create(self, cashID, desc, user, moneyAccount):
        uidTable = uuidTable.objects.create_uuid(CASH_TYPE)
        uidTable.save()
        cash = self.model(cashID=cashID, desc=desc, user=user)
        cash.uidT = uidTable
        cash.save()
        cash.moneyAccount.add(moneyAccount)
        return cash

class Cash(models.Model):
    cashID = models.CharField(max_length = 20)
    desc = models.CharField(max_length = 40)
    #subscriber = models.CharField(max_length = 20)
    user = models.CharField(max_length = 20)
    moneyAccount = models.ManyToManyField(MoneyUser)
    uidT = models.OneToOneField(uuidTable)

    objects = CashManager()
    
    def __type__(self):
        return CASH_TYPE

class CashAdmin(admin.ModelAdmin):
    list_display = ('cashID', 'desc', 'user', 'get_moneyaccount', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_moneyaccount(self, obj):
        users = ""
        for user in obj.moneyAccount.all():
            if users == "":
                users = user.username
            else:
                users = users + ", " +  user.username
        return users
admin.site.register(Cash, CashAdmin)

class CreditCardManager(models.Manager):    
    def create(self, cardCompany, cardID, personPNO, smsPNO, title, type, uID, uPWD, userName, thisMonthAmount, moneyAccount):
        uidTable = uuidTable.objects.create_uuid(CREDITCARD_TYPE)
        uidTable.save()
        creditcard = self.model(cardCompany = cardCompany, cardID = cardID, personPNO = personPNO, smsPNO = smsPNO, title = title, type = type, uID = uID, uPWD = uPWD, userName = userName, thisMonthAmount = thisMonthAmount)
        creditcard.uidT = uidTable
        creditcard.save()
        creditcard.moneyAccount.add(moneyAccount)
        return creditcard

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
    thisMonthAmount = models.FloatField()
    moneyAccount = models.ManyToManyField(MoneyUser)
    uidT = models.OneToOneField(uuidTable)

    objects = CreditCardManager()
     
    def __type__(self):
        return CREDITCARD_TYPE 

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('cardCompany', 'cardID', 'personPNO', 'smsPNO', 'title', 'type',
                    'uID', 'uPWD', 'userName', 'thisMonthAmount', 'get_moneyaccount', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_moneyaccount(self, obj):
        users = ""
        for user in obj.moneyAccount.all():
            if users == "":
                users = user.username
            else:
                users = users + ", " +  user.username
        return users
admin.site.register(CreditCard, CreditCardAdmin)
    
class StockAccountManager(models.Manager):    
    def create(self, accountID, owner, moneyAccount):
        uidTable = uuidTable.objects.create_uuid(STOCKACCOUNT_TYPE)
        uidTable.save()
        stockaccount = self.model(accountID = accountID, owner = owner)
        stockaccount.uidT = uidTable
        stockaccount.save()
        stockaccount.moneyAccount.add(moneyAccount) 
        return stockaccount

class StockAccount(models.Model):
    accountID = models.CharField(max_length = 20)
    owner = models.CharField(max_length = 20)
    #subscriber = models.CharField(max_length = 20)
    moneyAccount = models.ManyToManyField(MoneyUser)
    uidT = models.OneToOneField(uuidTable)

    objects = StockAccountManager()
        
    def __type__(self):
        return STOCKACCOUNT_TYPE

class StockAccountAdmin(admin.ModelAdmin):
    list_display = ('accountID', 'owner', 'get_moneyaccount', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_moneyaccount(self, obj):
        users = ""
        for user in obj.moneyAccount.all():
            if users == "":
                users = user.username
            else:
                users = users + ", " +  user.username
        return users
admin.site.register(StockAccount, StockAccountAdmin)

#History for User Money Usage Information
class BankAccountHistoryManager(models.Manager):    
    def create(self, amount, date, desc, historyID, receiverName, senderName, type, bankAccount):
        uidTable = uuidTable.objects.create_uuid(BANKACCOUNTHISTORY_TYPE)
        uidTable.save()
        bAHistory = self.model(amount = amount, date = date, desc = desc, historyID = historyID, receiverName=receiverName, senderName=senderName, type=type)
        bAHistory.uidT = uidTable
        bAHistory.bankAccount = bankAccount
        bAHistory.save()
        return bAHistory

class BankAccountHistory(models.Model):
    amount = models.FloatField()
    date = models.CharField(max_length=15)
    desc = models.CharField(max_length=30)
    historyID = models.CharField(max_length = 20)
    receiverName = models.CharField(max_length = 20)
    senderName = models.CharField(max_length = 20)
    type = models.IntegerField()
    bankAccount = models.ForeignKey(BankAccount)
    uidT = models.OneToOneField(uuidTable)
    objects = BankAccountHistoryManager()

class BankAccountHistoryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'desc', 'historyID', 'receiverName', 'senderName', 'type', 'get_bA', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_bA(self, obj):
        return obj.bankAccount.accountID
admin.site.register(BankAccountHistory, BankAccountHistoryAdmin)

class CashHistoryManager(models.Manager):    
    def create(self, amount, createdDate, desc, historyID, spentDate, storeName, storePNO, storeID, longtitude, latitude, storeAddress, cash):
        uidTable = uuidTable.objects.create_uuid(CASHHISTORY_TYPE)
        uidTable.save()
        cashHistory = self.model(amount = amount, createdDate = createdDate, desc = desc, historyID = historyID, spentDate = spentDate,
                                 storeName = storeName, storePNO = storePNO, storeID = storeID, longtitude = longtitude, latitude = latitude, storeAddress = storeAddress)
        cashHistory.uidT = uidTable
        cashHistory.cash = cash
        cashHistory.save()
        return cashHistory

class CashHistory(models.Model):
    amount = models.FloatField()
    createdDate = models.CharField(max_length=15)
    desc = models.CharField(max_length=30)
    historyID = models.CharField(max_length = 20)    
    spentDate = models.CharField(max_length=15)
    
    storeName = models.CharField(max_length = 30)
    storePNO = models.CharField(max_length = 20)
    storeID = models.CharField(max_length = 20)
    longtitude = models.FloatField()
    latitude = models.FloatField()
    storeAddress = models.CharField(max_length = 64)

    cash = models.ForeignKey(Cash)
    uidT = models.OneToOneField(uuidTable)

    objects = CashHistoryManager()

class CashHistoryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'createdDate', 'desc', 'historyID', 'spentDate', 'storeName', 'storePNO', 'storeID', 'longtitude', 'latitude', 'storeAddress',
                    'get_cash', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_cash(self, obj):
        return obj.cash.cashID
admin.site.register(CashHistory, CashHistoryAdmin)

class CreditCardHistoryManager(models.Manager):    
    def create(self, amount, createdDate, desc, historyID, storeName, storePNO, storeID, longtitude, latitude, storeAddress, creditCard):
        uidTable = uuidTable.objects.create_uuid(CREDITCARDHISTORY_TYPE)
        uidTable.save()
        ccHistory = self.model(amount = amount, createdDate = createdDate, desc = desc, historyID = historyID,
                               storeName = storeName, storePNO = storePNO, storeID = storeID,
                               longtitude = longtitude, latitude = latitude, storeAddress = storeAddress)
        ccHistory.uidT = uidTable
        ccHistory.creditCard = creditCard
        ccHistory.save()
        return ccHistory

class CreditCardHistory(models.Model):
    amount = models.FloatField()
    createdDate = models.CharField(max_length=15)
    desc = models.CharField(max_length=30)
    historyID = models.CharField(max_length = 20)

    storeName = models.CharField(max_length = 30)
    storePNO = models.CharField(max_length = 20)
    storeID = models.CharField(max_length = 20)
    longtitude = models.FloatField()
    latitude = models.FloatField()
    storeAddress = models.CharField(max_length = 64)

    creditCard = models.ForeignKey(CreditCard)
    uidT = models.OneToOneField(uuidTable)

    objects = CreditCardHistoryManager()

class CreditCardHistoryAdmin(admin.ModelAdmin):
    list_display = ('amount', 'createdDate', 'desc', 'historyID', 'storeName', 'storePNO', 'storeID', 'longtitude', 'latitude',  'storeAddress', 'get_creditCard', 'get_uid')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_creditCard(self, obj):
        return obj.creditCard.cardID
admin.site.register(CreditCardHistory, CreditCardHistoryAdmin)

class SAssetManager(models.Manager):    
    def create(self, assetID, stockAccount):
        uidTable = uuidTable.objects.create_uuid(SASSET_TYPE)
        uidTable.save()
        sasset = self.model(assetID = assetID)
        sasset.uidT = uidTable
        sasset.stockAccount = stockAccount
        sasset.save()
        return sasset

class SAsset(models.Model):
    assetID = models.CharField(max_length = 30)
    stockAccount = models.ForeignKey(StockAccount)
    uidT = models.OneToOneField(uuidTable)
    objects = SAssetManager()

class SAssetAdmin(admin.ModelAdmin):
    list_display = ('assetID', 'get_uid', 'get_bA')
    def get_uid(self, obj):
        return obj.uidT.uid
    def get_bA(self, obj):
        return obj.stockAccount.accountID
admin.site.register(SAsset, SAssetAdmin)
