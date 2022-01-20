import time

def welcome():
    """
    Add welcome page
    Display game name and author
    """
print(" ")
print(" ")
print(" _____                                   _        ___ ")
print("/  __ \                                 | |      /   |")
print("| /  \/  ___   _ __   _ __    ___   ___ | |_    / /| |")
print("| |     / _ \ |  _ \ |  _ \  / _ \ / __|| __|  / /_| |")
print("| \__/\| (_) || | | || | | ||  __/| (__ | |_   \___  |")
print(" \____/ \___/ |_| |_||_| |_| \___| \___| \__|      |_/")
print(" ")
print("           Created by Aleksandra H.")
print(" ")
print(" ")
print("Game Rules:")
print("The objective of the game is to be the first one to put four of your pieces which fall into columns next to each other in a row either horizontally, vertically or diagonally.")
print("Each column is numbered and you need to enter a column number in which you want to drop your piece.")
print("Good luck and enjoy!!!")
print(" ")

def select_game():
    """
    the program will first show two possible options
    user can select a game for either 2 or 1 player
    """
    print("Select game option:")
    game_options = "1) 2 Players \n2) Player vs. Computer\n"
    game_selected = input(game_options)
    separate_line()

    if game_selected == "1":
        print("2 players game selected")
        print(" ")
        get_players_names()

    elif game_selected == "2":
        print("Player vs computer")
        print(" ")
        # Add function for a game with computer

    # Validate if answers is either 1 or 2    
    while game_selected not in ("1", "2"):
        print("Please choose between one of the options.")
        game_selected = input(game_options)

        separate_line()

    return game_selected


def separate_line():
    """
    Print a - line to end the sections
    """
    print(" ")
    print("- "*20)
    print(" ")



def main():
    """
    Run all program functions
    """
    welcome()
    select_game()

if __name__ == "__main__":
    main()