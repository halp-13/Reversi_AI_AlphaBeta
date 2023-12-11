# -*- coding: utf-8 -*-

''' Fichier de règles du Reversi 
    Certaines parties de ce code sont fortement inspirée de 
    https://inventwithpython.com/chapter15.html

    '''

class Board:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0

    # Attention, la taille du plateau est donnée en paramètre
    def __init__(self, boardsize = 8):
      self._nbWHITE = 2
      self._nbBLACK = 2
      self._nextPlayer = self._BLACK
      self._boardsize = boardsize
      self._board = []
      for x in range(self._boardsize):
          self._board.append([self._EMPTY]* self._boardsize)
      _middle = int(self._boardsize / 2)
      self._board[_middle-1][_middle-1] = self._BLACK 
      self._board[_middle-1][_middle] = self._WHITE
      self._board[_middle][_middle-1] = self._WHITE
      self._board[_middle][_middle] = self._BLACK 
      
      self._stack= []
      self._successivePass = 0

    def reset(self):
        self.__init__()

    # Donne la taille du plateau 
    def get_board_size(self):
        return self._boardsize

    # Donne le nombre de pieces de blanc et noir sur le plateau
    # sous forme de tuple (blancs, noirs) 
    # Peut être utilisé si le jeu est terminé pour déterminer le vainqueur
    def get_nb_pieces(self):
      return (self._nbWHITE, self._nbBLACK)

    # Vérifie si player a le droit de jouer en (x,y)
    def is_valid_move(self, player, x, y):
        if x == -1 and y == -1:
            return not self.at_least_one_legal_move(player)
        return self.lazyTest_ValidMove(player,x,y)

    def _isOnBoard(self,x,y):
        return x >= 0 and x < self._boardsize and y >= 0 and y < self._boardsize 

    # Renvoie la liste des pieces a retourner si le coup est valide
    # Sinon renvoie False
    # Ce code est très fortement inspiré de https://inventwithpython.com/chapter15.html
    # y faire référence dans tous les cas
    def testAndBuild_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        tilesToFlip = [] # Si au moins un coup est valide, on collecte ici toutes les pieces a retourner
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y):
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. Let's collect
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
    
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    # Pareil que ci-dessus mais ne revoie que vrai / faux (permet de tester plus rapidement)
    def lazyTest_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y): # On a au moins 
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. 
                    self._board[xstart][ystart] = self._EMPTY
                    return True
                 
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        return False

    def _flip(self, player):
        if player == self._BLACK:
            return self._WHITE 
        return self._BLACK

    def is_game_over(self):
        if self.at_least_one_legal_move(self._nextPlayer):
            return False
        if self.at_least_one_legal_move(self._flip(self._nextPlayer)):
            return False
        return True 

    def push(self, move):
        [player, x, y] = move
        assert player == self._nextPlayer
        if x==-1 and y==-1: # pass
            self._nextPlayer = self._flip(player)
            self._stack.append([move, self._successivePass, []])
            self._successivePass += 1
            return
        toflip = self.testAndBuild_ValidMove(player,x,y)
        self._stack.append([move, self._successivePass, toflip])
        self._successivePass = 0
        self._board[x][y] = player
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK += 1 + len(toflip)
            self._nbWHITE -= len(toflip)
            self._nextPlayer = self._WHITE
        else:
            self._nbWHITE += 1 + len(toflip)
            self._nbBLACK -= len(toflip)
            self._nextPlayer = self._BLACK

    def pop(self):
        [move, self._successivePass, toflip] = self._stack.pop()
        [player,x,y] = move
        self._nextPlayer = player 
        if len(toflip) == 0: # pass
            assert x == -1 and y == -1
            return
        self._board[x][y] = self._EMPTY
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK -= 1 + len(toflip)
            self._nbWHITE += len(toflip)
        else:
            self._nbWHITE -= 1 + len(toflip)
            self._nbBLACK += len(toflip)

    # Est-ce que on peut au moins jouer un coup ?
    # Note: cette info pourrait être codée plus efficacement
    def at_least_one_legal_move(self, player):
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(player, x, y):
                   return True
        return False

    # Renvoi la liste des coups possibles
    # Note: cette méthode pourrait être codée plus efficacement
    def legal_moves(self):
        moves = []
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(self._nextPlayer, x, y):
                    moves.append([self._nextPlayer,x,y])
        if len(moves) == 0:
            moves = [[self._nextPlayer, -1, -1]] # We shall pass
        return moves

    # Exemple d'heuristique tres simple : compte simplement les pieces
    def heuristique(self, player=None):
        if player is None:
            player = self._nextPlayer
        if player is self._WHITE:
            return self._nbWHITE - self._nbBLACK
        return self._nbBLACK - self._nbWHITE

    def get_board_size(self):
        return self._boardsize

    def _piece2str(self, c):
        if c==self._WHITE:
            return 'O'
        elif c==self._BLACK:
            return 'X'
        else:
            return '.'

    def __str__(self):
        toreturn=""
        for l in self._board:
            for c in l:
                toreturn += self._piece2str(c)
            toreturn += "\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        toreturn += "(successive pass: " + str(self._successivePass) + " )"
        return toreturn

    __repr__ = __str__

