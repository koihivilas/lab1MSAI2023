from __future__ import annotations
from agent import Agent
from map import Map
from position import Direction

class State:
    def __init__(self, agent : Agent, map : Map) -> None:
        self.agent = agent
        self.map = map

    def posible_actions(self):
        return self.map.get_posible_actions(self.agent.map_position)
    
    def is_final(self):
        return self.map.is_treasure_position(self.agent.map_position)

    def move(self, action : Direction) -> State:
        new_agent_position = self.agent.map_position + action
        new_agent = Agent(new_agent_position, self.agent.position_history.copy())
        return State(new_agent, self.map)
    
    def copy(self):
        return State(self.agent, self.map)
    
    def __str__(self) -> str:
        return str(self.agent.map_position)
    
    def distance_to_nearest_treasure(self) -> int:
        treasure_positions = self.map.get_treasure_positions()
        agent_position = self.agent.get_position()
        lengths = [agent_position.manhattan(treasure_position) for treasure_position in treasure_positions]
        return min(lengths)