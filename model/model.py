import numpy as np
from model.player import Player


class Game:
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size), dtype=np.int)
        self.curr_player = Player.X
        self.board[int(board_size/2), int(board_size/2)
                   ] = int(self.curr_player)
        self.board[int(board_size/2-1), int(board_size/2 -
                   1)] = int(self.curr_player)
        self.board[int(board_size/2), int(board_size/2-1)
                   ] = int(3-self.curr_player)
        self.board[int(board_size/2-1), int(board_size/2)
                   ] = int(3-self.curr_player)

    def is_legal_move(self, row, col):
        if row < 0 or row >= len(self.board):
            return False
        if col < 0 or col >= len(self.board):
            return False
        if row is None or col is None:
            return False
        if self.board[row, col] != 0:
            return False

        else:
            # Generating the list of neighbours
            neighbour = False
            neighbours = []
            for i in range(max(0, row-1), min(row+2, len(self.board))):
                for j in range(max(0, col-1), min(col+2, len(self.board))):
                    if self.board[i][j] != 0:
                        neighbour = True
                        neighbours.append([i, j])
            # If there's no neighbours, it's an invalid move
            if not neighbour:
                return False
            else:
                # Iterating through neighbours to determine if at least one line is formed
                valid = False
                for neighbour in neighbours:

                    neighX = neighbour[0]
                    neighY = neighbour[1]

                    # If the neighbour colour is equal to your colour, it doesn't form a line
                    # Go onto the next neighbour
                    if self.board[neighX][neighY] == self.curr_player:
                        continue
                    else:
                        # Determine the direction of the line
                        deltaX = neighX-row
                        deltaY = neighY-col
                        tempX = neighX
                        tempY = neighY

                        while 0 <= tempX < len(self.board) and 0 <= tempY < len(self.board):
                            # If an empty space, no line is formed
                            if self.board[tempX][tempY] == 0:
                                break
                            # If it reaches a piece of the player's colour, it forms a line
                            if self.board[tempX][tempY] == self.curr_player:
                                valid = True
                                break
                            # Move the index according to the direction of the line
                            tempX += deltaX
                            tempY += deltaY
                return valid

    def make_move(self, row, col):
        self.board[row, col] = int(self.curr_player)
        neighbours = []
        for i in range(max(0, row-1), min(row+2, len(self.board))):
            for j in range(max(0, col-1), min(col+2, len(self.board))):
                if self.board[i][j] != 0:
                    neighbours.append([i, j])

        # Which tiles to convert
        convert = []

        # For all the generated neighbours, determine if they form a line
        # If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
            neighX = neighbour[0]
            neighY = neighbour[1]
            # Check if the neighbour is of a different colour - it must be to form a line
            if self.board[neighX][neighY] != self.curr_player:
                # The path of each individual line
                path = []

                # Determining direction to move
                deltaX = neighX-row
                deltaY = neighY-col

                tempX = neighX
                tempY = neighY

                # While we are in the bounds of the board
                while 0 <= tempX < len(self.board) and 0 <= tempY < len(self.board):
                    path.append([tempX, tempY])
                    value = self.board[tempX][tempY]
                    # If we reach a blank tile, we're done and there's no line
                    if value == 0:
                        break
                    # If we reach a tile of the player's colour, a line is formed
                    if value == self.curr_player:
                        # Append all of our path nodes to the convert array
                        for node in path:
                            convert.append(node)
                        break
                    # Move the tile
                    tempX += deltaX
                    tempY += deltaY

        # Convert all the appropriate tiles
        for node in convert:
            self.board[node[0]][node[1]] = self.curr_player

    def is_game_terminated(self):
        return self.has_player_won() or self.is_board_full()

    def has_player_won(self):

        return False

    def is_board_full(self):
        return not np.any(self.board == 0)

    def change_turn(self):
        self.curr_player = Player(len(Player) + 1 - self.curr_player)

    def get_winner(self):
        if self.has_player_won():
            return self.curr_player
        else:
            return 0
