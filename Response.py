import time

import requests
from lxml import html

from urllib3 import disable_warnings, exceptions

from Proxy import get_active_proxy


disable_warnings(exceptions.InsecureRequestWarning)

def search_captcha(response):
    tree = html.document_fromstring(response.content)
    if tree.xpath("//div[@class='firewall-container']"):
        return True
    return False


def send_request(page_url):
    is_successfull = False
    attempts = 0

    while is_successfull == False:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        }

        try:
            get_active_proxy()
            response = requests.get(
                page_url,
                headers=headers,
                timeout=15,
                verify=False
            )

            print(response.status_code, page_url)

            if response.status_code == 404:
                return 404

            if response.status_code == 200:
                if search_captcha(response):
                    print('Найдена капча', page_url)
                    time.sleep(600)
                    continue
                else:
                    is_successfull = True
                    response.encoding = 'cp-1251'
                    return response

        except Exception as e:
            attempts += 1
            print('Ошибка соединения', page_url, e)

            if attempts == 3:
                return

            continue


def send_request_with_proxy(page_url):
    is_successfull = False
    while is_successfull == False:
        print(page_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        }

        try:
            proxy = get_active_proxy()

            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
            response = requests.get(
                page_url,
                headers=headers,
                proxies=proxies,
                timeout=15
            )

            if response.status_code == 404:
                return 404

            if response.status_code == 200:
                if search_captcha(response):
                    print('Найдена капча', page_url)
                    time.sleep(600)
                    continue
                else:
                    is_successfull = True
                    response.encoding = 'cp-1251'
                    return response

        except Exception as e:
            print('Ошибка соединения', page_url, e)
            continue
