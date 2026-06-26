import math
from algorithms.utils import check_winner

def expectimax(board, depth, is_maximizing, stats):
    stats['nodes'] += 1
    score = check_winner(board)
    if score is not None:
        return score
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = expectimax(board, depth + 1, False, stats)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        empty_cells = [i for i, x in enumerate(board) if x == ' ']
        total_score = 0
        for i in empty_cells:
            board[i] = 'X'
            score = expectimax(board, depth + 1, True, stats)
            board[i] = ' '
            total_score += score
        return total_score / len(empty_cells)