from problem import Problem
from search import SearchStrategy
import os

def play(p: Problem, s: SearchStrategy):
    while True:
        user = input("Play as X or O: ")
        if user == "X":
            os.system('cls')
            print("You are X, PC is O\n")
            break
        elif user == "O":
            os.system('cls')
            print("You are O, PC is X\n")
            break
            
    p.print_board()
    ai_turn = False
    while True:
        game_over = p.terminal_test(p.get_board())
        player = p.player(p.get_board())
        if game_over:
            winner = p.winner(p.get_board())
            if winner is None:
                print("Game over: Tie")
                break
            else:
                print("Game over: ", winner, "win")
                break
        if user != player:
            if ai_turn:
                action = s.alpha_beta_search(p)
                p.set_move(action, player)
                os.system('cls')
                print("PC move: ", action, " \n")
                p.print_board()
            else:
                ai_turn = True
        else:
            p.player_move(user)
            os.system('cls')
            p.print_board()


p = Problem(8, 8)
s = SearchStrategy()
play(p, s)
