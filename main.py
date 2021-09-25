import random, os
from copy import deepcopy
from pickle import *
import time
def gen_field(n = 5, count_mine = 2):
    global tile_field, tile_mine, coord_mine
    cur_f = [[tile_field for i in range(n + 2)] for j in range(n + 2)]
    coord_mine = set()
    show_field = deepcopy(cur_f)
    # coord_mine = {(1, 1), (2, 1)}
    while len(coord_mine) != count_mine:
        coord_mine |= set([(random.randint(1, n), random.randint(1, n))])
    for (x, y) in coord_mine:
        cur_f[x][y] = tile_mine
    # print(*cur_f, sep = '\n')
    coord_x = [0, 1, 0, -1, 1, -1, -1, 1]
    coord_y = [1, 0, -1, 0, -1, 1, -1, 1]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            cur = 0
            for coor in range(len(coord_x)):
                if cur_f[i + coord_x[coor]][j + coord_y[coor]] == tile_mine:
                    cur += 1
            if cur_f[i][j] != tile_mine:
                cur_f[i][j] = cur



    return show_field, cur_f


def view(field):
    time.sleep(0.25)
    os.system('cls')
    for i in range(0, len(field) - 1):
        for j in range(0, len(field) - 1):
            if i == 0 or j == 0:
                print(str(i + j).rjust(3), end = '')
            else:
                print(str(field[i][j]).rjust(3), end = '')
        print()


def step(field_game):
    global tile_field, was
    try:
        x, y, action = input().split()
    except ValueError:
        return -1, 0, 0
    x = int(x)
    y = int(y)
    op_act = (action.lower() == 'open')

    if op_act:
        if field_game[x][y] == 0:
            was = set()
            return (3, x, y) # open 0
        if field_game[x][y] != tile_mine:
            return (1, x, y) # open
        else:
            return (0, '', '') # loose
    else:
        return (2, x, y) # set flag

def save_position(field_game, field_show):
    print('Pos Saved')
    f = open('save.dat', 'wb')
    dump([True, {'field_game': field_game, 'field_show': field_show}], f)
    f.close()





def check(x, game_field):
    return  len(game_field) - 1 >= x >= 1

was = set()
def open_zero(x, y, game_field, show_field):
    global was
    # print(x, y)
    if game_field[x][y] != 0 or not(check(x, game_field)) or not check(y, game_field) or (x, y) in was:
        # print(x, y, 'break')
        return
    else:
        coord_x = [0, 1, 0, -1, 1, -1, -1, 1]
        coord_y = [1, 0, -1, 0, -1, 1, -1, 1]
        show_field[x][y] = 0
        for i in range(len(coord_x)):
            show_field[x + coord_x[i]][y + coord_y[i]] = game_field[x + coord_x[i]][y + coord_y[i]]
        # view(show_field)
        was |= set([(x, y)])

    for i in range(len(coord_x)):
        open_zero(x + coord_x[i], y + coord_y[i], game_field, show_field)






def load_position():
    f = open('save.dat', 'rb')
    cur = load(f)
    f.close()
    if not cur[0]:
        n = int(input('Size of game_place: '))
        count_mine = int(input('Count of mine: '))
        field_show, field_game = gen_field(n = n, count_mine = count_mine)
        return field_show, field_game

    n = input('Load last game? y/n ')
    if n == 'y':
        cur = cur[1]
        return cur['field_show'], cur['field_game']
    n = int(input('Size of game_place: '))
    count_mine = int(input('Count of mine: '))
    field_show, field_game = gen_field(n = n, count_mine = count_mine)
    return field_show, field_game

def check_win(coord_mine, list_flags):
    return coord_mine == list_flags



def start_game():
    global tile_flag, coord_mine
    field_show, field_game = load_position()
    list_flags = set()
    view(field_show)
    # view(field_game)
    flag = True
    while flag:
        if check_win(coord_mine, list_flags):
            print('WIIIIIIIIIIIIIIIIIIIIIIN')
            view(field_game)
            f = open('save.dat', 'wb')
            dump([False], f)
            f.close()
            break
        tmp_event, x, y = step(field_game)
        if tmp_event == -1: # input error
            print('Repeat, pls')
        elif tmp_event == 3: # open zero
            open_zero(x, y, field_game, field_show)
        elif not tmp_event: # loose
            print("LOOOOOOOOOOOOOOOOOOOOOOSE")
            view(field_game)
            f = open('save.dat', 'wb')
            dump([False], f)
            f.close()
            break
        else:
            if tmp_event == 2: # flag
                field_show[x][y] = tile_flag
                list_flags.add((x, y))
            else:
                field_show[x][y] = field_game[x][y]
        view(field_show)
        save_position(field_game, field_show)


coord_mine = {}
# tile_field = '▩'
# tile_mine = '💣'
# tile_flag = '❗'


tile_field = '='
tile_mine = '*'
tile_flag = '!'




# f = open('save.dat', 'wb')
# dump([False], f)
# f.close()
#
while True:
    start_game()


    os.system('Pause')