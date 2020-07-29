#kivy import
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
'''
Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "288")
Config.set("graphics", "height", "512")
'''

#telegram import
from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetHistoryRequest
api_id = 713781
api_hash = '0c51c4c50d0587d53526c7ee082b3e65'
client = TelegramClient('session_feed', api_id, api_hash)

#APP

class parse_class(Screen):
    def on_enter(self):
        max = 10
        i = 0
        for dialog in client.iter_dialogs():
            try:
                

                print(dialog.title)
                

                channel_username=dialog.title # your channel
                channel_entity=client.get_entity(channel_username)
                #print(channel_entity)
                posts = client(GetHistoryRequest(
                    peer=channel_entity,
                    limit=1,
                    offset_date=None,
                    offset_id=0, 
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0))

                print(posts.messages[0].message)    

                btn = Button(text=dialog.title, size_hint_y=None, height=40)
                chats.add_widget(btn)

                text = Label(text=posts.messages[0].message, size_hint_y=None, height=80)
                chats.add_widget(text)
        
                i = i + 1
                if i > max: break
                
            except: pass


            

        
        scroll_view.add_widget(chats)
        
        
        
        

sm = ScreenManager()
login_screen = Screen(name="login")
parse_screen = parse_class(name="parse_chat")




class TelegramFeedApp(App):

    def get_code(self, args):
        self.phone = self.phone_input.text
        print(self.phone)
        
        client.send_code_request(self.phone)
        #client.sign_in(phone, input('Enter the code: '))

    def send_code(self, args):
        self.code = self.code_input.text
        client.sign_in(self.phone, self.code)
        sm.current = "parse_chat"
        

    def change_screen(self, args):
        sm.current = "parse_chat"


    def build(self):

        # Экран входа в аккаунт
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
        # закончили создавать - отдали в Login_screen

        #экран чатов
        global chats
        global scroll_view

        scroll_view = ScrollView()
        chats = GridLayout(cols=1, spacing=10, size_hint_y=None)
        chats.bind(minimum_height=chats.setter('height'))
        
        parse_screen.add_widget(scroll_view)
        # закончили создавать - отдали в parse_screen

        #добавляем экраны в приложение
        sm.add_widget(login_screen)
        sm.add_widget(parse_screen)

        client.connect()
        if not client.is_user_authorized():
            sm.current = "login"
        else:
            sm.current = "parse_chat"
        return sm

TelegramFeedApp().run()