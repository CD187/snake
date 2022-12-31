import os
from random import randint
from tty import *
from termios import *
from sys import stdin
from time import time
from vy_console import getch_noblock
import map_elements
from collections import defaultdict
import TUI_func as tf
from TUI_image_bg import snake 
from menus import tree_menu
from string import ascii_letters, digits

class Snake:
    def __init__(self):
        self.log_dir()

    def log_dir(self):
        main_dir = './snake'
        path_log = main_dir + '/.logs'
        try:
            self.users = os.listdir(path_log)
        except FileNotFoundError:
            if os.path.isdir(main_dir) == True:
                os.mkdir(path_log,0o777)
            else:
                os.mkdir(main_dir,0o777)
                os.mkdir(path_log,0o777)
        self.players = os.listdir(path_log)
        self.path_log = path_log 

    def load_player_settings(self):
        self.player_settings = {'map' : 0, 'difficulty': 0, 'border': 0, 'snake_color':0, 'background': 0, 'language':0}
        with open(self.path_log+f'/{self.player}','r') as file:
            for line in file:
                if line.startswith('map'):
                    a = line.split()
                    for i,item in enumerate(a):
                        if item in self.player_settings.keys():
                            self.player_settings[item] = a[i+1]

    def generate_land(self, land_size):
        columns, lines = land_size
        land = [
                [1 for column in range(columns)] 
                if 
                    line in [0,lines-1] 
                else 
                    [1 
                    if 
                        line in [0,columns-1] 
                    else 
                        0 
                    for line in range(columns)
                    ]    
                for line in range(lines)
               ]
        return land
   
    def generate_shortucts(self):
        dictionnary = defaultdict(list)
        for snake_el,d in self.snake_el.items():
            for new_direction in d.values():
                for old_direction in new_direction.values():
                    for value in old_direction:
                        dictionnary[snake_el].append(value)
        return dictionnary

    def new_apple(self):
        while True:
            new_apple_y = randint(1,self.land_size[1] - 2)
            free_space = []
            for i, value in enumerate(self.land[new_apple_y]):
                if value == 0:
                    free_space.append(i)
            a =len(free_space) 
            if a != 0:
                self.land[new_apple_y][free_space[randint(0, a-1)]] = 15
                break

    def extra(self):
        while True:
            extra_y = randint(1,self.land_size[1] - 2)
            free_space = []
            for i, value in enumerate(self.land[extra_y]):
                if value == 0:
                    free_space.append(i)
            a =len(free_space) 
            if a != 0:
                self.land[extra_y][free_space[randint(0, a-1)]] = 90
                break
            self.extra_time = time()
    
    def define_parameters(self):
        a,b = tree_menu['settings']['map'][int(self.language)]
        self.land_size = tuple([int(el) for el in b[int(self.player_settings['map'])].split('x')])  
        a,b = tree_menu['settings']['difficulty'][int(self.language)]
        self.difficulty = [0.2,0.15,0.1][int(self.player_settings['difficulty'])]
        self.border = int(self.player_settings['border'])
        self.col = int(self.player_settings['snake_color'])
        self.print_background = int(self.player_settings['background'])
        self.score = 0

    def delete_snake_tail(self):
        # delete old tail and generate new one:
        if self.snake_lenght == 2 :
            self.land[self.old_snake_head_y][self.old_snake_head_x] = 0           
        elif self.snake_lenght >= 3 :
            if self.flag_3:
                val = self.land[self.snake_tail_y][self.snake_tail_x]   
                if  30 <= val <= 33:
                    self.old_snake_tail_y, self.old_snake_tail_x = self.snake_tail_y, self.snake_tail_x
                    if val == 30:
                        self.snake_tail_x += 1
                        if not self.border and self.snake_tail_x == self.land_size[0] - 1:
                            self.snake_tail_x = 1
                    elif val == 31:
                        self.snake_tail_x -= 1
                        if not self.border and self.snake_tail_x == 0:
                            self.snake_tail_x = self.land_size[0] - 2
                    elif val == 32:
                        self.snake_tail_y -= 1
                        if not self.border and self.snake_tail_y == 0:
                            self.snake_tail_y = self.land_size[1] - 2
                    elif val == 33:
                        self.snake_tail_y += 1
                        if not self.border and self.snake_tail_y == (self.land_size[1] - 1):
                            self.snake_tail_y = 1
                    new_corps, old_corps = self.search_directions(self.land[self.snake_tail_y][self.snake_tail_x], 'corps')
                    i = 0
                    if self.land[self.snake_tail_y][self.snake_tail_x] > 15:
                        i = 1
                    self.land[self.snake_tail_y][self.snake_tail_x] = list(self.snake_el['tails'][new_corps]['all'].keys())[i]
                    self.land[self.old_snake_tail_y][self.old_snake_tail_x] = 0           
                else:
                    self.land[self.snake_tail_y][self.snake_tail_x] -= 15 
            if not self.flag_3 and not self.tail_was_born and not self.corps_was_born :
                self.flag_3 = True
                self.snake_tail_x, self.snake_tail_y = self.old_snake_head_x, self.old_snake_head_y 
                self.land[self.snake_tail_y][self.snake_tail_x] -= 15 

    def new_snake_head_location(self):
        self.old_snake_head_x, self.old_snake_head_y = self.snake_head_x, self.snake_head_y
        if self.direction == 'down':
            self.snake_head_y += 1
        elif self.direction == 'up':
            self.snake_head_y -= 1
        elif self.direction == 'left':
            self.snake_head_x -= 1
        elif self.direction == 'right':
            self.snake_head_x += 1
    
    def search_directions(self, map_value, snake_el, index = None):
        for new_direction, old_dir in self.snake_el[snake_el].items():
            for old_direction,dic in old_dir.items():
                    if not index:
                        if map_value in dic.keys():
                            return new_direction, old_direction
                    for i, value in enumerate(dic.keys()):
                        if value == map_value:
                            return i,new_direction, old_direction

    def calcul_events(self):
        next_case = self.land[self.snake_head_y][self.snake_head_x] 
        # if empty case:
        if next_case == 0:
            self.land[self.snake_head_y][self.snake_head_x]= list(self.snake_el['heads'][self.direction][self.old_direction].keys())[0]
        # if limit case or Snake :    
        elif next_case == 1:
            if self.border:
                self.game_over()
            else:
                if self.direction == 'down':
                    self.snake_head_y = 1
                    self.land[self.snake_head_y][self.snake_head_x]= list(self.snake_el['heads'][self.direction][self.old_direction].keys())[0]
                elif self.direction == 'up':
                    self.snake_head_y = self.land_size[1] - 2
                    self.land[self.snake_head_y][self.snake_head_x]= list(self.snake_el['heads'][self.direction][self.old_direction].keys())[0]
                elif self.direction == 'left':
                    self.snake_head_x = self.land_size[0] - 2
                    self.land[self.snake_head_y][self.snake_head_x]= list(self.snake_el['heads'][self.direction][self.old_direction].keys())[0]
                elif self.direction == 'right':
                    self.snake_head_x = 1
                    self.land[self.snake_head_y][self.snake_head_x]= list(self.snake_el['heads'][self.direction][self.old_direction].keys())[0]

        elif 3 <= next_case <= 48 and next_case != 15:
            self.game_over()
        # if apple case :
        elif next_case == 15:
            self.land[self.snake_head_y][self.snake_head_x]= list(self.snake_el['heads'][self.direction][self.old_direction].keys())[1]
            if self.snake_lenght == 1:
                self.tail_was_born = True
            elif self.snake_lenght == 2:
                if self.tail_was_born:
                    self.corps_was_born = True
            self.snake_lenght += 1
            self.new_apple()
            self.score += 15
            if self.difficulty == 0 :
                if randint(0,100) < 10:
                    self.extra()
            elif self.difficulty == 1:
                if randint(0,100) < 7:
                    self.extra()
            elif self.difficulty == 2:
                if randint(0,100) < 5:
                    self.extra()
        # if extra (timer is not implemented)
        elif next_case == 90:
            self.score += 30
        # Anyway :
        if self.snake_lenght == 1:
            self.land[self.old_snake_head_y][self.old_snake_head_x] = 0  
        elif self.snake_lenght == 2:
                self.land[self.old_snake_head_y][self.old_snake_head_x] =  list(self.snake_el['tails'][self.direction]['all'].keys())[0]
        elif self.snake_lenght >= 3:
            if self.tail_was_born:
                if self.corps_was_born:
                    self.temp_loc_x, self.temp_loc_y = self.old_snake_head_x, self.old_snake_head_y
                    self.land[self.old_snake_head_y][self.old_snake_head_x] =  list(self.snake_el['tails'][self.direction]['all'].keys())[0]
                    self.corps_was_born = None
                else:
                    if not self.flag_3:
                        self.land[self.old_snake_head_y][self.old_snake_head_x] =  list(self.snake_el['tails'][self.direction]['all'].keys())[1]
                    self.snake_tail_x, self.snake_tail_y = self.temp_loc_x, self.temp_loc_y 
                    self.land[self.snake_tail_y][self.snake_tail_x] = 0
                    self.temp_loc_x, self.temp_loc_y = self.old_snake_head_x, self.old_snake_head_y
                    self.tail_was_born = None
            else:
                i = 0
                if  self.land[self.old_snake_head_y][self.old_snake_head_x] > 62:
                    i = 1
                self.land[self.old_snake_head_y][self.old_snake_head_x]= list(self.snake_el['corps'][self.direction][self.old_direction].keys())[i]

