from copy import deepcopy
from rich.table import Table
from rich.console import Console
from rich import box
from rich.style import Style
from rich.text import Text

class Problem:

    def __init__ (self, n, m):
        self.n = n
        self.m = m
        self.board = self.initial_state(n, m)

    def initial_state(self, n, m):
        board = [[0 for _ in range(m)] for _ in range(n)] 
        return board 

    def print_board(self):
        console = Console()
        table = Table(show_header=True, show_lines=True, title_style="bold white", title="Tic Tac Toe 8x8\n", show_edge=False, header_style=Style(color="cyan", bold=False), box=box.MINIMAL)

        # Add columns
        table.add_column(" ")
        for i in range(self.m):
            table.add_column(str(i))

        # Add rows
        for i in range(self.n):
            # * unpacks the list
            table.add_row(Text(str(i), style="cyan"), *[str(self.board[i][j]) if self.board[i][j] != 0 else " " for j in range(self.m)])

        console.print(table)
        console.print()
    

    def get_board(self):
        return self.board

    def get_vertical(self, board):
        result = []
        for i in range(self.m):
            for j in range(5):
                result.append([board[j][i], board[j + 1][i], board[j + 2][i], board[j + 3][i]])
        return result
    
    def get_horizontal(self, board):
        result = []
        for i in range(self.n):
            for j in range(5):
                result.append([board[i][j], board[i][j + 1], board[i][j + 2], board[i][j + 3]])
        return result
    
    def get_diagonal_helper(self, board): 
        n = len(board)
        diagonals_1 = []  # lower-left-to-upper-right diagonals
        diagonals_2 = []  # upper-left-to-lower-right diagonals
        for p in range(2 * n - 1):
            diagonals_1.append([board[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
            diagonals_2.append([board[n - p + q - 1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
        for _ in range(3):
            diagonals_1.pop()
            diagonals_1.pop(0)

            diagonals_2.pop()
            diagonals_2.pop(0) 

        return diagonals_1, diagonals_2

    def get_diagonal(self, board):
        d1, d2 = self.get_diagonal_helper(board)
        result = []
        for i in range(len(d1)):
            m = len(d1[i])
            for j in range(0, m - 3):
                result.append([d1[i][j], d1[i][j + 1], d1[i][j + 2], d1[i][j + 3]])
                result.append([d2[i][j], d2[i][j + 1], d2[i][j + 2], d2[i][j + 3]])
        return result
    
    def winner(self, board):
        conditions = self.get_vertical(board) + self.get_horizontal(board) + self.get_diagonal(board)
        if ['O', 'O', 'O', 'O'] in conditions:
            return 'O'
        if ['X', 'X', 'X', 'X'] in conditions:
            return 'X'
        return None
    
    def player(self, board):
        count_x = 0
        count_o = 0
        for i in board:
            for j in i:
                if(j == "X"):
                    count_x = count_x + 1
                if(j == "O"):
                    count_o= count_o + 1
        return "O" if count_x > count_o else "X"
    
    def actions(self, board):
        blank = []
        for x, row in enumerate(board):
            for y, _ in enumerate(row):
                if board[x][y] == 0:
                    blank.append([x, y])
        return blank

    def result(self, board, action):
        i, j = action
        if(board[i][j] != 0):
            raise Exception("Invalid Move")
        next_move = self.player(board)
        dc_board = deepcopy(board)
        dc_board[i][j] = next_move
        return dc_board

    def is_board_full(self, board):
        return len(self.actions(board)) == 0

    def terminal_test(self, board):
        if self.winner(board) != None or self.is_board_full(board):
            return True
        return False

    def utility(self, board):
        if self.winner(board) == 'X':
            return 200
        elif self.winner(board) == 'O':
            return -200
        return 0

    def evaluate_board(self, board):
        if self.winner(board) == 'X':
            return 200
        elif self.winner(board) == 'O':
            return -200

        x3 = 0
        x2 = 0
        x1 = 0
        o3 = 0
        o2 = 0
        o1 = 0
        conditions = self.get_vertical(board) + self.get_horizontal(board) + self.get_diagonal(board)
        for condition in conditions:
            if condition.count('X') == 1 and condition.count(0) == 3:
                x1 += 1
            elif condition.count('X') == 2 and condition.count(0) == 2:
                x2 += 1
            elif condition.count('X') == 3 and condition.count(0) == 1:
                x3 += 1
            elif condition.count('O') == 1 and condition.count(0) == 3:
                o1 += 1
            elif condition.count('O') == 2 and condition.count(0) == 2:
                o2 += 1
            elif condition.count('O') == 3 and condition.count(0) == 1:
                o3 += 1

        if self.player(board) == 'O':       
            x_score = 70 * x3  + 10 * x2 + x1 # Multiply by 80 < 100 to make O find his winning move instead of keeping blocking X
            o_score = 100 * o3 + 10 * o2 + o1
        else:
            x_score = 100 * x3 + 10 * x2 + x1
            o_score = 70 * o3 + 10 * o2 + o1

        # Substract the score too see which player takes more advantage
        return x_score - o_score 
   
    def set_move(self, action, player):
        i, j = action
        self.board[i][j] = player
    
    def player_move(self, player):
        while True:
            try:
                x, y = map(int, input("Enter your move: ").split())
                if self.board[x][y] != 0:
                    print('Your move is invalid, try again')
                else:
                    self.set_move((x, y), player)
                    break
            except ValueError:
                print('Invalid input, try again')





