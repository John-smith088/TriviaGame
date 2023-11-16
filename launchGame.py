from triviagameLib import *

#init the game board and start the menu loop
def start_trivia():
    screen, clock, screenSize = init_game_display() # returns list with screen sizes and clock
    main_menu(screen, clock, screenSize)
    return

#testing:
start_trivia()