import streamlit as st


def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def check_winner(board, player):
    """
    فحص الفوز - يجب أن يكون هناك 3 من نفس الرمز (X أو O) في صف/عمود/قطر
    """
    
    if player == " " or player is None:
        return False
    
    
    for row in board:
        if row[0] == row[1] == row[2] == player:
            return True
    
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    
    
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    
    return False


def is_full(board):
    """فحص إذا كانت اللوحة ممتلئة"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# ================== MINIMAX AI ==================
def minimax(board, is_maximizing):
    """
    خوارزمية Minimax لإيجاد أفضل حركة
    الكمبيوتر هو O (maximizing)
    اللاعب هو X (minimizing)
    """
    
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = " "
                    best_score = min(best_score, score)
        return best_score


def best_move(board):
    """
    إيجاد أفضل حركة للكمبيوتر باستخدام Minimax
    """
    best_score = -1000
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def main():
    st.set_page_config(page_title="Tic Tac Toe", layout="centered")

   
    if "board" not in st.session_state:
        st.session_state.board = initialize_board()
        st.session_state.winner = None
        st.session_state.current_player = "X"
        st.session_state.game_mode = "Player vs Player"
        st.session_state.computer_turn = False

    
    st.markdown("""
       <style>
        .stButton>button {
            height: 80px;
            width: 150px;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4CAF50;
            border-radius: 10px;
            border: 2px solid #34a853;
            transition: background-color 0.3s, transform 0.2s;
        }
        .stButton>button:hover {
            background-color: #45d17c;
            transform: scale(1.05);
        }
        .stButton>button:disabled {
            background-color: #d3d3d3 !important;
            color: #808080 !important;
        }
        .winner {
            font-size: 35px;
            color: #FFD700;
            text-align: center;
            font-weight: bold;
            text-shadow: 2px 2px 4px #000000;
        }
        .title {
            font-size: 40px;
            color: #1E90FF;
            text-align: center;
            font-weight: bold;
            text-shadow: 2px 2px 4px #000000;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">Tic Tac Toe</div>', unsafe_allow_html=True)

    
    if (st.session_state.game_mode == "Player vs Computer" and 
        st.session_state.computer_turn and 
        not st.session_state.winner):
        
        move = best_move(st.session_state.board)
        if move:
            x, y = move
            st.session_state.board[x][y] = "O"
            
            
            winner_found = check_winner(st.session_state.board, "O")
            board_full = is_full(st.session_state.board)
            
            if winner_found:
                st.session_state.winner = "Computer"
            elif board_full:
                st.session_state.winner = "Tie"
            
            st.session_state.current_player = "X"
            st.session_state.computer_turn = False
        st.rerun()

    
    if st.button("Switch to Player vs Computer" if st.session_state.game_mode == "Player vs Player" else "Switch to Player vs Player"):
        st.session_state.game_mode = "Player vs Computer" if st.session_state.game_mode == "Player vs Player" else "Player vs Player"
        st.session_state.board = initialize_board()
        st.session_state.winner = None
        st.session_state.current_player = "X"
        st.session_state.computer_turn = False
        st.rerun()

    st.markdown(f"### Current Mode: {st.session_state.game_mode}")

    
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            with cols[j]:
                if st.session_state.board[i][j] == " " and st.session_state.winner is None:
                    if st.button(" ", key=f"{i}-{j}"):
                       
                        st.session_state.board[i][j] = "X"
                        
                        
                        winner_found = check_winner(st.session_state.board, "X")
                        board_full = is_full(st.session_state.board)
                        
                        if winner_found:
                            st.session_state.winner = "Player X"
                        elif board_full:
                            st.session_state.winner = "Tie"
                        elif st.session_state.game_mode == "Player vs Computer":
                            
                            st.session_state.computer_turn = True
                        else:
                            
                            st.session_state.current_player = "O"
                        
                        st.rerun()
                else:
                    st.button(st.session_state.board[i][j], key=f"{i}-{j}-disabled", disabled=True)

    
    if st.session_state.winner:
        if st.session_state.winner == "Tie":
            st.markdown('<div class="winner">It\'s a Tie!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="winner">{st.session_state.winner} Wins!</div>', unsafe_allow_html=True)
        if st.button("Restart Game"):
            st.session_state.board = initialize_board()
            st.session_state.winner = None
            st.session_state.current_player = "X"
            st.session_state.computer_turn = False
            st.rerun()


if __name__ == "__main__":
    main()