class TUI(Snake):
    def __init__(self):
        self.mode = 0
        Snake.__init__(self)
        self.arrow = ['up', 'down', 'right', 'left']
        self.valid_key = ['\x1b\x5b\x41', '\x1b\x5b\x42', '\x1b\x5b\x43', '\x1b\x5b\x44']
    
    def language_selection(self):
        lang = tf.selector_menu_maker(['english','français'], 
                                          selector=True, 
                                          background = snake, 
                                          width_menu = 30,
                                          prompt = 'LANGUAGE :')
        a,b = tree_menu['settings']['language'][0]
        for i, language in enumerate(b):
            if lang == language:
                self.language = i

    def print_land(self, array):
        screen = []
        for line in array:
            buffer = []
            for char in line:
                buffer.append(self.drawing(char))
            buffer.append('\x1b[0m')
            #print(''.join(buffer))
            screen.append(''.join(buffer))
        if self.print_background:
            tf.print_my_game(screen, background = snake, width_menu = self.land_size[0],  prompt = str(self.score))
        else:
            tf.print_my_game(screen, prompt = str(self.score))

    def drawing(self, char):
        if char in self.elements.keys():   
            return f'\x1b[48;5;{self.elements[char][self.mode]}m  '
        else:
            for k,v in self.values_shortcuts.items(): 
                if char in v:
                    el = k
                    for new_direction, old_dir in self.snake_el[el].items():
                        for old_direction,dic in old_dir.items():
                            for value, render in dic.items():
                                if char == value:
                                    return f'\x1b[48;5;{self.snake_el[el][new_direction][old_direction][value][self.mode][self.col]}m  ' 
    def play(self):
        try:
            self.define_parameters()
            # create the land to play and dictionnaries of all items on map
            self.land = self.generate_land(self.land_size)
            self.snake_el = map_elements.snake_el
            self.elements = map_elements.elements
            self.tree_directions = map_elements.tree_directions
            self.values_shortcuts = self.generate_shortucts()
            # snake location and direction
            self.direction = 'right' 
            self.snake_head_x, self.snake_head_y = (round((self.land_size[0]-1)/2), round((self.land_size[1]-1)/2))
            self.snake_lenght = 1
            self.land[self.snake_head_y][self.snake_head_x] = 50
            # flags
            self.tail_was_born = None
            self.corps_was_born = None
            self.flag_3 = None
            # first apple generation
            self.new_apple()
            self.key_pressed ='right'
            old_mode = tcgetattr(stdin)
            new_mode = tcgetattr(stdin)
            new_mode[3] = new_mode[3] & ~ECHO
            try:
                tcsetattr(stdin,TCSADRAIN,new_mode) #fix terminal printing bug 
                while True:                         
                    start_time = time()
                    while time() - start_time < self.difficulty:
                        self.get_a_key = self.keyboard_event()
                        if self.get_a_key:  
                            self.key_pressed = self.get_a_key
                    self.delete_snake_tail()
                    self.check_direction()
                    self.new_snake_head_location()
                    self.calcul_events()
                    self.print_land(self.land)
            finally:
                tcsetattr(stdin,TCSAFLUSH, old_mode)
        except KeyboardInterrupt:
            pass
            '''
            print('\n')
            for el in self.land:
                print(el)
            '''
    def check_direction(self):
        # avoid snake to return on itself:    
        self.old_direction = self.direction
        if self.key_pressed in self.tree_directions[self.direction]:
            self.direction = self.key_pressed


    def keyboard_event(self):
        char = next(getch_noblock())
        if char == '':
            return None 
        if char == '\x03':
            raise KeyboardInterrupt 
        if char in self.valid_key:
            for key_pressed, ret_val in zip(self.valid_key, self.arrow):
                if char == key_pressed:
                        return ret_val

    def menu_select_player(self):
        print('\x1b[?25l')                   #hide cursor 
        max_len_player_name = 16
        select_player, new_player = tree_menu['players'][self.language]
        if len(self.players) <= 9:                       #max 10 players
            self.players.append(new_player)
        player_name = tf.selector_menu_maker( self.players, 
                                              selector=True, 
                                              background = snake, 
                                              width_menu = 30,
                                              prompt = select_player)
        if player_name == new_player:
            new_name = '' 
            backspace = ['\x7f', '\x08']
            while True:
                char = tf.selector_menu_maker([new_name],
                                              background = snake,
                                              width_menu = 30,
                                              prompt = tree_menu['new_player'][self.language])
                if char in [*ascii_letters, *digits]:
                    new_name += char
                elif char in backspace:
                    if len(new_name) >= 1:
                        new_name = new_name[:-1] 
                elif char == '\x0d':
                    self.player = new_name
                    with open(self.path_log+f'/{new_name}','a') as file:
                        file.write(new_name + '\nmap 1 difficulty 1 border 0 snake_color 0 language ' + str(self.language))
                        self.players[-1] = player_name
                    break
        else:
            self.player = player_name
            if self.players[-1] ==  new_player: 
                self.players = self.players[:-1]

    def main_menu(self):
        next_step = tf.selector_menu_maker( tree_menu['play'][self.language],
                                            selector=True, 
                                            background = snake, 
                                            width_menu = 30)
        for i, choice in enumerate(tree_menu['play'][self.language]):
            if next_step == choice:
                return i
    
    def game_over(self):
        with open(self.path_log+f'/{self.player}','a') as file:
            file.write(str(self.score))
            for k,v in self.player_settings.items():
                file.write(' ' + str(k) + ':' + str(v))
            file.write('\n')
        self.get_best_score()
        a,b,c = tree_menu['game_over'][self.language]
        tf.selector_menu_maker( ['',a,'','',b,str(self.score), '', '',c, str(self.best_score),''],
                                background = snake, 
                                width_menu = 30)
        raise KeyboardInterrupt

    def get_best_score(self):
        with open(self.path_log+f'/{self.player}','r') as file:
            self.best_score = int(0)
            for line in file:
                try:
                    score = int(line.split()[0])
                    if self.best_score < score:
                        self.best_score = score
                except ValueError:
                    pass

    def override_player_settings(self):
        lines = []
        with open(self.path_log+f'/{self.player}','r') as file:
            for line in file:
                if line.startswith('map'):
                    lines.append('map ' + str(self.player_settings['map']) + ' difficulty ' + str(self.player_settings['difficulty']) + ' border ' + str(self.player_settings['border']) + ' snake_color ' + str(self.player_settings['snake_color']) + ' language ' + str(self.player_settings['language']) + '\n')
                else:
                    lines.append(line)
        with open(self.path_log+f'/{self.player}','w') as file:
            for line in lines:
                file.write(line)

        
if __name__ == '__main__':
    Snake = TUI()
    Snake.language_selection()
    Snake.menu_select_player()
    Snake.load_player_settings()
    Snake.language = int(Snake.player_settings['language'])
    while True:
        choice = Snake.main_menu()
        if choice == 0:
            Snake.play()
        elif choice == 1:
            tf.rolling_menu_maker(Snake.player_settings,
                                  background = snake,
                                  width_menu = 30)
            Snake.language = int(Snake.player_settings['language'])
            Snake.override_player_settings()
        elif choice == 2:
            Snake.menu_select_player()
        elif choice == 3:
            print('\x1b[?25h')
            raise KeyboardInterrupt
