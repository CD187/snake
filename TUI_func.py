"this file is a set of functions used for TUI graphicals functions that we can use in other programs. This file import the wonderfull function made by NOPHKE wrotten for Vy in order to get a key pressed without using any library as ncurses or keyboard"

import os
from vy_console import getch_noblock
from menus import tree_menu

def custom_input(input_validation, valid_char, prompt = None, timer = None, max_len = None, backspace = None, middle = None):
    if timer and timer > 0:
        starting_time = time()
    char = user_input = ''
    iterator = getch_noblock() 
    while not input_validation(user_input):            
        print('\x1b[2K', end='')
        if not middle:
            if prompt:
                print(prompt, user_input, end='\r')
            else:
                print(user_input, end='\r')
        else:
            if prompt:
                print(self.middle_line(prompt + user_input), end='\r')
            else:
                print(self.middle_line(user_input), end='\r')
        while True:              #this loop is done in order to avoid printing bug if we modify the terminal size 
            if timer and time() - starting_time > timer:
                user_input += 'ValueError\x0d'
                break
            char = next(iterator)
            if valid_char(char):
                if not max_len or max_len and len(user_input) < max_len:
                    user_input += char
                    break
            elif char == '\x7f'  or char == '\x08':
                if not backspace:
                    user_input = user_input[:-1]
                    break
    return user_input

def rolling_menu_maker(player_settings, background = None, width_menu = None, prompt = None, ngap = None, end = None):
    foreground = rolling_list_generator(tree_menu['settings'], player_settings)
    waiting_validation = True
    len_foreground = len(foreground)
    line_selector = 2
    if prompt:
        line_selector += 2
    if ngap:
        line_selector += (ngap-1)
    min_selector = line_selector 
    max_selector = min_selector + len_foreground
    keys = ['\x1b\x5b\x41', '\x1b\x5b\x42','\x1b\x5b\x43','\x1b\x5b\x44', '\x0d']
    while waiting_validation:
        col, lin = os.get_terminal_size()
        up_fg, len_menu, datas = lists_for_screen(col, lin, foreground, background = background, prompt = prompt, ngap = ngap, end = end)
        pointer = line_selector + up_fg
        print_menu_screen(up_fg, len_menu, datas, col, width_menu = width_menu, pointer = pointer, rolling = True)
        char = custom_input(lambda ui: True if ui != '' else False,
                            lambda char: True if char in keys else False)
        if char == '\x1b\x5b\x42':   #arrow down
            line_selector += 3
        elif char == '\x1b\x5b\x41': #arrow up
            line_selector -= 3
        elif char == '\x1b\x5b\x43': #arrow right
            arg = foreground[line_selector - min_selector]
            rolling_modif_val(1, foreground, player_settings, arg)
        elif char == '\x1b\x5b\x44': #arrow left
            arg = foreground[line_selector - min_selector]
            rolling_modif_val(-1, foreground, player_settings, arg)
        elif char == '\x0d':         #enter
            waiting_validation = False
        if line_selector == max_selector:
            line_selector = min_selector  
        elif line_selector == min_selector - 3:
            line_selector = max_selector - 3 
        foreground = rolling_list_generator(tree_menu['settings'], player_settings)

def rolling_list_generator(main_dico, player_settings):
    temp_values = []
    for k,v in player_settings.items():
        temp_values.append(v)
    temp_values.reverse()
    new_list = []
    for k,v in main_dico.items():
        param, list_param = v[int(player_settings['language'])]
        new_list.append(param)
        new_list.append(list_param[int(temp_values.pop())])
        new_list.append('')
    return new_list

def rolling_modif_val(val, foreground, player_settings, arg):
    for k,v in tree_menu['settings'].items():
        param, list_param = v[int(player_settings['language'])]
        if param == arg:
            temp_val = int(player_settings[k]) + val 
            if temp_val == len(list_param):
                player_settings[k] = 0
            elif temp_val == -1:
                player_settings[k] = len(list_param) - 1
            else:
                player_settings[k] = temp_val

def selector_menu_maker(foreground, selector = None, background = None, width_menu = None, prompt = None, ngap = None, end = None):
    waiting_validation = True
    if selector:
        len_foreground = len(foreground)
        line_selector = 1
        if prompt:
            line_selector += 2
        if ngap:
            line_selector += (ngap-1)
        min_selector = line_selector - 1
        max_selector = min_selector + len_foreground + 1
        keys = ['\x1b\x5b\x41', '\x1b\x5b\x42', '\x0d']
        while True: 
            while waiting_validation:
                col, lin = os.get_terminal_size()
                up_fg, len_menu, datas = lists_for_screen(col, lin, foreground, background = background, prompt = prompt, ngap = ngap, end = end)
                pointer = line_selector + up_fg
                print_menu_screen(up_fg, len_menu, datas, col, width_menu = width_menu, pointer = pointer)
                char = custom_input(lambda ui: True if ui != '' else False,
                                    lambda char: True if char in keys else False)
                if char == '\x1b\x5b\x42':   #arrow down
                    line_selector += 1
                elif char == '\x1b\x5b\x41': #arrow up
                    line_selector -= 1
                elif char == '\x0d':         #enter
                    waiting_validation = False
                if line_selector == max_selector:
                    line_selector = min_selector + 1
                elif line_selector == min_selector:
                    line_selector = max_selector -1
            return foreground[line_selector - min_selector - 1]
    while waiting_validation:
        col, lin = os.get_terminal_size()
        up_fg, len_menu, datas = lists_for_screen(col, lin, foreground, background = background, prompt = prompt, ngap = ngap, end = end)
        print_menu_screen(up_fg, len_menu, datas, col, width_menu = width_menu)
        char = custom_input(lambda ui: True if ui != '' else False,
                            lambda char: True if char else False)
        return char

