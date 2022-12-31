'''this file is the dictionnaries for TUI rendering'''

colors_TUI =  { 
                'limits' : 15, 
                'empty' : 0,
                'apple' : 9,
                'bonus' : 4,
                'corps' : [46, 226, 160, 130],
                'corps_full' : [28, 214, 126, 88],
                'tails' : [10, 227, 196, 137], 
                'tails_full' : [28, 214, 126, 88],
                'heads' : [2, 220, 124, 94],
                'heads_full' : [22, 208, 88, 1]
              }

elements = { 1 : [colors_TUI['limits']], #limit
             0 : [colors_TUI['empty']],  #empty
             15: [colors_TUI['apple']],  #apple
             90: [colors_TUI['bonus']]   #extra
           }                        

#corps wrotten : new direction / old direction 
snake_el =  {'corps':  {'right':{   'right':{   3  : [colors_TUI['corps']],         #Right / Right  
                                                18 : [colors_TUI['corps_full']]     #Right / Right + 'apple'
                                            },
                                    'up':   {   4  : [colors_TUI['corps']],         #Right / Up
                                                19 : [colors_TUI['corps_full']]     #Right / Up + 'apple'
                                            },
                                    'down': {   5  : [colors_TUI['corps']],         #Right / Down
                                                20 : [colors_TUI['corps_full']]     #Right / Down + 'apple'                                       
                                            }
                                },
                        'left': {   'left': {   6  : [colors_TUI['corps']],         #Left / Left
                                                21 : [colors_TUI['corps_full']]     #Left / Left + 'apple'
                                            },
                                    'up':   {   7  : [colors_TUI['corps']],         #Left / Up
                                                22 : [colors_TUI['corps_full']]     #Left / Up + 'apple'
                                            },
                                    'down': {   8  : [colors_TUI['corps']],         #Left / Down
                                                23 : [colors_TUI['corps_full']]     #Left / Down + 'apple'
                                            }
                                },
                        'up':   {   'right':{   9  : [colors_TUI['corps']],         #Up / Right
                                                24 : [colors_TUI['corps_full']]     #Up / Right + 'apple'   
                                            },
                                    'left': {   10 : [colors_TUI['corps']],         #Up / Left
                                                25 : [colors_TUI['corps_full']]     #Up / Left + 'apple'
                                            },
                                    'up':   {   11 : [colors_TUI['corps']],         #Up / Up
                                                26 : [colors_TUI['corps_full']]     #Up / Up + 'apple'
                                            }
                                },
                        'down': {   'right':{   12 : [colors_TUI['corps']],         #Down / Right
                                                27 : [colors_TUI['corps_full']]     #Down / Right + 'apple'
                                            },
                                    'left': {   13 : [colors_TUI['corps']],         #Down / Left
                                                28 : [colors_TUI['corps_full']]     #Down / Left + 'apple'
                                            },
                                    'down': {   14 : [colors_TUI['corps']],         #Down / Down
                                                29 : [colors_TUI['corps_full']]     #Down / Down + 'apple'
                                            }                           
                                }   
                       }, 
             'tails':  {'right':{   'all':  {   30 : [colors_TUI['tails']],         #snake_tail right
                                                45 : [colors_TUI['tails_full']]     #snake_tail right + 'apple'
                                            },
                                },
                        'left': {   'all':  {   31 : [colors_TUI['tails']],         #snake_tail Left
                                                46 : [colors_TUI['tails_full']]     #snake_tail Left + 'apple'
                                            },
                                },
                        'up':   {   'all':  {   32 : [colors_TUI['tails']],         #snake_tail Up
                                                47 : [colors_TUI['tails_full']]     #snake_tail Up + 'apple'
                                            }, 
                                },
                        'down': {   'all':  {   33 : [colors_TUI['tails']],         #snake_tail Down
                                                48 : [colors_TUI['tails_full']]     #snake_tail Down + 'apple'
                                            }       
                                } 
                       },
             'heads':  {'right':{   'right':{   50 : [colors_TUI['heads']],         #snake_head Right / Right  
                                                65 : [colors_TUI['heads_full']]     #snake_head Right / Right + 'apple'
                                            },
                                    'up':   {   51 : [colors_TUI['heads']],         #snake_head Right / Up
                                                66 : [colors_TUI['heads_full']]     #snake_head Right / Up + 'apple'
                                            },
                                    'down': {   52 : [colors_TUI['heads']],         #snake_head Right / Down
                                                67 : [colors_TUI['heads_full']]     #snake_head Right / Down + 'apple'
                                            }
                                },
                        'left': {   'left': {   53 : [colors_TUI['heads']],         #snake_head Left / Left
                                                68 : [colors_TUI['heads_full']]     #snake_head Left / Left + 'apple'
                                            },
                                    'up':   {   54 : [colors_TUI['heads']],         #snake_head Left / Up
                                                69 : [colors_TUI['heads_full']]     #snake_head Left / Up + 'apple'
                                            },
                                    'down': {   55 : [colors_TUI['heads']],         #snake_head Left / Down
                                                70 : [colors_TUI['heads_full']]     #snake_head Left / Down + 'apple'
                                            }
                                },
                        'up':   {   'right':{   56 : [colors_TUI['heads']],         #snake_head Up / Right
                                                71 : [colors_TUI['heads_full']]     #snake_head Up / Right + 'apple'
                                            },
                                    'left': {   57 : [colors_TUI['heads']],         #snake_head Up / Left
                                                72 : [colors_TUI['heads_full']]     #snake_head Up / Left + 'apple'
                                            },
                                    'up':   {   58 : [colors_TUI['heads']],         #snake_head Up / Up
                                                73 : [colors_TUI['heads_full']]     #snake_head Up / Up + 'apple'
                                            }
                                },
                        'down': {   'right':{   59 : [colors_TUI['heads']],         #snake_head Down / Right
                                                74 : [colors_TUI['heads_full']]     #snake_head Down / Right + 'apple'
                                            },
                                    'left': {   60 : [colors_TUI['heads']],         #snake_head Down / Left
                                                75 : [colors_TUI['heads_full']]     #snake_head Down / Left + 'apple'
                                            },
                                    'down': {   61 : [colors_TUI['heads']],         #snake_head Down / Down
                                                76 : [colors_TUI['heads_full']],    #snake_head Down / Down + 'apple'
                                            }                           
                                }   
                       } 
            }

tree_directions = { 'right':['right','up','down'],
                    'left': ['left','up','down'],
                    'up':   ['up','left','right'],
                    'down': ['down','left','right']
                  }
