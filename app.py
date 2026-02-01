from flask import Flask, render_template, request, jsonify
import math
app = Flask(__name__)
HUMAN = 'X'
AI = 'O'

def check_winner(board, player):
    win_positions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == player for i in pos) for pos in win_positions)

def is_draw(board):
    return '_' not in board

def minimax(board, is_max):
    if check_winner(board, AI):
        return 10
    if check_winner(board, HUMAN):
        return -10
    if is_draw(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == '_':
                board[i] = AI
                best = max(best, minimax(board, False))
                board[i] = '_'
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == '_':
                board[i] = HUMAN
                best = min(best, minimax(board, True))
                board[i] = '_'
        return best

def best_move(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == '_':
            board[i] = AI
            move_val = minimax(board, False)
            board[i] = '_'
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    board = request.json['board']

    if check_winner(board, HUMAN):
        return jsonify({'status': 'You Win'})
    if is_draw(board):
        return jsonify({'status': 'Draw'})

    ai_move = best_move(board)
    board[ai_move] = AI

    if check_winner(board, AI):
        return jsonify({'board': board, 'status': 'AI Wins'})
    if is_draw(board):
        return jsonify({'board': board, 'status': 'Draw'})

    return jsonify({'board': board, 'status': 'Continue'})

if __name__ == '__main__':
    app.run(debug=True)
