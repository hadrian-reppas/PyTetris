starting_level = 1

pixel_size = 2

# screen information

NES_width = 256
NES_height = 224
NES_frame_rate = 60.098813897441

# timing

start_delay = 160

initial_cooldown = 16
subsequent_cooldown = 6
down_cooldown = 2

fall_times = [48, 43, 38, 33, 28, 23, 18, 13,  8,  6,  5,  5,  5,  4,  4,
               4,  3,  3,  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2]

game_over_delay = 60
quit_on_game_over = False

# tetromino information
tetrominos = [
    [
        [(-1,  0), ( 0,  0), ( 1,  0), ( 0,  1)], # T down
        [( 0, -1), (-1,  0), ( 0,  0), ( 0,  1)], # T left
        [(-1,  0), ( 0,  0), ( 1,  0), ( 0, -1)], # T up
        [( 0, -1), ( 0,  0), ( 1,  0), ( 0,  1)], # T right
    ],
    [
        [(-1,  0), ( 0,  0), ( 1,  0), ( 1,  1)], # J down
        [( 0, -1), ( 0,  0), (-1,  1), ( 0,  1)], # J left
        [(-1, -1), (-1,  0), ( 0,  0), ( 1,  0)], # J up
        [( 0, -1), ( 1, -1), ( 0,  0), ( 0,  1)], # J right
    ],
    [
        [(-1,  0), ( 0,  0), ( 0,  1), ( 1,  1)], # Z horizontal
        [( 1, -1), ( 0,  0), ( 1,  0), ( 0,  1)], # Z vertical
    ],
    [
        [(-1,  0), ( 0,  0), (-1,  1), ( 0,  1)], # O only
    ],
    [
        [( 0,  0), ( 1,  0), (-1,  1), ( 0,  1)], # S horizontal
        [( 0, -1), ( 0,  0), ( 1,  0), ( 1,  1)], # S vertical
    ],
    [
        [(-1,  0), ( 0,  0), ( 1,  0), (-1,  1)], # L down
        [(-1, -1), ( 0, -1), ( 0,  0), ( 0,  1)], # L left
        [( 1, -1), (-1,  0), ( 0,  0), ( 1,  0)], # L up
        [( 0, -1), ( 0,  0), ( 0,  1), ( 1,  1)], # L right
    ],
    [
        [(-2,  0), (-1,  0), ( 0,  0), ( 1,  0)], # I horizontal
        [( 0, -2), ( 0, -1), ( 0,  0), ( 0,  1)], # I vertical
    ]
]

rotation_states = [4, 4, 2, 1, 2, 4, 2]

piece_probabilities = [0.1473, 0.1429, 0.1429, 0.1429, 0.1473, 0.1384, 0.1383]

square_colors = [0, 2, 1, 0, 2, 1, 0]

# scoring

soft_drop_bonus = 1

single_bonus = 40
double_bonus = 100
triple_bonus = 300
tetris_bonus = 1200

# screen positions

next_x = [204, 204, 204, 208, 204, 204, 208]
next_y = [112, 112, 112, 112, 112, 112, 116]

icon_x = [ 24,  24,  24,  24,  24,  24,  24]
icon_y = [ 80,  96, 112, 128, 144, 160, 184]
                   
stat_x = [ 48,  48,  48,  48,  48,  48,  48]
stat_y = [ 88, 104, 120, 136, 152, 168, 184]

board_x = 96
board_y = 40

type_x = 24
type_y = 24

lines_x = 152
lines_y = 16

top_score_x = 192
top_score_y = 32

score_x = 192
score_y = 56

level_x = 208
level_y = 160

# colors

def color(r, g, b):
    return 0xff000000 | (r << 16) | (g << 8) | b

black = color(  0,   0,   0)
red   = color(255,   0,   0)
blue  = color(  0,   0, 255)
white = color(255, 255, 255)

level_colors = [
    (color(  3,  59, 246), color( 51, 173, 251)),
    (color( 20, 156,   2), color(172, 252,  21)),
    (color(204,   0, 193), color(243,  88, 246)),
    (color(  3,  59, 246), color( 76, 212,  67)),
    (color(218,   0,  70), color( 79, 252, 134)),
    (color( 79, 252, 134), color( 85, 111, 251)),
    (color(243,  31,   7), color(105, 105, 105)),
    (color( 84,  33, 251), color(149,   0,  25)),
    (color(  3,  59, 246), color(243,  31,   7)),
    (color(243,  31,   7), color(249, 142,  53)),
]

red_text     = color(216,  40,   0)
white_text   = color(255, 255, 255)

scene_color  = color(116, 116, 116)
scene_accent = color(156, 252, 239)
flash_color  = color(255, 255, 255)

# sprite sheet information

sprite_file_path = 'resources/sprites.png'
scene_file_path = 'resources/scene.png'

icon_positions = [
    [
        [(4,  0), (4,  1), (4,  2)],
        [(5,  0), (5,  1), (5,  2)],
    ],
    [
        [(4,  9), (4, 10), (4, 11)],
        [(5,  9), (5, 10), (5, 11)],
    ],
    [
        [(4,  6), (4,  7), (4,  8)],
        [(5,  6), (5,  7), (5,  8)],
    ],
    [
        [(6,  0), (6,  1)],
        [(6,  2), (6,  3)],
    ],
    [
        [(4,  3), (4,  4), (4,  5)],
        [(5,  3), (5,  4), (5,  5)],
    ],
    [
        [(4, 12), (4, 13), (4, 14)],
        [(5, 12), (5, 13), (5, 14)],
    ],
    [
        [(6,  4), (6,  5), (6,  6)],
    ],
]
