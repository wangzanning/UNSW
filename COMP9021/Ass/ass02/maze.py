from collections import defaultdict
import numpy as np
import os
from collections import deque


# error
class MazeError(Exception):
    # init
    def __init__(self, message):
        self.message = message


class MazeNode(object):
    # check directions
    def check_directions(self):
        if self.value == '1':
            self.top = True
        elif self.value == '2':
            self.left = True
        elif self.value == '3':
            self.top = True
            self.left = True
        # right value
        if self.x + 1 < self.x_len \
                and self.input_digits[self.y][self.x + 1] in {'2', '3'}:
            self.right = True
        if self.y + 1 < self.y_len \
                and self.input_digits[self.y + 1][self.x] in {'1', '3'}:
            self.down = True
        self.directions = [self.top, self.down, self.left, self.right]

    # check
    def __init__(self, x=0, y=0, input_digits=[[]]):
        self.x = x
        self.y = y
        self.value = None
        self.top = False
        self.down = False
        self.left = False
        self.right = False
        self.directions = [False, False, False, False]
        if 0 <= self.x < len(input_digits[0]) and 0 <= self.y < len(input_digits):
            self.input_digits = input_digits
            self.x_len = len(input_digits[0])
            self.y_len = len(input_digits)
            self.value = input_digits[y][x]
            self.check_directions()

    # out put
    def __str__(self):
        return f'x:{self.x},y:{self.y},top:{self.top},down:{self.down},left:{self.left}:right:{self.right}'

    # out put
    def __repr__(self):
        return f'x:{self.x},y:{self.y},top:{self.top},down:{self.down},left:{self.left}:right:{self.right}'


# maze area
class MazeArea(object):

    # check
    def __init__(self, x, y):
        self.start = (x, y)
        self.paths = []
        self.gates = set()
        self.cul_de_sacs = []

    # out put
    def __str__(self):
        return f'start:{self.start}, paths:{self.paths}, gates:{self.gates}'

    # out put
    def __repr__(self):
        return f'start:{self.start}, paths:{self.paths}, gates:{self.gates}'


