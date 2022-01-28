import sys
import time
import gspread
from google.oauth2.service_account import Credentials
from email_validator import validate_email, EmailNotValidError
from colorama import init
import os

# Initializes Colorama
init(autoreset=True)

# Scope and constant vars defined as in love_sandwiches walk-through project
# by Code Institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# My updated values
SHEET = GSPREAD_CLIENT.open('connect4_database')
PLAYERS_WORKSHEET = SHEET.worksheet("Players")

# Text colors
YELLOW = "\033[1;33;48m"
RED = "\033[1;31;48m"
GREEN = "\033[1;32;48m"
BLUE = "\033[1;34;48m"
LOGO_Y = "\033[0;33;48m"
LOGO_R = "\033[0;31;48m"


def welcome():
    """
    Add welcome page
    Display game name and author
    """
    print(LOGO_Y + "  ____                                   _       ___ ")
    print(LOGO_Y + " / __ \                                 | |     /   |")
    print(LOGO_Y + "| /  \/  ___   _ __   _ __    ___   ___ | |_   / /| |")
    print(LOGO_R + "| |     / _ \ |  _ \ |  _ \  / _ \ / __|| __| / /_| |")
    print(LOGO_R + "| \__/\| (_) || | | || | | ||  __/| (__ | |_  \___  |")
    print(LOGO_Y + " \____/ \___/ |_| |_||_| |_| \___| \___| \__|     |_|")
    print(" ")
    print(" ")
    time.sleep(1)
    print(BLUE + "\u0332".join("Game Rules:"))
    print("The objective of the game is to be the first one to put four " +
          "of your pieces")
    print("which fall into columns next to each other in a row")
    print("either horizontally --, vertically | or diagonally / \.")
    print("Each column is numbered and you need to enter a column number")
    print("in which you want to drop your piece.")
    print("Good luck and enjoy!!!")
    print(" ")
    print(" ")


def select_game():
    """
    The program will first show two possible options of the game
    User can select a game for either 2 or 1 player
    """
    time.sleep(1)
    print(GREEN + "Select game option:")
    game_options = "1) 2 Players \n2) Player vs. Computer\n"
    game_selected = input(game_options)
    separate_line()

    # Validate if answer is either 1 or 2
    while game_selected not in ("1", "2"):
        print(GREEN + "Please choose between one of the two options:")
        game_selected = input(game_options)

        separate_line()

    if game_selected == "1":
        print(BLUE + "2 players game selected\n")
        get_players_names()

    elif game_selected == "2":
        print(BLUE + "Player vs computer game selected\n")
        login_or_register()

    return game_selected


def separate_line():
    """
    Print '-' lines to separate messages
    """
    print(" ")
    print("- "*30)
    print(" ")


def get_players_names():  # Option for 2 players game
    """
    Players can enter their names
    """
    while True:
        global player1name
        player1name = input("Please enter Player1 name:\n")

        if validate_username(player1name):
            time.sleep(1)
            print(BLUE + f"Hello {player1name}!\n")
            break

    while True:
        global player2name
        player2name = input("Please enter Player2 name:\n")

        if validate_username(player2name):
            time.sleep(1)
            print(BLUE + f"Hello {player2name}!")
            break

    time.sleep(1)
    separate_line()
    print(GREEN + "Are you ready?")
    print(RED + f"{player1name}" + GREEN + " & " + YELLOW + f"{player2name}")
    print(GREEN + "Let's play the game!")
    separate_line()
    time.sleep(2)
    cls()
    run_game()  # Game for 2 players


