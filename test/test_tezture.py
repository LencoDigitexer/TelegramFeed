'''
Скрипт для тестирования переноса текста в ограниченном пространстве
Проблема в переносе длинного текста описана зддесь https://stackoverflow.com/questions/18670687/how-i-can-adjust-variable-height-text-property-kivy
'''


import kivy
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MultiLineLabel(Button):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)


class DynamicHeight(App):
    def build(self):
        grid = GridLayout(cols=1,size_hint_x=None, width="300dp")

        l=['1066 In this year the monastery at Westminster was hallowed on Childermas day (28 December). And king Eadward died on Twelfth-mass eve (5 January) and he was buried on Twelfth-mass day, in the newly hallowed church at Westminster. And earl Harold succeeded to the Kingdom of England, as the king had granted it to him and men had also chosen him thereto and he was blessed as king on Twelfth-mass day. And in the same year that he was king he went out with a naval force against William ... And the while count William landed at Hastings, on St. Michaels mass-day and Harold came from the north and fought against him before his army had all come and there he fell and his two brothers Gyrth and Leofwine and William subdued this land, and came to Westminster and archbishop Ealdred hallowed him king and men paid him tribute and gave him hostages and afterwards bought their land', 'One line']

        for i in l:
            l = MultiLineLabel(text=i)
            print(l)
            grid.add_widget(l)
        return grid

DynamicHeight().run()