# class
class Maze(object):

    # read the input file
    def get_input(self, file):
        # self.input_digits = np.load(file_name)
        with open(file, 'r') as txt_file:
            for line in txt_file:
                # check the line is non blank
                if not line.isspace():
                    # check the line use space to check
                    self.input_digits.append(list("".join(line.split())))

        # check y dim at least 2 to 41
        self.len_y_dim = len(self.input_digits)
        if self.len_y_dim < 2 or self.len_y_dim > 41:
            raise MazeError('Incorrect input.')

        # check x dim at least 2 to 31
        len_x_dim = len(self.input_digits[0])
        for row in self.input_digits:
            # check each row has the same length
            if len_x_dim != len(row):
                raise MazeError('Incorrect input.')

            # check x dim at least 2 to 31
            len_x_dim = len(row)
            if len_x_dim < 2 or len_x_dim > 31:
                raise MazeError('Incorrect input.')

            # check the digits is correct
            if all(x not in self.init_digits for x in row):
                raise MazeError('Incorrect input.')

            # The last digit on every line with digits
            # cannot be equal to 1 or 3
            if row[-1] in {'1', '3'}:
                raise MazeError('Input does not represent a maze.')

        # length of x_dim
        self.len_x_dim = len_x_dim

        # the digits on the last line with digits cannot be equal to 2 or 3,
        #  which ensures that the input encodes a maze,
        if any(x in {'2', '3'} for x in self.input_digits[-1]):
            raise MazeError('Input does not represent a maze.')

        # set np a and y length
        self.len_x_np = self.len_x_dim * 3 - 2
        self.len_y_np = self.len_y_dim * 3 - 2
        # restructure
        # self.input_digits.insert(0, ['-1'] * self.len_x_dim)
        # self.input_digits.insert(self.len_y_dim + 1, ['-1'] * self.len_x_dim)
        # for row in self.input_digits:
        # row.insert(0, '-1')
        # row.insert(self.len_x_dim + 1, '-1')

    # construct new np array
    def get_np_array(self):

        self.np_digits = None
        for y in range(0, self.len_y_dim):
            line_digits = None
            for x in range(0, self.len_x_dim):
                node = MazeNode(x, y, input_digits=self.input_digits)
                node_list = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
                node_list[0][1] = int(node.top)
                node_list[2][1] = int(node.down)
                node_list[1][0] = int(node.left)
                node_list[1][2] = int(node.right)

                # node_list[1][1] = node
                # add the np
                if line_digits is None:
                    line_digits = np.array(node_list)
                else:
                    line_digits = np.hstack((line_digits, np.array(node_list)))

            if self.np_digits is None:
                self.np_digits = line_digits
            else:
                self.np_digits = np.vstack((self.np_digits, line_digits))

        # np.set_printoptions(threshold=np.inf)
        # print(self.np_digits)

    def get_walls_array(self):

        np_digits = None
        for y in range(0, self.len_y_dim):
            line_digits = None
            for x in range(0, self.len_x_dim):
                node = MazeNode(x, y, input_digits=self.input_digits)
                node_list = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                node_list[0, :] = int(node.top) if node.top else node_list[0, :]
                node_list[2, :] = int(node.down) if node.down else node_list[2, :]
                node_list[:, 0] = int(node.left) if node.left else node_list[:, 0]
                node_list[:, 2] = int(node.right) if node.right else node_list[:, 2]

                # node_list[1][1] = node
                # add the np
                if line_digits is None:
                    line_digits = np.array(node_list)
                else:
                    line_digits = np.hstack((line_digits, node_list))

            if np_digits is None:
                np_digits = line_digits
            else:
                np_digits = np.vstack((np_digits, line_digits))

        # print(np_digits)

        return np_digits

        # print(self.np_digits)

    # get all gates
    def get_gates(self):

        for x_dim in range(1, self.len_x_np, 3):
            # top
            if self.np_digits[0, x_dim] == 0:
                self.gates.add((x_dim, 0))
            # down
            if self.np_digits[self.len_y_np - 1, x_dim] == 0:
                self.gates.add((x_dim, self.len_y_np - 1))

        for y_dim in range(1, self.len_y_np, 3):
            # left
            if self.np_digits[y_dim, 0] == 0:
                self.gates.add((0, y_dim))
            # right
            if self.np_digits[y_dim, self.len_x_np - 1] == 0:
                self.gates.add((self.len_x_np - 1, y_dim))

        self.gates_count = len(self.gates)

    # get all the values
    def get_pillars_directions(self, walls_digits, point):
        direction_values = [True] * len(self.eight_directions)
        # get the current point
        (x, y) = point
        for i, k in enumerate(self.eight_directions):
            next_x, next_y = x + k[0], y + k[1]
            if self.len_x_np > next_x >= 0 \
                    and self.len_y_np > next_y >= 0 \
                    and walls_digits[next_y, next_x] != 0:
                direction_values[i] = False
                break

        return direction_values

    # get wall details
    def __get_walls_details(self, walls_digits):
        # current point value
        while self.queue:
            x, y = self.queue.popleft()
            # for each point
            for direction_x, direction_y in self.four_directions:
                new_x, new_y = x + direction_x, y + direction_y
                # check directions
                if 0 <= new_x < self.len_x_np and 0 <= new_y < self.len_y_np \
                        and walls_digits[new_y, new_x] == 1 \
                        and (new_x, new_y) not in self.visits:
                    self.visits.add((new_x, new_y))
                    self.queue.append((new_x, new_y))

    # get all the walls
    def get_walls(self):
        self.queue.clear()
        self.visits.clear()
        # deep copy
        walls_digits = self.get_walls_array()
        for y in range(0, len(walls_digits) - 2):
            for x in range(0, len(walls_digits[0]) - 2):
                if walls_digits[y, x] == 1 and (x, y) not in self.visits:
                    self.walls_count += 1
                    self.queue.append((x, y))
                    self.visits.add((x, y))
                    self.__get_walls_details(walls_digits)
                    # print(self.walls_count, y, x)
                    # print(walls_digits)

        for y_dim in range(0, self.len_y_np, 3):
            for x_dim in range(0, self.len_x_np, 3):
                if all(self.get_pillars_directions(walls_digits
                        , (x_dim, y_dim))):
                    self.pillars.append((x_dim // 3, y_dim // 3))
        # print(walls_digits)

    def __get_area_details(self, maze_area):
        # current point value
        while self.queue:
            path = self.queue.popleft()
            current_point = path[-1]
            x, y = path[-1]

            direction_values = []
            # set all the value
            for k in self.four_directions:
                next_x, next_y = x + k[0], y + k[1]
                if self.len_x_np > next_x >= 0 \
                        and self.len_y_np > next_y >= 0 \
                        and self.np_digits[next_y, next_x] == 0 and (next_x, next_y) not in self.visits:
                    # check the directions
                    direction_values.append((next_x, next_y))
            # not path access
            if len(direction_values) == 0:
                maze_area.paths.append(path)
                # print(path)
            else:
                # add to queue
                for value in direction_values:
                    # visited
                    self.visits.add(value)
                    self.queue.append(path + [value])

            # add current point to gates
            if current_point in self.gates:
                maze_area.gates.add(current_point)

    def get_areas(self):
        self.visits.clear()
        self.queue.clear()
        # 优先从门可以找
        gates = list(self.gates)
        for point in gates:
            if point not in self.visits:
                maze_area = MazeArea(point[0], point[1])
                # add to queue
                self.queue.append([point])
                self.visits.add(point)
                self.__get_area_details(maze_area)
                self.areas[point] = maze_area

        # check other point
        for y_dim in range(0, self.len_y_np):
            for x_dim in range(0, self.len_x_np):
                if self.np_digits[y_dim, x_dim] == 0 \
                        and (x_dim, y_dim) not in self.visits:
                    maze_area = MazeArea(x_dim, y_dim)
                    # add to queue
                    self.queue.append([(x_dim, y_dim)])
                    self.visits.add((x_dim, y_dim))
                    self.__get_area_details(maze_area)
                    self.areas[(x_dim, y_dim)] = maze_area

                    # print(self.areas)
                    # print(area_digits)

    # get all the inaccessible inner points and areas count
    def get_area_and_inner_point_count(self):
        self.visits.clear()
        for k, v in self.areas.items():
            if len(v.gates) == 0:
                for path in v.paths:
                    for point in path:
                        if point[0] % 3 == 1 and point[1] % 3 == 1:
                            self.visits.add((point[0] // 3, point[1] // 3))
            else:
                self.accessible_area_count += 1

        # remove the duplicate records
        self.inaccessible_inner_point_count = len(self.visits)

    # get all the values
    def get_forth_directions(self, np_digits, point, value, check_visited=False):
        direction_values = []
        # get the current point
        (x, y) = point

        for k in self.four_directions:
            next_x, next_y = x + k[0], y + k[1]
            if self.len_x_np > next_x >= 0 \
                    and self.len_y_np > next_y >= 0 \
                    and np_digits[next_y, next_x] == value:
                if check_visited and (next_x, next_y) in self.visits:
                    continue

                direction_values.append((next_x, next_y))
        return direction_values

    # cul_de_sacs
    def __get_cul_de_sacs_details(self, np_digits, cul_de_sacs):

        while len(self.queue) > 0:
            # get path
            path = self.queue.pop()
            point = path[-1]
            # get the current point
            x, y = point[0], point[1]
            # after check ,change value
            direction_values = self.get_forth_directions(np_digits, point, 0)
            if len(direction_values) == 1:
                np_digits[y, x] = 1
                # add the queue
                self.queue.append(path + [direction_values[0]])
            else:
                # print(point,path)
                if len(path) > 1:
                    cul_de_sacs.append(path)

    # cul_de_sacs
    def get_cul_de_sacs(self):
        self.queue.clear()
        np_digits = np.copy(self.np_digits)
        cul_de_sacs = []
        for k, v in self.areas.items():
            # acc
            if len(v.gates) > 0:
                for path in v.paths:
                    # 判断不是门的内容
                    if path[-1] not in self.gates:
                        # 最后一个节点
                        self.queue.append([path[-1]])
                        self.__get_cul_de_sacs_details(np_digits, cul_de_sacs)

        # print(len(cul_de_sacs))
        for i in range(len(cul_de_sacs)):
            path = cul_de_sacs[i]
            # print(path)
            flag = True
            for path1 in cul_de_sacs:
                if path[-1] in path1[:len(path1) - 1]:
                    flag = False

            if flag:
                self.cul_de_sacs_count += 1
                # self.cul_de_sacs.append(path)
        self.cul_de_sacs = cul_de_sacs
        self.queue.clear()

        self.get_entry_exit_path(np_digits)

        # print(self.cul_de_sacs)
        # print(self.cul_de_sacs_count)

    def _get_entry_exit_path_details(self, np_digits):
        self.visits.clear()
        while len(self.queue) > 0:
            # get path
            path = self.queue.pop()
            point = path[-1]
            # get the current point
            x, y = point[0], point[1]
            # add point
            self.visits.add(point)
            # after check ,change value
            direction_values = self.get_forth_directions(np_digits, point, 0, True)
            if len(direction_values) == 1:
                # add the queue
                self.queue.append(path + [direction_values[0]])
            else:
                # print(point,path)
                if len(path) > 1 and point in self.gates:
                    self.queue.clear()
                    self.entry_exit_path.append(path)
                    return path
        return None

    # get entry-exit path count
    def get_entry_exit_path(self, np_digits):
        exits_gates = set()
        for point in self.gates:
            if point not in exits_gates:
                self.queue.append([point])
                path = self._get_entry_exit_path_details(np_digits)
                if path:
                    exits_gates.add(path[0])
                    exits_gates.add(path[-1])

        self.visits.clear()

    def __init__(self, file):
        # input file name
        self.file_name = file
        # all the digits
        self.init_digits = {'0', '1', '2', '3'}
        self.visits = set([])
        self.queue = deque()
        self.np_digits = None

        # input digits
        # the length of x_dim, y_dim
        self.len_x_dim = 0
        self.len_y_dim = 0
        self.len_x_np = 0
        self.len_y_np = 0
        self.eight_directions = [(-1, 0), (1, 0)
            , (0, -1), (0, 1)
            , (-1, -1), (-1, 1)
            , (1, -1), (1, 1)]
        self.four_directions = [(-1, 0), (1, 0)
            , (0, -1), (0, 1)]

        self.input_digits = []
        # all the gates is dict
        self.gates = set([])
        self.gates_count = 0
        # walls
        self.walls_count = 0
        # areas
        self.areas = {}
        # inaccessible inner point
        self.inaccessible_inner_point_count = 0
        # accessible areas
        self.accessible_area_count = 0
        # pillars
        self.pillars = []
        # cul-de-sacs
        self.cul_de_sacs = []
        # cul-de-sacs count
        self.cul_de_sacs_count = 0

        self.entry_exit_path = []
        # read the maze file name
        self.get_input(file)
        # construct numpy array
        self.get_np_array()
        # get all gates
        self.get_gates()
        # get all the walls
        self.get_walls()
        # get all the areas
        self.get_areas()
        # get inaccessible inner point and areas
        self.get_area_and_inner_point_count()
        # get cul_de_sacs_count
        self.get_cul_de_sacs()

    # print all the info
    def __analyse_print(self):
        # print gates
        if self.gates_count == 0:
            print("The maze has no gate.")
        elif self.gates_count == 1:
            print("The maze has a single gate.")
        else:
            print(f"The maze has {self.gates_count} gates.")

        # print walls
        if self.walls_count == 0:
            print("The maze has no wall.")
        elif self.walls_count == 1:
            print("The maze has walls that are all connected.")
        else:
            print(f'The maze has {self.walls_count} sets of walls that are all connected.')

        # print inaccessible inner point
        if self.inaccessible_inner_point_count == 0:
            print("The maze has no inaccessible inner point.")
        elif self.inaccessible_inner_point_count == 1:
            print("The maze has a unique inaccessible inner point.")
        else:
            print(f"The maze has {self.inaccessible_inner_point_count} inaccessible inner points.")

        # print accessible area
        if self.accessible_area_count == 0:
            print("The maze has no accessible area.")
        elif self.accessible_area_count == 1:
            print("The maze has a unique accessible area.")
        else:
            print(f"The maze has {self.accessible_area_count} accessible areas.")

        # accessible cul - de - sac.
        if self.cul_de_sacs_count == 0:
            print("The maze has no accessible cul-de-sac.")
        elif self.cul_de_sacs_count == 1:
            print("The maze has accessible cul-de-sacs that are all connected.")
        else:
            print(f'The maze has {self.cul_de_sacs_count} sets of accessible cul-de-sacs that are all connected.')

        if len(self.entry_exit_path) == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif len(self.entry_exit_path) == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {len(self.entry_exit_path) } '
                  f'entry-exit paths with no intersections not to cul-de-sacs.')

    # analyse the maze
    def analyse(self):
        # print all the result
        self.__analyse_print()

    def __display_walls(self, file):

        # deal with row data
        y_walls = []
        # for loop y_dim
        for y_dim in range(0, len(self.np_digits) - 2, 3):
            temp_x = 0
            start_x = 0
            for x_dim in range(1, len(self.np_digits[0]) - 2, 3):
                if self.np_digits[y_dim, x_dim] == 1:
                    if temp_x == 0:
                        start_x = temp_x = x_dim
                    else:
                        if temp_x + 3 == x_dim:
                            temp_x = x_dim
                        else:
                            y_walls.append([(start_x // 3, y_dim // 3)
                                               , (temp_x // 3, y_dim // 3)])
                            start_x = temp_x = x_dim

            if start_x > 0:
                y_walls.append([(start_x // 3, y_dim // 3)
                                   , (temp_x // 3, y_dim // 3)])
        x_walls = []
        for x_dim in range(0, len(self.np_digits[0]) - 2, 3):
            temp_y = 0
            start_y = 0
            for y_dim in range(1, len(self.np_digits) - 2, 3):
                if self.np_digits[y_dim, x_dim] == 1:
                    if temp_y == 0:
                        start_y = temp_y = y_dim
                    else:
                        if temp_y + 3 == y_dim:
                            temp_y += 3
                        else:
                            x_walls.append([(x_dim // 3, start_y // 3)
                                               , (x_dim // 3, temp_y // 3)])
                            start_y = temp_y = y_dim

            if start_y > 0:
                x_walls.append([(x_dim // 3, start_y // 3), (x_dim // 3, temp_y // 3)])

        # print(y_walls)
        # print(x_walls)
        # write walls
        file.write('% Walls\n')
        for wall in y_walls:
            start = wall[0]
            end = wall[1]
            file.write('    \\draw (' + str(start[0]) + ',' + str(start[1]) + ') ')
            file.write('-- (' + str(end[0] + 1) + ',' + str(end[1]) + ');\n')
        for wall in x_walls:
            start = wall[0]
            end = wall[1]
            file.write('    \\draw (' + str(start[0]) + ',' + str(start[1]) + ') ')
            file.write('-- (' + str(end[0]) + ',' + str(end[1] + 1) + ');\n')

    # draw pillars
    def __display_pillars(self, file):
        file.write('% Pillars\n')
        for point in self.pillars:
            # print(point)
            (x, y) = point
            file.write('    \\fill[green] (' + str(x)
                       + ',' + str(y) + ')')
            file.write(' circle(0.2);\n')

    # draw inner point
    def __inner_accessible_cul_de_sacs(self, file):
        file.write('% Inner points in accessible cul-de-sacs\n')
        cul_de_sacs = defaultdict(list)
        for row in self.cul_de_sacs:
            for point in row[:len(row) - 1]:
                if point[0] % 3 == 1 and point[1] % 3 == 1:
                    x, y = point[0] // 3, point[1] // 3
                    cul_de_sacs[y].append(x)

        for y in sorted(cul_de_sacs.keys()):
            for x in sorted(set(cul_de_sacs[y])):
                file.write('    \\node at (' + str(x + 0.5)
                           + ',' + str(y + 0.5) + ')')
                file.write(' {};\n')

    # display details
    def __display_entry_exit_path_order_details(self, path, axis=0):
        path_list = []
        for current_point in path:
            if len(path_list) == 0:
                path_list.append([current_point, current_point])
            else:
                # get every point
                previous_points = path_list.pop()
                (start_x, start_y) = previous_points[0]
                (end_x, end_y) = previous_points[1]
                current_x, current_y = current_point

                # x axis
                if axis == 0:
                    if start_x == end_x == current_x:
                        if current_y - end_y == 1:
                            # add the new point
                            previous_points[1] = current_point
                            path_list.append(previous_points)
                        elif start_y - current_y == 1:
                            previous_points[0] = current_point
                            path_list.append(previous_points)
                        else:
                            # add the path_listthe two point
                            path_list.append(previous_points)
                            path_list.append([current_point, current_point])
                    else:
                        # add the path_listthe two point
                        path_list.append(previous_points)
                        path_list.append([current_point, current_point])
                else:
                    # check the value
                    if start_y == end_y == current_y:
                        if current_x - end_x == 1:
                            # add the new point
                            previous_points[1] = current_point
                            path_list.append(previous_points)
                        elif start_x - current_x == 1:
                            # add the new point
                            previous_points[0] = current_point
                            path_list.append(previous_points)
                        else:
                            # add the path_listthe two point
                            path_list.append(previous_points)
                            path_list.append([current_point, current_point])
                    else:
                        # add the path_listthe two point
                        path_list.append(previous_points)
                        path_list.append([current_point, current_point])

        return path_list

    # entry_extry
    def __display_entry_exit_paths(self, file):
        file.write('% Entry-exit paths without intersections\n')
        # return directly
        if len(self.entry_exit_path) == 0:
            return
        y_path_dict = defaultdict(list)
        x_path_dict = defaultdict(list)
        for path in self.entry_exit_path:
            for (x, y) in path:
                if y % 3 == 1 and x % 3 == 0:
                    y_path_dict[y // 3].append(x // 3)
                if y % 3 == 0 and x % 3 == 1:
                    x_path_dict[x // 3].append(y // 3)
        paths = []
        for key in sorted(y_path_dict.keys()):
            values = sorted(y_path_dict[key])
            for value in values:
                paths.append((value, key))
        paths = self.__display_entry_exit_path_order_details(paths, 1)
        for path in paths:
            (start_x, start_y) = path[0]
            (end_x, end_y) = path[1]
            file.write(f'    \draw[dashed, yellow] ({start_x-0.5},{start_y + 0.5}) '
                       f'-- ({end_x + 0.5},{end_y+ 0.5});\n')

        paths = []
        for key in sorted(x_path_dict.keys()):
            values = sorted(x_path_dict[key])
            for value in values:
                paths.append((key, value))

        paths = self.__display_entry_exit_path_order_details(paths, 0)
        for path in paths:
            (start_x, start_y) = path[0]
            (end_x, end_y) = path[1]
            file.write(f'    \draw[dashed, yellow] ({start_x + 0.5},{start_y - 0.5}) '
                       f'-- ({end_x + 0.5},{end_y+ 0.5});\n')

    # display the info
    def display(self):
        file_name = self.file_name.split('.')[0] + '.tex'
        # delete file
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as file:
            file.write('\\documentclass[10pt]{article}\n')
            file.write('\\usepackage{tikz}\n')
            file.write('\\usetikzlibrary{shapes.misc}\n')
            file.write('\\usepackage[margin=0cm]{geometry}\n')
            file.write('\\pagestyle{empty}\n')
            file.write('\\tikzstyle{every node}=[cross out, draw, red]\n')
            file.write('\n')
            file.write('\\begin{document}\n')
            file.write('\n')
            file.write('\\vspace*{\\fill}\n')
            file.write('\\begin{center}\n')
            file.write('\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n')

            # draw walls
            self.__display_walls(file)
            # draw pillars
            self.__display_pillars(file)
            # out inner_accessible_cul_de_sacs
            self.__inner_accessible_cul_de_sacs(file)
            # exit path
            self.__display_entry_exit_paths(file)

            # end
            file.write('\\end{tikzpicture}\n')
            file.write('\\end{center}\n')
            file.write('\\vspace*{\\fill}\n')
            file.write('\n')
            file.write('\\end{document}\n')

        # os.system("pdflatex " + file_name)


