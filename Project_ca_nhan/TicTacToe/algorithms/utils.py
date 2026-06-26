def check_winner(board):
    win_states = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for state in win_states:
        if board[state[0]] == board[state[1]] == board[state[2]] and board[state[0]] != ' ':
            return 10 if board[state[0]] == 'O' else -10
    
    if ' ' not in board:
        return 0
    return None