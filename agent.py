from position import Position

class Agent:
    def __init__(self, agent_position : Position, position_history = None) -> None:
        if position_history == None:
            position_history = list()
        self.map_position = agent_position
        self.position_history = position_history
        self.position_history.append(agent_position)
    
    def get_position(self):
        return self.map_position