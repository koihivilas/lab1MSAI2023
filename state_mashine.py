from state import State
from queue import PriorityQueue, Queue, LifoQueue
from settings import Settings as st
from map_field_states import Map_field_state
from position import Position
from map import Map
import time
import pygame
from typing import List

class StateMashine:
    def __init__(self, map : Map):
        self.map = map
    
    def __posible_actions(self, state : State):
        return self.map.get_posible_actions(state.agent.map_position)
    
    def __is_final(self, state : State):
        return self.map.is_treasure_position(state.agent.map_position)
    
    def __reconstruct_path(self, path : List[Position], new_state):
        self.map.change_nodes_states(path, new_state)
    
    def __reconstruct_node(self, node_position : Position, new_state):
        self.map.change_node_state(node_position, new_state)

    def bfs(self, s : State):
        open_set = list()
        open_set.append(s)

        while len(open_set) != 0:
            if st.has_step_delay:
                time.sleep(st.step_delay)
            
            current = open_set.pop(0)
            if self.__is_final(current):
                self.__reconstruct_path(current.agent.position_history[1:-1], Map_field_state.PATH)
                return current
            
            for action in self.__posible_actions(current):
                neighbor = current.move(action)
                position = neighbor.agent.get_position()
                neighbor_state = self.map.get_table()[position.y][position.x].get_state()
                if(neighbor_state not in [Map_field_state.START, Map_field_state.CLOSED, Map_field_state.OPEN]):
                    open_set.append(neighbor)
                    if st.shows_current_path:
                        self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.PATH)
                        yield False
                    if st.shows_current_path:
                        self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.CLOSED)
                    if not self.__is_final(neighbor):
                        self.__reconstruct_node(position, Map_field_state.OPEN)
            if current.agent.get_position() != self.map.get_start():
                self.__reconstruct_node(current.agent.get_position(), Map_field_state.CLOSED)
            yield False


