# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from get_chromedriver import get_chromedriver

class Links:

    def __init__(self, url):
        self.url = url

class Parse:

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_driver(self):
        driver, proxy = get_chromedriver(mobile=True)
        self.driver = driver
        self.proxy = proxy

    def send_auth_keys(self):
        self.driver.find_element_by_name('email').send_keys(self.login)
        self.driver.find_element_by_name('pass').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="mcont"]/div[1]/div[2]/div/div/form/div[1]/input').click()

    def auth_vk(self):
        self.driver.get('https://m.vk.com')
        time.sleep(2)
        self.send_auth_keys()


    def run(self):
        try:
            self.get_driver()
            self.auth_vk()
        except Exception as e:
            print(e)
        



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = Parse('89950953487','smailbu1')
    a.run()
    print('aboba')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
