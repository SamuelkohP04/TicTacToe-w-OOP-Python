"""
Tic Tac Toe class + game play implementation by Kylie Ying
YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 

Modified by: Samuel Koh
"""
import math
import random

class Player():
    def __init__(self, letter, start_first):
        self.letter = letter
        self.start_first = start_first
        
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (1-9): ')
            try:
                val = int(square)
                val -= 1
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val



class AI():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        #if the AI starts first, it chooses a square at random
        
        if len(game.available_moves()) == 9:
            print('Since the AI is starting first, it moves at random, ')
            print('without assigning a score to its decision.')
            square = random.choice(game.available_moves())
        
        else:
            decision = self.minimax(game, self.letter)
            print('AI\'s best decision:', decision)
            square = decision['position']
            if decision['score'] > 0:
                print('Be careful! The AI thinks you will surely lose ',end='')
                moves = 9-len(game.used_moves())-decision['score']
                if moves > 0:
                    print(moves, 'turn(s) later. :(')
                else:
                    print('\nThe AI is going to win, and *DRUM ROLL*...')
            
        return square



    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 *
                    (state.num_empty_squares() + 1) if
                    other_player == max_player else -1 * 
                        (state.num_empty_squares() + 1)}
        
        #if AI is the max player,
        #it multiplies (+)1 by (empty sq + 1)
        
        #else if AI is the min player,
        #it multiplies (-)1 by (empty sq + 1)

        # else if there is no winner, the result is straight away 0.
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
            # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}
            # each score should minimize
            
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)
            # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

class TicTacToe():
    def __init__(self):
        self.board = [' ' for i in range(9)]
        self.current_winner = None

    
    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print()


    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        #print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        #print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ') #counts the no. of empties

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]
    
    def used_moves(self):
        return [i for i, x in enumerate(self.board) if x != " "]



def play(game, x_player, o_player, letter):
    game.print_board()

    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
            
        if game.make_move(square, letter):
            if letter == 'X':
                print('(AI) ',end='')
            print(letter + ' makes a move to square {}.\n'.format(square+1))
            game.print_board()
            print()

            if game.current_winner:
                if letter == 'X':
                    print('(AI) ',end='')
                print(letter + ' wins!')
                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switches player
            
    print('It\'s a tie!')

# Main code starts here:
# -------------------------------------------------------------------------
x_player = AI('X')
o_player = Player('O',False)
t = TicTacToe()
print('Welcome to TTT!')
print('This is how to input your numbers (positions):\n')

# 1 | 2 | 3
number_board = [[str(i+1) for i in range(j*3, (j+1)*3)] for j in range(3)]
for row in number_board:
    print('| ' + ' | '.join(row) + ' |')

print('\nNOTE: The AI will assign a score for its decision. \n'+
      'If score is a positive number, the AI is potentially winning. \n'+
      'If score is a negative number, you are potentially winning. ')
print('__________________________________________________________________\n')
      
while True:
    o_player.start_first = input('Would you like to go first? (Y/N): ')
    if o_player.start_first.upper() == 'Y':
        o_player.start_first = True
        break
    elif o_player.start_first.upper() == 'N':
        o_player.start_first = False
        break
    else:
        print('Invalid input, please answer correctly')
    
letter = 'O' if o_player.start_first else 'X'

play(t, x_player, o_player, letter)
choice = 'Anything you want'
while choice != None:
    choice = input('Another round? (Y/N): ')
    if choice.upper() == 'Y':
        t = TicTacToe()
        play(t, x_player, o_player, letter)
    elif choice.upper() == 'N':
        exit()