import time
import math
from copy import deepcopy
import sys


class KidAI:
    def __init__(self, player, time_limit=10):
        self.player = player
        #self.depth = depth
        self. time_limit= time_limit
        self.memoization_table = {}   #Mémoire pour la mémorisation (stockage des résultats précédents)

    def IAIterativeDeepening(self, board):
        start_time = time.time() 
        # Continuez à augmenter la profondeur jusqu'à atteindre la limite de temps
        
        for depth in range(1, sys.maxsize):
            
            best_move, _ = self.minimax(deepcopy(board), depth, -math.inf, math.inf, True)
            
            if (time.time() - start_time) >= self.time_limit:
                break
        return best_move

    def get_move(self, board):
        best_move = self.IAIterativeDeepening(board)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        #L'algorithme Minimax pour choisir le meilleur mouvement en tenant compte de la profondeur souhaitée
        if depth == 0 or board.is_game_over(): #Si la profondeur est égale à zéro ou si le jeu est terminé, il évalue l'état actuel
            return None, board.heuristique(self.player)

        board_tuple = tuple(tuple(row) for row in board._board)  #Conversion en Tuple pour le hachage
        if (depth, board_tuple) in self.memoization_table: #Si l'état actuel a déjà été calculé, le résultat mémorisé est récupéré
            return None, self.memoization_table[(depth, board_tuple)] 

        legal_moves = board.legal_moves()
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in legal_moves:
                board.push(move)
                _, eval = self.minimax(board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                board.pop()
                if beta <= alpha:
                    break
            self.memoization_table[(depth, board_tuple)] = max_eval
            return best_move, max_eval
        else:
            min_eval = math.inf
            best_move = None
            for move in legal_moves:
                board.push(move)
                _, eval = self.minimax(board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                board.pop()
                if beta <= alpha:
                    break
            self.memoization_table[(depth, board_tuple)] = min_eval
            return best_move, min_eval

    def evaluate(self, board):
        #Méthode pour évaluer l'état actuel du plateau de jeu et déterminer sa valeur
        num_white, num_black = board.get_nb_pieces()
        corners = [(0, 0), (0, board.get_board_size() - 1), (board.get_board_size() - 1, 0),
                   (board.get_board_size() - 1, board.get_board_size() - 1)]

        #Calcul de la valeur en fonction des caractéristiques
        score = 0
        for x in range(board.get_board_size()):
            for y in range(board.get_board_size()):
                if (x, y) in corners:
                    score += 3 * board._board[x][y]
                else:
                    score += board._board[x][y]

        #Nombre de disques
        score += 2 * (num_white - num_black)

        return score
class LazyAI:
    def __init__(self, player,time_limit=10 ):
        self.player = player
        #self.depth = depth
        self.time_limit= time_limit
        self.memoization_table = {}   #Mémoire pour la mémorisation (stockage des résultats précédents)
    def IAIterativeDeepening(self, board):
        start_time = time.time() 
        # Continuez à augmenter la profondeur jusqu'à atteindre la limite de temps
        
        for depth in range(1, sys.maxsize):
            
            best_move, _ = self.minimax(deepcopy(board), depth, -math.inf, math.inf, True)
            
            if (time.time() - start_time) >= self.time_limit:
                break
        return best_move

    def get_move(self, board):
        best_move = self.IAIterativeDeepening(board)
        return best_move
    '''def get_move(self, board):
        # Méthode qui prend un plateau de jeu en entrée et renvoie le meilleur mouvement possible
        best_move, _ = self.minimax(deepcopy(board), self.depth, -math.inf, math.inf, True)
        return best_move'''

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        #L'algorithme Minimax pour choisir le meilleur mouvement en tenant compte de la profondeur souhaitée
        if depth == 0 or board.is_game_over(): #Si la profondeur est égale à zéro ou si le jeu est terminé, il évalue l'état actuel
            return None, self.evaluate(board)

        board_tuple = tuple(tuple(row) for row in board._board)  #Conversion en Tuple pour le hachage
        if (depth, board_tuple) in self.memoization_table: #Si l'état actuel a déjà été calculé, le résultat mémorisé est récupéré
            return None, self.memoization_table[(depth, board_tuple)]

        legal_moves = board.legal_moves()
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in legal_moves:
                board.push(move)
                _, eval = self.minimax(board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                board.pop()
                if beta <= alpha:
                    break
            self.memoization_table[(depth, board_tuple)] = max_eval
            return best_move, max_eval
        else:
            min_eval = math.inf
            best_move = None
            for move in legal_moves:
                board.push(move)
                _, eval = self.minimax(board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                board.pop()
                if beta <= alpha:
                    break
            self.memoization_table[(depth, board_tuple)] = min_eval
            return best_move, min_eval

    def evaluate(self, board):
        #Méthode pour évaluer l'état actuel du plateau de jeu et déterminer sa valeur
        num_white, num_black = board.get_nb_pieces()
        corners = [(0, 0), (0, board.get_board_size() - 1), (board.get_board_size() - 1, 0),
                   (board.get_board_size() - 1, board.get_board_size() - 1)]

        #Calcul de la valeur en fonction des caractéristiques
        score = 0
        for x in range(board.get_board_size()):
            for y in range(board.get_board_size()):
                if (x, y) in corners:
                    score += 3 * board._board[x][y]
                else:
                    score += board._board[x][y]

        #Nombre de disques
        score += 2 * (num_white - num_black)

        return score
def human_player(board):
    print(board)
    
    
    boardsize=board.get_board_size()
    while True:
        
        a= False
        legal_moves = board.legal_moves()
        if not legal_moves:
            print("No legal moves available. Passing the turn.")
            a= True
            return [board._nextPlayer, -1, -1]
        if a == True:
            break
        try:
            x = int(input("Enter the row (0-9): "))
            y = int(input("Enter the column (0-9): "))
            if 0<=x<boardsize and 0<=y<boardsize:
                if board.is_valid_move(board._nextPlayer, x, y):
                    return [board._nextPlayer, x, y]
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_player_choice():
    while True:
        print("Choose:")
        print("1. Play with Kid AI")
        print("2. Play with Lazy AI")
        print("3. Watch the game between Kid AI and Lazy AI")
        choice = input("Enter the number of the option: ")
        validchoice=["1","2","3"]
        if choice in validchoice:
            break
    return choice

def play_game():
    choice = get_player_choice()

    board = Board(10)

    if choice == "1":
        # Game between Kid AI and human player
        ai_player = KidAI(board._nextPlayer)
        while not board.is_game_over():
            # Human player's turn
            human_move = human_player(board)
            board.push(human_move)

            if board.is_game_over():
                break

            # Kid AI's turn
            ai_move = ai_player.get_move(board)
            print("AI plays: ", ai_move[1], ai_move[2])
            board.push(ai_move)

    elif choice == "2":
        # Game between Lazy AI and human player
        ai_player = LazyAI(board._nextPlayer)
        while not board.is_game_over():
            # Human player's turn
            human_move = human_player(board)
            board.push(human_move)

            if board.is_game_over():
                break

            # Lazy AI's turn
            ai_move = ai_player.get_move(board)
            print("AI plays: ", ai_move[1], ai_move[2])
            board.push(ai_move)

    elif choice == "3":
        # Game between Kid AI and Lazy AI, human observes
        ai_player_kid = KidAI("BLACK")
        ai_player_lazy = LazyAI("WHITE")
        while not board.is_game_over():
            # Kid AI's turn
            ai_move_kid = ai_player_kid.get_move(board)
            print("AI Kid plays: ", ai_move_kid[1], ai_move_kid[2])
            board.push(ai_move_kid)
            print(board)

            if board.is_game_over():
                break

            # Lazy AI's turn
            ai_move_lazy = ai_player_lazy.get_move(board)
            print("AI Lazy plays: ", ai_move_lazy[1], ai_move_lazy[2])
            board.push(ai_move_lazy)
            print(board)

        return

    print("Game over!")
    print("Final board state:")
    print(board)
    print("Winner: ", "BLACK" if board._nbBLACK > board._nbWHITE else "WHITE")

if __name__ == "__main__":
    play_game()
