#!/usr/bin/env python3
import os
import string

#Todo:
#-move history
#-stalemate
#-checkmate

alpha = tuple(string.ascii_uppercase[:8])


class DPawn():
    tag = " "
    utag = tag
    white = None


class Pawn(DPawn):
    tag = "p"
    utag = "♟︎"
    white = True
    movement = ((0, 1), )
    kill = ((-1, 1), (1, 1))
    first = True


class BPawn(Pawn):
    white = False
    movement = ((0, -1), )
    kill = ((-1, -1), (1, -1))


class Rook(DPawn):
    tag = "r"
    utag = "♜"
    white = True
    movement = []


class BRook(Rook):
    white = False


class Knight(DPawn):
    tag = "k"
    utag = "♞"
    white = True
    movement = ((1, 2), (1, -2), (-1, -2), (-1, 2),
                (2, 1), (2, -1), (-2, -1), (-2, 1))


class BKnight(Knight):
    white = False


class Bishop(DPawn):
    tag = "b"
    utag = "♝"
    white = True
    movement = []


class BBishop(Bishop):
    white = False


class Queen(DPawn):
    tag = "q"
    utag = "♛"
    white = True


class BQueen(Queen):
    white = False


class King(DPawn):
    tag = "K"
    utag = "♚"
    white = True
    movement = ((1, 1), (1, -1), (-1, -1), (1, -1))


class BKing(King):
    white = False


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
        self.white_outed = set()
        self.black_outed = set()
        self.last = ()

    def print(self, reverse=False):
        keys = list(self.keys())
        clear = "\033[m"
        whpawns = "\033[38;2;0;0;255m"
        blpawns = "\033[38;2;255;0;0m"
        whtile = "\033[48;2;255;255;255m"
        bltile = "\033[48;2;0;0;0m"
        ind = "\033[48;2;128;128;128m"
        yield " "
        rng = [7, -1, -1]
        rngr = [0, 8, 1]
        last = self.last
        if reverse:
            rng, rngr = rngr, rng
        for i in range(*rngr):
            yield f"| {keys[i][0]}".ljust(4)
        yield "|\n"+"-+"+"---+"*8
        for i in range(*rng):
            yield "\n"+str(int(keys[i*8][1]))
            for j in range(*rngr):
                if (i+j) % 2:
                    bg = whtile
                else:
                    bg = bltile
                piece = self[keys[j+i*8]]
                if piece.white:
                    fg = whpawns
                else:
                    fg = blpawns
                if j+i*8 in last:
                    piece = f"{ind}{piece.utag}{bg}"
                else:
                    piece = piece.utag
                yield "".join((f"|{bg}{fg} ",
                               str(piece),
                               f" {clear}"))
            yield "|\n"+"-+"+"---+"*8
        yield "\n"
        if self.white_outed:
            yield f"{whpawns}Out:"
            for i in self.white_outed:
                yield f" {i.utag}"
            yield f"{clear}\n"
        if self.black_outed:
            yield f"{blpawns}Out:"
            for i in self.black_outed:
                yield f" {i.utag}"
            yield f"{clear}\n"


class Chess():
    def __init__(self):
        self.reset()
        self.fields = tuple(self.board.keys())

    def reset(self):
        self.board = ChessBoard()
        self.whites = True

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
                if self.whites and type(self.board[field_to]) is not DPawn:
                    self.board.black_outed.add(self.board[field_to])
                elif not self.whites and type(self.board[field_to])\
                        is not DPawn:
                    self.board.white_outed.add(self.board[field_to])
                self.board[field_to] = pawn
                self.board[field_from] = DPawn()
                self.board.last = (
                        alpha.index(field_from[0])+(int(field_from[1])-1)*8,
                        alpha.index(field_to[0])+(int(field_to[1])-1)*8)
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
                if interactive:
                    inp = input("> ")
                if inp == "q":
                    raise EOFError
                elif inp == "r":
                    self.reset()
                else:
                    tmp = self.play(inp.strip(), self.whites)
                    if tmp:
                        if interactive:
                            print(tmp, end="")
                        else:
                            yield tmp
                    else:
                        self.whites = not self.whites
            except EOFError:
                break
            except (ValueError, KeyboardInterrupt, IndexError):
                continue
            finally:
                inp = ""


if __name__ == "__main__":
    import argparse
    if os.name != "nt":
        import readline
    parser = argparse.ArgumentParser()
    try:
        Chess().start(interactive=True).send(None)
    except StopIteration:
        pass
