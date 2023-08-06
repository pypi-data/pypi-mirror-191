from TheSilent.clear import *
from TheSilent.return_user_agent import *

import hashlib
import re
import requests
import time

cyan = "\033[1;36m"
red = "\033[1;31m"

tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

#create html sessions object
web_session = requests.Session()

#fake user agent
user_agent = {"User-Agent" : return_user_agent()}

#increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

#increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

def link_scanner(url, secure = True, tor = False, my_file = " ", crawl = "all", parse = " ", title = False, delay = 1):
    clear()

    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    hash_list = []
    my_list = []
    website_list = []

    website_list.append(my_secure + url)
    tracker = -1

    while True:
        time.sleep(delay)

        if crawl != "all":
            if tracker > int(crawl):
                break
            
        if parse != " ":
            counter = 0

            while website_list:
                counter += 1

                try:
                    if parse not in website_list[counter]:
                        website_list.pop(counter)
                        my_list.pop(counter)
                        counter -= 1

                except IndexError:
                    break

        length_count = 0
        tracker += 1
        
        hash_boolean = False
        website_list = list(dict.fromkeys(website_list))

        try:
            if not website_list[tracker].endswith("/"):
                my_url = website_list[tracker] + "/"

            if tor == True:
                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120), stream = True)

                for i in stream_boolean.iter_lines():
                    length_count += len(i)

            if tor == False:
                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                for i in stream_boolean.iter_lines():
                    length_count += len(i)
                    
        except IndexError:
            break

        except:
            print(red + "ERROR! " + my_url)
            website_list.pop(tracker)
            tracker -= 1

        if length_count <= 100000000:
            try:
                print(cyan + website_list[tracker])

                if tor == True:
                    my_regex = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120))

                if tor == False:
                    my_regex = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)) 

                if my_regex.status_code >= 200 and my_regex.status_code < 300:
                    my_hash = hashlib.sha512(my_regex.text.encode("utf8")).hexdigest()

                    for i in hash_list:
                        if i == my_hash:
                            hash_boolean = True
                            break

                    if hash_boolean == True:
                        print(red + "ERROR! Duplicate hash!")

                    if hash_boolean == False:
                        hash_list.append(my_hash)
                        domain = re.findall("https://\S+?[/]|http://\S+?[/]", my_url)
                        href = re.findall("href\s*=\s*[\"\'](\S+)[\"\']", my_regex.text)
                        js = re.findall("[\"\']/(\S+)[\"\']", my_regex.text)
                        src = re.findall("src\s*=\s*[\"\'](\S+)[\"\']", my_regex.text)
                        title_regex = re.findall("<title>([\n\S\s]+)</title>", my_regex.text)

                        if title == True:
                            try:
                                my_list.append(f"{title_regex[0]}: " + website_list[tracker])

                            except IndexError:
                                my_list.append(f"(UNTITLED): " + website_list[tracker])

                        if title == False:
                            my_list.append(website_list[tracker])

                        for i in href:
                            if not i.startswith("https://") and not i.startswith("http://"):
                                if not i.startswith("/"):
                                    try:
                                        website_list.append(domain[0] + i)

                                    except IndexError:
                                        website_list.append(domain[0] + i)

                                else:
                                    try:
                                        website_list.append(domain[0] + i[1:])

                                    except IndexError:
                                        website_list.append(domain[0] + i[1:])
                                    
                            else:
                                try:
                                    website_list.append(i)

                                except IndexError:
                                    website_list.append(i)

                        for i in js:
                            try:
                                website_list.append(domain[0] + i)

                            except IndexError:
                                website_list.append(domain[0] + i)

                        for i in src:
                            if not i.startswith("https://") and not i.startswith("http://"):
                                if not i.startswith("/"):
                                    try:
                                        website_list.append(domain[0] + i)

                                    except IndexError:
                                        website_list.append(domain[0] + i)

                                else:
                                    try:
                                        website_list.append(domain[0] + i[i:])

                                    except IndexError:
                                        website_list.append(domain[0] + i[i:])

                            else:
                                try:
                                    website_list.append(i)

                                except IndexError:
                                    website_list.append(i)

                else:
                    print(red + f"{my_regex.status_code}: {my_url}")
                    website_list.pop(tracker)
                    my_list.pop(tracker)
                    tracker -= 1

            except:
                continue

    website_list = list(dict.fromkeys(website_list))
    clear()

    if my_file != " ":
        with open(my_file, "a") as f:
            for i in my_list:
                f.write(i + "\n")

    return my_list
