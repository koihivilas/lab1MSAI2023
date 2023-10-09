from __future__ import annotations
from agent import Agent, PseudoCleverAgent
from map import Map
from position import Direction
from copy import deepcopy

class State:
    def __init__(self, agent : PseudoCleverAgent) -> None:
        self.agent = agent

    def move(self, action : Direction) -> State:
        new_agent_position = self.agent.map_position + action
        new_agent = PseudoCleverAgent(new_agent_position, self.agent.position_history.copy(), deepcopy(self.agent.map_knowlege))
        return State(new_agent)

    def __str__(self) -> str:
        return str(self.agent.map_position)
    
    def __repr__(self):
        return str(self.agent.map_position) + " " + str(len(self.agent.position_history))
    
    def __eq__(self, other):
        return self.agent.map_position == other.agent.map_position
    
    def __hash__(self) -> int:
        return self.agent.map_position.__hash__()

    def get_position(self):
        return self.agent.get_position()