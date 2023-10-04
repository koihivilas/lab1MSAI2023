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

    def heuristics(self, state : State):
        min = float('inf')
        treasures = self.map.get_treasure_positions()
        for treasure_position in treasures:
            distance = state.agent.get_position().manhattan(treasure_position)
            if distance < min:
                min = distance
        return min

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
                        yield
                    if st.shows_current_path:
                        self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.CLOSED)
                    if not self.__is_final(neighbor):
                        self.__reconstruct_node(position, Map_field_state.OPEN)
            if current.agent.get_position() != self.map.get_start():
                self.__reconstruct_node(current.agent.get_position(), Map_field_state.CLOSED)
            yield

    def astar(self, s : State):
        count = 0 # to break ties if we have the same f-score
        open_set = PriorityQueue()
        open_set.put((0, count, s)) # f-score, count, node

        grid = self.map.get_table()

        g_score = dict()
        g_score[s] = 0 # distance from start to start is 0

        f_score = dict()
        f_score[s] = self.heuristics(s) # distance from start to end is heuristic

        open_set_hash = {s} # to check if node is in open set (priority queue)

        while not open_set.empty():
            if st.has_step_delay:
                time.sleep(st.step_delay)

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if self.__is_final(current):
                self.__reconstruct_path(current.agent.position_history[1:-1], Map_field_state.PATH)
                return current

            for action in self.__posible_actions(current):
                neighbor = current.move(action)
                position = neighbor.agent.get_position()
                neighbor_state = self.map.get_table()[position.y][position.x].get_state()
                
                if st.shows_current_path:
                    self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.PATH)
                    yield

                if st.shows_current_path:
                    self.__reconstruct_path(neighbor.agent.position_history[1:-1], Map_field_state.CLOSED)
                
                temp_g_score = g_score[current] + 1 # assume distance between two nodes is 1 (cause it's grid)

                if temp_g_score < g_score.get(neighbor, float("inf")): # if we found better path
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristics(neighbor)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        if not self.__is_final(neighbor):
                            self.__reconstruct_node(position, Map_field_state.OPEN)
            if current.agent.get_position() != self.map.get_start():
                self.__reconstruct_node(current.agent.get_position(), Map_field_state.CLOSED)
            yield
        return False
