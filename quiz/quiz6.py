
from random import seed, randrange
import sys

dim = 10

def display_grid():
    for row in grid:
        print('   ', *row) 

def walls_and_paths():
    """turn 1 and 0 into (x,y)"""
    maze_array = grid
    shape = []
    walls = []
    for i in range(dim):
        for j in range(dim):
            pos = [j, -i]
            if maze_array[i][j] == 1:
                shape.append(pos)
            if maze_array[i][j] == 0:
                walls.append(pos)
    return shape, walls
    
def max_number_of_spikes(paths):
    visited = set()
    result = 1

    def dfs(path):
        spike_num = 0
        stack = [path]
        while stack:
            n_num = 0
            curr = stack.pop()
            visited.add(tuple(curr))
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (curr[0] + dx, curr[1] + dy)
                neighbor = list(neighbor)
                if any(neighbor == path for path in paths):
                    neighbor = tuple(neighbor)
                    n_num += 1
                    if neighbor not in visited:
                        stack.append(neighbor)
            if n_num == 1:
                spike_num += 1
            
        return spike_num

    for path in paths:
        if tuple(path) not in visited:
            temp = dfs(path)
            result = max(result, temp)

    return result

def colour_shapes():
    shape, wall = walls_and_paths()
    return shape

try: 
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )