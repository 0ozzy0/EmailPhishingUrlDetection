import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
from googlesearch import search
import requests
import whois
from datetime import datetime, date
import time
from dateutil.parser import parse as date_parse


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def generate_data_set(url):

    data_set = [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]


    if not re.match(r"^https?", url):
        url = "http://" + url

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999

    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.",domain):
            domain = domain.replace("www.","")


    try:
        whois_response = whois.whois(domain)
    except:
        pass


    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
            "name": domain
        })

    try:
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1
        pass

    #ip address existence
    try:
        ipaddress.ip_address(url)
        data_set[0] = -1
        #print("ip address -1")
    except:
        data_set[0] = 1
        #print("ip address 1")
        pass

    #url length
    if len(url) < 54:
        data_set[1] = 1
        #print("url length 1")
    elif len(url) >= 54 and len(url) <= 75:
        data_set[1] = 0
        #print("url length 0")
    else:
        data_set[1] = -1
        #print("url length -1")

    #shortining services
    match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
    if match:
        #print("shortining service -1")
        data_set[2] = -1
    else:
        #print("shortining service 1")
        data_set[2] = 1

    #at existence
    if re.findall("@", url):
        #print("@ existence -1")
        data_set[3] = -1
    else:
        #print("@ existence 1")
        data_set[3] = 1

    # // redirecting
    list=[x.start(0) for x in re.finditer('//', url)]
    if list[len(list)-1]>6:
        #print("redirecting -1")
        data_set[4] = -1
    else:
        #print("redirecting 1")
        data_set[4] = 1

    # Prefix suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        #print("Prefix suffix -1")
        data_set[5] = -1
    else:
        #print("Prefix suffix 1")
        data_set[5] = 1

    # subdomains existence
    if len(re.findall("../venv", url)) == 1:
        #print("subdomains 1")
        data_set[6] = 1
    elif len(re.findall("../venv", url)) == 2:
        #print("subdomains 0")
        data_set[6] = 0
    else:
        #print("subdomains -1")
        data_set[6] = -1

    #SSLfinalstate
    try:
        if response.text:
            #print("SSL 1")
            data_set[7] = 1
        else:
            #print("SSL -1")
            data_set[7] = -1
    except:
        #print("SSL -1")
        data_set[7] = -1



    # registration length
    try:
        expiration_date = whois_response.expiration_date
    except:
        pass
    registration_length = 0
    try:
        expiration_date = min(expiration_date)
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = abs((expiration_date - today).days)

        if registration_length / 365 <= 1:
            #print("registration length -1")
            data_set[8] = -1
        else:
            #print("registration length 1")
            data_set[8] = 1
    except:
        #print("registration length -1")
        data_set[8] = -1


    #Favicon

    if soup == -999:
        #print("favicon -1")
        data_set[9] = -1

    else:
        try:
            for head in soup.find_all('head'):
                for head.link in soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer('../venv', head.link['href'])]
                    if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                        #print("favicon 1")
                        data_set[9] = 1
                        raise StopIteration
                    else:
                        #print("favicon -1")
                        data_set[9] = -1
                        raise StopIteration
        except StopIteration:
            #print("favicon -1")
            data_set[9] = -1
            pass


    #port
    try:
        port = domain.split(":")[1]
        if port:
            #print("port -1")
            data_set[10] = -1
        else:
            #print("port 1")
            data_set[10] = 1
    except:
        #print("port -1")
        data_set[10] = -1

    # https
    if re.findall(r"^https://", url):
        #print("https 1")
        data_set[11] = 1
    else:
        #print("https -1")
        data_set[11] = -1
    # request_url
    i = 0
    success = 0
    if soup == -999:
        #print("request url -1")
        data_set[12] = -1
    else:
        for img in soup.find_all('img', src= True):
           dots= [x.start(0) for x in re.finditer('../venv', img['src'])]
           if url in img['src'] or domain in img['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for audio in soup.find_all('audio', src= True):
           dots = [x.start(0) for x in re.finditer('../venv', audio['src'])]
           if url in audio['src'] or domain in audio['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for embed in soup.find_all('embed', src= True):
           dots=[x.start(0) for x in re.finditer('../venv', embed['src'])]
           if url in embed['src'] or domain in embed['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for iframe in soup.find_all('iframe', src= True):
           dots=[x.start(0) for x in re.finditer('../venv', iframe['src'])]
           if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        try:
           percentage = success/float(i) * 100
           if percentage < 22.0 :
              #print("request url 1")
              data_set[12] = 1
           elif((percentage >= 22.0) and (percentage < 61.0)) :
              #print("request url 0")
              data_set[12] = 0
           else :
              #print("request url -1")
              data_set[12] = -1
        except:
            #print("request url 1")
            data_set[12] = 1

    # url of anchor
    percentage = 0
    i = 0
    unsafe=0
    if soup == -999:
        #print("url of anchor -1")
        data_set[13] = -1
    else:
        for a in soup.find_all('a', href=True):

            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
            if percentage < 31.0:
                #print("url of anchor 1")
                data_set[13] = 1
            elif ((percentage >= 31.0) and (percentage < 67.0)):
                #print("url of anchor 0")
                data_set[13] = 0
            else:
                #print("url of anchor -1")
                data_set[13] = -1


        except:
            #print("url of anchor 1")
            data_set[13] = 1


    # links in tags
    i=0
    success =0
    if soup == -999:
        #print("link in tags -1")
        data_set[14] = -1
    else:
        for link in soup.find_all('link', href= True):
           dots=[x.start(0) for x in re.finditer('../venv', link['href'])]
           if url in link['href'] or domain in link['href'] or len(dots)==1:
              success = success + 1
           i=i+1

        for script in soup.find_all('script', src= True):
           dots=[x.start(0) for x in re.finditer('../venv', script['src'])]
           if url in script['src'] or domain in script['src'] or len(dots)==1 :
              success = success + 1
           i=i+1
        try:
            percentage = success / float(i) * 100
            if percentage < 17.0:
                #print("link in tags 1")
                data_set[14] = 1
            elif ((percentage >= 17.0) and (percentage < 81.0)):
                #print("link in tags 0")
                data_set[14] = 0
            else:
                #print("link in tags -1")
                data_set[14] = -1
        except:
            #print("link in tags 1")
            data_set[14] = 1




        # SFH
        if soup.find_all('form' ,action=True) :
            for form in soup.find_all('form', action= True):
               if form['action'] =="" or form['action'] == "about:blank" :
                  #print("SFH -1")
                  data_set[15] = -1
                  break
               elif url not in form['action'] and domain not in form['action']:
                   #print("SFH 0")
                   data_set[15] = 0
                   break
               else:
                #print("SFH 1")
                data_set[15] = 1
                break
        else:
            #print("SFH -1")
            data_set[15] = -1
    # email submitting
    if response == "":
        #print("email submitting -1")
        data_set[16] = -1
    else:
        if re.findall(r"[mail\(\)|mailto:?]", response.text):
            #print("email submitting 1")
            data_set[16] = 1
        else:
            #print("email submitting -1")
            data_set[16] = -1
    # abnormal url
    if response == "":
        #print("abnormal url -1")
        data_set[17] = -1
    else:
        if response.text == "":
            #print("abnormal url 1")
            data_set[17] = 1
        else:
            #print("abnormal url -1")
            data_set[17] = -1

    # redirect
    if response == "":
        #print("redirect -1")
        data_set[18] = -1
    else:
        if len(response.history) <= 1:
            #print("redirect -1")
            data_set[18] = -1
        elif len(response.history) <= 4:
            #print("redirect 0")
            data_set[18] = 0
        else:
            #print("redirect 1")
            data_set[18] = 1
    # mouseover
    if response == "" :
        #print("mouseover -1")
        data_set[19] = -1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            #print("mouseover 1")
            data_set[19] = 1
        else:
            #print("mouseover -1")
            data_set[19] = -1
    # right click
    if response == "":
        #print("right click -1")
        data_set[20] = -1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            #print("right click 1")
            data_set[20] = 1
        else:
            #print("right click -1")
            data_set[20] = -1

    # popup
    if response == "":
        #print("popup -1")
        data_set[21] = -1
    else:
        if re.findall(r"alert\(", response.text):
            #print("popup 1")
            data_set[21] = 1
        else:
            #print("popup -1")
            data_set[21] = -1

    # Iframe
    if response == "":
        #print("Iframe -1")
        data_set[22] = -1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            #print("Iframe 1")
            data_set[22] = 1
        else:
            #print("Iframe -1")
            data_set[22] = -1
    # age of domain
    if response == "":
        #print("age of domain -1")
        data_set[23] = -1
    else:
        try:
            registration_date = re.findall(r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]

            if diff_month(date.today(), date_parse(registration_date)) >= 6:
                #print("age of domain -1")
                data_set[23] = -1
            else:
                #print("age of domain 1")
                data_set[23] = 1
        except:
            #print("age of domain 1")
            data_set[23] = 1


    #Dns record
    dns = 1
    try:
        d = whois.whois(domain)
    except:
        dns=-1

    if dns == -1:
        #print("Dns Record -1")
        data_set[24] = -1
    else:
        if registration_length / 365 <= 1:
            #print("Dns Record -1")
            data_set[24] = -1
        else:
            #print("Dns Record 1")
            data_set[24] = 1

    #web traffic
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank= int(rank)
        if (rank<100000):
            #print("web traffic 1")
            data_set[25] = 1
        else:
            #print("web traffic 0")
            data_set[25] = 0
    except TypeError:
        #print("web traffic -1")
        data_set[25] = -1


    #page rank
    try:
        if global_rank > 0 and global_rank < 100000:
            #print("page rank -1")
            data_set[26] = -1
        else:
            #print("page rank 1")
            data_set[26] = -1
    except:
        #print("page rank 1")
        data_set[26] = 1


    #google index
    site= search(url,5)

    if site:
        #print("google index 1")
        data_set[27] = 1
    else:
        #print("google index -1")
        data_set[27] = -1

    #link pointing to page
    if response == "":
        #print("link pointing to page -1")
        data_set[28] = -1
    else:
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            #print("link pointing to page 1")
            data_set[28] = 1
        elif number_of_links <= 2:
            #print("link pointing to page 0")
            data_set[28] = 0
        else:
            #print("link pointing to page -1")
            data_set[28] = -1
    #statistical report
    url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address=socket.gethostbyname(domain)
        ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                           '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                           '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                           '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                           '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                           '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)
        if url_match:
            # print("statistical report -1")
            data_set[29] = -1
        elif ip_match:
            #print("statistical report -1")
            data_set[29] = -1
        else:
            #print("statistical report 1")
            data_set[29] = 1
    except:
        #print("statistical report -1")
        data_set[29] = -1
        # print ('Lütfen bağlantınızı kontrol ediniz!!')

    return data_set

