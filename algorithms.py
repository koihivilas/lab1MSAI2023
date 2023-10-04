from state import State
from queue import PriorityQueue, Queue, LifoQueue
from settings import Settings as st
from map_field_states import Map_field_state
from position import Position
from map import Map
import time
import pygame
from typing import List

class Algorythms:
    def __init__(self, map : Map):
        self.__map = map
    
    def __reconstruct_path(self, path : List[Position], new_state):
        self.__map.change_nodes_states(path, new_state)
    
    def __reconstruct_node(self, node_position : Position, new_state):
        self.__map.change_node_state(node_position, new_state)

    def bfs(self, s : State):
        open_set = list()
        open_set.append(s)

        while len(open_set) != 0:
            if st.has_step_delay:
                time.sleep(st.step_delay)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            current = open_set.pop(0)
            if current.is_final():
                self.__reconstruct_path(current.agent.position_history[1:-1], Map_field_state.PATH)
                return current
            
            for action in current.posible_actions():
                neighbor = current.move(action)
                neighbor_state = neighbor.map.get_table()[neighbor.agent.get_position().y][neighbor.agent.get_position().x].get_state()
                if(neighbor_state not in [Map_field_state.START, Map_field_state.CLOSED, Map_field_state.OPEN]):
                    open_set.append(neighbor)
                    if st.shows_current_path:
                        self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.PATH)
                        yield False
                    if st.shows_current_path:
                        self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.CLOSED)
                    if not neighbor.is_final():
                        self.__reconstruct_node(neighbor.agent.get_position(), Map_field_state.OPEN)
            if current.agent.get_position() != current.map.get_start():
                self.__reconstruct_node(current.agent.get_position(), Map_field_state.CLOSED)
            yield False


