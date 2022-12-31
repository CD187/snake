'''this is a dictionnary for the menu in order to manage easily the languages'''

tree_menu  ={   'players' :     [('select player', 'new player'),
                                 ('choix du joueur','nouveau joueur')
                                ],
                'new_player':   ['write your name :', 
                                 'écris ton nom :'
                                ],
                'play' :        [['play','settings', 'change player', 'exit'], 
                                 ['jouer','réglages', 'changer de joueur', 'quitter']
                                ],
                'settings': {   'map' :[('size :', ['15x15', '20x20', '25x25', '35x25']),    
                                        ('taille :', ['15x15', '20x20', '25x25', '35x25'])],
                                'difficulty' :  [('difficulty :',['easy', 'medium', 'hard']),
                                                 ('difficulté :',['facile', 'moyen', 'difficile'])],
                                    
                                'border' : [('border :',['no','contour']),
                                            ('contour :',['sans','avec'])],

                                'snake_color': [('Snake color :', ['green', 'yellow', 'red', 'brown']),
                                                ('couleur de Snake :', ['vert','jaune','rouge','marron'])],

                                'background':[('background :',['yes', 'no']), ('arrière plan :',['sans','avec'])],
                                
                                'language':[('language :',['english','français']),
                                            ('language :',['english', 'français'])],
                            },
                'game_over':    [('GAME OVER !!!', 'your score :', 'your best score :'),
                                 ('PERDU !!!', 'ton score :', 'ton meilleur score :')]

            }


