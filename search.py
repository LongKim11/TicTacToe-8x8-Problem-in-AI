from problem import Problem

class SearchStrategy:
    
    def min_value(self, board, p: Problem, depth, alpha, beta):
        if p.terminal_test(board): 
            return p.utility(board), None
        
        if depth == 0:
            return p.evaluate_board(board), None

        v = float("inf")
        best_action = None
        for action in p.actions(board):
            max_val = self.max_value(p.result(board, action), p,  depth - 1, alpha, beta)[0] 
            if (max_val < v):
                v = max_val
                best_action = action
            if v <= alpha:
                return v, best_action
            beta = min(beta, v)
        return v, best_action


    def max_value(self, board, p: Problem, depth, alpha, beta):
        if p.terminal_test(board):
            return p.utility(board), None
    
        if depth == 0:
            return p.evaluate_board(board), None

        v = float("-inf")   
        best_action = None
        for action in p.actions(board):
            min_val = self.min_value(p.result(board, action), p, depth - 1, alpha, beta)[0]
            if (min_val > v):
                v = min_val
                best_action = action
            if v >= beta:
                return v, best_action
            alpha = max(alpha, v)
        return v, best_action
    
    def alpha_beta_search(self, p: Problem):
        board = p.get_board()
        depth = 2
        if p.player(board) == 'X':
            return self.max_value(board, p, depth, float("-inf"), float("inf"))[1]
        elif p.player(board) == 'O':
            return self.min_value(board, p, depth, float("-inf"), float("inf"))[1]
        return None
       
       
       