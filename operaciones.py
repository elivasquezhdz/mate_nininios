from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.factory import Factory
import itertools
import random
import configparser
import logging
from logging import FileHandler
import os


def startTheLogger():
    global logger1
    logPath = os.getcwd()
 
    logName = "aaaaa_.log"
    myFileName = logPath + "\\" + logName

    logger1 = logging.getLogger(myFileName)
    logger1.setLevel(logging.INFO)
    handlerScreen = FileHandler(myFileName)
    # handlerScreen.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    handlerScreen.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s",
                              "%Y/%m/%d %H:%M.%S"))

    #formatter = logging.Formatter()
    logger1.addHandler(handlerScreen)
    return myFileName

class YourWidget(Widget):
    random_number = StringProperty()
    count = StringProperty()
    s = ""
    correct_answer = ""
    cidx = 0
    colores = [list(x) + [1]  for x in (itertools.product([0, 1], repeat=3))]
    colores.pop(0)
    colores.pop(-1)

    def __init__(self, **kwargs):
        
        super(YourWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.random_number = ""#str(random.randint(1, 100))
        self.count = "0"
        self.config = self.read_config()
        self.operaciones()
        startTheLogger()
        logger1.info("hola")
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        sumas = True if config['OPERACIONES']['sumas'] == 'yes' else False
        restas = True if config['OPERACIONES']['restas'] == 'yes' else False
        mults= True if config['OPERACIONES']['multiplicaciones'] == 'yes' else False
        operandos = list(range(int(config['OPERACIONES']['rangomax'])+1))
        return {"sumas":sumas,"restas":restas,"mults":mults,"operandos":operandos}

    def _keyboard_closed(self):
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':     
            if(str(self.correct_answer) in self.s):
                self.count = str(int(self.count) + 1)
                self.operaciones()            
            else:
                self.change_color()     
            self.s = ""
        else:
            if(text):
                self.s+=text
        return True

    def sumas(self):
        id1 = random.randint(0,len(self.config['operandos'])-1)
        id2 = random.randint(0,len(self.config['operandos'])-1)
        op1 = self.config['operandos'][id1]
        op2 = self.config['operandos'][id2]      
        self.ids.label1.color = [1,1,1,1]
        self.correct_answer = op1+op2
        self.random_number = "{} + {}".format(op1,op2)

    def restas(self):
        id1 = random.randint(0,len(self.config['operandos'])-1)
        id2 = random.randint(0,len(self.config['operandos'])-1)
        op1 = self.config['operandos'][id1]
        op2 = self.config['operandos'][id2] 
        temp =0
        if(op2<op1):
            temp = op1
            op1= op2
            op2 = temp
        self.ids.label1.color = [1,1,1,1]
        self.correct_answer = op2-op1
        self.random_number = "{} - {}".format(op2,op1)

    def mults(self):
        id1 = random.randint(0,len(self.config['operandos'])-1)
        id2 = random.randint(0,len(self.config['operandos'])-1)
        op1 = self.config['operandos'][id1]
        op2 = self.config['operandos'][id2] 
        self.ids.label1.color = [1,1,1,1]
        self.correct_answer = op1*op2
        self.random_number = "{} x {}".format(op1,op2)

    def operaciones(self):
        operaciones_posibles = []
        if(self.config['sumas']):
            operaciones_posibles.append("sumas")
        if(self.config['restas']):
            operaciones_posibles.append("restas")
        if(self.config['mults']):
            operaciones_posibles.append("mults")
        idx = random.randint(0,len(operaciones_posibles))
        random.shuffle(operaciones_posibles)
        random.shuffle(operaciones_posibles)
        if(operaciones_posibles[0]=='sumas'):
            self.sumas()
        elif (operaciones_posibles[0]=='restas'):
            self.restas()
        elif (operaciones_posibles[0]=='mults'):
            self.mults()

    def change_color(self):
        self.ids.label1.color = self.colores[self.cidx]
        if(self.cidx + 1 ==len(self.colores)):
            self.cidx = 0
        self.cidx += 1
      
    def change_text(self):
        self.ids.label1.color = self.colores[self.cidx]
        if(self.cidx + 1 ==len(self.colores)):
            self.cidx = 0       
        self.cidx += 1
        self.mults()

class op(App):
    def build(self):
        return YourWidget()

if __name__ == '__main__':
    Window.fullscreen = True
    op().run()