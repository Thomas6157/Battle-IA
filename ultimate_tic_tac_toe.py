import random
import time

EMPTY = 0
X = 1
O = -1
DRAW = 2
ONGOING = 0


class GameState:
    def __init__(self):
        self.board = [[EMPTY for _ in range(9)] for _ in range(9)]
        self.small_status = [ONGOING for _ in range(9)]
        self.current_player = X
        self.next_board = -1
        self.last_move = None

    def small_board_index(self, row, col):
        return (row // 3) * 3 + (col // 3)

    def cell_index_inside_small_board(self, row, col):
        return (row % 3) * 3 + (col % 3)

    def get_legal_moves(self):
        moves = []

        if self.next_board != -1 and self.small_status[self.next_board] == ONGOING:
            start_row = (self.next_board // 3) * 3
            start_col = (self.next_board % 3) * 3

            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    if self.board[r][c] == EMPTY:
                        moves.append((r, c))

            return moves

        for r in range(9):
            for c in range(9):
                board_id = self.small_board_index(r, c)
                if self.board[r][c] == EMPTY and self.small_status[board_id] == ONGOING:
                    moves.append((r, c))

        return moves

    def play_move(self, move):
        row, col = move

        if move not in self.get_legal_moves():
            raise ValueError(f"Coup illegal : {move}")

        self.board[row][col] = self.current_player
        self.last_move = move

        board_id = self.small_board_index(row, col)
        self.small_status[board_id] = self.check_small_board(board_id)

        next_board = self.cell_index_inside_small_board(row, col)

        if self.small_status[next_board] == ONGOING:
            self.next_board = next_board
        else:
            self.next_board = -1

        self.current_player *= -1

    def check_small_board(self, board_id):
        start_row = (board_id // 3) * 3
        start_col = (board_id % 3) * 3

        cells = []
        for r in range(start_row, start_row + 3):
            row = []
            for c in range(start_col, start_col + 3):
                row.append(self.board[r][c])
            cells.append(row)

        lines = []

        for i in range(3):
            lines.append(cells[i])
            lines.append([cells[0][i], cells[1][i], cells[2][i]])

        lines.append([cells[0][0], cells[1][1], cells[2][2]])
        lines.append([cells[0][2], cells[1][1], cells[2][0]])

        for line in lines:
            s = sum(line)
            if s == 3:
                return X
            if s == -3:
                return O

        for r in range(3):
            for c in range(3):
                if cells[r][c] == EMPTY:
                    return ONGOING

        return DRAW

    def check_global_winner(self):
        b = self.small_status

        winning_lines = WINNING_LINES

        for line in winning_lines:
            values = [b[i] for i in line]
            if values == [X, X, X]:
                return X
            if values == [O, O, O]:
                return O

        if all(status != ONGOING for status in b):
            return DRAW

        return ONGOING

    def is_terminal(self):
        return self.check_global_winner() != ONGOING

    def display(self):
        symbols = {
            EMPTY: ".",
            X: "X",
            O: "O"
        }

        print("\n   1 2 3   4 5 6   7 8 9")

        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("   ------+-------+------")

            row_display = str(r + 1) + "  "

            for c in range(9):
                if c % 3 == 0 and c != 0:
                    row_display += "| "

                row_display += symbols[self.board[r][c]] + " "

            print(row_display)

        print()

        if self.next_board == -1:
            print("Prochain joueur peut jouer partout")
        else:
            print(f"Prochain joueur doit jouer dans le mini-board {self.next_board + 1}")


        self.display_big_board()
    

    def display_big_board(self):
        symbols = {
            ONGOING: ".",
            DRAW: "N",
            X: "X",
            O: "O"
        }

        print("\nGrand plateau :")
        for r in range(3):
            row_display = ""
            for c in range(3):
                board_id = r * 3 + c
                row_display += symbols[self.small_status[board_id]] + " "
            print(row_display)
        print()

    def undo_move(self, move, previous_next_board, previous_small_status, previous_last_move):
        row, col = move

        self.current_player *= -1
        self.board[row][col] = EMPTY
        self.next_board = previous_next_board
        self.small_status = previous_small_status[:]
        self.last_move = previous_last_move




WINNING_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]


def human_vs_ai():
    game = GameState()

    choix = input("Qui commence ? 1 = joueur, 2 = IA : ")

    if choix == "1":
        game.current_player = X
    else:
        game.current_player = O

    while not game.is_terminal():
        game.display()

        if game.current_player == X:
            print("Tour du joueur humain (X)")

            try:
                col = int(input("Colonne (1-9) : ")) - 1
                row = int(input("Ligne (1-9) : ")) - 1

                if row < 0 or row > 8 or col < 0 or col > 8:
                    raise IndexError

                print(f"Joueur joue : colonne {col + 1}, ligne {row + 1}")
                game.play_move((row, col))

            except ValueError as e:
                print("Erreur :", e)
            except IndexError:
                print("Erreur : entre une colonne et une ligne entre 1 et 9")

        else:
            print("Tour de l'IA Minimax (O)")

            start_time = time.perf_counter()
            move = minimax_bot(game, depth=6)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time

            row, col = move
            print(f"IA joue : colonne {col + 1}, ligne {row + 1}")
            print(f"Temps de réflexion de l'IA : {elapsed_time:.3f} secondes")

            game.play_move(move)

    game.display()

    winner = game.check_global_winner()

    if winner == X:
        print("Humain gagne")
    elif winner == O:
        print("IA gagne")
    else:
        print("Match nul")



def evaluate_line(values):
    x_count = values.count(X)
    o_count = values.count(O)
    empty_count = values.count(EMPTY)

    if x_count > 0 and o_count > 0:
        return 0

    if x_count == 3:
        return 100
    if x_count == 2 and empty_count == 1:
        return 10
    if x_count == 1 and empty_count == 2:
        return 1

    if o_count == 3:
        return -100
    if o_count == 2 and empty_count == 1:
        return -10
    if o_count == 1 and empty_count == 2:
        return -1

    return 0


def evaluate_small_board(game, board_id):
    status = game.small_status[board_id]

    if status == X:
        return 300
    if status == O:
        return -300
    if status == DRAW:
        return 0

    start_row = (board_id // 3) * 3
    start_col = (board_id % 3) * 3

    cells = []
    for r in range(start_row, start_row + 3):
        row = []
        for c in range(start_col, start_col + 3):
            row.append(game.board[r][c])
        cells.append(row)

    score = 0

    lines = []
    for i in range(3):
        lines.append(cells[i])
        lines.append([cells[0][i], cells[1][i], cells[2][i]])

    lines.append([cells[0][0], cells[1][1], cells[2][2]])
    lines.append([cells[0][2], cells[1][1], cells[2][0]])

    for line in lines:
        score += evaluate_line(line)

    if cells[1][1] == X:
        score += 3
    elif cells[1][1] == O:
        score -= 3

    return score


def evaluate_global_board(game):
    winner = game.check_global_winner()

    if winner == X:
        return 100000
    if winner == O:
        return -100000
    if winner == DRAW:
        return 0

    score = 0
    b = game.small_status

    for line in WINNING_LINES:
        values = [b[i] for i in line]

        x_count = values.count(X)
        o_count = values.count(O)
        open_count = values.count(ONGOING) + values.count(DRAW)

        if x_count > 0 and o_count > 0:
            continue

        if x_count == 2 and open_count == 1:
            score += 2000
        elif x_count == 1 and open_count == 2:
            score += 200

        if o_count == 2 and open_count == 1:
            score -= 2000
        elif o_count == 1 and open_count == 2:
            score -= 200

    if b[4] == X:
        score += 500
    elif b[4] == O:
        score -= 500

    return score


def evaluate(game):
    score = 0

    score += evaluate_global_board(game)

    for board_id in range(9):
        score += evaluate_small_board(game, board_id)

    return score


def minimax(game, depth, alpha, beta, maximizing):
    if depth == 0 or game.is_terminal():
        return evaluate(game)

    legal_moves = order_moves(game, game.get_legal_moves())

    if maximizing:
        best_score = -float("inf")

        for move in legal_moves:
            previous_next_board = game.next_board
            previous_small_status = game.small_status[:]
            previous_last_move = game.last_move

            game.play_move(move)

            score = minimax(game, depth - 1, alpha, beta, False)

            game.undo_move(
                move,
                previous_next_board,
                previous_small_status,
                previous_last_move
            )

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = float("inf")

        for move in legal_moves:
            previous_next_board = game.next_board
            previous_small_status = game.small_status[:]
            previous_last_move = game.last_move

            game.play_move(move)

            score = minimax(game, depth - 1, alpha, beta, True)

            game.undo_move(
                move,
                previous_next_board,
                previous_small_status,
                previous_last_move
            )

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score


def minimax_bot(game, depth=3):
    best_move = None

    legal_moves = order_moves(game, game.get_legal_moves())

    if game.current_player == X:
        best_score = -float("inf")

        for move in legal_moves:
            previous_next_board = game.next_board
            previous_small_status = game.small_status[:]
            previous_last_move = game.last_move

            game.play_move(move)

            score = minimax(
                game,
                depth - 1,
                -float("inf"),
                float("inf"),
                False
            )

            game.undo_move(
                move,
                previous_next_board,
                previous_small_status,
                previous_last_move
            )

            if score > best_score:
                best_score = score
                best_move = move

            elif score == best_score and random.random() < 0.3:
                best_move = move

    else:
        best_score = float("inf")

        for move in legal_moves:
            previous_next_board = game.next_board
            previous_small_status = game.small_status[:]
            previous_last_move = game.last_move

            game.play_move(move)

            score = minimax(
                game,
                depth - 1,
                -float("inf"),
                float("inf"),
                True
            )

            game.undo_move(
                move,
                previous_next_board,
                previous_small_status,
                previous_last_move
            )

            if score < best_score:
                best_score = score
                best_move = move

            elif score == best_score and random.random() < 0.3:
                best_move = move

    return best_move


def score_move_for_ordering(game, move):
    row, col = move
    score = 0

    # Bonus centre d'un mini-board
    if row % 3 == 1 and col % 3 == 1:
        score += 30

    # Bonus coins d'un mini-board
    if (row % 3, col % 3) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        score += 10

    board_id = game.small_board_index(row, col)
    current_status = game.small_status[board_id]

    # Si le board est encore en cours, on teste vite si le coup peut gagner
    if current_status == ONGOING:
        start_row = (board_id // 3) * 3
        start_col = (board_id % 3) * 3

        local = []
        for r in range(start_row, start_row + 3):
            line = []
            for c in range(start_col, start_col + 3):
                if r == row and c == col:
                    line.append(game.current_player)
                else:
                    line.append(game.board[r][c])
            local.append(line)

        lines = []
        for i in range(3):
            lines.append(local[i])
            lines.append([local[0][i], local[1][i], local[2][i]])

        lines.append([local[0][0], local[1][1], local[2][2]])
        lines.append([local[0][2], local[1][1], local[2][0]])

        for line in lines:
            if sum(line) == 3 * game.current_player:
                score += 1000
                break

    return score


def order_moves(game, moves):
    return sorted(
        moves,
        key=lambda move: score_move_for_ordering(game, move),
        reverse=True
    )



# Lancer le jeu
if __name__ == "__main__":
    human_vs_ai()