#!/usr/bin/env python3
import os
import string

alpha = tuple(string.ascii_uppercase[:8])


class DPawn():
    atag = " "
    tag = atag
    white = None


class Pawn(DPawn):
    atag = "p"
    tag = "♟︎"
    white = True
    movement = ((0, 1), )
    kill = ((-1, 1), (1, 1))
    first = True


class BPawn(Pawn):
    white = False
    movement = ((0, -1), )
    kill = ((-1, -1), (1, -1))


class Rook(DPawn):
    atag = "r"
    tag = "♜"
    white = True
    movement = []


class BRook(Rook):
    white = False


class Knight(DPawn):
    atag = "k"
    tag = "♞"
    white = True
    movement = ((1, 2), (1, -2), (-1, -2), (-1, 2),
                (2, 1), (2, -1), (-2, -1), (-2, 1))


class BKnight(Knight):
    white = False


class Bishop(DPawn):
    atag = "b"
    tag = "♝"
    white = True
    movement = []


class BBishop(Bishop):
    white = False


class Queen(DPawn):
    atag = "q"
    tag = "♛"
    white = True


class BQueen(Queen):
    white = False


class King(DPawn):
    atag = "K"
    tag = "♚"
    white = True
    movement = ((1, 1), (1, -1), (-1, -1), (1, -1))


class BKing(King):
    white = False


class ChessBoard(dict):
    def __init__(self):
        self.start_positions()
        self.white_outed = set()
        self.black_outed = set()
        self.history = []
        self.history_ind = 0

    def start_positions(self):
        for j in range(1, 9):
            for ind, i in enumerate(alpha):
                if j == 2:
                    self[i+str(j)] = Pawn()
                elif j == 7:
                    self[i+str(j)] = BPawn()
                elif i+str(j) in ["A1", "H1"]:
                    self[i+str(j)] = Rook()
                elif i+str(j) in ["A8", "H8"]:
                    self[i+str(j)] = BRook()
                elif i+str(j) in ["B1", "G1"]:
                    self[i+str(j)] = Knight()
                elif i+str(j) in ["B8", "G8"]:
                    self[i+str(j)] = BKnight()
                elif i+str(j) in ["C1", "F1"]:
                    self[i+str(j)] = Bishop()
                elif i+str(j) in ["C8", "F8"]:
                    self[i+str(j)] = BBishop()
                elif i+str(j) in ["D1"]:
                    self[i+str(j)] = Queen()
                elif i+str(j) in ["D8"]:
                    self[i+str(j)] = BQueen()
                elif i+str(j) in ["E1"]:
                    self[i+str(j)] = King()
                elif i+str(j) in ["E8"]:
                    self[i+str(j)] = BKing()
                else:
                    self[i+str(j)] = DPawn()

    def print(self, reverse=False):
        keys = list(self.keys())
        self.clear = "\033[m"
        self.whpawns = "\033[38;2;0;0;255m"
        self.blpawns = "\033[38;2;255;0;0m"
        whtile = "\033[48;2;255;255;255m"
        bltile = "\033[48;2;0;0;0m"
        ind = "\033[48;2;128;128;128m"
        rng = [7, -1, -1]
        rngr = [0, 8, 1]
        last = (
            alpha.index(self.history[max(-len(self.history),
                                         -1-self.history_ind)][0][0])
             +(int(self.history[max(-len(self.history),
                                    -1-self.history_ind)][0][1])-1)*8,
            alpha.index(self.history[max(-len(self.history),
                                         -1-self.history_ind)][1][0])
             +(int(self.history[max(-len(self.history),
                                    -1-self.history_ind)][1][1])-1)*8)\
            if self.history and self.history_ind < len(self.history)\
            else (-1, -1)
        if reverse:
            rng, rngr = rngr, rng
        print(" ", end="")
        for i in range(*rngr):
            print(f"| {keys[i][0]}".ljust(4), end="")
        print("|\n"+"-+"+"---+"*8, end="")
        for i in range(*rng):
            print("\n"+str(int(keys[i*8][1])), end="")
            for j in range(*rngr):
                if (i+j) % 2:
                    bg = whtile
                else:
                    bg = bltile
                piece = self[keys[j+i*8]]
                if piece.white:
                    fg = self.whpawns
                else:
                    fg = self.blpawns
                if j+i*8 in last:
                    piece = f"{ind}{piece.tag}{bg}"
                else:
                    piece = piece.tag
                print("".join((f"|{bg}{fg} ",
                                 str(piece),
                                 f" {self.clear}")), end="")
            print("|\n"+"-+"+"---+"*8, end="")
        print()
        if self.white_outed:
            print(f"{self.whpawns}Out:", end="")
            for i in self.white_outed:
                print(f" {i.tag}", end="")
            print(f"{self.clear}\n", end="")
        if self.black_outed:
            print(f"{self.blpawns}Out:", end="")
            for i in self.black_outed:
                print(f" {i.tag}", end="")
        print(self.clear)

    def show_history(self):
        if not self.history:
            print("No recorded moves")
            return
        for ind, i in enumerate(self.history):
            if ind >= len(self.history) - self.history_ind:
                break
            x = f"{i[0]}({self.whpawns if i[2].white else self.blpawns}"\
              +f"{i[2].tag}{self.clear}) => {i[1]}"
            if i[3].tag != " ":
                x += f"({self.whpawns if i[3].white else self.blpawns}"\
                  +f"{i[3].tag}{self.clear})"
            print(x)


