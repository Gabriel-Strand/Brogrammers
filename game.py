'''
Gabriel Strand
2023.10.16

ChangeLog:
    Cleaned up code
    Imported randint function
    Modified run_computer_turn function so that the computer doesn't always pick row 1 at the start
    Modified the print_board function to allow for any size board
    Removed the 'self.print_board(self.board)' line from the '__init__' method
    Added 'main()' function
'''
'''
TO DO LIST
    Improve AI by
        Making it not so slow past depth of 3
    Add 'Draw' Option to the check_for_winner function
        The simpler way to do this might be to track the number of turns taken vs total spaces on the board
        This is probably only important when *cough* sorry if I fix the ai
    Create a game GUI using tkinker
    Create Main Menu GUI:
    File IO for stat storage and accounts
    Use functions
'''

from copy import deepcopy
from random import randint

class Game:
    def __init__(self, w: int, h: int):
        '''Initalizes the game running variable, board variable, and prints the board'''
        self.running = True
        self.number_of_turns = 0

        self.width = w
        self.height = h
        #Width and Height are switched since we need to start with a rotated board
        self.board = [[0 for i in range(h)] for i in range(w)]

    def run_player_turn(self):
        '''Runs the code for the players turn'''
        #While it is the users turn, we want the user to input a row to play their piece,
        # However, we only want to accept movable spaces, which is what the if statement tests for
        user_turn = True
        while user_turn:
            num = int(input('Enter the row you would like to place your token in: ')) - 1
            if self.add_piece(1, num, self.board):
                user_turn = False
            else:
                print('That is not a valid option.')
        #Test to see if the player wins, if so, stop the game and say they won
        if self.test_for_winner(self.board, 1):
            print('\nPlayer 1 Wins')
            self.running = False

        self.number_of_turns += 1
    
    def run_ai_turn(self):
        '''Runs the code for the computers turn'''

        #Set a randomizer so that the first placement isn't in the far left row
        if self.number_of_turns < 2:
            lst = [randint(0,self.width)]
        else:
            #DO NOT SET THE DEPTH TO MORE THAN 3 IT WILL RUN SLOWLY
            lst = self.recursive_ai_functionality(self.board, 3)

        #This is just a fail safe that is in place until it is guareented that the recursive function won't fail
        #Note to future self: You NEED the self.add_piece function here WHETHER OR NOT it is being used in the if statement
        if not self.add_piece(2, lst[0], self.board):
            print('Issue. The Recursive Function is broken somehow')

        #Test to see if the computer wins, if so, stop the game and say they won
        if self.test_for_winner(self.board, 2):
            print('\nComputer Wins')
            self.running = False

        self.number_of_turns += 1

    def recursive_ai_functionality(self, board: list, depth: int) -> list:
        '''
        Takes elements board and list and returns a list as
            [Best row to play, score associated to that row]
        '''
        list_of_values = []
        for row in range(len(board)):
            cpy = deepcopy(board)

            #If you can't place a piece, we don't want to so give it a bad score a break out of the loop
            if not self.add_piece(2, row, cpy):
                list_of_values.append(-10 * depth)
            #If you can win, take it and don't bother calculating any other variations
            if self.test_for_winner(cpy, 2):
                list_of_values.append(3 * depth)
                break
            #If you can't win, but the depth is 1, don't bother trying to calculating futher
            elif depth == 1:
                list_of_values.append(1)
            #If you can't win and the depth isn't 1
            else:
                second_list_of_values = []
                is_there_winner = False
                for row2 in range(len(cpy)):
                    cpy2 = deepcopy(cpy)
                    add_piece_is = self.add_piece(1, row2, cpy2)
                    if add_piece_is and self.test_for_winner(cpy2, 1):
                        #Then assume that the player is smart and therefore putting your piece where you did was stupid
                        if not is_there_winner: #If statement only here so we don't print to list_of_values multiple times
                            list_of_values.append(-3 * depth)
                        #And break out of the loop
                        is_there_winner = True
                    elif add_piece_is:
                        lst = self.recursive_ai_functionality(cpy2, depth -1)
                        second_list_of_values.append(lst[1])
                if not is_there_winner:
                    list_of_values.append(max(second_list_of_values))
                
        #Return a list containing the row and the score that is the highest
        '''if depth == 3:
            print(list_of_values)'''
        return [list_of_values.index(max(list_of_values)), max(list_of_values)]

    def print_board(self, board: list):
        '''Takes the board, rotates it and prints'''
        #Flips to horizontal by taking the value in the length and putting it second so it is now height
        # and by taking the height value so that it will be the length meaning that
        #  the value in the top right will be in the bottom left
        new_board = [[board[height][length] for height in range(len(board))] for length in range(len(board[0]))]

        #Inverts so the pieces "fall" down instead of up
        another_one = [new_board[-i-1] for i in range(len(new_board))]
        
        num_of_dashes = '--' * self.width
        #Prints the board
        print(f'-{num_of_dashes}', end='')
        for row in another_one:
            print('\n|', end='')
            for num in row:
                if num == 0:
                    print(f' |', end='')
                else:
                    print(f'{num}|', end='')
        print(f'\n-{num_of_dashes}\n') 

    def add_piece(self, piece_value: int, row: int, board: list) -> bool:
        '''
        This function adds a given piece to the given row of the given board then applies gravity
        '''
        if piece_value > self.width:
            return False
        if board[row][-1] == 0:

            #This adds the piece to the last available spot in the row
            board[row][-1] = piece_value

            #this sorts the row so that all the zeros, or empty spots, appear at the end, creating "gravity"
            for row in board:
                for num in row:
                    if num == 0:
                        row.remove(num)
                        row.append(num)
            return True
        else: return False

    def test_for_winner(self, board: list, num: int) -> bool:
        '''This tests whether or not there is a winner on the board'''
        
        height = len(board)
        length = len(board[0])
        #This tests every up and down possiblity
        for x in range(height):
            for y in range(length - 3):
                if board[x][y] == num and board[x][y+1] == num and board[x][y+2] == num and board[x][y+3] == num:
                    return True
        #This tests every left to right possibility
        for x in range(height-3):
            for y in range(length):
                if board[x][y] == num and board[x+1][y] == num and board[x+2][y] == num and board[x+3][y] == num:
                    return True
        #This tests every bottom left to top right case
        for x in range(height - 3):
            for y in range(length - 3):
                if board[x][y] == num and board[x+1][y+1] == num and board[x+2][y+2] == num and board[x+3][y+3] == num:
                    return True
        #This tests every bottom right to top left case
        for x in range(3, height):
            for y in range(length - 3):
                if board[x][y] == num and board[x-1][y+1] == num and board[x-2][y+2] == num and board[x-3][y+3] == num:
                    return True
        #If a postitive win case wasn't found:
        return False

def main():
    #Create the 'Game' object 'g'
    g = Game(7, 6)
    g.print_board(g.board)
    #Set the turn to the user by default and start the main loop
    turn = 'user'
    while g.running:
        #Separate the User from the Computer
        if turn == 'user':
            g.run_player_turn()
            turn = 'computer'
        elif turn == 'computer':
            g.run_ai_turn()
            turn = 'user'
        #Rotate the board and then print it
        g.print_board(g.board)

if __name__ == "__main__":
    main()