import re
import secrets
import time
import pyautogui as pyg
from .data import websites, browsers, drivers, webdriver, browser_options, Website, dub_options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib.parse


class Helpers:

    @staticmethod
    def construct(desired_website, query):
        # replace returns the string if there is no whitespace or one space
        search_url = fr"{desired_website.search}{desired_website.keyword}={urllib.parse.quote(query)}"
        return f"{desired_website.url}{search_url}"

    @staticmethod
    def log_in(desired_website: Website, driver, payload: list):
        # TODO : Fix this later (currently works only for yugen)
        try:
            driver.get(url=desired_website.login) if desired_website.url else None

            def send_credentials():
                Helpers.find_and_click(desired_website.name_or_email, driver, 0, query=payload[0])
                Helpers.find_and_click(desired_website.password, driver, 0, query=payload[1])
                ActionChains.send_keys(Keys.ENTER)

            t_initial = time.time()
            send_credentials()

            t_final = time.time()
            t_delta = t_final - t_initial
            if t_delta == 60:
                raise TimeoutException

        except TimeoutException:
            pyg.alert("Captcha Completion Failed", "Error", "OK")

    @staticmethod
    def find_and_click(argument: str, driver, index: int, write=True, query="", click=True):
        functions = [driver.find_element_by_name, driver.find_elements_by_name,
                     driver.find_element_by_xpath, driver.find_elements_by_xpath,
                     driver.find_element_by_class_name, driver.find_elements_by_class_name]
        element = functions[index](argument)
        element.click() if click else None
        element.send_keys(query) if write else None
        return element


class Setup:
    def __init__(self, query, website, browser, dubbed, payload, goto_episode, login, debug):
        args = locals()
        del args["self"]
        self.__dict__.update(args)

    @staticmethod
    def options_setup(browser="brave"):
        get_browser_path = browsers[browser]
        # instantiates the options class
        get_options = lambda b: browser_options[b]() if b in browser_options else browser_options['default']()
        options = get_options(browser)
        options.binary_location = get_browser_path
        if browser not in browser_options:
            # option.add_extension(privacy_path)
            options.add_experimental_option("detach", True)
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")

        return options

    @staticmethod
    def driver_setup(browser='brave'):
        driver = drivers[browser] if browser in drivers.keys() else webdriver.Chrome
        return driver


class WebHandler:
    def __init__(self):
        pass

    def __call__(self, setup):
        browser = setup.browser
        query, website, dubbed, goto_episode = setup.query, setup.website, setup.dubbed, setup.goto_episode
        payload, login = setup.payload, setup.login
        desired_website = websites[website]
        options = Setup.options_setup(browser)
        driver = Setup.driver_setup(browser)
        debug = setup.debug
        read_only_query = query + dub_options[website] if dubbed else query
        actual_query = Helpers.construct(desired_website, query)
        print(actual_query)
        wait = secrets.choice(range(3, 6))
        options.set_headless() if debug else None
        driver = driver(options=options)
        website_meta = {
            'animekisa': driver.find_elements_by_class_name,
            'yugenanime': driver.find_elements_by_xpath,
            'crunchyroll': driver.find_elements_by_class_name,
            "9anime": driver.find_elements_by_xpath}
        dub_button = r"//a[contains(text(),'Dub')]"

        try:
            driver.set_window_size(1600, 1200)
            driver.implicitly_wait(wait)
            pyg.click(x=1914, y=136) if browser == 'brave' else 0
            driver.get(actual_query)
            an_list = website_meta[website](desired_website.anime)
            driver.maximize_window()
            time.sleep(5)
            pyg.doubleClick(x=311, y=334) if website == "9anime" else None
            def get_anime():
                for anime in an_list:
                    if anime.text.lower() == read_only_query.lower():
                        anime.click()
                        break
                else:
                    an_list[0].click()
                print("sucessfully got anime")
                return an_list

            def get_episode():
                Helpers.find_and_click(driver=driver, argument=r"//a[@class='link p-15']",
                                    index=3, write=False, click=False)[1].click() if website == "yugenanime" else None
                pyg.doubleClick(x=248, y=968) if website == "9anime" else None
                # TODO: Fix CR's retarded edge cases
                eps = website_meta[website](desired_website.episodes)
                for episode in eps:
                    if goto_episode == "".join(re.findall("[1-9]+",episode.text)):
                        episode.click()
                        break
                else:
                    eps[-1].click() if website != 'animekisa' else eps[0].click
                print("successfully got episode")
                try:
                    Helpers.find_and_click(dub_button, driver, 2, write=False) if website == "yugenanime" and dubbed else None
                
                except NoSuchElementException:
                    pyg.confirm(text="This anime probably doesn't have a dubbed version", title='Dub Version', buttons=['OK', 'Cancel'])
                return eps
            anime, episodes = get_anime(),  get_episode()
            driver.close() if debug else None
            return anime, episodes
        # except StaleElementReferenceException:
        #     pass
        except NoSuchWindowException:
            pass
        # This helps am not break in case no results were found
        except IndexError:
            pass