class Chess():
    def __init__(self):
        self.reset()
        self.fields = tuple(self.board.keys())

    def reset(self):
        self.board = ChessBoard()
        self.whites = True

    def pawn_char(self):
        Pawn.tag, Pawn.atag = Pawn.atag, Pawn.tag
        Rook.tag, Rook.atag = Rook.atag, Rook.tag
        Knight.tag, Knight.atag = Knight.atag, Knight.tag
        Bishop.tag, Bishop.atag = Bishop.atag, Bishop.tag
        Queen.tag, Queen.atag = Queen.atag, Queen.tag
        King.tag, King.atag = King.atag, King.tag

    def move_history(self, forward=False):
        if forward:
            if self.board.history_ind == 0:
                print("Already on last move")
            else:
                self.board.history_ind -= 1
                self.whites = not self.whites
        else:
            if self.board.history_ind == len(self.board.history):
                print("Already went back to start")
            else:
                self.board.history_ind += 1
                self.whites = not self.whites
        self.sync_history()

    def sync_history(self, reset=False):
        if reset and self.board.history_ind:
            self.board.history = self.board.history[:-self.board.history_ind]
            self.board.history_ind = 0
            return
        self.board.start_positions()
        for i in range(len(self.board.history)):
            if type(self.board.history[i][3]) is not DPawn:
                if i < len(self.board.history) - self.board.history_ind:
                    if self.board.history[i][3].white:
                        self.board.white_outed.add(self.board.history[i][3])
                    else:
                        self.board.black_outed.add(self.board.history[i][3])
                else:
                    if self.board.history[i][3] in self.board.white_outed:
                        self.board.white_outed.remove(self.board.history[i][3])
                    elif self.board.history[i][3] in self.board.black_outed:
                        self.board.black_outed.remove(self.board.history[i][3])
            if i < len(self.board.history) - self.board.history_ind:
                self.board[self.board.history[i][0]] = DPawn
                self.board[self.board.history[i][1]] = self.board.history[i][2]

    def checkvh(self, from_coords, pawn, movement):
        x, y = from_coords
        if isinstance(pawn, (Queen, Rook)):
            done = [False, False, False, False]
            for i in range(1, 8):
                if False not in done:
                    break
                if not done[0] and y + i <= 8 and\
                        self.board[f"{alpha[x]}{y+i}"].white != self.whites:
                    if type(self.board[f"{alpha[x]}{y+i}"]) is not DPawn:
                        done[0] = True
                    movement.add((0, i))
                else:
                    done[0] = True
                if not done[1] and x + i < 8 and\
                        self.board[f"{alpha[x+i]}{y}"].white != self.whites:
                    if type(self.board[f"{alpha[x+i]}{y}"]) is not DPawn:
                        done[1] = True
                    movement.add((i, 0))
                else:
                    done[1] = True
                if not done[2] and y - i > 0 and\
                        self.board[f"{alpha[x]}{y-i}"].white != self.whites:
                    if type(self.board[f"{alpha[x]}{y-i}"]) is not DPawn:
                        done[2] = True
                    movement.add((0, -i))
                else:
                    done[2] = True
                if not done[3] and x + i >= 0 and\
                        self.board[f"{alpha[x-i]}{y}"].white != self.whites:
                    if type(self.board[f"{alpha[x-i]}{y}"]) is not DPawn:
                        done[3] = True
                    movement.add((-i, 0))
                else:
                    done[3] = True
        if isinstance(pawn, (Queen, Bishop)):
            done = [False, False, False, False]
            for i in range(1, 8):
                if False not in done:
                    break
                if not done[0] and y + i <= 8 and x + i < 8 and\
                        self.board[f"{alpha[x+i]}{y+i}"].white != self.whites:
                    if type(self.board[f"{alpha[x+i]}{y+i}"]) is not DPawn:
                        done[0] = True
                    movement.add((i, i))
                else:
                    done[0] = True
                if not done[1] and y - i > 0 and x + i < 8 and\
                        self.board[f"{alpha[x+i]}{y-i}"].white != self.whites:
                    if type(self.board[f"{alpha[x+i]}{y-i}"]) is not DPawn:
                        done[1] = True
                    movement.add((i, -i))
                else:
                    done[1] = True
                if not done[2] and y - i > 0 and x - i >= 0 and\
                        self.board[f"{alpha[x-i]}{y-i}"].white != self.whites:
                    if type(self.board[f"{alpha[x-i]}{y-i}"]) is not DPawn:
                        done[2] = True
                    movement.add((-i, -i))
                else:
                    done[2] = True
                if not done[3] and y + i <= 8 and x - i >= 0 and\
                        self.board[f"{alpha[x-i]}{y+i}"].white != self.whites:
                    if type(self.board[f"{alpha[x-i]}{y+i}"]) is not DPawn:
                        done[3] = True
                    movement.add((-i, i))
                else:
                    done[3] = True
        return movement

    def check(self, field_from, field_to):
        pawn = self.board[field_from]
        if self.whites != pawn.white or type(pawn) is DPawn or\
                self.board[field_to].white == self.whites:
            return "Invalid move\n"
        xfrom = alpha.index(field_from[0])
        xto = alpha.index(field_to[0])
        vector = (xto-xfrom, int(field_to[1])-int(field_from[1]))
        from_coords = (xfrom, int(field_from[1]))
        try:
            movement = set()
            if isinstance(pawn, (Queen, Rook, Bishop)):
                movement = self.checkvh(from_coords, pawn, movement)
            else:
                for i in pawn.movement:
                    movement.add(i)
                if isinstance(pawn, Pawn):
                    if pawn.first:
                        if pawn.white:
                            movement.add((0, 2))
                        else:
                            movement.add((0, -2))
            if vector in movement or (isinstance(pawn, Pawn) and vector
                                      in pawn.kill and
                                      type(self.board[field_to]) is not DPawn):
                self.sync_history(True)
                if self.whites and type(self.board[field_to]) is not DPawn:
                    self.board.black_outed.add(self.board[field_to])
                elif not self.whites and type(self.board[field_to])\
                        is not DPawn:
                    self.board.white_outed.add(self.board[field_to])
                self.board.history.append(
                    (field_from, field_to, self.board[field_from], self.board[field_to]))
                self.board[field_from] = DPawn()
                self.board[field_to] = pawn
                if isinstance(pawn, Pawn) and pawn.first:
                    pawn.first = False
            else:
                raise ValueError
        except ValueError:
            return "Invalid move\n"

    def play(self, inp, whites):
        try:
            field_from = inp[:2].strip()
            field_to = inp[2:].strip()
            if len(field_from) != 2 or len(field_to) != 2:
                raise ValueError
            field_from = field_from.upper()
            field_to = field_to.upper()
            if not field_from[1].isdigit():
                field_from = field_from[::-1]
            if not field_to[1].isdigit():
                field_to = field_to[::-1]
            if field_from not in self.fields or field_to not in self.fields or\
                    not field_from or not field_to or field_from == field_to:
                raise ValueError
            return self.check(field_from, field_to)
        except ValueError:
            return "Invalid choice\n"

    def help(self):
        print("Welcome to chess!\n"
              +"To mitigate problems with some terminals\n"
              +"white pawns are blue and black are red\n"
              +"Help:\n"
              +"? - this helhelp text\n"
              +"a - change between ascii and unicode pawns\n"
              +"hb - go back to previous move\n"
              +"hf - redo move if went back and did not make any move\n"
              +"h - show history\n"
              +"r - reset board\n"
              +"q - quit")

    def start(self, ascii_pawns):
        cols, rows = os.get_terminal_size()
        if rows < 21 or cols < 34:
            print("Terminal too small! For comfortable use it "
                  f"should be at least {rows}/21 rows and {cols}/34 columns."
                  "Exiting now...")
            return
        self.whites = True
        if ascii_pawns:
            self.pawn_char()
        self.help()
        while True:
            try:
                cols, rows = os.get_terminal_size()
                while rows < 21 or cols < 34:
                    print("Terminal too small! For comfortable use it "
                          f"should be at least {rows}/21 rows and "
                          f"{cols}/34 columns."
                          " Fix terminal height and width and type "
                          "anything to continue... ")
                    inp = input("> ")
                    cols, rows = os.get_terminal_size()
                if self.whites:
                    reverse = False
                else:
                    reverse = True
                self.board.print(reverse)
                inp = input("> ")
                if inp == "q":
                    raise EOFError
                elif inp == "r":
                    self.reset()
                elif inp == "h":
                    self.board.show_history()
                elif inp == "hf":
                    self.move_history(True)
                elif inp == "hb":
                    self.move_history()
                elif inp == "a":
                    self.pawn_char()
                elif inp == "?":
                    self.help()
                else:
                    tmp = self.play(inp.strip(), self.whites)
                    if tmp:
                        print(tmp, end="")
                    else:
                        self.whites = not self.whites
            except EOFError:
                break
            except (ValueError, KeyboardInterrupt, IndexError):
                continue


if __name__ == "__main__":
    import argparse
    if os.name != "nt":
        import readline
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-a", "--ascii", help="show ascii pawns instead of unicode ones",
            default=False, action="store_true")
    args = parser.parse_args()
    Chess().start(args.ascii)
