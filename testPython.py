
import random

map_size = 7
village_map = {(x, y) : '-' for x in range(map_size) for y in range(map_size) }
#village_map2 = [x: 2*x for x in range(map_size) ]


class TestPython(object):


    def __init__(self):
        #self.call_with_args(1, 2, 3, row=4, column=5)
        #self.test_map()

        #  self.testIntersection()
        self.test_duplicates()
	

    def call_with_args(self, first, *args, **kwargs):
        print(first)
        print(args[1])
        print(kwargs['row'])

    def test_map(self):
    	#map = [ (x, y) for x in range(map_size) for y in range(map_size) ]
    	print(village_map)

    def testIntersection(self):
        list1 = [1,2,8,9,3,4,5]
        list2 = [4,5,6,7]
        result_set = set(list1) - set(list2)
        print(result_set)
        print(sorted(result_set))
        new_list = list(result_set)
        print(new_list[len(new_list)-1])
        print(random.choice(list(result_set)))

    def test_duplicates(self):
        l = [1,1,3,4,5,3]
        xx = set([x for x in l if l.count(x) > 1])
        print(xx)

obj = TestPython()
