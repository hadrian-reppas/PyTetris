import constants
import draw
import game
import images

import pygame

def main():
    pygame.init()
    clock = pygame.time.Clock()

    width = constants.pixel_size*constants.NES_width
    height = constants.pixel_size*constants.NES_height
    screen = pygame.display.set_mode((width, height))

    state = game.init()
    surfaces = images.get_surfaces()

    running = True
    while running:
        state, running = game.update(state)
        draw.draw(state, surfaces, screen)
        clock.tick(constants.NES_frame_rate)

    pygame.quit()

if __name__ == '__main__':
    main()