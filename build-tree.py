#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
import argparse
import numpy as np
from anytree import util
from Config import Config
from Games import Games
from Board import Player

# Auxiliary function
def check_left_siblings(node, mirror=True):
    board = node.board
    if mirror:
        board = board.mirror()
    node = util.leftsibling(node)
    while node != None:
        if node.board == board:
            return True
        node = util.leftsibling(node)
    return False
        
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
        pre = r"\graph [layered layout] {"
        post = ""
        level = 1
        shown_boards = []
        max_level = 20
        for node in games.render_tree(maxlevel=None):
            board = node.board
            if board.turn_num > max_level:
                continue
            if check_left_siblings(node):
                max_level = board.turn_num
                continue
            c = len(shown_boards)
            nodetext = "n"+str(c)+" [as="+board.draw_chessboard()+"]"
            shown_boards.append(board)
            if board.turn_num > level:
                level = board.turn_num
                pre = "\n -> {"
                post = ""
            elif board.turn_num < level:
                pre = (level - board.turn_num)*" }"+ ", \n "
                post = ""            
                level = board.turn_num
                max_level = 20
            elif level > 1:
                pre = ",\n"
                post = ""
            #pre = pre.strip()
            #if pre == "|":
            #    pre = "child {"
            #    post = "}"
            #elif pre == "+":
            #    pre = "child {"
            #    post = "}"
            print(pre, nodetext, post, end="", sep="")

        print((level)*" }", ";")
        # Draw cross-edges
        #for (u, v) in edges:
        #    print(r"\draw[thin] (n", u, ".south) -- (n", v, ".north);", sep="")

    