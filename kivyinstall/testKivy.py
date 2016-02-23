from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.lang import Builder

Builder.load_string('''
<MyWidget>:
    CheckBox:
        active: root.is_active
    CheckBox:
        active: not root.is_active
    Button:
        text: 'toggle'
        on_press: root.toggle()
''')

class MyWidget(BoxLayout):
    is_active = BooleanProperty(False)

    def toggle(self):
        self.is_active = not self.is_active

class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()