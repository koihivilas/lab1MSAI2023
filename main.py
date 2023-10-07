import pygame
import math
import time
import random
from queue import PriorityQueue, Queue, LifoQueue
from settings import Settings as st
from thumbnail import Thumbnail
from table import Table
from node import Node
from window import Window
from map_field_states import Map_field_state
from map import Map
from event_types import Event_type
from state_machine import StateMachine
from state import State
from agent import Agent
from file_map_operator import File_map_operator
from text import Text
from file_browser import FileBrowser

# TODO: make possible to change heuristic from Manhatten to Euclidean or other
def heuristics(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def bi_reconstruct_path(came_from, current, draw):
    while current in came_from:
        current.set_state(st.path)
        current = came_from[current]

    draw()

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_state(st.path)

    draw()

def clear_path(came_from, current, draw):
    if st.has_path_delay:
        time.sleep(st.path_delay)

    while current in came_from:
        current = came_from[current]
        current.set_state(st.closed)

    draw()

def bfs_clear_path(grid, draw):
    for row in grid:
        for node in row:
            if node.has_state(st.path):
                node.set_state(st.closed)

    draw()

def count_path_length(came_from, current):
    length = 0
    while current in came_from:
        current = came_from[current]
        length += 1

    return length

def reset_map_state(grid):
    for row in grid:
        for node in row:
            if node.has_state(st.open) or node.has_state(st.closed) or node.has_state(st.path):
                node.reset()

def astar(draw, grid, start, end):
    count = 0 # to break ties if we have the same f-score
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # f-score, count, node
    came_from = {} # to reconstruct the path

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # distance from start to start is 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristics(start.get_pos(), end.get_pos()) # distance from start to end is heuristic

    open_set_hash = {start} # to check if node is in open set (priority queue)

    while not open_set.empty():
        if st.has_step_delay:
            time.sleep(st.step_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.set_state(st.start)
            end.set_state(st.treasure)
            return True

        for neighbor in current.neighbors:
            if st.shows_current_path:
                reconstruct_path(came_from, neighbor, draw)
                start.set_state(st.start)
                end.set_state(st.treasure)

            temp_g_score = g_score[current] + 1 # assume distance between two nodes is 1 (cause it's grid)

            if temp_g_score < g_score[neighbor]: # if we found better path
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristics(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_state(st.open)

            if st.shows_current_path:
                clear_path(came_from, neighbor, draw)
                start.set_state(st.start)
                end.set_state(st.treasure)

        draw()

        if current != start:
            current.set_state(st.closed)

    return False

# TODO: neighbors system is somehow broken and recalculating paths is not working properly (just visually)
def greedy(draw, grid, start, end):
    count = 0 # to break ties if we have the same f-score
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # f-score, count, node
    came_from = {} # to reconstruct the path

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # distance from start to start is 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristics(start.get_pos(), end.get_pos()) # distance from start to end is heuristic

    open_set_hash = {start} # to check if node is in open set (priority queue)

    while not open_set.empty():
        if st.has_step_delay:
            time.sleep(st.step_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.set_state(st.start)
            end.set_state(st.treasure)
            return True

        for neighbor in current.neighbors:
            if st.shows_current_path:
                reconstruct_path(came_from, neighbor, draw)
                start.set_state(st.start)
                end.set_state(st.treasure)

            temp_g_score = g_score[current] + 1 # assume distance between two nodes is 1 (cause it's grid)

            if temp_g_score < g_score[neighbor]: # if we found better path
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = heuristics(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_state(st.open)

            if st.shows_current_path:
                clear_path(came_from, neighbor, draw)
                start.set_state(st.start)
                end.set_state(st.treasure)

        draw()

        if current != start:
            current.set_state(st.closed)

    return False

def bfs(draw, map):
    end = None

    start = map.get_start()
    grid = map.get_table()

    open_set = Queue()
    open_set.put(start)
    came_from = {} # to reconstruct the path

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # distance from start to start is 0

    while not open_set.empty():
        if st.has_step_delay:
            time.sleep(st.step_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()

        if current.has_state(st.treasure):
            end = current
            reconstruct_path(came_from, end, draw)
            start.set_state(st.start)
            end.set_state(st.treasure)
            return end

        for neighbor in current.neighbors:
            if st.shows_current_path:
                reconstruct_path(came_from, neighbor, draw)
                start.set_state(st.start)

            if not neighbor.has_state(st.start) and not neighbor.has_state(st.open) and not neighbor.has_state(st.closed):
                came_from[neighbor] = current
                g_score[neighbor] = g_score[current] + 1
                open_set.put(neighbor)
                if not neighbor.has_state(st.treasure):
                    neighbor.set_state(st.open)

            if st.shows_current_path:
                bfs_clear_path(grid, draw)
                start.set_state(st.start)

        draw()

        if current != start:
            current.set_state(st.closed)

    return None

def dfs(draw, grid, start):
    end = None

    open_set = LifoQueue()
    open_set.put(start)
    came_from = {} # to reconstruct the path

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # distance from start to start is 0

    while not open_set.empty():
        if st.has_step_delay:
            time.sleep(st.step_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()

        if current.has_state(st.treasure):
            end = current
            reconstruct_path(came_from, end, draw)
            start.set_state(st.start)
            end.set_state(st.treasure)
            return end

        for neighbor in current.neighbors:
            if not neighbor.has_state(st.start) and not neighbor.has_state(st.open) and not neighbor.has_state(st.closed):
                came_from[neighbor] = current
                g_score[neighbor] = g_score[current] + 1
                open_set.put(neighbor)
                if not neighbor.has_state(st.treasure):
                    neighbor.set_state(st.open)

        draw()

        if current != start:
            current.set_state(st.closed)

    return None

# not really sure if it's correct version
def dfs_depth_limited(draw, grid, start, depth_limit):
    end = None

    open_set = LifoQueue()
    open_set.put(start)
    came_from = {} # to reconstruct the path

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # distance from start to start is 0

    while not open_set.empty():
        if st.has_step_delay:
            time.sleep(st.step_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()
        curr_depth = count_path_length(came_from, current)

        if curr_depth > depth_limit:
            continue

        if current.has_state(st.treasure):
            end = current
            reconstruct_path(came_from, end, draw)
            start.set_state(st.start)
            end.set_state(st.treasure)
            return end

        for neighbor in current.neighbors:
            if not neighbor.has_state(st.start) and not neighbor.has_state(st.open) and not neighbor.has_state(st.closed):
                came_from[neighbor] = current
                g_score[neighbor] = g_score[current] + 1
                open_set.put(neighbor)
                if not neighbor.has_state(st.treasure):
                    neighbor.set_state(st.open)

        draw()

        if current != start:
            current.set_state(st.closed)

    return None

def bi_directional(draw, grid, start, end):
    # part from start
    start_open_set = Queue()
    start_open_set.put(start)
    start_came_from = {} # to reconstruct the path
    start_visited = [start]

    # part from end
    end_open_set = Queue()
    end_open_set.put(end)
    end_came_from = {} # to reconstruct the path
    end_visited = [end]

    # making step and trying to find intersection
    while not start_open_set.empty() and not end_open_set.empty():
        if st.has_step_delay:
            time.sleep(st.step_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        common_visited = [x for x in start_visited if x in end_visited]
        if len(common_visited) > 0:
            common_element = common_visited[0]
            bi_reconstruct_path(start_came_from, common_element, draw)
            bi_reconstruct_path(end_came_from, common_element, draw)
            start.set_state(st.start)
            end.set_state(st.treasure)
            return True

        start_current = start_open_set.get()
        end_current = end_open_set.get()

        for neighbor in start_current.neighbors:
            if st.shows_current_path:
                reconstruct_path(start_came_from, neighbor, draw)
                start.set_state(st.start)

            if neighbor not in start_visited:
                start_came_from[neighbor] = start_current
                start_open_set.put(neighbor)
                start_visited.append(neighbor)
                if not neighbor.has_state(st.treasure):
                    neighbor.set_state(st.open)

            if st.shows_current_path:
                bfs_clear_path(grid, draw)
                start.set_state(st.start)

        draw()

        if start_current != start:
            start_current.set_state(st.closed)
            start_visited.append(start_current)

        for neighbor in end_current.neighbors:
            if st.shows_current_path:
                reconstruct_path(end_came_from, neighbor, draw)
                end.set_state(st.treasure)

            if neighbor not in end_visited:
                end_came_from[neighbor] = end_current
                end_open_set.put(neighbor)
                end_visited.append(neighbor)
                if not neighbor.has_state(st.start):
                    neighbor.set_state(st.open)

            if st.shows_current_path:
                bfs_clear_path(grid, draw)
                end.set_state(st.treasure)

        draw()

        if end_current != end:
            end_current.set_state(st.closed)
            end_visited.append(end_current)

    return False

def make_grid(rows, cols, node_size):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, node_size, rows, cols)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, cols, node_size, width, height):
    for i in range(rows + 1):
        pygame.draw.line(window, st.light_grey, (0, i * node_size), (width, i * node_size))

    for i in range(cols):
        pygame.draw.line(window, st.light_grey, (i * node_size, 0), (i * node_size, height))

def draw(window, grid, rows, cols, width, height, thumbnail):
    window.fill(st.white)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, cols, st.get_node_size(), width, height)
    thumbnail.draw(window)

    pygame.display.update()


def get_clicked_pos(pos, node_size):
    x, y = pos

    row = y // node_size
    col = x // node_size

    return row, col

def get_clicked_node(grid, node_size):
    pos = pygame.mouse.get_pos()
    row, col = get_clicked_pos(pos, node_size)

    return grid[row][col]

def set_node_state(start, node, thumbnail_state, treasures):
    if thumbnail_state == st.start:
        if not start and node not in treasures:
            node.set_state(st.start)
    elif thumbnail_state == st.treasure:
        if node != start and node not in treasures:
            node.set_state(st.treasure)
            treasures.append(node)
    elif thumbnail_state == st.exit:
        if node != start and node not in treasures:
            node.set_state(st.exit)

def set_node_state(start, node, thumbnail_state, treasures):
    if thumbnail_state == st.start and start:
        return
    if node != start and node not in treasures:
        node.set_state(thumbnail_state)
        if thumbnail_state == st.treasure:
            treasures.append(node)

def reset_node(node, treasures):
    if node.has_state(st.treasure):
        treasures.remove(node)

    node.reset()

def choose_end_node(treasures):
    if len(treasures) > 0:
        return random.choice(treasures)
    else:
        return None

def main(window, width, height):
    pygame.init()
    map = Map(st.rows, st.cols)

    #UI
    thumbnail = Thumbnail(Map_field_state.START,
                          st.thumbnail_size, st.thumbnail_margin_x, st.thumbnail_margin_y,
                          possible_states = [Map_field_state.START, Map_field_state.TREASURE, Map_field_state.EXIT])

    node_size = st.get_node_size()
    table = Table(0, 0, st.cols * node_size, st.rows * node_size, node_size, data_source = map, mouse_thumbnail = thumbnail)

    test_text = Text(table.get_width() // 2 + 10, table.get_height() // 2 + 10, 100, 100, "test")

    # btn = Button()

    main_window = Window(window, width, height)
    main_window.add_element(table, 1)
    main_window.add_element(test_text, 2)

    start = None
    end = None # for bfs not necessary

    treasures = []

    run = True

    generator_algorithm = None
    is_working = False

    while run:
        if(is_working):
            try:
                result = next(generator_algorithm)
            except StopIteration as ex:
                result = ex.value
                is_working = False
        main_window.draw()
        #TODO: Make EventHandler class
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEWHEEL:
                pos_x, pos_y = pygame.mouse.get_pos()
                if main_window.is_coordinates_in_boundaries(pos_x, pos_y):
                    main_window.event(Event_type.MOUSE_WHEEL, y = event.y)

            if pygame.mouse.get_pressed()[0]: # left click
                pos_x, pos_y = pygame.mouse.get_pos()
                if main_window.is_coordinates_in_boundaries(pos_x, pos_y):
                    main_window.event(Event_type.BUTTON_LEFT_PRESSED, x = pos_x, y = pos_y)

            elif pygame.mouse.get_pressed()[2]: # right click
                pos_x, pos_y = pygame.mouse.get_pos()
                if main_window.is_coordinates_in_boundaries(pos_x, pos_y):
                    main_window.event(Event_type.BUTTON_RIGHT_PRESSED, x = pos_x, y = pos_y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and True:
                    map.reset()
                    alg = StateMachine(map)
                    main_window.draw()

                    #for bfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    algorithm = alg.bfs
                    #for bidirectional bfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # algorithm = alg.bi_directional_bfs
                    #for astar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #algorithm = alg.astar
                    #for greedy !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #algorithm = alg.greedy
                    #for iterative_astar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # algorithm = alg.iterative_astar

                    if(not is_working):
                        s = State(Agent(map.get_start()))
                        generator_algorithm = iter(algorithm(s))
                        is_working = True
                        #time.sleep(2)
                    # for bi-directional !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # end = choose_end_node(treasures)
                    # if end:
                    #     for row in grid:
                    #         for node in row:
                    #             node.update_neighbors(grid)

                    #     reset_map_state(grid)
                    #     for treasure in treasures:
                    #         treasure.set_state(st.treasure)
                    #     bi_directional(lambda: draw(window, grid, st.rows, st.cols, width, height, thumbnail), grid, start, end)

                    # for dfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # for row in grid:
                    #     for node in row:
                    #         node.update_neighbors(grid)

                    # reset_map_state(grid)
                    # for treasure in treasures:
                    #     treasure.set_state(st.treasure)

                    # end = dfs_depth_limited(lambda: draw(window, grid, st.rows, size, thumbnail), grid, start, st.DEPTH_LIMIT)

                    # for dfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # for row in grid:
                    #     for node in row:
                    #         node.update_neighbors(grid)

                    # reset_map_state(grid)
                    # for treasure in treasures:
                    #     treasure.set_state(st.treasure)

                    # end = dfs(lambda: draw(window, grid, st.rows, st.cols, width, height, thumbnail), grid, start)

                    # for bfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    

                    # for astar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # end = choose_end_node(treasures)
                    # if end:
                    #     for row in grid:
                    #         for node in row:
                    #             node.update_neighbors(grid)

                    #     reset_map_state(grid)
                    #     for treasure in treasures:
                    #         treasure.set_state(st.treasure)
                    #     astar(lambda: draw(window, grid, st.rows, st.cols, width, height, thumbnail), grid, start, end)

                    # for greedy !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # end = choose_end_node(treasures)
                    # if end:
                    #     for row in grid:
                    #         for node in row:
                    #             node.update_neighbors(grid)

                    #     reset_map_state(grid)
                    #     for treasure in treasures:
                    #         treasure.set_state(st.treasure)
                    #     greedy(lambda: draw(window, grid, st.rows, st.cols, width, height, thumbnail), grid, start, end)

                if event.key == pygame.K_c:
                    map.clear()

                if event.key == pygame.K_r:
                    map.reset()

                if event.key == pygame.K_s:
                    operator = File_map_operator()
                    path_to_save = FileBrowser.prompt_savepath()
                    if path_to_save:
                        operator.write_map(map = map, file_path = path_to_save)
                    else:
                        operator.write_map(map = map, file_path = "map.txt")

                if event.key == pygame.K_l:
                    operator = File_map_operator()
                    filename = FileBrowser.prompt_file()
                    if filename:
                        map = operator.read_map(filename)
                    else:
                        map = operator.read_map("map.txt")
                    table.link_table(map)
                    map.reset()
                    main_window.draw()


    pygame.quit()

main(st.window, st.width, st.height)