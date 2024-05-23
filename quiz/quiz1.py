import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

##question1

temp = []
visited = []

for key in keys:
    while key not in (temp and visited):
        visited.append(key)
        temp.append(key)
        try:
            key = mapping[key]
        except KeyError:
            pass
    for i in range(len(temp)):
        start = temp[0]
        try:
            end = mapping[temp[i]]
        except KeyError:
            pass
        if start == end:
            cycles.append(temp)
            break
    temp = []
    visited = []

uniq = []
same = set()
for item in cycles:
    item_tuple = tuple(sorted(item))
    if item_tuple not in same:
        uniq.append(item)
        same.add(item_tuple)
cycles = uniq

##question2
temp = {}
for key, value in mapping.items():
    if value not in temp:
        temp[value] = [key]
    else:
        temp[value].append(key)

for key, value in temp.items():
    length = len(value)
    if length not in reversed_dict_per_length.keys():
        reversed_dict_per_length[length] = {key: value}
    else:
        if isinstance(reversed_dict_per_length[length], dict):
            reversed_dict_per_length[length][key] = value
        else:
            reversed_dict_per_length[length] = {reversed_dict_per_length[length]}
            reversed_dict_per_length[length][key] = value
    


print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)
