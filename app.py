import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.slider import Slider
import pickle
import random
global d
try:
    with open('opens.pickle', 'rb') as f:
        d = pickle.load(f)
except:
    d = {'UTG':{}, 'MP':{},'CO':{}, 'BTN':{}, 'SB':{}}

class hand_button(Button):
    col = -1
    row = -1
    n = 0
    def __init__(self, count = 0, position = '', **kwargs):
        super(hand_button, self).__init__(**kwargs)
        self.count = count % 2
        self.background_color = [[255, 0, 0, 1],[125,125,125,0.5]][(self.count + 1) % 2]
        self.border = (12,12,12,1)
        self.color = [2,2,2,1]
        self.p = position
        hand_button.col = (hand_button.col + 1)%13
        if(not hand_button.col):
            hand_button.row = (hand_button.row + 1)%13
        i = hand_button.row
        j = hand_button.col
        self.combos = [4, 12, 6][(i>j) - (i == j)]
        hand_button.n += [0, self.combos][self.count]
        #print(self.text, self.combos)
    
    def on_press(self):
        global d
        self.count += [1, -1][self.count]
        self.background_color = [[255, 0, 0, 1],[125,125,125,0.5]][(self.count + 1) % 2]

        d[self.p][self.text] = self.count
        #hand_button.n += (self.combos * [1,-1][(self.count+1)%2])
        #print(self.count,self.pos)
        
        

class hands_screen(GridLayout):
    def __init__(self, name = "", **kwargs):
        super(hands_screen, self).__init__(**kwargs)
        global d
        self.l = ['A', 'K', 'Q', 'J', 'T'] + [str(i) for i in range(9,1,-1)]
        self.cols = 13
        self.rows = 13
        self.count = 0
        self.name = name
        for i in range(13):
            for j in range(13):
                hand = [str(self.l[i])+str(self.l[j]) + 's', str(self.l[j]) + str(self.l[i])+'o', str(self.l[j]) + str(self.l[i])][(i>j) - (i == j)]
                c = [0,1][(hand in d[name]) and d[name][hand]]
                self.add_widget(hand_button(text = hand, position = name, count = c))
                #print(self.AA)

class position_button(CheckBox):
    def __init__(self, **kwargs):
        super(position_button,self).__init__(**kwargs)
        self.group = "position"
        self.allow_no_selection = False
        self.color = [255,0,0,1]

class menu_screen(GridLayout):
    def on_checkbox_active(self,chkbox,value):
        app = App.get_running_app()
        app.root.screen.manager.current = chkbox.id
        #print(chkbox.id)
        
    def __init__(self, **kwargs):
        super(menu_screen, self).__init__(**kwargs)
        positions = ['UTG', 'MP', 'CO', 'BTN', 'SB']
        self.size_hint_x = 0.25
        self.cols = 2
        self.background_color = [255,0,0,1]
        for i in range(5):
            chkbox = [position_button(id = positions[i]), position_button(state = 'down', id = positions[i])][i == 0]
            chkbox.bind(active=self.on_checkbox_active)
            self.add_widget(chkbox)
            self.add_widget(Label(text = positions[i]))
        #self.orientation = "horizontal"
        
class big_screen(Screen):
    def __init__(self, **kwargs):
        super(big_screen, self).__init__(**kwargs)
        self.h = hands_screen(name = self.name)
        self.add_widget(self.h)
        
        
class Manager(ScreenManager):
    def __init__(self, **kwargs):
        self.transition = NoTransition()
        super(Manager, self).__init__(**kwargs)
        self.utg = big_screen(name='UTG')
        self.mp = big_screen(name='MP')
        self.co = big_screen(name='CO')
        self.btn = big_screen(name='BTN')
        self.sb = big_screen(name='SB')
        self.add_widget(self.utg)
        self.add_widget(self.mp)
        self.add_widget(self.co)
        self.add_widget(self.btn)
        self.add_widget(self.sb)
        self.current = 'UTG'

class randomizer(BoxLayout):
    def callback(self, instance):
        self.label.text = str(random.randint(0,99))
    def __init__(self, **kwargs):
        super(randomizer, self).__init__(**kwargs)
        self.size_hint_y = 0.2
        btn = Button(text = "Generate", size_hint_x = 0.4)
        btn.bind(on_press=self.callback)
        self.label = Label(text = "0")
        self.add_widget(btn)
        self.add_widget(self.label)
   
class color_button(CheckBox):
    def __init__(self, **kwargs):
        super(color_button,self).__init__(**kwargs)
        self.group = "color"
        self.allow_no_selection = False
        self.color = [255,0,0,1]
        self.background_color = [255,0,0,1]
    
class menu_color(BoxLayout):
    def __init__(self, **kwargs):
        super(menu_color, self).__init__(**kwargs)
        self.size_hint_x = 0.25
        self.cols = 2
        self.rows = 2
        self.orientation = 'vertical'
        self.background_color = [255,0,0,1]
        self.red = color_button(state = 'down')
        self.blue = color_button()
        self.green = color_button()
        self.slider_red = freq_slider()
        self.slider_green = freq_slider()
        self.slider_blue = freq_slider()
        
        self.add_widget(self.red)
        self.add_widget(Button(background_color = [255,0,0,1]))
        self.add_widget(self.slider_red)
        self.add_widget(self.blue)
        self.add_widget(Button(background_color = [0,0,255,1]))
        self.add_widget(self.slider_blue)
        self.add_widget(self.green)
        self.add_widget(Button(background_color = [0,255,0,1]))
        self.add_widget(self.slider_green)
      
class freq_slider(BoxLayout):
    def on_touch_move(self,touch):
        self.label.text = str(int(self.slider.value))
    def __init__(self, **kwargs):
        super(freq_slider, self).__init__(**kwargs)
        self.slider = Slider(min=0,max=101,value=75,value_track = True)
        self.add_widget(self.slider)
        self.label = Label(text = str(self.slider.value))
        self.add_widget(self.label)
        
class screen(BoxLayout):
    def __init__(self, **kwargs):
        super(screen, self).__init__(**kwargs)
        self.menu = menu_screen()
        self.add_widget(self.menu)
        self.manager = Manager()
        self.add_widget(self.manager)
        self.color_menu = menu_color()
        self.add_widget(self.color_menu)

class main_screen(BoxLayout):
    def __init__(self, **kwargs):
        super(main_screen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.screen = screen()
        self.add_widget(self.screen)
        self.add_widget(randomizer()) 
        
class ranges_app(App):
    def build(self):
        return main_screen()
    
    def on_stop(self):
        global d
        with open('opens.pickle','wb') as f:
            pickle.dump(d, f, protocol = pickle.HIGHEST_PROTOCOL)
        #print(f.name)
        #self.pickle_object(f.name, f.h)
    


if __name__ == '__main__':
    ranges_app().run()
