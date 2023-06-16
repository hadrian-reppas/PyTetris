import constants
import game

import pygame

def draw(state, surfaces, screen):
    draw_scene(state, surfaces, screen)
    draw_statistics(state, surfaces, screen)
    draw_type(state, surfaces, screen)
    draw_lines(state, surfaces, screen)
    draw_scores(state, surfaces, screen)
    draw_level(state, surfaces, screen)
    draw_next(state, surfaces, screen)
    draw_board(state, surfaces, screen)
    draw_piece(state, surfaces, screen)
    pygame.display.flip()

def draw_number(n, digits, chars, x, y, screen):
    s = str(n % 10**digits).rjust(digits, '0')
    for c in s:
        screen.blit(chars[ord(c) - ord('0')], (x, y))
        x += chars[0].get_width()

def draw_scene(state, surfaces, screen):
    line_clear = state.stage == game.animation_stage.line_clear
    is_tetris = line_clear and len(state.full_lines) == 4
    if is_tetris and state.animation_timer % 5 < 2:
        screen.blit(surfaces.flash_scene, (0, 0))
    else:
        screen.blit(surfaces.scene, (0, 0))

def draw_statistics(state, surfaces, screen):
    icons = surfaces.icons[state.level % 10]
    stats = state.statistics
    chars = surfaces.red_chars
    for i in range(7):
        icon_x = constants.pixel_size*constants.icon_x[i]
        icon_y = constants.pixel_size*constants.icon_y[i]
        screen.blit(icons[i], (icon_x, icon_y))
        stat_x = constants.pixel_size*constants.stat_x[i]
        stat_y = constants.pixel_size*constants.stat_y[i]
        draw_number(stats[i], 3, chars, stat_x, stat_y, screen)

def draw_type(state, surfaces, screen):
    char = surfaces.white_chars[11 - state.a_type]
    x = constants.pixel_size*constants.type_x
    y = constants.pixel_size*constants.type_y
    screen.blit(char, (x, y))

def draw_lines(state, surfaces, screen):
    x = constants.pixel_size*constants.lines_x
    y = constants.pixel_size*constants.lines_y
    chars = surfaces.white_chars
    draw_number(state.lines, 3, chars, x, y, screen)

def draw_scores(state, surfaces, screen):
    chars = surfaces.white_chars
    top_x = constants.pixel_size*constants.top_score_x
    top_y = constants.pixel_size*constants.top_score_y
    draw_number(state.top_score, 6, chars, top_x, top_y, screen)
    score_x = constants.pixel_size*constants.score_x
    score_y = constants.pixel_size*constants.score_y
    draw_number(state.score, 6, chars, score_x, score_y, screen)

def draw_level(state, surfaces, screen):
    x = constants.pixel_size*constants.level_x
    y = constants.pixel_size*constants.level_y
    chars = surfaces.white_chars
    draw_number(state.level, 2, chars, x, y, screen)

def draw_next(state, surfaces, screen):
    square_color = constants.square_colors[state.next_piece]
    square = surfaces.squares[state.level % 10][square_color]
    piece = constants.tetrominos[state.next_piece][0]
    center_x = constants.pixel_size*constants.next_x[state.next_piece]
    center_y = constants.pixel_size*constants.next_y[state.next_piece]
    for dx, dy in piece:
        x = center_x + 8*constants.pixel_size*dx
        y = center_y + 8*constants.pixel_size*dy
        screen.blit(square, (x, y))

def draw_board(state, surfaces, screen):
    squares = surfaces.squares[state.level % 10]
    for i in range(20):
        y = constants.pixel_size*(constants.board_y + 8*i)
        for j in range(10):
            x = constants.pixel_size*(constants.board_x + 8*j)
            if state.board[i][j] is not None:
                screen.blit(squares[state.board[i][j]], (x, y))
    if state.stage == game.animation_stage.line_clear:
        remove_squares = 5 - state.animation_timer // 4
        for line in state.full_lines:
            y = constants.pixel_size*(constants.board_y + 8*line)
            for i in range(remove_squares):
                size = 8*constants.pixel_size
                x1 = constants.pixel_size*(constants.board_x + 8*(5 + i))
                r1 = pygame.Rect(x1, y, size, size)
                x2 = constants.pixel_size*(constants.board_x + 8*(4 - i))
                r2 = pygame.Rect(x2, y, size, size)
                pygame.draw.rect(screen, constants.black, r1)
                pygame.draw.rect(screen, constants.black, r2)
    elif state.stage == game.animation_stage.game_over:
        diff = 84 + constants.game_over_delay - state.animation_timer
        bars = min(diff//4, 20)
        c1, c2 = constants.level_colors[state.level % 10]
        x = constants.pixel_size*constants.board_x
        w = 80*constants.pixel_size
        for i in range(bars):
            y = constants.pixel_size*(constants.board_y + 8*i)
            r1 = pygame.Rect(x, y, w, 2*constants.pixel_size)
            y += 2*constants.pixel_size
            r2 = pygame.Rect(x, y, w, 3*constants.pixel_size)
            y += 3*constants.pixel_size
            r3 = pygame.Rect(x, y, w, 2*constants.pixel_size)
            pygame.draw.rect(screen, c1, r1)
            pygame.draw.rect(screen, constants.white, r2)
            pygame.draw.rect(screen, c2, r3)

def draw_piece(state, surfaces, screen):
    if state.stage != game.animation_stage.play:
        return
    square_color = constants.square_colors[state.piece]
    square = surfaces.squares[state.level % 10][square_color]
    piece = constants.tetrominos[state.piece][state.piece_pos.rot]
    center_x = constants.pixel_size*(constants.board_x + 8*state.piece_pos.col)
    center_y = constants.pixel_size*(constants.board_y + 8*state.piece_pos.row)
    for dx, dy in piece:
        x = center_x + 8*constants.pixel_size*dx
        y = center_y + 8*constants.pixel_size*dy
        if y >= constants.pixel_size*constants.board_y:
            screen.blit(square, (x, y))