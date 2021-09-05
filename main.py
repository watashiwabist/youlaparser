import time

from appium import webdriver
from loguru import logger

from misc import ENCODING, parsed_data, create_xlsx, get_desired_capabilities, auth_start, hash_crypt, id_generator, \
    encode


class File:

    def __init__(self, path, flags='rt'):
        self.path = path
        self.file = open(path, mode=flags, encoding=ENCODING)

    def read_content(self):
        self.content = self.file.read()

    def get_content(self):
        try:
            self.content
        except:
            self.read_content()
        return self.content


class Link:
    def __init__(self, link):
        self.link = link
        self.bad = 0


class Account:
    def __init__(self, account):
        self.account = account
        self.login = account.split(':')[0]
        self.password = account.split(':')[1]
        self.bad = 0


class Parse:

    @logger.catch()
    def __init__(self, links):
        self.link_list = links

        # self.parsed_data = {
        #     'Ссылка': [],
        #     'Цена': [],
        #     'Номер': []
        # }
        self.ads_count = 0

    def set_acc(self, account):
        self.account = account

    # @logger.catch()
    # def get_driver(self):
    #     driver, proxy = get_chromedriver(mobile=True)
    #     self.driver = driver
    #     self.proxy = proxy

    @logger.catch()
    def split_keys(self):
        return self.account.split(':')

    def send_auth_keys(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/email_or_phone').send_keys(self.account.login)
            self.driver.find_element_by_id('com.vkontakte.android:id/vk_password').send_keys(self.account.password)
            self.driver.find_element_by_id('com.vkontakte.android:id/continue_btn').click()
        except Exception as e:
            print(f'send_auth_keys: {e}')

    def get_android_driver(self, platform_version, device_name):
        try:
            desired_capabilities = get_desired_capabilities(platform_version, device_name)
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities=desired_capabilities)
            self.driver = driver
            self.driver_size = self.driver.get_window_size()
            self.x_size = self.driver_size['width']
            self.y_size = self.driver_size['height']
            logger.info('Андроид драйвер успешно запущен.')
            time.sleep(4)
            return True
        except Exception as e:
            logger.error('Не удалось запустить андроид драйвер.')
            print(f'get_android_driver: {e}')
            return False

    def back_to_profile(self):
        while True:
            try:
                self.driver.find_element_by_id('com.vkontakte.android:id/tab_menu').click()
                return True
            except:
                self.driver.back()
                continue

    def login_vk(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/login_button').click()
        except:
            pass
        try:
            time.sleep(4)
            self.send_auth_keys()
            time.sleep(14)
            if self.check_log_in():
                return 1
            return 0
        except Exception as e:
            self.driver.quit()
            print(f'login_vk: {e}')
            return -1

    def wait_loading(self):
        try:
            text = self.driver.find_element_by_id('android:id/message').text
            while 'агрузка' in text:
                text = self.driver.find_element_by_id('android:id/message').text
                time.sleep(1.5)
        finally:
            return 1

    def check_number_verif(self):
        try:
            self.driver.find_element_by_xpath(
                '//android.view.View[@content-desc="Пропустить ввод номера"]/android.widget.TextView')
            self.driver.back()
            time.sleep(4)
            return True
        except:
            return False

    def check_sent(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/bubble')
            return 1
        except:
            return 0

    def send_link_msg(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/writebar_edit').send_keys(self.current_link.link)
        except:
            pass
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/writebar_send').click()
            self.wait_loading()
            time.sleep(5)
        except:
            pass

    def set_current_link(self):
        self.current_link = self.link_list.pop()

    def click_to_link(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/bubble').click()
            # self.driver.find_element_by_id('com.vkontakte.android:id/fhl').click()
            time.sleep(6)
            try:
                self.driver.find_element_by_id('com.vkontakte.android:id/progress').click()
            except:
                pass
            return 1
        except Exception as e:
            return 0

    def clear_msg_history(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/title_dropdown').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[4]').click()
            time.sleep(2)
            self.driver.find_element_by_id('com.vkontakte.android:id/btn_positive').click()
            time.sleep(2)
        except Exception as e:
            print(f'clear_msg_history: {e}')

    def check_log_in(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/incorrect_login_view')
            return False
        except Exception as e:
            return True

    def go_to_saved_msg(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/tab_messages').click()
            time.sleep(3)
            self.driver.find_element_by_id('com.vkontakte.android:id/search').click()
            time.sleep(3)
            self.driver.find_element_by_id('com.vkontakte.android:id/msv_query').send_keys('Избранное')
            time.sleep(3)
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout').click()
            time.sleep(3)
        except Exception as e:
            print(f'go_to_saved_msg: {e}')

    def click_to_ponyatno(self):
        try:
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.Button').click()
            time.sleep(2)
        except:
            pass

    def get_number_from_ad(self):
        try:
            # click to button Позвонить
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[6]/android.widget.Button[1]'
            ) \
                .click()
            time.sleep(1.5)
            if not self.check_number():
                return -1
            # click to number
            self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]'
            ).click()
            time.sleep(5)
            number = self.driver.find_element_by_id('com.google.android.dialer:id/digits').text
            logger.success(f'Получен номер: {number}')
            return number
        except Exception as e:
            return 0

    def get_data(self):
        number = self.get_number_from_ad()
        if not number:
            self.current_link.bad += 1
            self.account.bad += 1
            if number != -1:
                self.link_list.insert(0, self.current_link)
            logger.info(f'Не удалось спарсить номер: {self.current_link.link}\n'
                        f'Попытка номер {self.current_link.bad - 1}')
            return False
        elif number == -1:
            logger.info('')
        self.back_to_vk()
        self.driver.tap([(self.x_size / 2, self.y_size / 2)])
        price = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[4]'
        ).text
        self.append_data(number, price)
        self.ads_count += 1
        logger.success(f'Объявлений спаршено: {self.ads_count}\n'
                       f'Текущие данные:\n'
                       f'   Ссылка: {self.current_link.link}\n'
                       f'   Номер: {number}\n'
                       f'   Цена: {price}')
        return True

    def back_to_vk(self):
        while True:
            self.driver.back()
            try:
                self.driver.find_element_by_id('com.vkontakte.android:id/action_bar_root')

                logger.info('Приложение VK снова открыто.')
                return
            except:
                continue

    def back_to_saved_msg(self):
        while True:
            try:
                self.driver.find_element_by_id('com.vkontakte.android:id/bubble')
                return True
            except:
                self.driver.back()
                continue

    def append_data(self, number, price):
        parsed_data['Ссылка'].append(self.current_link.link)
        parsed_data['Номер'].append(''.join(list(filter(str.isdigit, number))))
        parsed_data['Цена'].append(''.join(list(filter(str.isdigit, price))))

    def check_number(self):
        try:
            call_later_text = self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View[2]') \
                .text
            logger.error(f'Ошибка парса номера: {call_later_text}')
            if 'Пользователь разрешил звонки' in call_later_text:
                self.driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[2]/android.widget.Button[1]') \
                    .click()
            return False
        except:
            return True

    def open_menu_tab(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/right_menu_main_action').click()
        except Exception as e:
            print(f'open_menu_tab: {e}')

    def open_settings_tab(self):
        try:
            self.driver.find_element_by_id('com.vkontakte.android:id/menu_settings').click()

        except Exception as e:
            print(f'open_settings_tab: {e}')

    def logout_from_vk(self):
        try:
            self.driver.swipe(start_x=self.x_size / 2, start_y=self.y_size / 2, end_x=self.x_size / 2,
                              end_y=self.y_size / 6)
            time.sleep(1)
            self.driver.find_element_by_id('com.vkontakte.android:id/logout').click()
            time.sleep(1)
            self.driver.find_element_by_id('android:id/button1').click()
            time.sleep(2)
            logger.info(f'Успешный выход с аккаунта: {self.account.account}')
            self.driver.find_element_by_id('com.vkontakte.android:id/use_another_account').click()
        except Exception as e:
            print(f'logout_from_vk: {e}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logged, logged_admin = auth_start()
    vk_file = File('vk.txt')
    links_file = File('links.txt')
    while True:
        if not logged:
            print('Вы не авторизовались. Попробуйте ещё раз.\n')
            logged, logged_admin = auth_start()
        else:
            text = "Для старта парсера напишите: 1\n" \
                   "Для выдачи доступа напишите: 2\n" \
                if logged_admin \
                else "Для старта парсера напишите: 1\n"
            action = input(text)
            if action == '1':
                platform_version = input('Введите версию андроида:\n')
                device_name = input('Введите название устройства:\n')
                vk_content = vk_file.get_content()
                vk_accounts = [Account(account) for account in vk_content.split('\n')
                               if account != '' and ':' in account]
                links_content = links_file.get_content()
                links_list = [Link(link) for link in links_content.split('\n')
                              if link != '' and 'https://youla.ru/' in link]
                parse = Parse(links_list)
                logger.info('Запускаю андроид.')
                if not parse.get_android_driver(platform_version, device_name):
                    logger.error('Попробуйте запустить программу еще раз.\n\n')
                    time.sleep(8)
                    exit()
                for account in vk_accounts:
                    try:
                        parse.set_acc(account)
                        login = parse.login_vk()
                        if login == 1:
                            logger.success(f'Удачная авторизация в VK || {parse.account.account}')
                            while len(parse.link_list):
                                if parse.account.bad >= 5:
                                    raise Exception('DeadAcc')
                                parse.go_to_saved_msg()
                                parse.clear_msg_history()
                                parse.set_current_link()
                                logger.info(f'Идет парсинг: {parse.current_link.link}')
                                parse.send_link_msg()
                                if not parse.check_sent():
                                    parse.send_link_msg()
                                    parse.check_number_verif()
                                parse.click_to_link()
                                time.sleep(14)
                                parse.click_to_ponyatno()
                                parse.get_data()
                                parse.back_to_saved_msg()
                                # back
                            if not parse.link_list:
                                break
                            parse.back_to_profile()
                            parse.open_menu_tab()
                            parse.open_settings_tab()
                            parse.logout_from_vk()
                        elif login == 0:
                            logger.error(f'Неверные данные от аккаунта || {parse.account.account}')
                    except Exception as e:
                        if 'DeadAcc' in e.args:
                            logger.info(f'Мертвый аккаунт: {parse.account}')
                            continue
                        elif 'A session is either terminated or not started' in e.args:
                            logger.error('Ошибка с андроидом. Попробуйте перезапустить программу или компьютер.')
                            time.sleep(8)
                            exit()
                len_xlsx = create_xlsx()
                if len_xlsx:
                    logger.success(f'Был создан excel файл с {len_xlsx} номерами.')
                else:
                    logger.error('Не удалось создать excel файл.')
                logger.info('Работа выполнена.')
                try:
                    parse.driver.quit()
                except:
                    pass
            elif action == '2' and logged_admin:
                while True:
                    login = 'user'
                    password = id_generator()
                    with open('accounts', encoding='windows-1251') as file:
                        lines = file.read().splitlines()
                        crypted_acc = f"{hash_crypt(encode(f'{login}:{password}'))}"
                        if crypted_acc not in lines:
                            break
                with open('accounts', 'a') as accs:
                    accs.write(f'\n{crypted_acc}')
                print(f'Пользователь создан: {login} {password}\n\n')
            else:
                print('Вы ввели неверную команду, попробуйте заново.\n')
