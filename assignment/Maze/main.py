
class MazeError(Exception):
    def __init__(self, message):
        self.message = message

class Maze:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name, 'r') as file:
            self.maze_text = file.read()
        self.walls_and_paths()
    def input(self):
        """strip the whitespace and organize the maze text"""
        maze_array = []
        for line in self.maze_text:
            for e in line:
                if e.isdigit():
                    maze_array.append(int(e))
                if e == "\n" and maze_array != []:
                    if maze_array[-1] != ",":
                        maze_array.append(",")
        pre_count = 0
        count = 0
        for i in range(len(maze_array)):
            if maze_array[i] == ",":
                if pre_count != 0 and count != pre_count:
                    raise MazeError('Incorrect input.')
                pre_count = count
                count = 0
            else:
                count += 1

        newarray = []
        tmp = []
        for i in range(len(maze_array)):
            if maze_array[i] == ",":
                newarray.append(tmp)
                tmp = []
            else:
                tmp.append(maze_array[i])
        if tmp != []:
            newarray.append(tmp)
        row = len(newarray)
        col = len(newarray[0])
        ##Error check
        if col > 31 or row > 41 or col < 2 or row < 2:
            raise MazeError('Incorrect input.')
        for n in newarray:
            if n[-1] != 0 and n[-1] != 2:
                raise MazeError('Input does not represent a maze.')
        for n in newarray[-1]:
            if n != 0 and n != 1:
                raise MazeError('Input does not represent a maze.')
        return newarray
    def dimentionalize(self):
        """turn the maze into 1 and 0 graph"""
        zero = [1,0,0,0]
        one = [1,1,0,0]
        two = [1,0,1,0]
        three = [1,1,1,0]
        result = []
        eachrow = []
        arrays = self.input()
        for array in arrays:
            for e in array:
                if e == 0:
                    eachrow.extend(zero[:2])
                elif e == 1:
                    eachrow.extend(one[:2])
                elif e == 2:
                    eachrow.extend(two[:2])
                elif e == 3:
                    eachrow.extend(three[:2])
                else:
                    raise MazeError('Incorrect input.')
            result.append(eachrow)
            eachrow = []
            for e in array:
                if e == 0:
                    eachrow.extend(zero[2:])
                elif e == 1:
                    eachrow.extend(one[2:])
                elif e == 2:
                    eachrow.extend(two[2:])
                elif e == 3:
                    eachrow.extend(three[2:])
            result.append(eachrow)
            eachrow = []

        return result
    def walls_and_paths(self):
        """turn 1 and 0 into (x,y)"""
        maze_array = self.dimentionalize()
        row = len(maze_array) - 1
        col = len(maze_array[0]) - 1
        paths = []
        walls = []
        for i in range(row):
            for j in range(col):
                pos = [j, -i]
                if maze_array[i][j] == 0:
                    paths.append(pos)
                if maze_array[i][j] == 1:
                    walls.append(pos)
        return paths,walls
    def gate_counter(self, graph, row, col):
        gate = 0
        gate_set = []
        for i in range(row):
            for j in range(col):
                if i == 0 or i == row - 1 or j == 0 or j == col - 1:
                    if graph[i][j] == 0:
                        gate += 1
                        gate_set.append([j, -i])
        return gate, gate_set
    def wall_counter(self):
        paths_set, wall_set = self.walls_and_paths()
        walls = wall_set
        visited = set()
        groups_num = 0
        pillar_temp = []
        pillar = []
        wall_set = []
        def dfs(wall):
            stack = [wall]
            while stack:
                curr = stack.pop()
                visited.add(tuple(curr))
                pillar_temp.append(curr)
                wall_set.append(curr)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (curr[0] + dx, curr[1] + dy)
                    neighbor = list(neighbor)
                    if any(neighbor == wall for wall in walls):
                        neighbor = tuple(neighbor)
                        if neighbor not in visited:
                            stack.append(neighbor)

        for wall in walls:
            if tuple(wall) not in visited:
                dfs(wall)
                wall_set.clear()
                if len(pillar_temp) > 1:
                    groups_num += 1
                else:
                    pillar.extend(pillar_temp)
                pillar_temp.clear()
        return groups_num, pillar
    def path_counter(self, paths, row, col):
        visited = set()
        path_num = 0
        inner_num = 0
        inner_temp = []
        inner = []
        accessable = []
        def dfs(path):
            stack = [path]
            while stack:
                curr = stack.pop()
                visited.add(tuple(curr))
                inner_temp.append(tuple(curr))
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (curr[0] + dx, curr[1] + dy)
                    neighbor = list(neighbor)
                    if any(neighbor == path for path in paths):
                        neighbor = tuple(neighbor)
                        if neighbor not in visited:
                            stack.append(neighbor)

        for path in paths:
            if tuple(path) not in visited:
                dfs(path)
                if len(inner_temp) > 1 and (inner_temp[0][0] == 0 or inner_temp[0][1] == - row + 1 or inner_temp[0][1] == 0 or inner_temp[0][0] == col - 1 or inner_temp[-1][0] == 0 or inner_temp[-1][1] == - row + 1 or inner_temp[-1][1] == 0 or inner_temp[-1][0] == col - 1):
                        path_num += 1
                        for t in inner_temp:
                            accessable.append(list(t))
                else:
                    inn = [list(t) for t in inner_temp]
                    inner.append(inn)
                inner_temp.clear()

        for i in range(len(inner)):
            for j in range(len(inner[i])):
                if inner[i][j][0] % 2 == 1 and inner[i][j][1] % 2 == 1:
                    inner_num += 1

        return path_num, inner_num, accessable
    def cds_counter(self, paths, walls, row, col):
        visited = set()
        cds_set = []
        visited2 = set()

        def max_cds(cds):
            n_num = 0
            stack = [cds]
            temp = []
            while stack:
                curr = stack.pop()
                visited2.add(tuple(curr))
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (curr[0] + dx, curr[1] + dy)
                    neighbor = list(neighbor)
                    if any(neighbor == path for path in paths):
                        neighbor = tuple(neighbor)
                        if neighbor not in visited2:
                            stack.append(neighbor)
                            temp.append(list(neighbor))
                            n_num += 1
                if n_num == 1:
                    cds_set.append(temp[0])
                    temp = []
                else:
                    if cds_set[-1][0] != 0 and cds_set[-1][1] != 0 and cds_set[-1][0] != col - 1 and cds_set[-1][1] != -row + 1 and n_num > 1:
                        visited2.remove(tuple(cds_set[-1]))
                        cds_set.remove(cds_set[-1])
                    break
                n_num = 0

        def dfs(path):
            n_num = 0
            stack = [path]
            while stack:
                curr = stack.pop()
                visited.add(tuple(curr))
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (curr[0] + dx, curr[1] + dy)
                    neighbor = list(neighbor)
                    if any(neighbor == path for path in paths):
                        neighbor = tuple(neighbor)
                        if neighbor not in visited:
                            stack.append(neighbor)
                    elif any(neighbor == wall for wall in walls):
                        n_num += 1
                if n_num == 3:
                    cds_set.append(list(curr))
                n_num = 0


        for path in paths:
            if tuple(path) not in visited:
                dfs(path)

        for cds in cds_set:
            max_cds(cds)

        return cds_set
    def ee_group(self, cds_set, accessable, row, col):
        visited = set()
        for c in cds_set:
            visited.add(tuple(c))
        temp = []
        ee_set = []
        def dfs(a, ee):
            gate = 0
            stack = [a]
            n_num = 0
            cross = 0
            while stack:
                curr = stack.pop()
                visited.add(tuple(curr))
                temp.append(tuple(curr))
                if curr[0] == 0 or curr[1] == 0 or curr[0] == col - 1 or curr[1] == -row + 1:
                    gate += 1
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (curr[0] + dx, curr[1] + dy)
                    neighbor = list(neighbor)
                    if any(neighbor == acc for acc in accessable):
                        neighbor = tuple(neighbor)
                        if neighbor not in visited:
                            stack.append(neighbor)
                            n_num += 1
                if n_num > 1:
                    cross = 1
                n_num = 0
            if gate == 2 and cross == 0:
                for i in range(len(temp)):
                    if gate > 0:
                        ee.append(list(temp[i]))
                    if temp[i][0] == 0 or temp[i][1] == 0 or temp[i][0] == col - 1 or temp[i][1] == -row + 1:
                        gate -= 1

        for acc in accessable:
            if tuple(acc) not in visited:
                dfs(acc, ee_set)
                temp = []
        return ee_set
    def cds_group(self, cds_set):
        visited = set()
        groups_num = 0
        result = []
        temp = []
        def dfs(wall):
            stack = [wall]
            while stack:
                curr = stack.pop()
                visited.add(tuple(curr))
                temp.append(list(curr))
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (curr[0] + dx, curr[1] + dy)
                    neighbor = list(neighbor)
                    if any(neighbor == cds for cds in cds_set):
                        neighbor = tuple(neighbor)
                        if neighbor not in visited:
                            stack.append(neighbor)

        for cds in cds_set:
            if tuple(cds) not in visited:
                dfs(cds)
                groups_num += 1
                result.append(temp)
                temp = []

        return groups_num, result
    def analyse(self):
        graph = self.dimentionalize()
        row = len(graph) - 1
        col = len(graph[0]) - 1
        paths_set, wall_set = self.walls_and_paths()
        gate, gate_set = self.gate_counter(graph, row, col)
        wall_num, pillar = self.wall_counter()
        path_num, inner_area, accessable = self.path_counter(gate_set + paths_set, row, col)
        cds_set = self.cds_counter(gate_set + accessable, wall_set, row, col)

        ee_set = self.ee_group(cds_set, accessable, row, col)
        cds, cds_group = self.cds_group(cds_set)
        ee, ee_group = self.cds_group(ee_set)


        if gate == 0:
            print('The maze has no gate.')
        elif gate == 1:
            print('The maze has a single gate.')
        else:
            print(f"The maze has {gate} gates.")

        if wall_num == 0:
            print('The maze has no wall.')
        elif wall_num == 1:
            print('The maze has walls that are all connected.')
        else:
            print(f"The maze has {wall_num} sets of walls that are all connected.")

        if inner_area == 0:
            print('The maze has no inaccessible inner point.')
        elif inner_area == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print(f"The maze has {inner_area} inaccessible inner points.")

        if path_num == 0:
            print('The maze has no accessible area.')
        elif path_num == 1:
            print('The maze has a unique accessible area.')
        else:
            print(f"The maze has {path_num} accessible areas.")

        if cds == 0:
            print('The maze has no accessible cul-de-sac.')
        elif cds == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f"The maze has {cds} sets of accessible cul-de-sacs that are all connected.")

        if ee == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif ee == 1:
            print(f"The maze has a unique entry-exit path with no intersection not to cul-de-sacs.")
        else:
            print(f"The maze has {ee} entry-exit paths with no intersections not to cul-de-sacs.")


    """ DISPLAY PART"""
    def simplfy(self, display):
        if display == []:
            return []
        sample = []
        result = []
        sample.append(display[0])
        sample.append(display[1])
        for i in range(2, len(display), 2):
            y = sample[0][1]
            if display[i][1] == y:
                if display[i][0] > sample[1][0]:
                    result.extend(sample)
                    sample.clear()
                    sample.append(display[i])
                    sample.append(display[i + 1])
                if display[i][0] < sample[0][0]:
                    sample[0] = display[i]
                if display[i + 1][0] > sample[1][0]:
                    sample[1] = display[i + 1]
            else:
                result.extend(sample)
                sample.clear()
                sample.append(display[i])
                sample.append(display[i + 1])
        result.extend(sample)
        return result
    def simplfy2(self, display):
        if display == []:
            return []
        sample = []
        result = []
        sample.append(display[0])
        sample.append(display[1])
        for i in range(2, len(display), 2):
            x = sample[0][0]
            if display[i][0] == x:
                if display[i][1] > sample[1][1] or display[i + 1][1] < sample[0][1]:
                    result.extend(sample)
                    sample.clear()
                    sample.append(display[i])
                    sample.append(display[i + 1])
                if display[i][1] < sample[0][1]:
                    sample[0] = display[i]
                if display[i + 1][1] > sample[1][1]:
                    sample[1] = display[i + 1]
            else:
                result.extend(sample)
                sample.clear()
                sample.append(display[i])
                sample.append(display[i + 1])
        result.extend(sample)
        return result
    def wall_display(self):
        grid = self.dimentionalize()
        h, l = len(grid), len(grid[0])
        nums = [[0] * l for i in range(h)]

        def edge(i, j):
            for n in range(j, l):
                if grid[i][n] == 1:
                    nums[i][j] += 1
                else:
                    break
        for i in range(h):
            for j in range(l):
                edge(i, j)
        display_lr = []
        for i in range(len(nums)):
            for j in range(len(nums[0])):
                if nums[i][j] > 2:
                    l = nums[i][j] // 3
                    x = j // 2
                    y = i // 2
                    display_lr.append([x, y])
                    display_lr.append([x + l, y])
        result = self.simplfy(display_lr)
        return result
    def rotate(self):
        matrix = self.dimentionalize()
        transposed_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        rotated_matrix = [row[::-1] for row in transposed_matrix]
        return rotated_matrix
    def wall_display2(self):
        grid = self.rotate()
        h, l = len(grid), len(grid[0])
        nums = [[0] * l for i in range(h)]

        def edge(i, j):
            for n in range(j, l):
                if grid[i][n] == 1:
                    nums[i][j] += 1
                else:
                    break
        for i in range(h):
            for j in range(l):
                edge(i, j)
        display_ud = []
        for i in range(len(nums)):
            for j in range(len(nums[0])):
                ofst = len(nums[0])//2 - 1
                if nums[i][j] > 2:
                    l = nums[i][j] // 3
                    x = j // 2
                    y = i // 2

                    display_ud.append([y, -(x + l - ofst)])
                    display_ud.append([y, -(x - ofst)])
        result = self.simplfy2(display_ud)
        result = sorted(result, key=lambda l: (l[0], l[1]))
        return result

    def cds_display(self):
        graph = self.dimentionalize()
        row = len(graph) - 1
        col = len(graph[0]) - 1
        paths_set, wall_set = self.walls_and_paths()
        gate, gate_set = self.gate_counter(graph, row, col)
        path_num, inner_area, accessable = self.path_counter(gate_set + paths_set, row, col)
        cds_set = self.cds_counter(gate_set + accessable, wall_set, row, col)

        ee_set = self.ee_group(cds_set, accessable, row, col)
        ee, ee_set2 = self.cds_group(ee_set)
        cds_set = [[x, -y] for x, y in cds_set]
        cds_set = sorted(cds_set, key=lambda p: (p[0], p[1]))
        cds_display = []
        for i in range(len(cds_set)):
            if cds_set[i][0] % 2 == 1 and cds_set[i][1] % 2 == 1:
                cds_set[i][0] = cds_set[i][0]/2
                cds_set[i][1] = cds_set[i][1]/2
                cds_display.append(cds_set[i])
        ee_set = [[x, -y] for x, y in ee_set]

        return cds_display, ee_set

    def ee_display(self, ee_set):

        graph = self.dimentionalize()
        result_lr = []
        result_ud = []
        row = len(graph) - 1
        col = len(graph[0]) - 1
        for j in range(col):
            for i in range(row):
                if [j, i] in ee_set:
                    graph[i][j] = 8

        for i in range(len(graph)):
            temp = []
            for j in range(len(graph[i])):
                if graph[i][j] == 8:
                    temp.append([j, i])
                else:
                    if len(temp) > 1:
                        result_lr.append(temp[0])
                        result_lr.append(temp[-1])
                    temp = []

        for j in range(len(graph[i])):
            temp = []
            for i in range(len(graph)):
                if graph[i][j] == 8:
                    temp.append([j, i])
                else:
                    if len(temp) > 1:
                        result_ud.append(temp[0])
                        result_ud.append(temp[-1])
                    temp = []



        for i in range(len(result_lr)):
            if result_lr[i][0] == 0:
                result_lr[i][0] = -1
            if result_lr[i][1] == 0:
               result_lr[i][1] = -1
            if result_lr[i][0] == col - 1:
                result_lr[i][0] = col
            if result_lr[i][1] == row - 1:
                result_lr[i][1] = row

        for i in range(len(result_ud)):
            if result_ud[i][0] == 0:
                result_ud[i][0] = -1
            if result_ud[i][1] == 0:
               result_ud[i][1] = -1
            if result_ud[i][0] == col - 1:
                result_ud[i][0] = col
            if result_ud[i][1] == row - 1:
                result_ud[i][1] = row

        return result_lr, result_ud
    def display(self):

        wall_lr = self.wall_display()
        wall_ud = self.wall_display2()
        pillar = self.wall_counter()[1]

        cds_set, ee_set1 = self.cds_display()
        cds_set = sorted(cds_set, key=lambda l: l[1])
        ee_set_lr, ee_set_ud = self.ee_display(ee_set1)

        with open(f'{self.file_name[:-4]}.tex', 'w') as f:
            f.write('\\documentclass[10pt]{article}\n'
                    '\\usepackage{tikz}\n'
                    '\\usetikzlibrary{shapes.misc}\n'
                    '\\usepackage[margin=0cm]{geometry}\n'
                    '\\pagestyle{empty}\n'
                    '\\tikzstyle{every node}=[cross out, draw, red]\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\\vspace*{\\fill}\n'
                    '\\begin{center}\n'
                    '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n'
                    '% Walls\n'
                    )
            for i in range(0, len(wall_lr) - 1, 2):
                f.write(" " * 4 + f'\\draw ({wall_lr[i][0]},{wall_lr[i][1]}) -- ({wall_lr[i + 1][0]},{wall_lr[i + 1][1]});\n')
            for i in range(0, len(wall_ud) - 1, 2):
                f.write(" " * 4 + f'\\draw ({wall_ud[i][0]},{wall_ud[i][1]}) -- ({wall_ud[i + 1][0]},{wall_ud[i + 1][1]});\n')
            f.write('% Pillars\n')
            for i in range(0, len(pillar)):
                f.write(" " * 4 + f'\\fill[green] ({pillar[i][0]//2},{-pillar[i][1]//2}) circle(0.2);\n')

            f.write('% Inner points in accessible cul-de-sacs\n')
            for i in range(0, len(cds_set)):
                f.write(" " * 4 + f'\\node at ({cds_set[i][0]},{cds_set[i][1]}) {{}};\n')
            f.write('% Entry-exit paths without intersections\n')
            for i in range(0, len(ee_set_lr) - 1, 2):
                f.write(
                    " " * 4 + f'\\draw[dashed, yellow] ({ee_set_lr[i][0] / 2},{ee_set_lr[i][1] / 2}) -- ({ee_set_lr[i + 1][0] / 2},{ee_set_lr[i + 1][1] / 2});\n')
            for i in range(0, len(ee_set_ud) - 1, 2):
                f.write(
                    " " * 4 + f'\\draw[dashed, yellow] ({ee_set_ud[i][0] / 2},{ee_set_ud[i][1] / 2}) -- ({ee_set_ud[i + 1][0] / 2},{ee_set_ud[i + 1][1] / 2});\n')
            f.write('\\end{tikzpicture}\n'
                    '\\end{center}\n'
                    '\\vspace*{\\fill}\n'
                    '\n\\end{document}\n')

maze = Maze('labyrinth.txt')
maze.analyse()
#maze.display()



