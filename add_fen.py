import csv
import chess
import pandas as pd
import re

def get_fen_from_moves(move_str):
    # Strip move numbers like "1." or "23..."
    move_str = re.sub(r'\d+\.(\.\.)?', '', move_str)
    # Normalize whitespace
    move_str = re.sub(r'\s+', ' ', move_str).strip()

    board = chess.Board()
    for move in move_str.split():
        try:
            board.push_san(move)
        except:
            break
    return board.board_fen()

df = pd.read_csv("eco-codes/opening_names.csv")
df["fen"] = df["pgn"].apply(get_fen_from_moves)
df.to_csv("eco-codes/opening_names_with_fen.csv", index=False)
