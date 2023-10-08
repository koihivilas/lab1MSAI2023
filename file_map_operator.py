from map import Map, Position
class File_map_operator:
    def __read_until_delimiter(self, file, delimetr):
            word = ''
            while True:
                symbol = file.read(1)
                if not symbol:
                    return None
                if(symbol == delimetr):
                    yield word
                    word = ''
                word += symbol

    def read_map(self, file_path) -> Map:
        try:
            file = open(file_path, "r")
            read_int = lambda : int(self.__read_until_delimiter(file, ' ').__next__())
            map_width = read_int()
            map_height = read_int()
            start_x = read_int()
            start_y = read_int()
            start_position = Position(start_x, start_y) 
            exit_positions = []
            treasure_positions = []
            amount_of_treasures = read_int()
            for _ in range(amount_of_treasures):
                treasure_x = read_int()
                treasure_y = read_int()
                treasure_positions.append(Position(treasure_x, treasure_y))
            amount_of_exits = read_int()
            for _ in range(amount_of_exits):
                exit_x = read_int()
                exit_y = read_int()
                exit_positions.append(Position(exit_x, exit_y))
        except FileNotFoundError:
            raise Exception("File not found")
        except Exception:
            raise Exception("File corrupted")
        finally:
            file.close()
        return Map(map_height, map_width, start_position = start_position, exits_positions = exit_positions, trasures_positions = treasure_positions)

    def write_map(self, file_path, map : Map) -> None:
        with open(file_path, "w") as file:
            write = lambda number: file.write(str(number) + ' ')
            write(map.get_width())
            write(map.get_heigth())
            start_position = map.get_start()
            write(start_position.x)
            write(start_position.y)
            treasure_positions = map.get_treasure_positions()
            write(len(treasure_positions))
            for treasure_position in treasure_positions:
                write(treasure_position.x)
                write(treasure_position.y)
            exit_positions = map.get_exit_positions()
            write(len(exit_positions))
            for exit_position in exit_positions:
                write(exit_position.x)
                write(exit_position.y)