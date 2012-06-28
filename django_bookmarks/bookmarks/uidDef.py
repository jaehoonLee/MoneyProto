from bookmarks.models import *
from django.utils import simplejson

MONEYUSER_TYPE = 0
BANKACCOUNT_TYPE = 1
CASH_TYPE = 2
CREDITCARD_TYPE = 3
STOCKACCOUNT_TYPE = 4
BANKACCOUNTHISTORY_TYPE = 5
CASHHISTORY_TYPE = 6
CREDITCARDHISTORY_TYPE = 7
SASSET_TYPE = 8

#UNIQUE_ID Function
def money_user_uid(moneyuser):
    return_data = {
        'type': MONEYUSER_TYPE,
        'username': moneyuser.username,
        'sex' : moneyuser.sex,
        'age' : moneyuser.age,
        'uid' : moneyuser.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def bankaccount_uid(bankaccount):
    return_data = {
        'type' : BANKACCOUNT_TYPE,
        'accountID' : bankaccount.accountID,
        'accountType' : bankaccount.accountType,
        'bankCompany' : bankaccount.bankCompany,
        'ownerName' : bankaccount.ownerName,
        'title' : bankaccount.title,
        'uid' : bankaccount.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def cash_uid(cash):
    return_data = {
        'type' : CASH_TYPE,
        'cashID' : cash.cashID,
        'desc' : cash.desc,
        'user' : cash.user,
        'uid' : cash.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def creditcard_uid(creditcard):
    return_data = {
        'type' : CREDITCARD_TYPE,
        'cardCompany' : creditcard.cardCompany,
        'cardID' : creditcard.cardID,
        'personPNO' : creditcard.personPNO,
        'smsPNO' : creditcard.smsPNO,
        'title' : creditcard.title,
        'type' : creditcard.type,
        'uID' : creditcard.uID,
        'userName' : creditcard.userName,
        'thisMonthAmount' : creditcard.thisMonthAmount,
        'uid' : creditcard.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def stockaccount_uid(stockaccount):
    return_data = {
        'type' : STOCKACCOUNT_TYPE,
        'accountID' : stockaccount.accountID,
        'owner' : stockaccount.owner,
        'uid' : stockaccount.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def bankaccounthis_uid(bAhis):
    return_data = {
        'type' : BANKACCOUNTHISTORY_TYPE,
        'amount' : bAhis.amount,
        'date' : bAhis.date,
        'desc' : bAhis.desc,
        'historyID' : bAhis.historyID,
        'receiverName' : bAhis.receiverName,
        'senderName' : bAhis.senderName,
        'type' : bAhis.type,
        'bankAccount' : bAhis.bankAccount.accountID,
        'uid' : bAhis.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def cashhis_uid(cashhis):
    storeLocation = {'longtitude' : cashhis.longtitude, 'latitude' : cashhis.latitude}
    store = {'storeName' : cashhis.storeName, 'storePNO' : cashhis.storePNO,
             'storeID' : cashhis.storeID, 'storeLocation' : storeLocation,
             'storeAddress' : cashhis.storeAddress}
    return_data = {
        'type' : CASHHISTORY_TYPE,
        'amount' : cashhis.amount,
        'createdDate' : cashhis.createdDate,
        'desc' : cashhis.desc,
        'historyID' : cashhis.historyID,
        'spentDate' : cashhis.spentDate,
        'store' : store,
        'cash' : cashhis.cash.cashID,
        'uid' : cashhis.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def creditcardhis_uid(cChis):
    storeLocation = {'longtitude' : cChis.longtitude, 'latitude' : cChis.latitude}
    store = {'storeName' : cChis.storeName, 'storePNO' : cChis.storePNO,
             'storeID' : cChis.storeID, 'storeLocation' : storeLocation,
             'storeAddress' : cChis.storeAddress}
    return_data = {
        'type' : CREDITCARDHISTORY_TYPE,
        'amount' : cChis.amount,
        'createdDate' : cChis.createdDate,
        'desc' : cChis.desc,
        'historyID' : cChis.historyID,
        'store' : store,
        'cardID' : cChis.creditCard.cardID,
        'uid' : cChis.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

def sasset_uid(sasset):
    return_data = {
        'type' : SASSET_TYPE,
        'assetID' : sasset.assetID,
        'stockAccount' : sasset.stockAccount.accountID,
        'uid' : sasset.uidT.uid}
    serial_data = simplejson.dumps(return_data, ensure_ascii = False)
    return serial_data

# MONEY_USER/ACCOUNTS Request Function
def user_bankaccount(accounts):
    bankAccountList = []
    for bankaccount in accounts:
        return_data = {
            'type' : BANKACCOUNT_TYPE,
            'accountID' : bankaccount.accountID,
            'accountType' : bankaccount.accountType,
            'bankCompany' : bankaccount.bankCompany,
            'ownerName' : bankaccount.ownerName,
            'title' : bankaccount.title,
            'uid' : bankaccount.uidT.uid}
        bankAccountList.append(return_data)
    serial_data = simplejson.dumps(bankAccountList, ensure_ascii = False)
    return serial_data

def user_cash (accounts):
    cashList = []
    for cash in accounts:
        return_data = {
            'type' : CASH_TYPE,
            'cashID' : cash.cashID,
            'desc' : cash.desc,
            'user' : cash.user,
            'uid' : cash.uidT.uid}
        cashList.append(return_data)
    serial_data = simplejson.dumps(cashList, ensure_ascii = False)
    return serial_data

def user_creditcard(accounts):
    creditCardList = []
    for creditcard in accounts:
        return_data = {
            'type' : CREDITCARD_TYPE,
            'cardCompany' : creditcard.cardCompany,
            'cardID' : creditcard.cardID,
            'personPNO' : creditcard.personPNO,
            'smsPNO' : creditcard.smsPNO,
            'title' : creditcard.title,
            'type' : creditcard.type,
            'uID' : creditcard.uID,
            'userName' : creditcard.userName,
            'thisMonthAmount' : creditcard.thisMonthAmount,
            'uid' : creditcard.uidT.uid}
        creditCardList.append(return_data)
    serial_data = simplejson.dumps(creditCardList, ensure_ascii = False)
    return serial_data

def user_stockaccount(accounts):
    sAssetList = []
    for stockaccount in accounts:
        return_data = {
            'type' : STOCKACCOUNT_TYPE,
            'accountID' : stockaccount.accountID,
            'owner' : stockaccount.owner,
            'uid' : stockaccount.uidT.uid}
        sAssetList.append(return_data)
    serial_data = simplejson.dumps(sAssetList, ensure_ascii = False)
    return serial_data

# UNIQUE_ID_ACCOUNT/HISTORIES Request Function
def bankaccount_history(histories):
    bankAccountHisList = []
    for bAhis in histories:
        return_data = {
            'type' : BANKACCOUNTHISTORY_TYPE,
            'amount' : bAhis.amount,
            'date' : bAhis.date,
            'desc' : bAhis.desc,
            'historyID' : bAhis.historyID,
            'receiverName' : bAhis.receiverName,
            'senderName' : bAhis.senderName,
            'type' : bAhis.type,
            'bankAccount' : bAhis.bankAccount.accountID,
            'uid' : bAhis.uidT.uid}
        bankAccountHisList.append(return_data)
    serial_data = simplejson.dumps(bankAccountHisList, ensure_ascii = False)
    return serial_data
        
def cash_history(histories):
    cashHisList = []
    for cashhis in histories:
        storeLocation = {'longtitude' : cashhis.longtitude, 'latitude' : cashhis.latitude}
        store = {'storeName' : cashhis.storeName, 'storePNO' : cashhis.storePNO,
                 'storeID' : cashhis.storeID, 'storeLocation' : storeLocation,
                 'storeAddress' : cashhis.storeAddress}
        return_data = {
            'type' : CASHHISTORY_TYPE,
            'amount' : cashhis.amount,
            'createdDate' : cashhis.createdDate,
            'desc' : cashhis.desc,
            'historyID' : cashhis.historyID,
            'spentDate' : cashhis.spentDate,
            'store' : store,
            'cash' : cashhis.cash.cashID,
            'uid' : cashhis.uidT.uid}
        cashHisList.append(return_data)
    serial_data = simplejson.dumps(cashHisList, ensure_ascii = False)
    return serial_data

def creditcard_history(histories):
    creditCardHisList = []
    for cChis in histories:
        storeLocation = {'longtitude' : cChis.longtitude, 'latitude' : cChis.latitude}
        store = {'storeName' : cChis.storeName, 'storePNO' : cChis.storePNO,
                 'storeID' : cChis.storeID, 'storeLocation' : storeLocation,
                 'storeAddress' : cChis.storeAddress}
        return_data = {
            'type' : CREDITCARDHISTORY_TYPE,
            'amount' : cChis.amount,
            'createdDate' : cChis.createdDate,
            'desc' : cChis.desc,
            'historyID' : cChis.historyID,
            'store' : store,
            'cardID' : cChis.creditCard.cardID,
            'uid' : cChis.uidT.uid}
        creditCardHisList.append(return_data)
    serial_data = simplejson.dumps(creditCardHisList, ensure_ascii = False)
    return serial_data

def sasset_history(histories):
    sAssetList = []
    for sasset in histories:
        return_data = {
            'type' : SASSET_TYPE,
            'assetID' : sasset.assetID,
            'stockAccount' : sasset.stockAccount.accountID,
            'uid' : sasset.uidT.uid}
        sAssetList.append(return_data)
    serial_data = simplejson.dumps(sAssetList, ensure_ascii = False)
    return serial_data

