from position import Position
from settings import Settings as st
from enum import Enum, auto
from map import Map, Door_colors
from elements_container import Elements_container
class Agent:
    def __init__(self, agent_position : Position, position_history = None) -> None:
        if position_history == None:
            position_history = list()
        self.map_position = agent_position
        self.position_history = position_history
        self.position_history.append(agent_position)
    
    def reevaluate(self, position):
        pass

    def get_evaluation(self, position):
        return 100

    def get_position(self):
        return self.map_position
    
class Agent_assumption(Enum):
    potential_treasure = auto()
    treasure = auto()
    potential_exit = auto()
    weak_posible_exit = auto()
    exit = auto()
    only_empty = auto()
    empty = auto()
class PseudoCleverAgent:
    def __init__(self, agent_position : Position, position_history = None, map_knowlege = None) -> None:
        if position_history == None:
            position_history = list()
        self.map_position = agent_position
        self.position_history = position_history
        self.position_history.append(agent_position)
        self.weak_exit_cost = 2
        self.posible_exit_cost = 3
        self.real_exit_cost = 4
        self.potential_treasures_cost = -1
        self.treasure_cost = -100
        self.empty_cost = 2
        self.decay = 1
        if map_knowlege is None:
            self.map_knowlege = [[Agent_assumption.empty for i in range(st.cols)] for j in range(st.rows)]
        else:
            self.map_knowlege = map_knowlege
        self.map_evaluation = [[0 for i in range(st.cols)] for j in range(st.rows)]
        self.potential_treasures = []
        self.potential_exits = []
        self.weak_potential_exits = []
        self.real_exit = []
        self.real_treasure = []
    
    def reevaluate(self, position):
        map = Elements_container().elements["map"]
        self.map_knowlege[position.y][position.x] = Agent_assumption.only_empty
        for move in map.get_possible_moves(position):
            neighbor = position + move
            color = map.get_color_to(neighbor)
            if(color == Door_colors.black):
                self.map_knowlege[neighbor.y][neighbor.x] = Agent_assumption.exit
                self.real_exit.append(neighbor)
            if(color == Door_colors.white):
                self.map_knowlege[neighbor.y][neighbor.x] = Agent_assumption.treasure
                self.real_treasure.append(neighbor)
            if(color == Door_colors.blue):
                for deep_move in map.get_possible_moves(neighbor):
                    neighbor_of_neighbor = neighbor + deep_move
                    self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.only_empty
            near = {}
            for deep_move in map.get_possible_moves(neighbor):
                neighbor_of_neighbor = neighbor + deep_move
                assumption = self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x]
                near[assumption] = near.get(assumption, 0) + 1
            if(color == Door_colors.red):
                for deep_move in map.get_possible_moves(neighbor):
                    neighbor_of_neighbor = neighbor + deep_move
                    assumption = self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x]
                    if(assumption == Agent_assumption.empty):
                        if(near[Agent_assumption.only_empty] > 1):
                            self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.potential_exit
                        elif(Agent_assumption.exit in near.keys()):
                            self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.weak_posible_exit
                        else:
                            self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.potential_exit
                    elif(assumption == Agent_assumption.weak_posible_exit):
                        self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.potential_exit
                    elif(assumption == Agent_assumption.potential_exit):
                        self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.exit
            if(color == Door_colors.green):
                 for deep_move in map.get_possible_moves(neighbor):
                    neighbor_of_neighbor = neighbor + deep_move
                    assumption = self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x]
                    if(assumption == Agent_assumption.empty):
                        if(near[Agent_assumption.only_empty] > 1):
                            self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.treasure
                        elif(Agent_assumption.treasure in near.keys()):
                            self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.potential_treasure
                    elif(assumption == Agent_assumption.potential_treasure):
                        self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.treasure
                    elif(assumption == Agent_assumption.potential_exit):
                        if(Agent_assumption.treasure in near.keys()):
                            self.map_knowlege[neighbor_of_neighbor.y][neighbor_of_neighbor.x] = Agent_assumption.potential_treasure
        min_calc = 1000
        self.map_evaluation = [[0 for i in range(st.cols)] for j in range(st.rows)]
        for y in range(len(self.map_knowlege)):
            for x in range(len(self.map_knowlege[0])):
                empty_magic = True
                calc = self.map_evaluation[y][x]
                if self.map_knowlege[y][x] == Agent_assumption.potential_treasure:
                    calc += self.potential_treasures_cost
                elif self.map_knowlege[y][x] == Agent_assumption.treasure:
                    calc += self.treasure_cost
                elif self.map_knowlege[y][x] == Agent_assumption.potential_exit:
                    calc += self.posible_exit_cost
                elif self.map_knowlege[y][x] == Agent_assumption.weak_posible_exit:
                    calc += self.weak_exit_cost
                elif self.map_knowlege[y][x] == Agent_assumption.exit:
                    calc += self.real_exit_cost
                elif self.map_knowlege[y][x] == Agent_assumption.only_empty:
                    calc += self.empty_cost
                elif self.map_knowlege[y][x] == Agent_assumption.empty:
                    calc += self.empty_cost
                counter = 0
                for move in map.get_possible_moves(Position(x,y)):
                    counter += 1
                    if self.map_knowlege[y][x] == Agent_assumption.potential_treasure:
                        calc += self.potential_treasures_cost
                    elif self.map_knowlege[y][x] == Agent_assumption.treasure:
                        calc += self.treasure_cost
                    elif self.map_knowlege[y][x] == Agent_assumption.potential_exit:
                        calc += self.posible_exit_cost
                    elif self.map_knowlege[y][x] == Agent_assumption.weak_posible_exit:
                        calc += self.weak_exit_cost
                    elif self.map_knowlege[y][x] == Agent_assumption.exit:
                        calc += self.real_exit_cost
                    elif self.map_knowlege[y][x] == Agent_assumption.only_empty:
                        calc += self.empty_cost
                    elif self.map_knowlege[y][x] == Agent_assumption.empty:
                        calc += self.empty_cost
                calc -= counter * self.decay
                self.map_evaluation[y][x] = calc

    def get_evaluation(self, position):
        return self.map_evaluation[position.y][position.x]

    def get_position(self):
        return self.map_position
    