def print_my_game(foreground, background = None, width_menu = None, prompt = None, ngap = None, end = None):       
    col, lin = os.get_terminal_size()
    up_fg, len_menu, datas = lists_for_screen(col, lin, foreground, background = background, prompt = prompt, ngap = ngap, end = end)
    print_menu_screen(up_fg, len_menu, datas, col, width_menu = width_menu)
             

def print_menu_screen(up_fg, len_menu, datas, col, width_menu = None, pointer = None, rolling = None):
        i = 0
        eom = len_menu + up_fg
        for foreground, background in datas:
            if i == pointer:
                print(middle_line(col, foreground, background = background, width_menu = width_menu, prefixe = '\x1b[30;107m', suffixe = '\x1b[0;1m', rolling = rolling))
                i += 1
            elif i < up_fg:
                print(middle_line(col, foreground,  background = background))
                i += 1
            elif up_fg <= i < eom:
                print(middle_line(col, foreground, background = background, width_menu = width_menu))
                i += 1
            else:
                print(middle_line(col, foreground,  background = background)) 
                i += 1

def lists_for_screen(col,lin, foreground, background = None, prompt = None, ngap = None, end = None):
    menu_foreground = list_menu_generator(foreground, prompt = prompt, ngap = ngap, end = end)
    empty = ['']
    len_menu_foreground = len(menu_foreground)
    if lin > len_menu_foreground :
        temp = lin - len_menu_foreground + 1
        accu = temp%2
        up_fg = int((temp - accu)/2)
        down_fg = temp - up_fg + accu
        menu_foreground = up_fg*empty + menu_foreground + down_fg*empty
    else:
        up_fg = 0
        menu_foreground = menu_foreground[:lin]
    if background:
        if lin > len(background):
            temp2 = lin - len(background) + 1
            accu2 = temp2%2
            up_bg = int((temp2 - accu2)/2)
            down_bg = temp2 - up_bg + accu2 
            background = up_bg*empty + background + down_bg*empty
        else:
            background = background[:lin]
    else:
        background = [None for el in menu_foreground]
    return(up_fg, len_menu_foreground, zip(menu_foreground,background))

def list_menu_generator(foreground, prompt = None, ngap = None, end = None):
    gap = ['']
    if prompt:
        if ngap:
            if end:
                return gap + [prompt] + ngap*gap + foreground + ngap*gap + [end] + gap
            return gap + [prompt] + ngap*gap + foreground + gap
        if end:
            return gap + [prompt] + gap + foreground + gap + [end] + gap
        return gap + [prompt] + gap + foreground + gap
    else:
        if end:
            if ngap:
                return gap + foreground + ngap*gap + [end] + gap
            return gap + foreground + gap + [end] + gap
        return gap + foreground + gap

def middle_line(col, string,  background = None,  width_menu = None, prefixe = None, suffixe = None, rolling = None):
    if width_menu:
        if string == '':
            foreground = ' '*width_menu
        else:
            temp = width_menu - len(string) + len_esc_str(string)  
            accu = temp%2
            colored_spaces_l = int((temp - accu)/2) 
            colored_spaces_r = temp - colored_spaces_l 
            if prefixe and suffixe: #width menu > len_foreground !!!!
                if not rolling:
                    foreground = prefixe + ' ' * colored_spaces_l + string + ' ' * colored_spaces_r + suffixe
                else:
                    foreground = prefixe + ' ' * (colored_spaces_l - 3) + '<  ' + string + '  >' + ' ' * (colored_spaces_r - 3) + suffixe
            else:
                foreground = ' ' * colored_spaces_l + string + ' ' * colored_spaces_r
    else:
        if prefixe and suffixe:
            foreground = prefixe + string + suffixe
        else:
            foreground = string 
    len_foreground = len(foreground) - len_esc_str(foreground)
    if len_foreground < col:
        if not background or len(background) <= len_foreground:
            temp = col - len_foreground
            accu = temp%2
            left_fg = int((temp - accu)/2) 
            return ' '*left_fg + foreground
        else:
            if len(background) < col:
                temp = col - len(background)
                accu = temp%2
                left_bg = int((temp - accu)/2) 
                temp2 = len(background) - len_foreground 
                accu2 = temp%2
                left_fg = int((temp2)/2)  
                right_fg = len_foreground + left_fg
                return' '*left_bg + ''.join(background[:left_fg]) +  foreground + ''.join(background[right_fg:])
            else:
                temp = len(background) - col
                accu = temp%2
                remove_l = int((temp - accu)/2 - accu)
                temp2 = col - len_foreground
                accu2 = temp2%2
                left_fg = int((temp2-accu2)/2) 
                remove_r = remove_l + len_foreground + left_fg
                right_fg = col - len_foreground - left_fg 
                return ''.join(background[remove_l:][:left_fg]) + foreground + ''.join(background[remove_r:][:right_fg])
    else:
        return foreground[:col]

def len_esc_str(string):
    counter = 0
    flag = 0
    for char in string:
        if char == '\x1b':
            flag = 1
        if flag == 1:
            counter += 1
        if flag == 1 and char == 'm':
            flag = 0
    return counter
