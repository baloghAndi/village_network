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

map_size = 7
tower_number = 3
village_number = 7


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


class VillageMap(GridLayout):

    def __init__(self, *args, **kwargs):
        super(VillageMap, self).__init__(*args, **kwargs)

        # self.village_map = {(x, y): grid_elem for x in range(self.map_size)
        #  for y in range(self.map_size) for grid_elem in GridEntry(
        #     row=x, column=y)  }
        self.village_map = []
        for row in range(map_size):
            for column in range(map_size):
                count = column + row * map_size
                #  print(row, column, count)
                grid_elem = GridEntry(nr=count, row=row, column=column)

                self.add_widget(grid_elem)
                self.village_map.append(grid_elem)

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
                self.village_map[index].tower.is_active = True
                print("tower at", row, column)
                towers.append(self.village_map[index])
        return sorted(towers) #NOT SURE IT WORKS LIKE THIS - fixed it

    def check_if_tower(self, row, column):
        index = column + row * map_size
        if (self.village_map[index].isTower):
            return False
        return True

    # def get_covered_area(self, grid_tower):
    #     covered_area = []
    # second row
    #     covered_area.append(grid_tower)
    #     top_left_corner = self.village_map[grid_tower.index - 1]
    #     covered_area.append(top_left_corner)
    #     top_right_corner = self.village_map[grid_tower.index + 2]
    #     covered_area.append(self.village_map[grid_tower.index+ 1])
    #     covered_area.append(top_right_corner)

    # third row
    #     index = grid_tower.index + map_size -1
    #     for i in range(index,index+4) :
    #         covered_area.append(self.village_map[i])

    # forth row
    #     index =  grid_tower.index + 2*map_size
    #     for i in range(index,index+2):
    #         covered_area.append(self.village_map[i])

    # second row
    #     index = grid_tower.index - map_size
    #     for i in range(index,index+2):
    #         covered_area.append(self.village_map[i])

    #     return covered_area

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
                    # neighbour_row.append(self.village_map[index]) return
                    # actual grid elements
                    neighbour_row.append(index)
        return neighbour_row

    # there are no other villages in the distance of 4 squares or if they are
    # they belon to the same towers area
#     def generate_minimum_coverage(self,towers):
#         covered_area = self.get_covered_area(towers[0].row, towers[0].column)
#         random_index = random.randint(0, len(covered_area)-1)
#         temp_village = covered_area[random_index]
#         self.village_map[temp_village.index].isVillage = True
#         self.village_map[temp_village.index].village.text = "village"
# already_covered = [] #  already covered places
#         print (temp_village.index)
#         for index in range(1,len(towers)-1):
#             covered_area1 = self.get_covered_area(towers[index-1].row, towers[index-1].column)
#             covered_area2 = self.get_covered_area(towers[index].row, towers[index].column)
#             already_covered =
# self.generate_village(covered_area1,covered_area2, already_covered)`

#         covered_area1 = self.get_covered_area(towers[len(towers)-2].row, towers[len(towers)-2].column)
#         covered_area2 = self.get_covered_area(towers[len(towers)-1].row, towers[len(towers)-1].column)
#         self.generate_village(covered_area1,covered_area2)
# LOOKOUT HERE IS NOT OPTIMAL

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
        towers = self.simulate_towers(tower_number)
        self.generate_minimum_coverage(towers)
        self.complete_map_with_villages(self.get_total_covered_area(towers))
        # for elem in w.village_map:
        #     if elem.isTower:
        #         elem.tower.activated = True




    # def generate_village(self, covered_area1, covered_area2):
    #     indexes1 = []
    #     for element in covered_area1:
    #         indexes1.append(element.index)
    #     indexes2 = []
    #     for element in covered_area2:
    #         indexes2.append(element.index)
    #     difference1 = sorted(set(indexes1) - set(indexes2))
    # random_index = random.choice(list(difference))
    #     difference2 = sorted(set(indexes2) - set(indexes1))
    #     value1 = difference1[0] - difference2[len(difference2) - 1]
    #     value2 = difference2[0] - difference1[len(difference1) - 1]
    #     if abs(value1) > abs(value2):
    #         self.village_map[difference1[0]].isVillage = True
    #         self.village_map[
    #             difference2[len(difference2) - 1]].isVillage = True

    #         self.village_map[difference1[0]].village.text = "village"
    #         self.village_map[
    #             difference2[len(difference2) - 1]].village.text = "village"

    #         print(self.village_map[difference1[0]].index,
    #               self.village_map[difference2[len(difference2) - 1]].index)

    #     else:
    #         self.village_map[difference2[0]].isVillage = True
    #         self.village_map[
    #             difference1[len(difference1) - 1]].isVillage = True

    #         self.village_map[difference2[0]].village.text = "village"
    #         self.village_map[
    #             difference1[len(difference1) - 1]].village.text = "village"
    #         print(self.village_map[difference2[0]].index,
    #               self.village_map[difference1[len(difference1) - 1]].index)


class VillageMapApp(App):

    def build(self):
        w = VillageMap()
        w.generate_map()
        return w

if __name__ == '__main__':
    VillageMapApp().run()
