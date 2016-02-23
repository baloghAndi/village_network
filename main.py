from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.checkbox import CheckBox


class Village(Button):
    coords = ListProperty([0, 0])


class WifiTower(CheckBox):
    pass


class GridEntry(FloatLayout):

    grid_entry_village = Village()
    grid_entry_tower = WifiTower()
    
    def __init__(self, *args, **kwargs):
        super(GridEntry, self).__init__(*args, **kwargs)
       
        self.add_widget(grid_entry_village)
        self.add_widget(grid_entry_tower)


class VillageMap(GridLayout):

    def __init__(self, *args, **kwargs):
        super(VillageMap, self).__init__(*args, **kwargs)
        for row in range(7):
            for column in range(7):
                grid_elem = GridEntry()
                self.add_widget(grid_elem)
                '''grid_entry_village = Village(coords=(row, column))
              # grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry_village)
                grid_entry_tower = WifiTower()
                self.add_widget(grid_entry_tower)'''

        '''for row in range(7):
            for column in range(7):
                grid_entry_village = Village(coords=(row, column))
                self.add_widget(grid_entry_village)
                if column == row :
                    grid_entry_tower = WifiTower()
                    self.add_widget(grid_entry_tower)'''


class VillageNetworkApp(App):

    def build(self):
        return VillageMap()

if __name__ == '__main__':
    VillageNetworkApp().run()
