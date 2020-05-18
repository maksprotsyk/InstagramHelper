"""
Module contains Controller class
which helps to gather data from instagram
!!! This module needs a chrome webdriver in the system PATH
"""
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as NoElement
from selenium.webdriver.remote.webelement import WebElement


class LoginError(Exception):
    """
    Exception for bad username and password
    """


class Processor:
    """
    Class for processing Instagram actions
    """
    login_pause = 30
    actions_delay = 2
    loading_delay = 11
    URL = 'https://www.instagram.com/{}/'

    def __init__(self) -> None:
        """
        Initializes Processor object with new Chrome webdriver
        """
        self.browser = webdriver.Chrome('chromedriver')


    def check_element(self, xpath: str) -> WebElement:
        """
        Checks if the given xpath is present
        on the opened web page
        """
        try:
            return self.browser.find_element_by_xpath(xpath)
        except NoElement:
            return False


    def load_element(self, xpath: str, wait=5) -> WebElement:
        """
        Tries to load element if it is not
        present on the given web page
        (waits for 'wait' seconds)
        """
        start = time.time()
        while True:
            elem = self.check_element(xpath)
            if elem:
                return elem
            elif time.time() - start > wait:
                return None

    def send_keys(self, message: str, path: str) -> None:
        """
        Enters given letters in the given field
        (Chooses a random delay between 0 and 1)
        """
        elem = self.load_element(path)
        for char in message:
            elem.send_keys(char)
            time.sleep(random.random())

    def login(self, username: str, password: str) -> None:
        """
        Login into the given Instagram account
        """

        if len(password) < 6:
            raise LoginError('Password should be '
                             'at least 6 characters long')
        else:
            #Opens login page
            self.get(self.URL[:-3])
            time.sleep(self.actions_delay)

            #enters username
            self.send_keys(username, '//*[@id="react-root"]/section'
                                     '/main/article/div[2]'
                                     '/div[1]/div/form/div[2]'
                                     '/div/label/input')
            time.sleep(self.actions_delay)

            #enters password
            self.send_keys(password, '//*[@id="react-root"]/section'
                                     '/main/article/div[2]/div[1]'
                                     '/div/form/div[3]/div/label'
                                     '/input')
            time.sleep(self.actions_delay)

            login_path = ('//*[@id="react-root"]/section/main'
                          '/article/div[2]/div[1]'
                          '/div/form/div[4]/button')

            #clicks on the login button
            self.load_element(login_path).click()

            # if the button is still on the page,
            # than the password is incorrect
            time.sleep(self.login_pause)
            if self.check_element(login_path):
                raise LoginError('Wrong password or username')

            try:
                #closes instagram login message
                self.load_element('/html/body/div[4]/div/div'
                                  '/div[3]/button[2]').click()
            except AttributeError:
                pass

    @staticmethod
    def convert_num(num: str) -> int:
        """
        Converts Instagram number in string format
        into int
        """
        if 'm' in num:
            return int(float(num[:-1]) * 1000000)
        elif 'k' in num:
            return int(float(num[:-1]) * 1000)
        else:
            return int(num.replace(',', ''))

    def get(self, url: str, refresh=False) -> None:
        """
        Opens given url if it is not opened,
        If refresh parameter is True,
        function opens page anyway
        """
        if self.browser.current_url != url or refresh:
            self.browser.get(url)

    def _get_info(self, username: str, ind: int) -> int:
        """
        Gets info about the user
        (Posts (ind = 1), Followers (ind = 2),
        Following (ind = 3))
        """
        self.get(self.URL.format(username))
        return self.convert_num(self.load_element(
                        '//div[@id="react-root"]'
                        '/section/main/div/header'
                        f'/section/ul/li[{ind}]/a'
                        '/span').text)

    def followers_num(self, username: str) -> int:
        """
        Returns the number of user followers
        """
        return self._get_info(username, 2)

    def following_num(self, username: str) -> int:
        """
        Returns the number of user followings
        """
        return self._get_info(username, 3)

    def biography(self, username: str) -> str:
        """
        Returns user biography
        """
        self.get(self.URL.format(username))
        return self.load_element('//*[@id="react-root"]'
                                 '/section/main/div/'
                                 'header/section'
                                 '/div[2]/span').text

    def quit(self) -> None:
        """
        Closes the current browser
        """
        self.browser.stop_client()
        self.browser.close()

    def is_private(self) -> bool:
        """
        Checks if the current page is private
        """
        elem = self.check_element('//*[@id="react-root"]'
                                  '/section/main/div'
                                  '/div/article/div'
                                  '/div/h2')
        if elem:
            return True
        else:
            return False



    def scroll(self, scroller: WebElement,
               part: int, sleep=0.8) -> None:
        """
        Scrolls the given scrollbar
        and sleeps for 'sleep' seconds
        """
        self.browser.execute_script("arguments[0].scrollTop ="
                                    f"arguments[0].scrollHeight/{part}",
                                    scroller)
        time.sleep(sleep)

    def get_following(self, username: str,
                      filename: str, limit=200, errors=10) -> None:
        """
        Collects followings of the given
        user and writes them into a file
        """
        # opens the profile page
        self.browser.get(self.URL.format(username))

        followings = self.following_num(username)

        #clicks on Following button
        self.load_element('//*[@id="react-root"]/section'
                          '/main/div/header/section'
                          '/ul/li[3]/a').click()

        # loads scroller element
        processing_start = time.time()
        scroller = self.load_element('/html/body/div[4]'
                                     '/div/div[2]', wait=(self.loading_delay-1))
        time.sleep(self.loading_delay + processing_start - time.time())

        # makes some big scrolls
        parts = [2, 3, 4, 5]
        random.shuffle(parts)
        for part in parts:
            self.scroll(scroller, part)

        # writes users into a file
        with open(filename, 'a') as output:
            error_num = 0
            for num in range(1, min(followings + 1, limit)):

                # if there are too many errors in a row,
                # finishes the process
                if error_num == errors:
                    time.sleep(2 * self.loading_delay)
                    break

                xpath = ("/html/body"
                         "/div[4]/div"
                         "/div[2]/ul/div"
                         "/li[{}]/div/div[1]"
                         "/div[2]/div[1]/a")
                try:
                    # tries to collect the 'num'th user
                    following = self\
                            .load_element(xpath.format(num), wait=1)\
                            .get_attribute('title')

                    print(following)
                    output.write(following + ' ')
                    error_num = 0
                except AttributeError:
                    error_num += 1
                    print("Can't find the user")

                # scrolls every sixth time and
                # waits randomly from 0.2 to 1.2 seconds
                if num % 6 == 0:
                    self.scroll(scroller, 0.2 + random.random())

    def get_post_description(self, username: str,
                             row: int, col: int, delay=0.1) -> str:
        """
        Gets description of the users post in the given position
        """
        self.get(self.URL.format(username))
        try:
            # opens the post
            self.load_element(f'//*[@id="react-root"]/section'
                              f'/main/div/div[3]/article/div[1]'
                              f'/div/div[{row}]/div[{col}]', wait=0.1).click()
            time.sleep(delay)
            # saves the message
            message = self.load_element('/html/body/div[4]/div[2]'
                                        '/div/article/div[2]/div[1]'
                                        '/ul/div/li/div/div'
                                        '/div[2]/span').text
            # closes the post
            self.load_element('/html/body/div[4]/div[3]/button').click()
            return message
        except AttributeError:
            return ''

    @staticmethod
    def set_proxy(proxy: str) -> None:
        """
        Sets a new proxy
        """
        webdriver.DesiredCapabilities.CHROME['proxy'] =\
            {'httpProxy': proxy,
             "proxyType": "MANUAL"}


if __name__ == '__main__':
    pass
