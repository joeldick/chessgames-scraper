import csv
import chess
import chess.pgn
import io

def get_pgn_moves(pgn):
    game = chess.pgn.read_game(io.StringIO(pgn))
    return [move.san() for move in game.mainline()]

def find_opening_from_pgn(pgn, openings_csv_path="eco-codes\opening_names_with_fen.csv"):
    pgn_moves = get_pgn_moves(pgn)
    best_match_len = 0
    best_name = ""

    # Load FENs from opening file into a dictionary
    fen_lookup = {}
    with open(openings_csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fen = row["fen"].strip()
            name = row["name"].strip()
            fen_lookup[fen] = name

    board = chess.Board()
    for i, move in enumerate(pgn_moves):
        try:
            board.push_san(move)
        except:
            break
        fen = board.board_fen()
        if fen in fen_lookup and i + 1 > best_match_len:
            best_match_len = i + 1
            best_name = fen_lookup[fen]

    return best_name or "Unknown Opening"


if __name__ == "__main__":
    pgn = "1.e4 e6 2.Nf3 Nf6 3.Nc3 Bb4 4.d4 c5 5.Bd3 cxd4 6.Nxd4 e5"

    print(find_opening_from_pgn(pgn))