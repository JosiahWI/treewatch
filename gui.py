import pygame

import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

RADIUS = 5
MIN_MARGIN = 20

def start_gui(tree, callback):
    pygame.init()
    # Fit the screen width and height.
    display = pygame.display.set_mode((1000, 600))
    gui_init(display)
    callback()
    gui_loop(display, tree)
    pygame.quit()

def gui_init(main_display):
    clear_surface(main_display)

def clear_surface(surface):
    surface.fill(WHITE)

def gui_loop(main_display, tree):
    clock = pygame.time.Clock()
    while not pygame_have_quit_event():
        clock.tick(30)
        clear_surface(main_display)
        with tree:
            if not tree.is_empty():
                draw_tree(main_display, tree)
        pygame.display.flip();

def pygame_have_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    else:
        return False

def draw_tree(main_display, tree):
    max_width = get_max_width(tree)
    full_diameter = 2 * (RADIUS + MIN_MARGIN)
    max_pixel_width  = max_width * full_diameter
    left_edge = (main_display.get_width() - max_pixel_width) // 2

    def draw_tree_helper(node, index, depth):
        if node is None:
            return
        width = 1 << (depth - 1)
        space_per_node = max_pixel_width // width
        margin = (space_per_node - (2 * RADIUS)) // 2
        y = 50 + full_diameter * (depth - 1)
        x = left_edge + margin + RADIUS + space_per_node * index
        line_thickness = 0 if node.is_selected() else 2
        pygame.draw.circle(main_display, BLACK, (x, y), RADIUS, width=line_thickness)
        place_text(main_display, (x - MIN_MARGIN, y - MIN_MARGIN), str(node.value))
        left_child_pos = draw_tree_helper(node.left, 2 * index, depth + 1)
        if left_child_pos is not None:
            pygame.draw.line(main_display, RED, (x, y), left_child_pos)
        right_child_pos = draw_tree_helper(node.right, 2 * index + 1, depth + 1)
        if right_child_pos is not None:
            pygame.draw.line(main_display, RED, (x, y), right_child_pos)
        return (x, y)

    draw_tree_helper(tree.get_root(), 0, 1)

def place_text(main_display, pos, text):
    font = pygame.font.SysFont("Comic Sans MS", 25)
    text_surface = font.render(text, False, RED)
    main_display.blit(text_surface, pos)


def get_max_width(tree):
    return 1 << (tree.height())
