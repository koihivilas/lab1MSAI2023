from __future__ import annotations
from agent import Agent
from map import Map
from position import Direction

class State:
    def __init__(self, agent : Agent) -> None:
        self.agent = agent

    def move(self, action : Direction) -> State:
        new_agent_position = self.agent.map_position + action
        new_agent = Agent(new_agent_position, self.agent.position_history.copy())
        return State(new_agent)
    
    def copy(self):
        return State(self.agent)
    
    def __str__(self) -> str:
        return str(self.agent.map_position)
    
    def get_position(self):
        return self.agent.get_position()