#!/usr/bin/env python3
import sys
import string

alpha = tuple(string.ascii_uppercase[:8])

# TODO
# -diagonal movement
# -functionality


class DPawn():
    tag = " "
    color_white = None
    movement = None
    kill = None


class Pawn(DPawn):
    tag = "p"
    color_white = True
    movement = ((0, 1))
    kill = ((-1, 1), (1, 1))


class BPawn(Pawn):
    color_white = False


class Rook(DPawn):
    tag = "r"
    color_white = True
    movement = ((0, "*"), ("*", 0))


class BRook(Rook):
    color_white = False


class Knight(DPawn):
    tag = "k"
    color_white = True
    movement = ((1, 3), (1, -3), (-1, -3), (-1, 3))


class BKnight(Knight):
    color_white = False


class Bishop(DPawn):
    tag = "b"
    color_white = True
    movement = []
    def __init__(self):
        for i in range(0, 8):
            self.movement.append((i, i))
            self.movement.append((i, -i))
            self.movement.append((-i, -i))
            self.movement.append((-i, i))


class BBishop(Bishop):
    color_white = False


class Queen(DPawn):
    tag = "q"
    color_white = True
    movement = [(0, "*"), ("*", 0)]
    def __init__(self):
        for i in range(0, 8):
            self.movement.append((i, i))
            self.movement.append((i, -i))
            self.movement.append((-i, -i))
            self.movement.append((-i, i))


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


class Chess(dict):
    def __init__(self):
        self.fields = []
        for i in alpha:
            for j in range(1, 9):
                self.fields.append(i+str(j))
        self.reset()

    def reset(self):
        self.board = ChessBoard()

    def check(self, field_from, field_to):
        pawn = self.board[field_from]
        movement = set()
        for i in pawn.movement:
            movement.add(i)
        if isinstance(pawn, Pawn):
            movement.add(pawn.kill)
        available = []
        if (0, "*") in movement:
            ind = alpha.index(field_from[1]-1)
            for i in range(ind, 1, -1):
                pass
        if not self.whites != pawn.color_white:
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
        self.whites = True
        while interactive or (not interactive and inp):
            try:
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
                if self.whites:
                    self.whites = False
                else:
                    self.whites = True
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
            except EOFError:
                sys.exit(0)
            except (ValueError, KeyboardInterrupt, IndexError):
                continue
            finally:
                inp = ""


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    Chess().start(interactive=True).send(None)
