#kivy import
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "288")
Config.set("graphics", "height", "512")


#telegram import
from telethon import TelegramClient, sync
api_id = 713781
api_hash = '0c51c4c50d0587d53526c7ee082b3e65'
client = TelegramClient('session_feed', api_id, api_hash)

#APP
sm = ScreenManager()
login_screen = Screen(name="login")
parse_screen = Screen(name="parse_chat")
parse_screen.add_widget(Label(text="Начало парсинга, ожидайте"))



class TelegramFeedApp(App):

    def get_code(self, args):
        self.phone = self.phone_input.text
        print(self.phone)
        client.connect()
        client.send_code_request(self.phone)
        #client.sign_in(phone, input('Enter the code: '))

    def send_code(self, args):
        self.code = self.code_input.text
        client.sign_in(self.phone, self.code)

    def change_screen(self, args):
        sm.current = "parse_chat"


    def build(self):
        bl = BoxLayout(orientation='vertical')

        self.phone_input = TextInput()
        self.phone_button = Button(text="Отправить номер", on_press=self.get_code)
        self.code_input = TextInput()
        self.code_button = Button(text="Отправить код", on_press=self.send_code)
        bl.add_widget(self.phone_input)
        bl.add_widget(self.phone_button)
        bl.add_widget(self.code_input)
        bl.add_widget(self.code_button)

        bl.add_widget(Button(on_press=self.change_screen))
        
        login_screen.add_widget(bl)
        sm.add_widget(login_screen)
        sm.add_widget(parse_screen)
        sm.current = "login"
        return sm

TelegramFeedApp().run()