def cls():
    """
    Clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")


def validate_username(playername):
    """
    Validation if the user name input meets the criteria
    It should be between 2 - 12 long using only A-Z
    """
    if len(playername) < 2 or len(playername) > 12:
        print(RED + "\nPlayer name must be between 2 - 12 characters long.")
        print(RED + "Please try again.\n")

    elif not playername.isalpha():
        print(RED + "\nPlayer name must only contain A-Z. Please try again.\n")

    else:
        return True


# Option for 1 player game
def login_or_register():
    """
    Player has an option to either log in to an exisiting account
    or register a new user
    """
    time.sleep(1)
    print(GREEN + "Would you like to:")
    options = "1) Log in\n2) Create a new player\n"
    selected_option = input(options)
    separate_line()

    # Validate if answers is either 1 or 2
    while selected_option not in ("1", "2"):
        print(GREEN + "Please choose between one of the two options:")
        selected_option = input(options)

        separate_line()

    if selected_option == "1":
        time.sleep(1)
        log_in_player()

    elif selected_option == "2":
        time.sleep(1)
        register_new_player()


def log_in_player():
    """
    User can log in to existing account
    """
    print(BLUE + "Welcome back! Please help me verify your login details.")

    while True:
        email = get_email()
        existing_player = is_player_registered(email)

        if existing_player:
            email_row = PLAYERS_WORKSHEET.find(email).row
            global old_player_name
            old_player_name = PLAYERS_WORKSHEET.row_values(email_row)[0]
            start_game_message(old_player_name)
            
            # Add function to start the game for this player
            break

        else:
            print(RED + "\nSorry, this email is not registered.\n")
            selected_option = email_not_registered()

            if selected_option == "1":
                print("Please write your email again:")

            elif selected_option == "2":
                register_new_player()
                break


def get_email():
    """
    Ask user to input their email address
    """
    while True:
        email = input("What's your email address?\n").strip()

        if validate_user_email(email):
            break

    return email


def validate_user_email(email):
    """
    Validate the email address.
    It must be of the form name@example.com
    """
    try:
        validate_email(email)
        return True

    except EmailNotValidError as e:
        print(RED + "\n" + str(e) )
        print(RED + "Please try again.\n")


def is_player_registered(email):
    """
    Verify if the player is registered
    by checking if email exists in the database
    """
    email_column = PLAYERS_WORKSHEET.col_values(2)
    
    if email in email_column:
        return True
    else:
        return False


def email_not_registered():
    """
    Called when the email is not registered on the worksheet/database
    Give user an option to enter another email or create a new user
    """
    time.sleep(1)
    print(GREEN + "Would you like to:")
    options = "1) Try another email\n2) Create a new player\n"
    selected_option = input(options)
    separate_line()

    while selected_option not in ("1", "2"):
        print("Please choose between one of the options:")
        selected_option = input(options)

        separate_line()

    return selected_option


def register_new_player():
    """
    Register a new player
    """
    player_info = create_new_player()
    update_players_worksheet(player_info)


def create_new_player():
    """
    Create a new player
    Get player's name and email
    Check if email is already in the database
    """
    time.sleep(1)
    print(BLUE + "Creating a new player...")

    email_column = PLAYERS_WORKSHEET.col_values(2)

    while True:
        global new_player_name
        new_player_name = input("What's your name?\n")
        print(" ")

        if validate_username(new_player_name):
            break

    while True:
        email = get_email()

        # Verify if email is already in use
        if email not in email_column:
            break

        else:
            print(RED + f"\nSorry {new_player_name}, this email is already used.")
            print(RED + "Please try another email.\n")

    return [new_player_name, email]


def update_players_worksheet(data):
    """
    Update players worksheet, add a new row with the player's data provided
    """
    PLAYERS_WORKSHEET.append_row(data)
    print(BLUE + f"\nThanks {new_player_name}, your details have been registered!")
    start_game_message(new_player_name)


def start_game_message(player_name):
    time.sleep(1)
    separate_line()
    print(RED + f"{player_name}" + GREEN + ", are you ready?")
    print(GREEN + "Let's play the game!")
    separate_line()
    time.sleep(2)
    # cls()


BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class Board():
    def __init__(self):
        self.board = [[' ' for x in range(BOARD_WIDTH)]
                      for y in range(BOARD_HEIGHT)]
        self.moves = 0
        self.last_move = [-1, -1]  # Coordinates outside of the board

    def display_board(self):
        """
        Display a game board of 7 columns and 6 rows
        Dimensions specified in the constant variable
        """
        print(" ")
        for row in range(0, BOARD_HEIGHT):
            print(BLUE + '|', end="")
            for col in range(0, BOARD_WIDTH):
                print(f"  {self.board[row][col]}" + BLUE + "  |", end="")
            print("\n")

        print(BLUE + " -"*21)

        # Display number of columns on the board
        for row in range(BOARD_WIDTH):
            print(BLUE + f"   {row+1}  ", end="")
        print("\n")

    def whos_move(self):
        """
        Alternate moves between player 1 and 2
        """
        pieces = ['X', 'O']
        return pieces[self.moves % 2]

    def move(self, column):
        """
        Look for the first available slot in the column
        and place current player's piece in that space
        """
        for row in range(BOARD_HEIGHT-1, -1, -1):
            # If the space has not been filled in yet
            if self.board[row][column] == ' ':
                # Display pieces in different colors on the board
                if self.whos_move() == 'X':
                    self.board[row][column] = RED + self.whos_move()
                else:
                    self.board[row][column] = YELLOW + self.whos_move()

                self.last_move = [row, column]
                self.moves += 1
                return True

        # If there is no available space in the column
        print(RED + "You cannot put a piece in the full column.")
        print("Please choose another column.\n")
        return False

    def winning_move(self):
        """
        Check for 4 pieces in a row
        either horizontally, vertically or diagonally
        """
        last_row = self.last_move[0]
        last_col = self.last_move[1]
        last_move = self.board[last_row][last_col]  # Either 'X' or 'O'

        # Check horizontal lines for win
        def horizontal_win():
            for row in range(0, BOARD_HEIGHT):
                # Subtracting 3 as impossible to connect 4 from [row, col > 3]
                for col in range(0, (BOARD_WIDTH - 3)):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row][col+1]):
                        if(last_move == self.board[row][col+2] and
                           last_move == self.board[row][col+3]):
                            return True
            return False

        # Check vertical lines for win
        def vertical_win():
            # Subtracting 3 as impossible to connect 4 from [row < 3 , col]
            for row in range(0, (BOARD_HEIGHT-3)):
                for col in range(0, BOARD_WIDTH):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row+1][col]):
                        if(last_move == self.board[row+2][col] and
                           last_move == self.board[row+3][col]):
                            return True
            return False

        # Check diagonal lines for win going up and to the right
        def diagonal_win():
            for row in range(3, BOARD_HEIGHT):
                # Possible to connect 4 starting at [row >= 3 & col =< 3]
                for col in range(0, (BOARD_WIDTH-3)):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row-1][col+1]):
                        if(last_move == self.board[row-2][col+2] and
                           last_move == self.board[row-3][col+3]):
                            return True

            # Check diagonal lines for win going down and to the right
            # Possible to connect 4 starting at [row < 3 & col =< 3]
            for row in range(0, (BOARD_HEIGHT-3)):
                for col in range(0, (BOARD_WIDTH-3)):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row+1][col+1]):
                        if(last_move == self.board[row+2][col+2] and
                           last_move == self.board[row+3][col+3]):
                            return True

            return False  # If there is no winner

        if horizontal_win() or vertical_win() or diagonal_win():
            cls()
            self.display_board()
            if last_move == RED + 'X':
                print(GREEN + "\n----> " +
                      f"{player1name.upper()}" + " is the winner <----\n")
            else:
                print(GREEN + "\n----> " +
                      f"{player2name.upper()}" + " is the winner <----\n")

            time.sleep(2)
            separate_line()
            play_again()

        return False  # If there are no winners


def run_game():
    """
    Start the game once both players have validated their names
    """
    game = Board()

    game_won = False

    while not game_won:
        # If the game continues and there is no winner
        cls()
        game.display_board()

        is_move_valid = False

        while not is_move_valid:
            if game.whos_move() == 'X':
                print(f"{player1name}'s move. You play with " + RED + "X")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")
            else:
                print(f"{player2name}'s move. You play with " + YELLOW + "O")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")

            # if player types invalid input
            try:
                is_move_valid = game.move(int(player_move)-1)
            except:
                print(RED + f"Please choose a column 1 - {BOARD_WIDTH}.\n")

        # The game is over when the last move connects 4 pieces
        game_won = game.winning_move()

        # The game is over if there is a tie
        if game.moves == BOARD_HEIGHT * BOARD_WIDTH:
            cls()
            game.display_board()
            print(GREEN + "\n----> The game is over - it's a tie! <----\n")

            time.sleep(2)
            separate_line()
            play_again()


def play_again():
    """
    Give players an option to carry on playing with same players names
    go back to the main menu or exit the game
    """
    print(GREEN + "What would you like to do:")
    options = "1) Play again\n2) Go to main menu\n3) Quit game\n"
    selected = input(options)
    separate_line()

    # Validate if answer is either 1 or 2 or 3
    while selected not in ("1", "2", "3"):
        print(GREEN + "Please choose between one of below options:")
        selected = input(options)

        separate_line()

    if selected == "1":
        print(BLUE + "Starting a new game for " +
              f"{player1name} & {player2name}!\n")
        time.sleep(2)
        run_game()

    elif selected == "2":
        time.sleep(1)
        cls()
        main()

    elif selected == "3":
        print(BLUE + "Thanks for playing! See you soon!\n")
        sys.exit()


def main():
    """
    Run all program functions
    """
    welcome()
    select_game()

if __name__ == "__main__":
    main()
