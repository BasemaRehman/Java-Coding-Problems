# -*- coding: utf-8 -*-
''' 
There are 3 main elements to building a chess game. The board, moves and 
current state (has anyone won)
'''

import chess

# (1) Making the board

#Creates the board, allows us to complete/undo a move, check for mate etc.
board = chess.Board()

#(2) Evaluating the state - When has one team won
# When either white or black returns -1, they have lost, 1 is a win, 0 is draw

def check_state():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    #Creates all the pieces
    
    wk = len(board.pieces(chess.KING, chess.WHITE))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    wkn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bk = len(board.pieces(chess.KING, chess.BLACK))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    bkn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    
    #Calculate the value of the current pieces on the board - Chess points can
    #be found here https://www.chessprogramming.org/Simplified_Evaluation_Function
    
    material = 100 * (wp - bp) + 320 * (wkn - bkn) + 330 * (wb - bb) 
    + 500 * (wr - br) + 900 * (wq - bq)
    
    kingspos = [-30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                 20, 20,  0,  0,  0,  0, 20, 20,
                 20, 30, 10,  0,  0, 10, 30, 20]
    
    queenspos = [-20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20]
    
    rookspos = [0,  0,  0,  0,  0,  0,  0,  0,
                  5, 10, 10, 10, 10, 10, 10,  5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                  0,  0,  0,  5,  5,  0,  0,  0]
    
    bishopspos = [-20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20]
    
    knightspos = [-50,-40,-30,-30,-30,-30,-40,-50,
                    -40,-20,  0,  0,  0,  0,-20,-40,
                    -30,  0, 10, 15, 15, 10,  0,-30,
                    -30,  5, 15, 20, 20, 15,  5,-30,
                    -30,  0, 15, 20, 20, 15,  0,-30,
                    -30,  5, 10, 15, 15, 10,  5,-30,
                    -40,-20,  0,  5,  5,  0,-20,-40,
                    -50,-40,-30,-30,-30,-30,-40,-50]
    pawnspos = [ 0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                 5,  5, 10, 25, 25, 10,  5,  5,
                 0,  0,  0, 20, 20,  0,  0,  0,
                 5, -5,-10,  0,  0,-10, -5,  5,
                 5, 10, 10,-20,-20, 10, 10,  5,
                 0,  0,  0,  0,  0,  0,  0,  0]

    # We assume that good values for white are bad for black and vice versa
    
    pawnsq = sum([pawnspos[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawnspos[chess.square_mirror(i)]
                       for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightspos[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightspos[chess.square_mirror(i)]
                           for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopspos[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopspos[chess.square_mirror(i)]
                           for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookspos[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookspos[chess.square_mirror(i)]
                       for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenspos[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenspos[chess.square_mirror(i)]
                         for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingspos[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
    kingsq = kingsq + sum([-kingspos[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KING, chess.BLACK)])

    # With -9999 and 9999 as winning and losing, eval shows how close you are to each
    eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval
