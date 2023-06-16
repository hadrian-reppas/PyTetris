import constants
import controls

import pygame
from dataclasses import dataclass
from enum import Enum, auto
import random


@dataclass
class key_cooldowns:
    down: bool = False
    left: bool = False
    right: bool = False
    down_key: bool = False
    left_key: bool = False
    right_key: bool = False
    down_cd: int = 0
    left_cd: int = 0
    right_cd: int = 0
    rotate_left: bool = False
    rotate_right: bool = False
    rotated_left: bool = False
    rotated_right: bool = False

class animation_stage(Enum):
    play = auto()
    line_clear = auto()
    game_over = auto()

@dataclass
class piece_position:
    row: int
    col: int
    rot: int

@dataclass
class game_state:
    board: list[list[int]]
    piece: int
    piece_pos: piece_position
    next_piece: int
    keys: key_cooldowns
    fall_timer: int
    level: int
    lines: int
    score: int

    top_score: int
    a_type: bool
    statistics: list[int]
    
    key_arr: list[bool] = None

    animations: bool = True
    stage: animation_stage = animation_stage.play
    animation_timer: int = None
    full_lines: list[int] = None

def init(key_arr=None):
    board = [[None for _ in range(10)] for _ in range(20)]
    piece = generate_piece()
    piece_pos = piece_position(0, 5, 0)
    next_piece = generate_piece(piece)
    keys = key_cooldowns()
    statistics = [int(i == piece) for i in range(7)]
    return game_state(
        board,
        piece,
        piece_pos,
        next_piece,
        keys,
        constants.start_delay,    # fall timer
        constants.starting_level, # level
        0,      # lines
        0,      # score
        10_000, # top score
        True,   # a type
        statistics,
        key_arr,
    )

def update(state):
    running = handle_events(state)
    if state.stage == animation_stage.play:
        update_play(state)
    elif state.stage == animation_stage.line_clear:
        update_line_clear(state)
    else:
        state, r = update_game_over(state)
        running &= r
    decrement_keys(state)
    if state.animations or state.stage != animation_stage.game_over:
        return state, running
    elif constants.quit_on_game_over:
        return state, False
    else:
        return init(state.key_arr), True

def update_play(state):
    if check_keys(state):
        return
    state.fall_timer -= 1
    if state.fall_timer == 0:
        try_drop(state, False)

def update_line_clear(state):
    state.animation_timer -= 1
    if state.animation_timer == 0:
        update_score_lines_and_level(state)
        remove_lines(state)
        update_piece(state)
        state.stage = animation_stage.play

def check_keys(state: game_state):
    keys = state.keys
    if keys.down:
        try_drop(state, True)
        return True
    
    if keys.left:
        try_left(state)
    elif keys.right:
        try_right(state)
    
    if keys.rotate_left:
        try_rot_left(state)
    elif keys.rotate_right:
        try_rot_right(state)
    
    return False
    
def try_drop(state, by_player):
    piece = constants.tetrominos[state.piece][state.piece_pos.rot]
    row, col = state.piece_pos.row, state.piece_pos.col
    can_drop = True
    for d_col, d_row in piece:
        if row + d_row + 1 >= 20:
            can_drop = False
            break
        elif row + d_row + 1 < 0:
            continue
        elif state.board[row + d_row + 1][col + d_col] is not None:
            can_drop = False
            break
    if can_drop:
        state.piece_pos.row += 1
        if by_player:
            score_soft_drop(state)
    else:
        place_piece(state)
    state.fall_timer = get_fall_time(state)

def try_left(state):
    piece = constants.tetrominos[state.piece][state.piece_pos.rot]
    row, col = state.piece_pos.row, state.piece_pos.col
    can_move = True
    for d_col, d_row in piece:
        if col + d_col - 1 < 0:
            can_move = False
            break
        elif row + d_row < 0:
            continue
        elif state.board[row + d_row][col + d_col - 1] is not None:
            can_move = False
            break
    if can_move:
        state.piece_pos.col -= 1

