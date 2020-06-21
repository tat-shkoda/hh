import time

import requests
from urllib3 import disable_warnings, exceptions

disable_warnings(exceptions.InsecureRequestWarning)

def search_captcha(response):
    pass


def send_request(page_url):
    is_successfull = False
    attempts = 0

    while is_successfull == False:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        }

        try:
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
