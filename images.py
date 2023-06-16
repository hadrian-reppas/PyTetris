import constants

import pygame
from dataclasses import dataclass

@dataclass
class surface_holder:
    scene: pygame.Surface
    flash_scene: pygame.Surface
    red_chars: list[pygame.Surface]
    white_chars: list[pygame.Surface]
    squares: list[list[pygame.Surface]]
    icons: list[list[pygame.Surface]]

def get_surfaces():
    falsecolor_scene = pygame.image.load(constants.scene_file_path).convert()
    scene = get_scene(falsecolor_scene, False)
    flash_scene = get_scene(falsecolor_scene, True)

    sprite_sheet = pygame.image.load(constants.sprite_file_path).convert()
    red_chars = get_chars(sprite_sheet, constants.red_text)
    white_chars = get_chars(sprite_sheet, constants.white_text)
    squares = get_squares(sprite_sheet)
    icons = get_icons(sprite_sheet)
    
    return surface_holder(
        scene,
        flash_scene,
        red_chars,
        white_chars,
        squares,
        icons,
    )

def replace_colors(falsecolor_surface, replace_red, replace_blue):
    width, height = falsecolor_surface.get_size()
    pixels = pygame.PixelArray(falsecolor_surface.copy())  
    for x in range(width):
        for y in range(height):
            color = pixels[x, y]
            if color == constants.red:
                pixels[x, y] = replace_red
            elif color == constants.blue:
                pixels[x, y] = replace_blue
            else:
                if not (color == constants.black or color == constants.white):
                    print(x, y, color)
    return pixels.surface

def join_surfaces(surfaces):
    width = sum(surface.get_width() for surface in surfaces[0])
    height = sum(row[0].get_height() for row in surfaces)
    joined = pygame.Surface((width, height))
    y = 0
    for row in surfaces:
        x = 0
        for surface in row:
            joined.blit(surface, (x, y))
            x += surface.get_width()
        y += row[0].get_height()
    return joined

def resize_surface(surface, n):
    width = n*surface.get_width()
    height = n*surface.get_height()
    resized = pygame.Surface((width, height))
    old_pixels = pygame.PixelArray(surface)
    pixels = pygame.PixelArray(resized)
    for x in range(width):
        for y in range(height):
            pixels[x, y] = old_pixels[x//n, y//n]
    return pixels.surface

def get_scene(falsecolor_scene, flash):
    c1 = constants.flash_color if flash else constants.scene_color
    c2 = constants.scene_accent
    scene = replace_colors(falsecolor_scene, c1, c2)
    return resize_surface(scene, constants.pixel_size).convert()

def get_sprite(sprite_sheet, row, col):
    sprite = pygame.Surface((8, 8))
    sprite.blit(sprite_sheet, (0, 0), (8*col, 8*row, 8, 8))
    return sprite

def get_chars(sprite_sheet, color):
    chars = []
    for i in range(36):
        row, col = divmod(i, 16)
        falsecolor = get_sprite(sprite_sheet, row, col)
        char = replace_colors(falsecolor, color, None)
        char = resize_surface(char, constants.pixel_size).convert()
        chars.append(char)
    return chars

def get_squares(sprite_sheet):
    falsecolor = []
    for i in range(3):
        square = get_sprite(sprite_sheet, 7, 11 + i)
        falsecolor.append(square)
    squares = []
    for c1, c2 in constants.level_colors:
        sqrs = [replace_colors(fc, c1, c2) for fc in falsecolor]
        sqrs = [resize_surface(s, constants.pixel_size) for s in sqrs]
        squares.append(sqrs)
    return squares

def get_icons(sprite_sheet):
    falsecolor = []
    for positions in constants.icon_positions:
        icon = []
        for pos_row in positions:
            icon_row = []
            for row, col in pos_row:
                sprite = get_sprite(sprite_sheet, row, col)
                icon_row.append(sprite)
            icon.append(icon_row)
        falsecolor.append(join_surfaces(icon))
    icons = []
    for c1, c2 in constants.level_colors:
        icns = [replace_colors(fc, c1, c2) for fc in falsecolor]
        icns = [resize_surface(i, constants.pixel_size) for i in icns]
        icons.append(icns)
    return icons