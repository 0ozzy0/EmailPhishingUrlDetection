import concurrent
import imaplib
import re
import getpass
import threading
from datetime import datetime, date, timedelta
import MachineLearning as RF
import FakeDomains as FD
import time
import email
from win10toast import ToastNotifier

email_user = input("Lütfen Email Adresini Giriniz: ")
email_pass = getpass.getpass(prompt='Lütfen Şifrenizi Giriniz: ')

print("Dünün ve bugünün okunmamış mailleri değerlendirilecek.")

url_checked_list = []
mydic = [  {"urls" : [], "sender" : ""} ]
toaster = ToastNotifier()

def connect_email_account():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(email_user, email_pass)
        mail.select("inbox")
        return mail

    except Exception as e:
             print("Mail adresinize bağlanırken bir hata oluştu. Lütfen kullanıcı adınızı ve şifrenizi kontrol ediniz.")


def find_links():
    yesterday = (date.today() - timedelta(1)).strftime("%d-%b-%Y")
    typ, search_data = connect_email_account().search(None, '(UNSEEN)', '(SENTSINCE {0})'.format(yesterday))
    search_data = search_data[0].split()

    for emailid in search_data:
        temp_dic = {"urls":[], "sender":""}
        resp, data = connect_email_account().fetch(emailid, '(UID BODY[TEXT])')
        _, b = connect_email_account().fetch(emailid, '(RFC822)')
        _, c = b[0]
        text = str(data[0][1])
        email_message = email.message_from_bytes(c)
        regex1 = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        for index, link in enumerate(re.finditer(regex1, text)):
            if link.group() not in temp_dic["urls"]:
                temp_dic["urls"].append(link.group())
        temp_dic["sender"] = email_message["from"]
        mydic.append(temp_dic)


def the_function(url_list):

    sender = ""
    need = 0
    i = 0
    for url in url_list:
        if not re.match(r"^https?", url):
            url = "http://" + url
        domain = re.findall(r"://([^/]+)/?", url)[0]
        if re.match(r"^www.", domain):
            domain = domain.replace("www.", "")
        if domain not in url_checked_list:
            url_checked_list.append(domain)
            i += 1
            if (RF.randomForestChecker(url) == url + " Kriter Testinden Geçemedi!!!"):
                need = 1
                print ("Bir mailinizde tespit edilen " + url + " Kriter Testinden Geçemedi!!!")
                respond = RF.randomForestChecker(url)
                toaster.show_toast(respond)
                sender = mydic[i]["sender"]
            if need == 0:
                if FD.fakeDomainChecker(domain) != 0:
                    need = 1
                    print("Bir mailinizde tespit edilen " + domain + " domain adresi sahte olabilir! lütfen kontrol ediniz.")
                    respond = domain + " domain adresi sahte olabilir! lütfen kontrol ediniz."
                    toaster.show_toast(respond)
                    sender = mydic[i]["sender"]

    # print("Mailde toplam " +str(i) +" adet link bulundu")
            if need == 1:
                print("Maili gönderen " + sender)

threads = []
while 0 < 1:
    find_links()
    try:
        for i in range(len(mydic)):
            t = threading.Thread(target=the_function, args = [mydic[i]["urls"]])
            t.start()
            threads.append(t)
    except:
        pass

    try:
        for thread in threads:
            thread.join()
    except:
        pass

    time.sleep(30)









