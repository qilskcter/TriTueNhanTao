import math
from algorithms.utils import check_winner

def alpha_beta(board, depth, alpha, beta, is_maximizing, stats):
    stats['nodes'] += 1
    score = check_winner(board)
    if score is not None:
        return score
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = alpha_beta(board, depth + 1, alpha, beta, False, stats)
                board[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = alpha_beta(board, depth + 1, alpha, beta, True, stats)
                board[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score