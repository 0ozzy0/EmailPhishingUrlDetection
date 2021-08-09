import time
from datetime import time
from bs4 import BeautifulSoup
import requests

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent" : USER_AGENT}

url = "https://www.phishtank.com/phish_search.php?page=1&valid=y&Search=Search"

source = requests.get(url, headers=headers)

soup = BeautifulSoup(source.text, "xml")
print(soup.prettify())
table = soup.find('table' ,attrs={'class':'data'})
first_td = table.find('td')
print(first_td)