def try_right(state):
    piece = constants.tetrominos[state.piece][state.piece_pos.rot]
    row, col = state.piece_pos.row, state.piece_pos.col
    can_move = True
    for d_col, d_row in piece:
        if col + d_col + 1 >= 10:
            can_move = False
            break
        elif row + d_row < 0:
            continue
        elif state.board[row + d_row][col + d_col + 1] is not None:
            can_move = False
            break
    if can_move:
        state.piece_pos.col += 1

def try_rot_left(state):
    row, col = state.piece_pos.row, state.piece_pos.col
    rot = state.piece_pos.rot
    new_rot = rot - 1
    if new_rot < 0:
        new_rot += constants.rotation_states[state.piece]
    piece = constants.tetrominos[state.piece][new_rot]
    can_rot = True
    for d_col, d_row in piece:
        if col + d_col < 0 or col + d_col >= 10:
            can_rot = False
            break
        elif row + d_row >= 20:
            can_rot = False
            break
        elif row + d_row < 0:
            continue
        elif state.board[row + d_row][col + d_col] is not None:
            can_rot = False
            break
    if can_rot:
        state.piece_pos.rot = new_rot

def try_rot_right(state):
    row, col = state.piece_pos.row, state.piece_pos.col
    rot = state.piece_pos.rot
    new_rot = (rot + 1) % constants.rotation_states[state.piece]
    piece = constants.tetrominos[state.piece][new_rot]
    can_rot = True
    for d_col, d_row in piece:
        if col + d_col < 0 or col + d_col >= 10:
            can_rot = False
            break
        elif row + d_row >= 20:
            can_rot = False
            break
        elif row + d_row < 0:
            continue
        elif state.board[row + d_row][col + d_col] is not None:
            can_rot = False
            break
    if can_rot:
        state.piece_pos.rot = new_rot

def get_fall_time(state):
    if state.level > 28:
        return 1
    return constants.fall_times[state.level]

def place_piece(state):
    piece = constants.tetrominos[state.piece][state.piece_pos.rot]
    row, col = state.piece_pos.row, state.piece_pos.col
    color = constants.square_colors[state.piece]
    game_over = False
    for d_col, d_row in piece:
        if row + d_row < 0:
            continue
        game_over |= state.board[row + d_row][col + d_col] is not None
        state.board[row + d_row][col + d_col]  = color
    if game_over:
        start_game_over_animation(state)
    elif has_full_lines(state):
        start_line_clear_animation(state)
    else:
        update_piece(state)
    state.keys.down_cd = -1

def start_line_clear_animation(state):
    state.full_lines = get_full_lines(state)
    if state.animations:
        state.stage = animation_stage.line_clear
        state.animation_timer = 20
    else:
        update_score_lines_and_level(state)
        remove_lines(state)
        update_piece(state)

def start_game_over_animation(state):
    state.stage = animation_stage.game_over
    if state.animations:
        state.animation_timer = 84 + constants.game_over_delay
    else:
        state.animation_timer = 1

def has_full_lines(state):
    for row in state.board:
        if all(x is not None for x in row):
            return True
    return False

def get_full_lines(state):
    full_lines = []
    for i, row in enumerate(state.board):
        if all(x is not None for x in row):
            full_lines.append(i)
    return full_lines

def update_game_over(state: game_state):
    state.animation_timer -= 1
    if state.animation_timer == 0:
        if constants.quit_on_game_over:
            return state, False
        return init(state.key_arr), True
    return state, True

def update_piece(state):
    state.piece = state.next_piece
    state.statistics[state.piece] += 1
    state.piece_pos.row = 0
    state.piece_pos.col = 5
    state.piece_pos.rot = 0
    state.next_piece = generate_piece(state.piece)

def remove_lines(state):
    for row in state.full_lines[::-1]:
        del state.board[row]
    for _ in state.full_lines:
        row = [None for _ in range(10)]
        state.board.insert(0, row)

def score_soft_drop(state):
    state.score += constants.soft_drop_bonus

