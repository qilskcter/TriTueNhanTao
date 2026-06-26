import math
from algorithms.utils import check_winner

def minimax(board, depth, is_maximizing, stats):
    stats['nodes'] += 1
    score = check_winner(board)
    if score is not None:
        return score
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False, stats)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True, stats)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score