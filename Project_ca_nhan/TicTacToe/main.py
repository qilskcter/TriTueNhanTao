import tkinter as tk
from tkinter import ttk
import math

from algorithms.utils import check_winner
from algorithms.minimax import minimax
from algorithms.alphabeta import alpha_beta
from algorithms.expectimax import expectimax

def get_best_move(board, algorithm):
    best_score = -math.inf
    best_move = None
    stats = {'nodes': 0}
    
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if algorithm == "Minimax":
                score = minimax(board, 0, False, stats)
            elif algorithm == "Alpha-Beta":
                score = alpha_beta(board, 0, -math.inf, math.inf, False, stats)
            elif algorithm == "Expectimax":
                score = expectimax(board, 0, False, stats)
            board[i] = ' '
            
            if score > best_score:
                best_score = score
                best_move = i
                
    return best_move, stats['nodes']

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        
        self.board = [' ' for _ in range(9)]
        
        self.setup_ui()
        self.log("Người chơi 'X' (Đi trước), AI là 'O'.\nChọn thuật toán và bắt đầu chơi.\n" + "-"*30)

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack()
        
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.grid(row=0, column=0, padx=10)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text=' ', font=('Consolas', 36, 'bold'), 
                            height=1, width=3, bg='#f0f0f0',
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)
            
        control_frame = tk.Frame(main_frame)
        control_frame.grid(row=0, column=1, padx=10, sticky="n")
        
        tk.Label(control_frame, text="Chọn thuật toán AI:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.algo_var = tk.StringVar(value="Alpha-Beta")
        self.algo_dropdown = ttk.Combobox(control_frame, textvariable=self.algo_var, state="readonly", width=25)
        self.algo_dropdown['values'] = ("Minimax", "Alpha-Beta", "Expectimax")
        self.algo_dropdown.pack(pady=5)
        
        tk.Button(control_frame, text="Làm mới bàn cờ", command=self.reset_game, bg='#d9d9d9').pack(fill="x", pady=10)
        
        tk.Label(control_frame, text="Console Logs:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.log_text = tk.Text(control_frame, height=14, width=40, state="disabled", bg='#1e1e1e', fg='#00ff00', font=('Consolas', 9))
        self.log_text.pack()

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        for btn in self.buttons:
            btn.config(text=' ', state="normal", bg='#f0f0f0')
        self.log("\n>>> BÀN CỜ ĐÃ ĐƯỢC LÀM MỚI <<<")

    def make_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = 'X'
            self.buttons[index].config(text='X', fg="blue")
            self.log(f"Người chơi (X) đánh ô: {index}")
            
            if self.check_game_over():
                return
                
            self.root.after(50, self.ai_move)

    def ai_move(self):
        algo = self.algo_var.get()
        self.log(f"AI đang phân tích bằng {algo}...")
        self.root.update()
        
        best_move, nodes_evaluated = get_best_move(self.board, algo)
        
        if best_move is not None:
            self.board[best_move] = 'O'
            self.buttons[best_move].config(text='O', fg="red")
            self.log(f"-> AI (O) chọn ô: {best_move}")
            self.log(f"-> Trạng thái đã duyệt: {nodes_evaluated} nodes.")
            self.log("-" * 30)
            self.check_game_over()

    def check_game_over(self):
        winner_score = check_winner(self.board)
        if winner_score == 10:
            self.log("KẾT QUẢ: AI THẮNG!")
            self.disable_board()
            return True
        elif winner_score == -10:
            self.log("KẾT QUẢ: BẠN THẮNG!")
            self.disable_board()
            return True
        elif winner_score == 0:
            self.log("KẾT QUẢ: HÒA!")
            self.disable_board()
            return True
        return False

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()