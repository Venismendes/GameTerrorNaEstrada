from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.button import Button
import json
import random

Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 450)


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.transition = FadeTransition()
        self.current = 'inicio'
        
    pass


class Inicio(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
    pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.roteiro = json.load(open('roteiro.json', 'r', encoding='utf8'))


    def on_enter(self, *args):
        self.fase='Reiniciar'
        self.escrever()


    def escrever(self, *args):
        self.ids.contexto.text = ''
        self.texto = self.roteiro[self.fase][0]
        self.index = 0
        self.tempo = 5 / len(self.texto)
        Clock.schedule_interval(self.adicionar_letra, self.tempo)

        self.quantidade_opcoes = len(self.roteiro[self.fase])
        self.adicionar_opcoes(opcao=self.fase)


    def adicionar_letra(self, *args):
        self.ids.contexto.text += self.texto[self.index]
        self.index += 1
        if self.index >= len(self.texto):
            Clock.unschedule(self.adicionar_letra)

    
    def pressionar_botao(self, opcao, *args):
        self.fase = opcao.text
        if opcao.text == 'Voltar':
            sorteio = random.choices(['Voltar1', 'Voltar2'], weights=[8, 2])
            self.fase = sorteio[0]
        if opcao.text == 'Fim':
            App.get_running_app().root.current = 'final'
            return
        self.escrever()


    def adicionar_opcoes(self, opcao, *args):
        self.opcao = opcao
        self.ids.grid_opcoes.clear_widgets()
        for i in range(1, self.quantidade_opcoes):
            self.fase = self.roteiro[self.opcao][i]
            opcao_texto = self.fase

            nova_opcao = Button(text=opcao_texto, font_size=20, background_color=(0.125, 0.643, 0.952, 1), on_release=self.pressionar_botao)
            self.ids.grid_opcoes.add_widget(nova_opcao)

    pass


class Final(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    pass




class Jogo(App):
    def build(self):
        return Manager()
    pass


Jogo().run()