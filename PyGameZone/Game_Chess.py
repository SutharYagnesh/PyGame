import Game_Chess
# import chess.engine
import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# --------------------------- Chess Game Class ---------------------------
class AIChess:
    def __init__(self):
        # self.board = chess.Board()
        self.undo_stack = []  # Stack for Undo
        self.redo_stack = []  # Stack for Redo
        # self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")  # AI Chess Engine

    def make_ai_move(self):
        """AI selects the best move"""
        result = self.engine.play(self.board, Game_Chess.engine.Limit(time=0.1))
        self.undo_stack.append(self.board.fen())  # Save state for undo
        self.board.push(result.move)

    def player_move(self, move):
        """Player makes a move"""
        if Game_Chess.Move.from_uci(move) in self.board.legal_moves:
            self.undo_stack.append(self.board.fen())  # Save state for undo
            self.board.push(Game_Chess.Move.from_uci(move))
        else:
            print("Invalid move!")

    def undo(self):
        """Undo last move"""
        if self.undo_stack:
            self.redo_stack.append(self.board.fen())  # Save for redo
            last_state = self.undo_stack.pop()
            self.board.set_fen(last_state)
        else:
            print("No moves to undo.")

    def redo(self):
        """Redo last undone move"""
        if self.redo_stack:
            self.undo_stack.append(self.board.fen())  # Save for undo
            last_state = self.redo_stack.pop()
            self.board.set_fen(last_state)
        else:
            print("No moves to redo.")

    # def display_board(self):
    #     """Display board in CMD"""
    #     print(self.board)

    def close_engine(self):
        """Close chess engine"""
        self.engine.quit()

# --------------------------- Database Class ---------------------------
class ChessDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ChessGame"
        )
        self.cursor = self.conn.cursor()

    def add_player(self, username):
        """Add new player"""
        self.cursor.execute("INSERT INTO Players (username) VALUES (%s)", (username,))
        self.conn.commit()

    def save_match(self, player_id, moves, winner):
        """Save match details"""
        self.cursor.execute("INSERT INTO Matches (player_id, moves, winner) VALUES (%s, %s, %s)",
                            (player_id, moves, winner))
        self.conn.commit()

    def get_leaderboard(self):
        """Fetch top players"""
        self.cursor.execute("SELECT username, rating FROM Players ORDER BY rating DESC")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# --------------------------- PDF Report Class ---------------------------
class ChessReport:
    def generate_report(self, username, games_played, win_rate):
        """Generate PDF Report"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, f"Chess Report for {username}", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Games Played: {games_played}", ln=True)
        pdf.cell(200, 10, f"Win Rate: {win_rate}%", ln=True)

        pdf.output(f"{username}_chess_report.pdf")

# --------------------------- Data Analytics Class ---------------------------
class ChessAnalytics:
    def __init__(self):
        self.db = ChessDatabase()
        self.df = pd.read_sql("SELECT * FROM Matches", self.db.conn)

    def plot_win_rate(self):
        """Plot player win rates"""
        win_rates = self.df['winner'].value_counts(normalize=True) * 100
        win_rates.plot(kind='bar', color=['blue', 'green'])
        plt.title("Win Rate of Players")
        plt.xlabel("Players")
        plt.ylabel("Win Percentage")
        plt.show()

# --------------------------- File Handling Class ---------------------------
class ChessFileHandler:
    def save_match(self, filename, moves):
        """Save match moves to a file"""
        with open(filename, "w") as file:
            file.write("\n".join(moves))

    def load_match(self, filename):
        """Load match moves from a file"""
        with open(filename, "r") as file:
            moves = file.readlines()
        return [move.strip() for move in moves]

# --------------------------- Main Game Loop ---------------------------
def main():
    game = AIChess()

    print("Welcome to AI Chess Game!")
    print("Commands: 'move e2e4' | 'undo' | 'redo' | 'ai' | 'exit'\n")
    
    while not game.board.is_game_over():
        # game.display_board()
        command = input("\nEnter your move: ").strip().lower()
        
        if command == "exit":
            break
        elif command.startswith("move "):
            move = command.split(" ")[1]
            game.player_move(move)
        elif command == "undo":
            game.undo()
        elif command == "redo":
            game.redo()
        elif command == "ai":
            game.make_ai_move()
        else:
            print("Invalid command.")

    print("\nGame Over!")
    game.display_board()
    game.close_engine()

if __name__ == "__main__":
    main()
