#Project 1 CAP4630 Summer 2022
#Professor: Oge Marques PhD
#Topic: Checkers game
#Updated: 6-13-2022
#Updated by: Armando Arias-Castro
#Created by: Anak Wannaphaschaiyong
#Team members:
#Flor Aguirre Garcia - Documentation
#Joshua Gardner - Designer
#Armando Arias-Castro - Developer
#Github: https://github.com/faguirregarc2015/GroupAI

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from easyAI import solve_with_iterative_deepening
import numpy as np
from sys import exit
# black_square
even = [0,2,4,6]
odd = [1,3,5,7]

# init
even_row = [(i,j) for i in even for j in odd]
odd_row = [(i,j) for i in odd for j in even]

black_squares = even_row + odd_row

class Checker(TwoPlayerGame):
    
    def __init__(self, players):
        self.players = players
        # self.board = np.arange(8 * 8).reshape(8,8)
        self.blank_board = np.zeros((8,8), dtype=object)
        self.board = self.blank_board.copy()
        self.black_pieces = [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        self.white_pieces = [
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        for i,j in self.black_pieces:
            self.board[i,j] = "B"
        for i,j in self.white_pieces:
            self.board[i,j] = "W"

        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]


        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces

        self.current_player = 1  # player 1 starts.
        
    
    def possible_moves_on_white_turn(self):

        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move
        for i,j in old_new_piece_pos:
            #print(f"i = {i}")
            b = board.copy()
            b[i[0], i[1]] = 0 # old position
            b[j[0], j[1]] = "W" # new position
            # print(b)
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"


        self.board = board
        return table_pos

    def possible_moves_on_black_turn(self):
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move

        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos

    def possible_moves(self):
        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()
        print("In possible moves")

    def get_piece_pos_from_table(self, table_pos):
        if self.current_player-1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player-1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")

        assert len(np.where(table_pos != 0)[0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        return [(i,j) for i,j in zip(x[0], x[1])]
        

    def make_move(self, pos):
        """
        This function receives as parameter variable pos.
        Variable pos contains a board that shows a possible move.
        The function will extract a list with the position of all the pieces
        from pos using self.get_piece_pos_from_table(pos).
        After checking which player's turn it is to play,
        the list is assigned to them.
        Finally the board is updated using variable pos.
        The function returns the updated board
        """
        #Create a copy of the position array passed as parameter
        #It will be used to update the board at the end
        new_move = pos.copy()
        
        #Create a list with all the positions of the pieces
        #in the array pos passed as parameter
        lst = self.get_piece_pos_from_table(pos)
        
        #Check which player's turn it is to play
        #Player 0 is white pieces
        #Player 1 is black pieces
        #Assigned the list of position to the position array
        #of the corresponding player
        if self.current_player-1 == 0:
            self.players[0].pos = lst
            
        elif self.current_player-1 == 1:
            self.players[1].pos = lst
        
        #Update the board
        self.board = new_move.copy()
        
        #Return the updated board
        return self.board

    def lose(self):
        """
        Black lose if white piece is in black territory
        White lose if black piece is in white territory
        This function verifies if any white pieces are in black territory
        or any black pieces are in white territory.
        The function also checks if there are no possible moves.
        The function will return True or False.
        """
        #Check if there are any possible moves
        if self.possible_moves() == []:
            return True
        
        #Check if any white pieces are in black territory
        for i in self.black_territory:
            if i in self.players[0].pos:
                return True
            
        #Check if any black pieces are in white territory   
        for i in self.white_territory:
            if i in self.players[1].pos:
                return True
    
        #Return False if no player has won and there are possible moves
        return False
        

    def is_over(self):
        """
        Game is over immediately when one player get one of its piece into opponent's territory.
        This function calls function self.lose and return the same result.
        The function will return True or False.
        """
        return self.lose()


    def show(self):
        """
        show 8*8 checker board.
        """
        board = self.blank_board.copy()
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print('\n')
        print(board)
        self.is_over()#Check if any player won already
        
    def scoring(self):       
        """
        win = 0
        lose = -100
        This function returns 0 if the player won and -100 if the player lost
        This function calls function self.lose to check wether a player won or not
        """
        return -100 if self.lose() else 0
           
   
if __name__ == "__main__":
    ai = Negamax(1) # The AI will think 13 moves in advance
    game = Checker( [ AI_Player(ai), AI_Player(ai) ] )
    history = game.play()