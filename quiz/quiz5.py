from random import seed, randrange
import sys

dim = 10

def display_grid():
    for row in grid:
        print('   ', *row) 

def trans_left(matrix):
    new_grid = [matrix[0]]
    for i in range(1, dim):
        temp = i*[0]
        fregmt = matrix[i][:-i]
        new_grid.append(temp + fregmt)
    return new_grid

def trans_right(matrix):
    new_grid = [matrix[0]]
    for i in range(1, dim):
        temp = i*[0]
        fregmt = matrix[i][i:]
        new_grid.append(fregmt + temp)
    return new_grid

def size_of_largest_parallelogram():
    a = rec_num(grid)
    ng = grid
    b = 0
    c = 0
    for i in range(dim):
        ng = ng[1:] + [ng[0]]
        t = rec_num(trans_left(ng))
        b = max(b, t)
        t2 = rec_num(trans_right(ng))
        c = max(c, t2)

    return max(a, b, c)


def rec_num(grid):
    h, l = dim, dim
    nums = [[0] * l for i in range(h)]
    def edge(i, j):
        for n in range(j, l):
            if grid[i][n] == 1:
                nums[i][j] += 1
            else:
                break
    ans = 0
    for i in range(h):
        for j in range(l):
            edge(i, j)
    print(nums)
    for i in range(h):
        for j in range(l):
            tmp = nums[i][j]
            for k in range(i, h):
                tmp = min(nums[k][j], tmp)
                if tmp > 1 and (k - i + 1) > 1:
                    ans = max(ans, tmp * (k - i + 1))
    return ans


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
size = size_of_largest_parallelogram()
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
         )
else:
    print('There is no parallelogram with horizontal sides.')