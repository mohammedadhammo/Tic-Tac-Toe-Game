import streamlit as st
import heapq


def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def check_winner(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board):
    return all(all(cell != " " for cell in row) for row in board)


def heuristic(board, player):
    opponent = "X" if player == "O" else "O"
    score = 0

    # تقييم الصفوف
    for row in board:
        if row.count(player) > 0 and row.count(opponent) == 0:
            score += 1

    # تقييم الأعمدة
    for col in range(3):
        col_values = [board[row][col] for row in range(3)]
        if col_values.count(player) > 0 and col_values.count(opponent) == 0:
            score += 1

    # تقييم الأقطار
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2 - i] for i in range(3)]
    if diag1.count(player) > 0 and diag1.count(opponent) == 0:
        score += 1
    if diag2.count(player) > 0 and diag2.count(opponent) == 0:
        score += 1

    return score


def a_star(board, player):
    opponent = "X" if player == "O" else "O"
    priority_queue = []
    heapq.heapify(priority_queue)

    for x in range(3):
        for y in range(3):
            if board[x][y] == " ":
                new_board = [row[:] for row in board]
                new_board[x][y] = player
                g_cost = 1  # تكلفة الحركة الحالية
                h_cost = heuristic(new_board, player)
                total_cost = g_cost + h_cost
                heapq.heappush(priority_queue, (-total_cost, (x, y)))

    if priority_queue:
        return heapq.heappop(priority_queue)[1]
    return None


def main():
    st.set_page_config(page_title="Tic Tac Toe", layout="centered")

    if "board" not in st.session_state:
        st.session_state.board = initialize_board()
        st.session_state.winner = None
        st.session_state.current_player = "X"
        st.session_state.game_mode = "Player vs Player"

    # Styling
    st.markdown("""
        <style>
            .stButton>button {
                height: 80px;
                width: 150px;
                font-size: 25px;
                font-weight: bold;
                background-color: rgb(145, 141, 141); /* خلفية سوداء */
                color:rgb(255, 255, 255); /* لون النص ذهبي */
                border: 2px solid #4682B4;
                border-radius: 10px;
                text-align: center; /* لضمان محاذاة النص */
                transition: transform 0.2s, background-color 0.3s;
            }
            .stButton>button:hover {
                background-color: #4682B4; /* خلفية أفتح عند التمرير */
                color: white; /* لون النص أبيض عند التمرير */
                transform: scale(1.1);
            }
            .winner {
                font-size: 40px;
                color: #FFD700; /* نص ذهبي */
                text-align: center;
                font-weight: bold;
                text-shadow: 2px 2px 4px #000000; /* ظل أسود */
            }
            .title {
                font-size: 50px;
                color: #FF4500; /* عنوان برتقالي */
                text-align: center;
                font-weight: bold;
                text-shadow: 2px 2px 5px #000000; /* ظل أسود */
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">Tic Tac Toe</div>', unsafe_allow_html=True)

    if st.button("Switch to Player vs Computer" if st.session_state.game_mode == "Player vs Player" else "Switch to Player vs Player"):
        st.session_state.game_mode = "Player vs Computer" if st.session_state.game_mode == "Player vs Player" else "Player vs Player"
        st.session_state.board = initialize_board()
        st.session_state.winner = None
        st.session_state.current_player = "X"

    st.markdown(f"### Current Mode: {st.session_state.game_mode}")

    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            with cols[j]:
                # إذا كانت الخانة فارغة
                if st.session_state.board[i][j] == " " and st.session_state.winner is None:
                    if st.button(" ", key=f"{i}-{j}"):
                        st.session_state.board[i][j] = st.session_state.current_player
                        if check_winner(st.session_state.board, st.session_state.current_player):
                            st.session_state.winner = f"Player {st.session_state.current_player}"
                        elif is_full(st.session_state.board):
                            st.session_state.winner = "Tie"
                        else:
                            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
                else:
                    # إذا كانت الخانة مملوءة، عرض العلامة (X أو O)
                    st.button(st.session_state.board[i][j], key=f"{i}-{j}-disabled", disabled=True)

    if st.session_state.game_mode == "Player vs Computer" and st.session_state.current_player == "O" and st.session_state.winner is None:
        best_move = a_star(st.session_state.board, "O")
        if best_move:
            x, y = best_move
            st.session_state.board[x][y] = "O"
            if check_winner(st.session_state.board, "O"):
                st.session_state.winner = "Computer"
            elif is_full(st.session_state.board):
                st.session_state.winner = "Tie"
            else:
                st.session_state.current_player = "X"

    if st.session_state.winner:
        if st.session_state.winner == "Tie":
            st.markdown('<div class="winner">It\'s a Tie!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="winner">{st.session_state.winner} Wins!</div>', unsafe_allow_html=True)
        if st.button("Restart Game"):
            st.session_state.board = initialize_board()
            st.session_state.winner = None
            st.session_state.current_player = "X"


if __name__ == "__main__":
    main()
