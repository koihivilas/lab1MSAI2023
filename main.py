import tkinter
from tkinter import filedialog
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
from agent import Agent, PseudoCleverAgent
from file_map_operator import File_map_operator
from enum import Enum, auto
from event_handler import Event_handler, Event
import pygame
from elements_container import Elements_container
from text import Text
from stats import Stats as stats

def clear():
    map = Elements_container().elements["map"]
    map.clear()
    stats.reset_stats()
    app_state_change(Elements_container().elements["app_state"], AppState.drawing)

def reset():
    map = Elements_container().elements["map"]
    map.reset()
    stats.reset_stats()
    app_state_change(Elements_container().elements["app_state"], AppState.drawing)

def save_map():
    path_to_save = tkinter.filedialog.asksaveasfilename(defaultextension='.txt', initialfile = 'my_map')
    if path_to_save:
        stats.reset_stats()
        map = Elements_container().elements["map"]
        operator = File_map_operator()
        operator.write_map(map = map, file_path = path_to_save)
        app_state_change(Elements_container().elements["app_state"], AppState.drawing)

def load_map():
    filetypes = (
                            ('maps', '*.txt'),
                            ('All files', '*.*')
                        )
    filename = tkinter.filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        stats.reset_stats()
        operator = File_map_operator()
        table = Elements_container().elements["table"]
        map = operator.read_map(filename)
        table.link_table(map)
        map.reset()
        Elements_container().elements["map"] = map
        app_state_change(Elements_container().elements["app_state"], AppState.drawing)

class AppState(Enum):
    starting = auto()
    drawing = auto()
    working = auto()
    paused = auto()

def app_state_change(current_state : AppState, new_state : AppState):
    map = Elements_container().elements["map"]
    table = Elements_container().elements["table"]
    thumbnail = Elements_container().elements["table_thumbnail"]
    event_handler = Event_handler()
    if(new_state == AppState.drawing):
        Elements_container().elements["app_state"] = AppState.drawing
        if(current_state == AppState.starting):
            event_handler.add_handler(Event_type.ON_KEY_S,
                                    save_map)
            event_handler.add_handler(Event_type.ON_KEY_L,
                                    load_map)   
            event_handler.add_handler(Event_type.ON_K_SPACE,
                                    start_algorithm)
            table.enable_events()
        elif(current_state == AppState.working):
            event_handler.remove_handler(Event_type.ON_K_SPACE,
                                    pause_algorithm)
            event_handler.remove_handler(Event_type.BEFORE_DRAW,
                                    algroithm_step)
            table.enable_events()
            event_handler.add_handler(Event_type.ON_KEY_S,
                                    save_map)
            event_handler.add_handler(Event_type.ON_KEY_L,
                                    load_map)   
            event_handler.add_handler(Event_type.ON_K_SPACE,
                                    start_algorithm)
        elif(current_state == AppState.paused):
            event_handler.remove_handler(Event_type.ON_K_SPACE,
                                    continue_algorithm)
            table.enable_events()
            event_handler.add_handler(Event_type.ON_KEY_S,
                                    save_map)
            event_handler.add_handler(Event_type.ON_KEY_L,
                                    load_map)   
            event_handler.add_handler(Event_type.ON_K_SPACE,
                                    start_algorithm)
        elif(current_state == AppState.drawing):
            pass
    if(new_state == AppState.working):
        Elements_container().elements["app_state"] = AppState.working
        if(current_state == AppState.drawing):
            event_handler.remove_handler(Event_type.ON_KEY_S,
                                    save_map)
            event_handler.remove_handler(Event_type.ON_KEY_L,
                                    load_map)  
            event_handler.remove_handler(Event_type.ON_K_SPACE,
                                    start_algorithm)
            table.disable_events()
            event_handler.add_handler(Event_type.ON_K_SPACE,
                                    pause_algorithm)
            event_handler.add_handler(Event_type.BEFORE_DRAW,
                                    algroithm_step)
        if(current_state == AppState.paused):
            event_handler.remove_handler(Event_type.ON_K_SPACE,
                                    continue_algorithm)
            event_handler.add_handler(Event_type.ON_K_SPACE,
                                    pause_algorithm)      
            event_handler.add_handler(Event_type.BEFORE_DRAW,
                                    algroithm_step)    
    if(new_state == AppState.paused):
        Elements_container().elements["app_state"] = AppState.paused
        if(current_state == AppState.working):
            event_handler.remove_handler(Event_type.ON_K_SPACE,
                                    pause_algorithm)  
            event_handler.remove_handler(Event_type.BEFORE_DRAW,
                                    algroithm_step)
            event_handler.add_handler(Event_type.ON_K_SPACE,
                                    continue_algorithm)

def algroithm_step():
    try:
        result = next(Elements_container().elements["generator_algorithm"])
        stats.iterations += 1
        stats.visited_nodes = Elements_container().elements["map"].count_visited_nodes()
    except StopIteration as ex:
        result = ex.value
        if result is None:
            #TODO: Say something like world will suffer, path not found
            pass
        app_state_change(AppState.working, AppState.drawing)

