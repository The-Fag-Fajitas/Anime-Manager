from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu

from helpers.data import websites
from helpers.utils import Setup, WebHandler

Config.set('graphics', 'resizable', True)


class MainScreen(Screen):
    pass


class BrowserScreen(Screen):
    pass


# browser items:
class browserConfirm(OneLineAvatarIconListItem):
    divider = None


class FrontApp(MDApp):
    browser = "firefox"
    choices = ["Librewolf", "Brave", "Chrome", "Firefox", "Edge", "Vivaldi"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.builderstr = Builder.load_file('front.kv')

        # menu:
        items = ['Browsers', 'Login']
        menu_items = [{'text': f'{i}'} for i in items]

        self.menu = MDDropdownMenu(
            caller=self.builderstr.get_screen('mainscreen').ids.menubutton,
            items=menu_items,
            width_mult=4,
        )

    def build(self):
        self.title = 'Anime Manager'
        self.theme_cls.theme_style = 'Dark'
        return self.builderstr

    # main func:
    def onClick(self):
        site_name = self.builderstr.get_screen('mainscreen').ids.animeweb.text.lower()
        anime_name = self.builderstr.get_screen('mainscreen').ids.animename.text.lower()
        episode_nbr = self.builderstr.get_screen('mainscreen').ids.episodenbr.text

        if site_name in websites.keys():
            setup = Setup(query=anime_name, website=site_name, browser=FrontApp.browser, dubbed=False, payload=None,
                          goto_episode=episode_nbr, login=False, debug=False)
            handler = WebHandler()
            handler(setup)

        else:
            self.popup_show()

    # menu function:
    def menucaller(self, instance):
        if instance.text == 'Browsers':
            self.browserdialog()

        elif instance.text == 'Login':
            print('Login')

    # browser dialog:
    def browserdialog(self):
        self.bdialog = MDDialog(

            title='BROWSERS',
            auto_dismiss=False,
            type="confirmation",
            items=[OneLineAvatarIconListItem(text=i, on_release=self.browser_choice, divider=None) for i in
                   FrontApp.choices],
            buttons=[
                MDFlatButton(
                    text='DISMISS', text_color=self.theme_cls.primary_color, on_release=self.bdialog_close
                ),
                MDFlatButton(
                    text='SUBMIT', text_color=self.theme_cls.primary_color, on_release=self.bdialog_close
                )
            ]
        )
        self.bdialog.open()

    def bdialog_close(self, obj):
        self.bdialog.dismiss()

    # browser func:
    def browser_choice(self, instance):
        FrontApp.browser = instance.text.lower()
        return FrontApp.browser

    # popups:
    def popup_show(self):
        self.dialog = MDDialog(

            title='ERROR 101',
            text='Warning! The website you tried is not available please try again!\n\nRecommended Websites: animekisa, 4anime, YugenAnime, Crunchyroll',
            size_hint=(0.5, 0.65),
            auto_dismiss=False,
            buttons=[

                MDFlatButton(
                    text='CANCEL', text_color=self.theme_cls.primary_color, on_release=self.popup_close
                )

            ]
        )

        self.dialog.open()

    def popup_close(self, obj):
        self.dialog.dismiss()


# screens:
sm = ScreenManager()
sm.add_widget(MainScreen(name='mainscreen'))
sm.add_widget(BrowserScreen(name='browserscreen'))

if __name__ == "__main__":
    anime_manager = FrontApp()
    anime_manager.run()
