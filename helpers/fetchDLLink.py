from seleniumwire import webdriver
from seleniumwire.utils import decode
import requests
import json

def fetchDLLink(url):
    '''Fetches the direct download link from the given URL with retry'''
    MAX_RETRIES = 3

    for i in range(MAX_RETRIES):
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        print(">> running selenium in headless mode")

        driver = webdriver.Firefox(options=options)
        try:
            driver.get(url)
            driver.implicitly_wait(15)

            for request in driver.requests:
                if request.response and request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    data = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    if data:
                        try:
                            parsed_data = json.loads(data)
                            server = parsed_data.get('server')
                            enc_value = parsed_data.get('enc')
                            if server and enc_value:
                                result = f"{server}/getvid?evid={enc_value}"
                                response = requests.get(result, allow_redirects=True)
                                dl_link = response.url
                                return dl_link
                        except json.JSONDecodeError:
                            print(">> failed to parse JSON response.")
            print(f">> XHR not found. Trying again...({i+1})")

        finally:
            driver.quit()

    print(">> failed to find a valid XHR link after 3 attempts.")
    return