def start_algorithm():
    map = Elements_container().elements["map"]
    map.reset()
    stats.reset_stats()
    alg = StateMachine(map)

    #for bfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #algorithm = alg.bfs
    # for dfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # algorithm = alg.dfs
    # for dfs_limited !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # algorithm = alg.dfs_limited
    # for bidirectional bfs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # algorithm = alg.bi_directional_bfs
    #for astar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    algorithm = alg.astar
    #for greedy !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # algorithm = alg.greedy
    #for iterative_astar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # algorithm = alg.iterative_astar
    start = map.get_start()
    if(start == None):
        #TODO: Show that start is needed
        pass
    else:
        s = State(PseudoCleverAgent(start))
        Elements_container().elements["generator_algorithm"] = iter(algorithm(s)) # TODO: None it some moment
        app_state_change(AppState.drawing, AppState.working)   

def pause_algorithm():
    app_state_change(AppState.working, AppState.paused)

def continue_algorithm():
    app_state_change(AppState.paused, AppState.working)

def update_stats():
    Elements_container().elements["max_fringe_size_value"].set_text(str(stats.max_fringe_size))
    Elements_container().elements["visited_nodes_value"].set_text(str(stats.visited_nodes))
    Elements_container().elements["path_length_value"].set_text(str(stats.path_length))
    Elements_container().elements["iterations_value"].set_text(str(stats.iterations))

def main(window, width, height):
    pygame.init()
    map = Map(st.rows, st.cols)

    Elements_container().add_element("map", map)
    Elements_container().add_element("generator_algorithm", None)
    Elements_container().add_element("app_state", AppState.starting)
    #UI
    thumbnail = Thumbnail("table_thumbnail", Map_field_state.START,
                          st.thumbnail_size, st.thumbnail_margin_x, st.thumbnail_margin_y,
                          possible_states = [Map_field_state.START, Map_field_state.TREASURE, Map_field_state.EXIT])

    node_size = st.get_node_size()
    table = Table("table", 0, 0, st.cols * node_size, st.rows * node_size, node_size, data_source = map, mouse_thumbnail = thumbnail)
    # stats text
    max_fringe_size_text = Text("max_fringe_size_text", 10, table.get_height() + 10, 100, 100, "Max fringe size: ")
    max_fringe_size_value = Text("max_fringe_size_value",max_fringe_size_text.get_width() + 10, table.get_height() + 10, 100, 100, "0")
    visited_nodes_text = Text("visited_nodes_text",10, table.get_height() + max_fringe_size_text.get_height() + 10, 100, 100, "Visited nodes: ")
    visited_nodes_value = Text("visited_nodes_value",visited_nodes_text.get_width() + 10, table.get_height() + max_fringe_size_text.get_height() + 10, 100, 100, "0")
    path_length_text = Text("path_length_text",10, table.get_height() + max_fringe_size_text.get_height() + visited_nodes_text.get_height() + 10, 100, 100, "Path length: ")
    path_length_value = Text("path_length_value",path_length_text.get_width() + 10, table.get_height() + max_fringe_size_text.get_height() + visited_nodes_text.get_height() + 10, 100, 100, "0")
    iterations_text = Text("iterations_text",10, table.get_height() + max_fringe_size_text.get_height() + visited_nodes_text.get_height() + path_length_text.get_height() + 10, 100, 100, "Iterations: ")
    iterations_value = Text("iterations_value",iterations_text.get_width() + 10, table.get_height() + max_fringe_size_text.get_height() + visited_nodes_text.get_height() + path_length_text.get_height() + 10, 100, 100, "0")
    main_window = Window("main_window", window, width, height)
    main_window.add_element(table, 1)
    main_window.add_element(max_fringe_size_text, 2)
    main_window.add_element(max_fringe_size_value, 2)
    main_window.add_element(visited_nodes_text, 2)
    main_window.add_element(visited_nodes_value, 2)
    main_window.add_element(path_length_text, 2)
    main_window.add_element(path_length_value, 2)
    main_window.add_element(iterations_text, 2)
    main_window.add_element(iterations_value, 2)
    
    run = True

    #register events
    event_handler = Event_handler()
    event_handler.add_handler(Event_type.BEFORE_DRAW,
                              lambda: window.fill(st.white))
    event_handler.add_handler(Event_type.BEFORE_DRAW, update_stats)
    event_handler.add_handler(Event_type.AFTER_DRAW,
                              pygame.display.update)
    event_handler.add_handler(Event_type.ON_KEY_C,
                              clear)
    event_handler.add_handler(Event_type.ON_KEY_R,
                              reset)
    app_state_change(AppState.starting, AppState.drawing)
    
    while run:
        Event_handler().events[Event_type.BEFORE_DRAW.name].invoke()
        main_window.draw()
        Event_handler().events[Event_type.AFTER_DRAW.name].invoke()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            Event_handler().handle_pygame(event, main_window)

    pygame.quit()

main(st.window, st.width, st.height)