def update_score_lines_and_level(state):
    cleared_lines = len(state.full_lines)
    if cleared_lines == 1:
        state.score += constants.single_bonus*(state.level + 1)
    elif cleared_lines == 2:
        state.score += constants.double_bonus*(state.level + 1)
    elif cleared_lines == 3:
        state.score += constants.triple_bonus*(state.level + 1)
    elif cleared_lines == 4:
        state.score += constants.tetris_bonus*(state.level + 1)
    t1 = 10*constants.starting_level + 10
    t2 = max(100, 10*constants.starting_level - 50)
    threshold = min(t1, t2)
    if state.lines + cleared_lines < threshold:
        state.lines += cleared_lines
        return
    if (state.lines + cleared_lines) % 10 < state.lines % 10:
        state.level += 1
    state.lines += cleared_lines

def generate_piece(last_piece=None):
    piece = random_piece()
    if piece == last_piece:
        return random_piece()
    return piece

def random_piece():
    r = random.random()
    cum_sum = 0
    for i, p in enumerate(constants.piece_probabilities):
        cum_sum += p
        if r <= cum_sum:
            return i
    return 6

def decrement_keys(state: game_state):

    state.keys.down = False
    if state.keys.down_key:
        state.keys.down_cd -= 1
        if state.keys.down_cd == 0:
            state.keys.down = True
            state.keys.down_cd = constants.down_cooldown

    state.keys.left = False
    if state.keys.left_key:
        state.keys.left_cd -= 1
        if state.keys.left_cd == 0:
            state.keys.left = True
            state.keys.left_cd = constants.subsequent_cooldown
        
    state.keys.right = False
    if state.keys.right_key:
        state.keys.right_cd -= 1
        if state.keys.right_cd == 0:
            state.keys.right = True
            state.keys.right_cd = constants.subsequent_cooldown
    
    state.keys.rotate_left = False
    state.keys.rotate_right = False

def handle_events(state):
    if state.key_arr is not None:
        # TODO: implement this
        if not state.keys.down_key and state.key_arr[0]:
            # down just pressed
            state.keys.down_key = True
            state.keys.down = True
            state.keys.down_cd = constants.down_cooldown
        elif state.keys.down_key and not state.key_arr[0]:
            # down just released
            state.keys.down_key = False
        
        if not state.keys.left_key and state.key_arr[1]:
            # left just pressed
            state.keys.left_key = True
            state.keys.left = True
            state.keys.left_cd = constants.initial_cooldown
        elif state.keys.left_key and not state.key_arr[1]:
            # left just released
            state.keys.left_key = False
        
        if not state.keys.right_key and state.key_arr[2]:
            # right just pressed
            state.keys.right_key = True
            state.keys.right = True
            state.keys.right_cd = constants.initial_cooldown
        elif state.keys.right_key and not state.key_arr[2]:
            # right just released
            state.keys.right_key = False
        
        if state.key_arr[3] and not state.keys.rotated_left:
            # rotate_left just pressed
            state.keys.rotate_left = True
            state.keys.rotated_left = True
        elif not state.key_arr[3]:
            # rotate_left just released
            state.keys.rotated_left = False
        
        if state.key_arr[4] and not state.keys.rotated_right:
            # rotate_left just pressed
            state.keys.rotate_right = True
            state.keys.rotated_right = True
        elif not state.key_arr[4]:
            # rotate_left just released
            state.keys.rotated_right = False

        return True
    
    running = True
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == controls.down:
                state.keys.down_key = True
                state.keys.down = True
                state.keys.down_cd = constants.down_cooldown
            elif event.key == controls.left:
                state.keys.left_key = True
                state.keys.left = True
                state.keys.left_cd = constants.initial_cooldown
            elif event.key == controls.right:
                state.keys.right_key = True
                state.keys.right = True
                state.keys.right_cd = constants.initial_cooldown
            elif event.key == controls.rotate_left:
                state.keys.rotate_left = True
                state.keys.rotated_left = True
            elif event.key == controls.rotate_right:
                state.keys.rotate_right = True
                state.keys.rotated_right = True
        elif event.type == pygame.KEYUP:
            if event.key == controls.down:
                state.keys.down_key = False
            elif event.key == controls.left:
                state.keys.left_key = False
            elif event.key == controls.right:
                state.keys.right_key = False
            elif event.key == controls.rotate_left:
                state.keys.rotated_left = False
            elif event.key == controls.rotate_right:
                state.keys.rotated_right = False
        elif event.type == pygame.QUIT:
            running = False
    return running