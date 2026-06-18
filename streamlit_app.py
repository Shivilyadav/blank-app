import random

import streamlit as st

st.set_page_config(page_title="Slide Grid Puzzle", page_icon="🧩", layout="centered")

SHUFFLE_MULTIPLIER = 30
MOVE_LIMIT_MULTIPLIER = 4


def board_cells(size: int) -> int:
    return size * size


def solved_board(size: int) -> list[int]:
    return [*range(1, board_cells(size)), 0]


def get_neighbors(index: int, size: int) -> list[int]:
    row, col = divmod(index, size)
    neighbors: list[int] = []
    if row > 0:
        neighbors.append(index - size)
    if row < size - 1:
        neighbors.append(index + size)
    if col > 0:
        neighbors.append(index - 1)
    if col < size - 1:
        neighbors.append(index + 1)
    return neighbors


def make_shuffled_board(size: int) -> list[int]:
    solved = solved_board(size)
    board = solved.copy()
    empty_index = len(board) - 1
    for _ in range(board_cells(size) * SHUFFLE_MULTIPLIER):
        swap_index = random.choice(get_neighbors(empty_index, size))
        board[empty_index], board[swap_index] = board[swap_index], board[empty_index]
        empty_index = swap_index
    if board == solved:
        swap_index = random.choice(get_neighbors(empty_index, size))
        board[empty_index], board[swap_index] = board[swap_index], board[empty_index]
    return board


def is_solved(board: list[int], size: int) -> bool:
    return board == solved_board(size)


def move_tile(value: int) -> bool:
    if st.session_state.phase != "active":
        return False
    board = st.session_state.board
    size = st.session_state.board_size
    empty_index = board.index(0)
    tile_index = board.index(value)
    if tile_index not in get_neighbors(empty_index, size):
        return False
    board[empty_index], board[tile_index] = board[tile_index], board[empty_index]
    st.session_state.moves_used += 1
    st.session_state.phase = "won" if is_solved(board, size) else "active"
    if st.session_state.moves_used >= st.session_state.move_limit and st.session_state.phase != "won":
        st.session_state.phase = "lost"
    return True


def start_game(size: int) -> None:
    st.session_state.board_size = size
    st.session_state.board = make_shuffled_board(size)
    st.session_state.moves_used = 0
    st.session_state.move_limit = board_cells(size) * MOVE_LIMIT_MULTIPLIER
    st.session_state.phase = "active"


st.markdown(
    """
    <style>
    .stApp {
      background: radial-gradient(circle at 20% 20%, #1f2657, #10152d 55%, #090d1a);
      color: #f2f5ff;
    }
    .game-shell {
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: max(14px, env(safe-area-inset-top)) 10px max(16px, env(safe-area-inset-bottom));
    }
    .game-card {
      width: min(100%, 460px);
      background: linear-gradient(170deg, rgba(255,255,255,0.16), rgba(255,255,255,0.08));
      border: 1px solid rgba(255,255,255,0.16);
      border-radius: 20px;
      box-shadow: 0 24px 40px rgba(0, 0, 0, 0.28);
      backdrop-filter: blur(8px);
      padding: clamp(14px, 2.4vw, 24px);
    }
    .game-card h1 {
      margin: 0 0 6px;
      font-size: clamp(1.3rem, 3.8vw, 2rem);
    }
    .game-note {
      margin-bottom: 14px;
      color: #d4ddff;
      font-size: clamp(0.92rem, 2.9vw, 1rem);
    }
    .metric-row {
      display: flex;
      gap: 8px;
      margin: 8px 0 14px;
      flex-wrap: wrap;
    }
    .pill {
      background: rgba(6, 18, 55, 0.6);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 0.84rem;
    }
    .stButton>button {
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.2);
      font-weight: 700;
      width: 100%;
    }
    .tile-btn button {
      height: clamp(52px, 10.5vw, 78px);
      font-size: clamp(1.02rem, 4vw, 1.45rem);
      background: linear-gradient(180deg, #f8fbff, #deeaff);
      color: #0d2148;
    }
    .tile-empty button {
      height: clamp(52px, 10.5vw, 78px);
      background: rgba(255,255,255,0.06);
      border-style: dashed;
      color: transparent;
      pointer-events: none;
    }
    @media (max-width: 450px) {
      .game-card { width: 100%; border-radius: 16px; }
    }
    @media (min-width: 900px) {
      .game-shell { padding: 28px 16px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "phase" not in st.session_state:
    st.session_state.phase = "start"
if "board_size" not in st.session_state:
    st.session_state.board_size = 4
if "board" not in st.session_state:
    st.session_state.board = []
if "moves_used" not in st.session_state:
    st.session_state.moves_used = 0
if "move_limit" not in st.session_state:
    st.session_state.move_limit = 0

st.markdown('<div class="game-shell"><div class="game-card">', unsafe_allow_html=True)
st.markdown("<h1>🧩 Slide Grid Puzzle</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='game-note'>Slide numbered tiles into order. Use strategy before you run out of moves.</div>",
    unsafe_allow_html=True,
)

if st.session_state.phase == "start":
    size_label = st.selectbox("Difficulty", ("3 x 3", "4 x 4"), index=1)
    selected_size = 3 if size_label.startswith("3") else 4
    if st.button("Start Game", type="primary"):
        start_game(selected_size)
        st.rerun()
else:
    st.markdown(
        (
            "<div class='metric-row'>"
            f"<div class='pill'>Moves: {st.session_state.moves_used}</div>"
            f"<div class='pill'>Limit: {st.session_state.move_limit}</div>"
            f"<div class='pill'>Grid: {st.session_state.board_size}x{st.session_state.board_size}</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    size = st.session_state.board_size
    game_active = st.session_state.phase == "active"
    for row in range(size):
        cols = st.columns(size, gap="small")
        for col in range(size):
            tile = st.session_state.board[row * size + col]
            with cols[col]:
                if tile == 0:
                    st.markdown('<div class="tile-empty">', unsafe_allow_html=True)
                    st.button(" ", key=f"empty-{row}-{col}", disabled=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown('<div class="tile-btn">', unsafe_allow_html=True)
                    if st.button(str(tile), key=f"tile-{row}-{col}-{tile}", disabled=not game_active):
                        move_tile(tile)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.phase == "won":
        st.success("🎉 Perfect! Puzzle solved.")
    elif st.session_state.phase == "lost":
        st.error("💥 Move limit reached. Try again with a new shuffle.")

    controls = st.columns(2, gap="small")
    with controls[0]:
        if st.button("Restart Same Size", type="primary"):
            start_game(st.session_state.board_size)
            st.rerun()
    with controls[1]:
        if st.button("Back to Start"):
            st.session_state.phase = "start"
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)
