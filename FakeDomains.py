from datetime import time
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
from http import cookiejar
import time

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent" : USER_AGENT}

def fakeDomainChecker(search):

    sended_number = 0
    url = f"https://www.google.com/search?&q={search}"
    source = requests.Session()
    source.cookies.set_policy(BlockAll())
    try:
        #source = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        source = requests.get(url, headers=headers)

        if source.status_code == 429:
            time.sleep(int(source.headers["Retry-After"]))
    except Exception:
        print(Exception)


    soup = BeautifulSoup(source.text,"html.parser")
    divs = soup.find_all('div')
    spans = soup.find('span', {'class':'gL9Hy'})
    heads = soup.find_all('div', {'class':'TbwUpd'})
    heads2 = soup.find_all('div', {'class':'Zu0yb LWAWHf qzEoUe"'} )

    result = 0

    #Checking for titles
    for head in heads:
        if search in head.getText():
            result = result +1

        else:
            result = result + 0

    #Checking for titles
    for head in heads2:
        if search in head.getText():
            result = result + 1

        else:
            result = result + 0

    if result == 0:
        sended_number = 1
    else:
        sended_number = 0

    # Checking for no result
    for s in divs:
        if "ile ilgili hiçbir arama sonucu mevcut değil." in s.text:
            sended_number = sended_number +1

        else:
            sended_number = sended_number + 0

    # Checking for spell checking"
    if spans != None:
        sended_number = sended_number +1

    else:
        sended_number = sended_number + 0


    return sended_number




