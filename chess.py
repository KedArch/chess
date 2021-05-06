#!/usr/bin/env python3
import os
import sys
import string

alpha = tuple(string.ascii_uppercase[:8])

# TODO
# -diagonal movement
# -functionality


class DPawn():
    tag = " "
    color_white = None

class Pawn(DPawn):
    tag = "p"
    color_white = True
    movement = ((0, 1),)
    kill = ((-1, 1), (1, 1))
    first = True


class BPawn(Pawn):
    color_white = False
    movement = ((0, -1),)
    kill = ((-1, -1), (1, -1))


class Rook(DPawn):
    tag = "r"
    color_white = True
    movement = []
    def __init__(self):
        for i in range(1,8):
            self.movement.append((0,i))
            self.movement.append((0,-i))
            self.movement.append((i,0))
            self.movement.append((-i,0))
        self.movement = tuple(self.movement)

class BRook(Rook):
    color_white = False


class Knight(DPawn):
    tag = "k"
    color_white = True
    movement = ((1, 2), (1, -2), (-1, -2), (-1, 2),
            (2, 1), (2, -1), (-2, -1), (-2, 1))


class BKnight(Knight):
    color_white = False


class Bishop(DPawn):
    tag = "b"
    color_white = True
    movement = []
    def __init__(self):
        for i in range(1, 8):
            self.movement.append((i, i))
            self.movement.append((i, -i))
            self.movement.append((-i, -i))
            self.movement.append((-i, i))
        self.movement = tuple(self.movement)


class BBishop(Bishop):
    color_white = False


class Queen(DPawn):
    tag = "q"
    color_white = True
    movement = []
    def __init__(self):
        for i in range(1,8):
            self.movement.append((0,i))
            self.movement.append((0,-i))
            self.movement.append((i,0))
            self.movement.append((-i,0))
            self.movement.append((i, i))
            self.movement.append((i, -i))
            self.movement.append((-i, -i))
            self.movement.append((-i, i))
        self.movement = tuple(self.movement)

class BQueen(Queen):
    color_white = False


class King(DPawn):
    tag = "K"
    color_white = True
    movement = ((1, 1), (1, -1), (-1, -1), (1, -1))


class BKing(King):
    color_white = False

class ChessBoard(dict):
    def __init__(self):
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
        yield " "
        rng = [7, -1, -1]
        rngr = [0, 8, 1]
        if reverse:
            rng, rngr = rngr, rng
        for i in range(*rngr):
            yield f"| {keys[i][0]}".ljust(4)
        yield "|\n"+"-+"+"---+"*8
        for i in range(*rng):
            yield "\n"+str(int(keys[i*8][1]))
            for j in range(*rngr):
                if (i+j)%2:
                    brgb = "255;255;255"
                else:
                    brgb = "0;0;0"
                piece = self[keys[j+i*8]]
                if piece.color_white:
                    frgb = "0;0;255"
                else:
                    frgb = "255;0;0"
                yield "".join((f"|\033[48;2;{brgb}m",
                    f"\033[38;2;{frgb}m {self[keys[j+i*8]].tag} ","\033[m"))
            yield "|\n"+"-+"+"---+"*8
            yield "\033[|"
        yield "\n"


class Chess():
    def __init__(self):
        self.reset()
        self.fields = tuple(self.board.keys())

    def reset(self):
        self.board = ChessBoard()

    def check(self, field_from, field_to):
        pawn = self.board[field_from]
        if self.whites != pawn.color_white or type(pawn) is DPawn:
            return "Invalid move\n"
        movement = set()
        for i in pawn.movement:
            movement.add(i)
        xfrom = alpha.index(field_from[0])
        xto = alpha.index(field_to[0])
        vector = (xto-xfrom, int(field_to[1])-int(field_from[1]))
        try:
            if isinstance(pawn, Pawn):
                if pawn.first:
                    if pawn.color_white:
                        movement.add((0,2))
                    else:
                        movement.add((0,-2))
            if vector in movement:
                self.board[field_to] = pawn
                self.board[field_from] = DPawn()
                if isinstance(pawn, Pawn) and pawn.first:
                    pawn.first = False
            else:
                if isinstance(pawn, Pawn):
                    if vector in pawn.kill and type(self.board[field_to]) is not DPawn:
                        self.board[field_to] = pawn
                        self.board[field_from] = DPawn()
                        if pawn.first:
                            pawn.first = False
                else:
                    raise ValueError
        except ValueError:
            return "Invalid move\n"

    def play(self, inp, whites):
        try:
            field_from, field_to = inp.split(" ", 1)
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

    def start(self, inp="", interactive=False):
        cols, rows = os.get_terminal_size()
        if rows < 21 or cols < 34:
            print("Terminal too small! For comfortable use it "
                  f"should be at least {rows}/21 rows and {cols}/34 columns."
                  "Exiting now...")
            yield
        self.whites = True
        while interactive or (not interactive and inp):
            try:
                cols, rows = os.get_terminal_size()
                while rows < 21 or cols < 34:
                    print("Terminal too small! For comfortable use it "
                          f"should be at least {rows}/21 rows and "
                          f"{cols}/34 columns."
                          " Fix terminal height and width and type "
                          "anything to continue... ")
                    if interactive:
                        inp = input("> ")
                    else:
                        yield
                    cols, rows = os.get_terminal_size()
                if self.whites:
                    reverse = False
                else:
                    reverse = True
                for i in self.board.print(reverse):
                    if interactive:
                        print(i, end="")
                    else:
                        yield i
                if self.whites:
                    if interactive:
                        print("Whites turn")
                    else:
                        yield "Whites turn\n"
                else:
                    if interactive:
                        print("Blacks turn")
                    else:
                        yield "Blacks turn\n"
                if interactive:
                    inp = input("> ")
                if inp == "e":
                    raise EOFError
                elif inp == "r":
                    self.reset()
                else:
                    tmp = self.play(inp, self.whites)
                    if tmp:
                        if interactive:
                            print(tmp, end="")
                        else:
                            yield tmp
                    else:
                        self.whites = not self.whites
            except EOFError:
                sys.exit(0)
            except (ValueError, KeyboardInterrupt, IndexError):
                continue
            finally:
                inp = ""


if __name__ == "__main__":
    import argparse
    if os.name != "nt":
        import readline
    parser = argparse.ArgumentParser()
    Chess().start(interactive=True).send(None)
