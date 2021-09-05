import hashlib
import os
import random
import string
import uuid

import pandas as pd
import pyaes as pyaes

ENCODING = 'windows-1251'
LOGIN = 'admin'
PASSWORD = 'k3fa4'
admin_builds = ['a660a555c570e8d2bf5004ebf68829bf81d3651b709c7e1d3f9b22b2a8e471e3',
                'fd8ceebf8605c623e877bbcd8f7eb4828b98d69c7fd545be97d5150202e3f0f1',
                'a17ea537c511bb1991e25c466eea2472d96eab2cb601e4f7939c6f0a042aaa04',
                'd4710ab48ae334543ed105666ec50e03477b79f95577c7d367643ea7ca7566f2']  # 1mac, 2win, 3og

key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
crypt_key = 'pbyebb2LOi31KBx2eTyVRhxLC0kDbagD'

def get_desired_capabilities(platform_version, device_name):
    path = os.path.dirname(__file__)
    desired_capabilities = {
        "platformName": "Android",
        "platformVersion": platform_version,
        "deviceName": device_name,
        "app": f"{path}\\app_apk\\vk.apk",
        'appPackage': 'com.vkontakte.android',
        'appActivity': '.MainActivity',
        'newCommandTimeout': '600'
    }
    return desired_capabilities


parsed_data = {
    'Ссылка': [],
    'Цена': [],
    'Номер': []
}


def create_xlsx():
    df = pd.DataFrame(parsed_data)
    df.to_excel('result.xlsx')
    return len(df)

def auth_start():
    login = input('Введите логин\n')
    password = input('Введите пароль\n')
    return check_login(login, password)

def current_build():
    mac_addr = hex(uuid.getnode()).replace('0x', '').encode(ENCODING)
    return hash_crypt(mac_addr)

def hash_crypt(text):
    hash = hashlib.sha256(text)
    return hash.hexdigest()

def encode(text):
    curr_key = crypt_key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(curr_key)
    ciphertext = aes.encrypt(text)
    return ciphertext

def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def check_balance(api_key):
    try:
        client = AnticaptchaClient(api_key, language_pool='ru')
        print(f'На вашем счету: {client.getBalance()}$')
    except:
        return -1

def check_login(login, password):
    logged, logged_admin = False, False
    if login == LOGIN and password == PASSWORD:
        logged = True
        logged_admin = True
    else:
        with open('accounts', mode='r+', encoding='windows-1251') as file_accs:
            accs = file_accs.read().splitlines()
            entered_acc = f'{login}:{password}'
            crypted_entered = hash_crypt(encode(entered_acc))
            for account in accs:
                if logged:
                    break
                if crypted_entered == account:
                    with open('machines', mode='r+', encoding='windows-1251') as file_machine:
                        codes = file_machine.read().splitlines()
                        build = current_build()
                        if build in admin_builds:
                            logged_admin = True
                        if build in codes:
                            logged = True
                        elif len(codes) != len(accs):
                            file_machine.write(f'{build}\n')
                            logged = True
    return logged, logged_admin
