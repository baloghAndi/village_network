from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty


import random

map_size = 8
tower_number = random.choice(range(2,5))
village_number = random.choice(range(tower_number,tower_number+7))


class Village(Button):
    text = StringProperty()


class WifiTower(CheckBox):
    is_active = BooleanProperty(False)

class GridEntry(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(GridEntry, self).__init__(*args, **kwargs)
        # not absolutely necessary but I don't understand why

        self.index = kwargs['nr']
#       self.id = str(self.index)
        self.village.index = self.index
        self.row = kwargs['row']
        self.column = kwargs['column']
        if self.row == map_size - 1 or self.column == map_size - 1:
            self.tower.index = -1
            self.remove_widget(self.tower)
        else:
            self.tower.index = self.index
        self.isTower = False
        self.isVillage = False

    def __lt__(self, other):
        return self.index < other.index

    def activate_tower(self):
        self.tower.is_active = not self.tower.is_active


class VillageMap(GridLayout):

    def print_content(self, *args):
        forward = [w for w in self.walk(loopback=True)]
        for grid_elem in forward[1:]:
            # if grid_elem.index
            print("{} -> {}".format(grid_elem, grid_elem.index))

    def simulate_towers(self, nr_towers):
        towers = []  # list of grid elems where there is a tower
        for i in range(nr_towers):
            # get random position for a tower
            row = random.randint(0, map_size - 2)
            column = random.randint(0, map_size - 2)
            # not already a tower mark now
            index = column + row * map_size
            if self.check_if_tower(row, column):
                self.village_map[index].isTower = True  # set to be a tower
                # make a list of GridEntry where there are towers
                #self.village_map[index].tower.is_active = True # THIS SETS THE TOWER VISIBLE
                print("tower at", row, column)
                towers.append(self.village_map[index])
        return sorted(towers) #NOT SURE IT WORKS LIKE THIS - fixed it

    def check_if_tower(self, row, column):
        index = column + row * map_size
        if (self.village_map[index].isTower):
            return False
        return True

    # return indexes of area
    def get_covered_area(self, tower_row, tower_column):
        first_row = self.get_row(tower_row - 1, tower_column, 2)
        second_row = self.get_row(tower_row, tower_column - 1, 4)
        third_row = self.get_row(tower_row + 1, tower_column - 1, 4)
        forth_row = self.get_row(tower_row + 2, tower_column, 2)

        return first_row + second_row + third_row + forth_row

    def get_row(self, row, column, nr_elements):
        neighbour_row = []
        if row >= 0 and row < map_size:
            for tempColumn in range(column, column + nr_elements):
                if (tempColumn >= 0 and tempColumn < map_size):
                    index = tempColumn + row * map_size
                    # actual grid elements
                    neighbour_row.append(index)
        return neighbour_row

    def get_duplicate_coverage(self, towers):
        covered_area_indexes = self.get_total_covered_area(towers)
        duplicate_coverage = set(
            [x for x in covered_area_indexes if covered_area_indexes.count(x) > 1])
        return duplicate_coverage

    def get_total_covered_area(self, towers):
        covered_area_indexes = []
        for tower in towers:
            covered_area_indexes.extend(self.get_covered_area(tower.row, tower.column))
        return covered_area_indexes

    # def enforce_tower_validity(self, duplicate_coverage, tower_covered_area):
    #     #if no uniquly covered areas exist for the given tower
    #     if (set(tower_covered_area) - set(duplicate_coverage)) == set(): 

    # TODO finish this. if no unique place left delete tower generate a new one. check if ok
    # add it to list and update duplicate coverage



    def generate_minimum_coverage(self, towers):
        villages = []
        duplicate_coverage = self.get_duplicate_coverage(towers)
        covered = self.get_covered_area(towers[0].row, towers[0].column)
        difference = set(covered) - set(duplicate_coverage)
        # temp_village_index = random.choice(list(difference))
        # if difference == set():
        #     temp_village_index = random.choice(covered)
        # else:
        temp_village_index = min(list(difference))

        self.village_map[temp_village_index].isVillage = True
        self.village_map[temp_village_index].village.text = "village"
        villages.append(temp_village_index)

        for index in range(1, len(towers)):
            villages = self.generate_village(duplicate_coverage, villages, towers[index])

        return villages


    def generate_village(self, duplicate_coverage, villages, tower):
        current_tower_coverage = self.get_covered_area(tower.row, tower.column)
        covered_indexes = []
        #  not already covered area by previous towers
        difference = list(set(current_tower_coverage) - set(duplicate_coverage))
        distance = [0] * len(difference)
        for index in range(0,len(distance) - 1):
            for village_index in villages:
                distance[index] += abs(village_index - difference[index])
        max_index = distance.index(max(distance))
        
        self.village_map[difference[max_index]].isVillage = True
        self.village_map[difference[max_index]].village.text = "village"
        villages.append(max_index)
        
        return villages

    def complete_map_with_villages(self,covered_area):
        village_counter = tower_number
        while (village_counter < village_number):
            random_position = random.choice(covered_area)
            if not self.village_map[random_position].isVillage and not self.village_map[random_position].isTower:
                self.village_map[random_position].isVillage = True
                self.village_map[random_position].village.text = "village"
                village_counter += 1

    def generate_map(self):
        #self.village_map = village_map_elements
        towers = self.simulate_towers(tower_number)
        self.generate_minimum_coverage(towers)
        self.complete_map_with_villages(self.get_total_covered_area(towers))
        return self.village_map

    def checkSolution(self):
        covered_area = []
        tower_counter = 0
        for elem in self.village_map:
            if elem.row != map_size -1 and elem.column != map_size -1:
               # print(elem.index,elem.tower.is_active)
                if elem.tower.is_active:
                    covered_area.extend(self.get_covered_area(elem.row, elem.column))
                    tower_counter +=1
        if tower_counter > tower_number:
            return False
        for elem in self.village_map:
            if elem.isVillage:
                if elem.village.index not in covered_area:
                    return False
        return True
        

class Game(BoxLayout):

    village_map = ObjectProperty(None)
    result_label = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
       # self.village_map = kwargs['map']
       # self.village_map.generate_map(self.village_map_elements)

        self.gameApp = kwargs['app']
        self.village_map_elements = []
        for row in range(map_size):
            for column in range(map_size):
                count = column + row * map_size
                #print(row, column, count)
                grid_elem = GridEntry(nr=count, row=row, column=column)
                self.village_map.add_widget(grid_elem)
                #self.add_widget(grid_elem)
                self.village_map_elements.append(grid_elem)
        self.village_map.village_map = self.village_map_elements
        self.village_map.generate_map()

    def submit_solution(self):
        print("submit")
        result = self.village_map.checkSolution()
        print("is it a solution? ",result)
        if result:
            self.result_label.text = "You won!"
        else: 
            self.result_label.text = "Not correct solution."

    def new_game(self):
        #self.gameApp.canvas.clear()
        self.gameApp.root.clear_widgets()
        self.gameApp.run()
        

class VillageMapApp(App):

    def build(self):
        self.game = Game(app=self) 
        return self.game 

if __name__ == '__main__':
    VillageMapApp().run()
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty


import random

map_size = 8
tower_number = random.choice(range(2,5))
village_number = random.choice(range(tower_number,tower_number+7))


class Village(Button):
    text = StringProperty()


class WifiTower(CheckBox):
    is_active = BooleanProperty(False)

class GridEntry(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(GridEntry, self).__init__(*args, **kwargs)
        # not absolutely necessary but I don't understand why

        self.index = kwargs['nr']
#       self.id = str(self.index)
        self.village.index = self.index
        self.row = kwargs['row']
        self.column = kwargs['column']
        if self.row == map_size - 1 or self.column == map_size - 1:
            self.tower.index = -1
            self.remove_widget(self.tower)
        else:
            self.tower.index = self.index
        self.isTower = False
        self.isVillage = False

    def __lt__(self, other):
        return self.index < other.index

    def activate_tower(self):
        self.tower.is_active = not self.tower.is_active


class VillageMap(GridLayout):

    def print_content(self, *args):
        forward = [w for w in self.walk(loopback=True)]
        for grid_elem in forward[1:]:
            # if grid_elem.index
            print("{} -> {}".format(grid_elem, grid_elem.index))

    def simulate_towers(self, nr_towers):
        towers = []  # list of grid elems where there is a tower
        for i in range(nr_towers):
            # get random position for a tower
            row = random.randint(0, map_size - 2)
            column = random.randint(0, map_size - 2)
            # not already a tower mark now
            index = column + row * map_size
            if self.check_if_tower(row, column):
                self.village_map[index].isTower = True  # set to be a tower
                # make a list of GridEntry where there are towers
                #self.village_map[index].tower.is_active = True # THIS SETS THE TOWER VISIBLE
                print("tower at", row, column)
                towers.append(self.village_map[index])
        return sorted(towers) #NOT SURE IT WORKS LIKE THIS - fixed it

    def check_if_tower(self, row, column):
        index = column + row * map_size
        if (self.village_map[index].isTower):
            return False
        return True

    # return indexes of area
    def get_covered_area(self, tower_row, tower_column):
        first_row = self.get_row(tower_row - 1, tower_column, 2)
        second_row = self.get_row(tower_row, tower_column - 1, 4)
        third_row = self.get_row(tower_row + 1, tower_column - 1, 4)
        forth_row = self.get_row(tower_row + 2, tower_column, 2)

        return first_row + second_row + third_row + forth_row

    def get_row(self, row, column, nr_elements):
        neighbour_row = []
        if row >= 0 and row < map_size:
            for tempColumn in range(column, column + nr_elements):
                if (tempColumn >= 0 and tempColumn < map_size):
                    index = tempColumn + row * map_size
                    # actual grid elements
                    neighbour_row.append(index)
        return neighbour_row

    def get_duplicate_coverage(self, towers):
        covered_area_indexes = self.get_total_covered_area(towers)
        duplicate_coverage = set(
            [x for x in covered_area_indexes if covered_area_indexes.count(x) > 1])
        return duplicate_coverage

    def get_total_covered_area(self, towers):
        covered_area_indexes = []
        for tower in towers:
            covered_area_indexes.extend(self.get_covered_area(tower.row, tower.column))
        return covered_area_indexes

    # def enforce_tower_validity(self, duplicate_coverage, tower_covered_area):
    #     #if no uniquly covered areas exist for the given tower
    #     if (set(tower_covered_area) - set(duplicate_coverage)) == set(): 

    # TODO finish this. if no unique place left delete tower generate a new one. check if ok
    # add it to list and update duplicate coverage



    def generate_minimum_coverage(self, towers):
        villages = []
        duplicate_coverage = self.get_duplicate_coverage(towers)
        covered = self.get_covered_area(towers[0].row, towers[0].column)
        difference = set(covered) - set(duplicate_coverage)
        # temp_village_index = random.choice(list(difference))
        # if difference == set():
        #     temp_village_index = random.choice(covered)
        # else:
        temp_village_index = min(list(difference))

        self.village_map[temp_village_index].isVillage = True
        self.village_map[temp_village_index].village.text = "village"
        villages.append(temp_village_index)

        for index in range(1, len(towers)):
            villages = self.generate_village(duplicate_coverage, villages, towers[index])

        return villages


    def generate_village(self, duplicate_coverage, villages, tower):
        current_tower_coverage = self.get_covered_area(tower.row, tower.column)
        covered_indexes = []
        #  not already covered area by previous towers
        difference = list(set(current_tower_coverage) - set(duplicate_coverage))
        distance = [0] * len(difference)
        for index in range(0,len(distance) - 1):
            for village_index in villages:
                distance[index] += abs(village_index - difference[index])
        max_index = distance.index(max(distance))
        
        self.village_map[difference[max_index]].isVillage = True
        self.village_map[difference[max_index]].village.text = "village"
        villages.append(max_index)
        
        return villages

    def complete_map_with_villages(self,covered_area):
        village_counter = tower_number
        while (village_counter < village_number):
            random_position = random.choice(covered_area)
            if not self.village_map[random_position].isVillage and not self.village_map[random_position].isTower:
                self.village_map[random_position].isVillage = True
                self.village_map[random_position].village.text = "village"
                village_counter += 1

    def generate_map(self):
        #self.village_map = village_map_elements
        towers = self.simulate_towers(tower_number)
        self.generate_minimum_coverage(towers)
        self.complete_map_with_villages(self.get_total_covered_area(towers))
        return self.village_map

    def checkSolution(self):
        covered_area = []
        tower_counter = 0
        for elem in self.village_map:
            if elem.row != map_size -1 and elem.column != map_size -1:
               # print(elem.index,elem.tower.is_active)
                if elem.tower.is_active:
                    covered_area.extend(self.get_covered_area(elem.row, elem.column))
                    tower_counter +=1
        if tower_counter > tower_number:
            return False
        for elem in self.village_map:
            if elem.isVillage:
                if elem.village.index not in covered_area:
                    return False
        return True
        

class Game(BoxLayout):

    village_map = ObjectProperty(None)
    result_label = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
       # self.village_map = kwargs['map']
       # self.village_map.generate_map(self.village_map_elements)

        self.gameApp = kwargs['app']
        self.village_map_elements = []
        for row in range(map_size):
            for column in range(map_size):
                count = column + row * map_size
                #print(row, column, count)
                grid_elem = GridEntry(nr=count, row=row, column=column)
                self.village_map.add_widget(grid_elem)
                #self.add_widget(grid_elem)
                self.village_map_elements.append(grid_elem)
        self.village_map.village_map = self.village_map_elements
        self.village_map.generate_map()

    def submit_solution(self):
        print("submit")
        result = self.village_map.checkSolution()
        print("is it a solution? ",result)
        if result:
            self.result_label.text = "You won!"
        else: 
            self.result_label.text = "Not correct solution."

    def new_game(self):
        #self.gameApp.canvas.clear()
        self.gameApp.root.clear_widgets()
        self.gameApp.run()
        

class VillageMapApp(App):

    def build(self):
        self.game = Game(app=self) 
        return self.game 

if __name__ == '__main__':
    VillageMapApp().run()
