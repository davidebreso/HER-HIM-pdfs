#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
import argparse
import numpy as np
from Config import Config
from Games import Games
from Board import Player

# Parse command line arguments
parser = argparse.ArgumentParser(description="Builds LaTeX source file for the complete position tree for hexapawn.")
args = parser.parse_args()

# Load the config file
config = Config()
c = 0
edges = []
# Just for initial development, show the starting position
with open("tree.tex", "r") as bfile :
    for line in bfile :
        line = line.strip()
        if line != "%TIKZ" :
            print(line)
            continue

        # Build game tree
        games = Games(config)

        # Now draw position tree
        pre = "\Tree [."
        post = ""
        level = 1
        shown_boards = []
        for node in games.render_tree(maxlevel=None):
            board = node.board
            if board in shown_boards:
                parent = node.parent.board
                if parent in shown_boards:
                    edges.append((shown_boards.index(parent), shown_boards.index(board)))
                continue
            elif board.mirror() in shown_boards:
                parent = node.parent.board
                if parent in shown_boards:
                    edges.append((shown_boards.index(parent), shown_boards.index(board.mirror())))
                continue
            c = len(shown_boards)
            shown_boards.append(board)
            if board.turn_num > level:
                level = board.turn_num
                pre = "\n [."
                post = ""
            elif board.turn_num < level:
                pre = (level - board.turn_num)*" ]"+ " ]\n [."
                post = ""            
                level = board.turn_num
            elif level > 1:
                pre = " ]\n  [."
                post = ""
            #pre = pre.strip()
            #if pre == "|":
            #    pre = "child {"
            #    post = "}"
            #elif pre == "+":
            #    pre = "child {"
            #    post = "}"
            print(pre, r"\node(n", c, ")", board.draw_chessboard(), ";", post, end="", sep="")

        print((level)*" ]")
        # Draw cross-edges
        for (u, v) in edges:
            print(r"\draw[thin] (n", u, ".south) -- (n", v, ".north);", sep="")

    