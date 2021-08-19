# The main website information mega class
# This allows the website information to be
# automated and extracted fairly easily.
import os
import platform
from dataclasses import dataclass
from selenium import webdriver


@dataclass
class Website:
    name: str
    url: str
    anime: str
    episodes: str
    keyword: str
    search: str
    login: str
    name_or_email: str
    password: str
    has_captcha: bool


# Global Variables

Ak = Website(name="animekisa", url='https://animekisa.tv', anime='similardd',
             episodes='centerv', keyword='q', search=r'/search?', login='', name_or_email='', password='', has_captcha=False)
nine_a = Website('9anime', 'https://9anime.to', anime=r'//*[@id="body"]/div[2]/aside[1]/section/div/ul/descendant::a',
                 episodes='//*[@id="episodes"]/section/div[2]/ul/descendant::a', keyword='keyword',
                 search=r'/search?', login='',
                 name_or_email='', password='', has_captcha=False)
Yugen = Website('yugenanime', 'https://yugenani.me/', anime="anime_name",
                episodes=r'ep-title',
                keyword='q', search=r'search?', login='https://yugenani.me/login/',
                name_or_email='email', password='password', has_captcha=True)

Crunchyroll = Website("crunchyroll", "https://www.crunchyroll.com/",
                      r'name',
                      episodes=r'series-title block ellipsis',
                      keyword=r'from=&q', search=r'search?', login='https://www.crunchyroll.com/login',
                      name_or_email='login_form[name]', password='login_form[password]', has_captcha=True)

# Crunchyroll  to be added for the American weebs
sites = (Ak, nine_a, Yugen, Crunchyroll)
paths = {"Windows": {
    "chromium_path": fr"{os.path.expanduser('~')}\AppData\Local\Chromium\Application\chrome.exe",
    "brave_path  ": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "chrome_path ": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox_path": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "librewolf_path": r"C:\Program Files\Librewolf\librewolf.exe",
    "vivaldi_path": fr"{os.path.expanduser('~')}\AppData\Local\Vivaldi\Application\vivaldi.exe",
    "firefox_developer_path": r"C:\Program Files\Firefox Developer Edition\firefox.exe"},
    "Linux": {
        "chromium_path": "/snap/bin/chromium",
        "brave_path": "/usr/bin/brave-browser-stable",
        "chrome_path ": "/usr/local/bin",
        "firefox_path": "/usr/bin/firefox",
        "librewolf_path": "/usr/local/bin",
        "vivaldi_path": "/usr/local/bin",
        "firefox_developer_path": "/usr/local/bin"},
    "Darwin": {
        "chromium_path": "usr/local/bin",
        "brave_path  ": "usr/local/bin",
        "chrome_path ": "usr/local/bin",
        "firefox_path": "usr/local/bin",
        "librewolf_path": "usr/local/bin",
        "vivaldi_path": "usr/local/bin",
        "firefox_developer_path": "usr/local/bin"}}

operating_system = platform.system()
websites = {website.name: website for website in sites}
browsers = {name.replace("_path", "").strip(): paths[operating_system][name] for name in paths[operating_system]}
drivers = {'ie': webdriver.Ie, 'firefox': webdriver.Firefox,
           'edge': webdriver.Edge, 'safari': webdriver.Safari,
           'android': webdriver.android, 'librewolf': webdriver.Firefox}

browser_options = {'firefox': webdriver.firefox.options.Options,
                   'librewolf': webdriver.firefox.options.Options,
                   'default': webdriver.chrome.options.Options}

dub_options = {'animekisa': " dubbed", 'yugenanime': "",
               '4anime': "(dub)", 'crunchyroll': "(dub)",
               '9anime': "(dub)"}
