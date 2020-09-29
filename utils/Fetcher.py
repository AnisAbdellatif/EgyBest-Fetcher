import os
from time import sleep

from selenium import webdriver


class Fetcher:
    def __init__(self, option, params):
        self.masterURL = "http://egy.best"
        if option == "series":
            self.url = f'{self.masterURL}/episode/{params[0]}-season-{params[1]}-ep-{params[2]}'
            self.fullinfo = f"'{params[0]} S:{params[1]} Ep:{params[2]}'"
        else:
            self.url = f"{self.masterURL}/movie/{params[0]}-{params[1]}"
            self.fullinfo = f"'{params[0]} {params[1]}'"

        # set Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('log-level=2')
        # get driver path
        driverdir = f"{os.path.split(os.path.dirname(__file__))[0]}/WebDriver/chromedriver.exe"

        # start Chrome
        self.browser = webdriver.Chrome(
            executable_path=driverdir, options=chrome_options)

    def FetchQualities(self):
        self.browser.get(self.url)
        try:
            tr = self.browser.find_elements_by_xpath('//*[@id="watch_dl"]/table/tbody/tr')
            if not tr:
                return [False, ""]
            qualities = []
            for elements in tr:
                quality = elements.find_elements_by_tag_name("td")
                link = self.masterURL + quality[3].find_element_by_tag_name("a").get_attribute("data-url")
                link = quality[3].find_element_by_tag_name("a")
                qualities.append([
                    quality[0].text,
                    quality[1].text,
                    quality[2].text,
                    link
                ])
            return [True, self.fullinfo, qualities]

        except Exception as e:
            print(e)
            return [False, e, '']

    def getDownloadLink(self, quality):
        quality[3].click()

        self.browser.switch_to.window(self.browser.window_handles[-1])

        link = self.browser.find_element_by_xpath('/html/body/div[1]/div/p[2]/a[1]')
        while link.get_attribute('href') is None:
            sleep(0.5)
            link = self.browser.find_element_by_xpath('/html/body/div[1]/div/p[2]/a[1]')
        link = link.get_attribute('href')
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[-1])
        return [True, self.fullinfo, link]

    def closeBrowser(self):
        self.browser.quit()
