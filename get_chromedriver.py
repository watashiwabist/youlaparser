import os
import random
import zipfile

from loguru import logger
from selenium import webdriver

# from misc import proxy_list


def get_chromedriver(use_proxy=False, mobile=False):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    proxy = None
    if use_proxy:
        proxy_list = None
        proxy = random.choice(proxy_list)
        curr_proxy = proxy[0].split(':')
        # proxy_list = [
        #     '46.188.74.15', '41657', '0af8689d6b', 'a166e849db']
        PROXY_HOST = curr_proxy[0]
        PROXY_PORT = curr_proxy[1]
        PROXY_USER = curr_proxy[2]
        PROXY_PASS = curr_proxy[3]
        manifest_json = '\n    {\n        "version": "1.0.0",\n        "manifest_version": 2,\n        "name": "Chrome ' \
                        'Proxy",\n        "permissions": [\n            "proxy_list",\n            "tabs",\n            ' \
                        '"unlimitedStorage",\n            "storage",\n            "<all_urls>",\n            ' \
                        '"webRequest",\n            "webRequestBlocking"\n        ],\n        "background": {\n           ' \
                        ' "scripts": ["background.js"]\n        },\n        "minimum_chrome_version":"22.0.0"\n    }\n '
        background_js = '\n    var config = {\n            mode: "fixed_servers",\n            rules: {\n            ' \
                        'singleProxy: {\n                scheme: "http",\n                host: "%s",\n                ' \
                        'port: parseInt(%s)\n            },\n            bypassList: ["localhost"]\n            }\n       ' \
                        ' };\n\n    chrome.proxy_list.settings.set({value: config, scope: "regular"}, function() {});\n\n    ' \
                        'function callbackFn(details) {\n        return {\n            authCredentials: {\n               ' \
                        ' username: "%s",\n                password: "%s"\n            }\n        };\n    }\n\n    ' \
                        'chrome.webRequest.onAuthRequired.addListener(\n                callbackFn,\n                {' \
                        'urls: ["<all_urls>"]},\n                [\'blocking\']\n    );\n    ' % (
                            PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as (zp):
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)
        chrome_options.add_extension(pluginfile)
    if mobile:
        mobile_list = [
            {'deviceName': 'iPhone 6'}, {'deviceName': 'iPhone X'},
            {'deviceName': 'iPhone 7'}, {'deviceName': 'iPhone 8'}, {'deviceName': 'iPhone 5'},
            {'deviceName': 'iPhone SE'}]
        mobile_emulation = random.choice(mobile_list)
        logger.info(mobile_emulation['deviceName'])
        chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
    preferences = {'webrtc.ip_handling_policy': 'disable_non_proxied_udp', 'webrtc.multiple_routes_enabled': False,
                   'webrtc.nonproxied_udp_enabled': False}
    chrome_options.add_experimental_option('prefs', preferences)
    params = {'latitude': 53.1785,
              'longitude': 50.1267,
              'accuracy': 100}
    driver = webdriver.Chrome(f'{path}\\chromedriver', chrome_options=chrome_options)
    driver.set_page_load_timeout(10)
    driver.execute_cdp_cmd('Page.setGeolocationOverride', params)
    return driver, proxy
