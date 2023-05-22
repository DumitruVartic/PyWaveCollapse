from random import randint
from .map_data import MapData # why i need to make it relative?, if there is a problem remove dot or add it -> (.map_data)

class MapGenerator: # wave function collapse alghorithm implementation
    next_tiles = []
    def __init__(self, tile_count): # tile_count -> number_of_tiles in the square matrix
        self.tile_count = tile_count
        self.map_data = MapData(self.tile_count)
    
    def reset(self):
        self.map_data.tile_indices.clear()
        self.map_data.tile_possibilities.clear()
        self.map_data.create_tile_indices_matrix(self.tile_count)
        self.map_data.create_tile_possibilities_matrix(self.tile_count)

    def run_wave_function_collapse(self):
        # Choose a random starting position
        matrix_position = randint(0, (self.tile_count * self.tile_count) - 1)
        x, y = self.get_positions(matrix_position)
        tile_index = randint(0, len(self.map_data.tile_rules) - 2)
        self.place_tile_on_position(x, y, tile_index)
        self.check_neighbors(x, y, tile_index)
        
        # Loop until there are no more empty tiles
        while self.exists_empty_tiles(): # checking exists_empty_tiles every iteration, instead better do this after placing a new tile
            if self.collapsed(): # reductant (outside the loop same code)
                self.place_tile_by_posibility_list()
                # break # if they are already collapsed no need to continue this loop?

            # Choose the next tile to fill
            self.next_tiles = [i for i in self.next_tiles if i is not None]
            # if not self.next_tiles:
            #     break
            x, y, tile_index = self.next_tiles.pop()

            # Place the tile if there's only one possibility
            # The dumbest thing alive, if there is only one, then place IT, not tile_index
            if len(self.map_data.tile_possibilities[x][y]) == 1: # reductant (*if this code will be eliminated the eliminate_invalid_tiles() will do the same thing)) 
                self.place_tile_on_position(x, y, tile_index) # eliminate_invalid_tiles() is replacing this code?!
                # print(self.map_data.tile_possibilities[x][y][0])
                # print([x, y, tile_index])
                # maybe check here-> if not self.exists_empty_tiles(): break, instead of checking every turn?

            # Eliminate invalid tile possibilities
            self.eliminate_invalid_tiles(x, y, [tile_index])
            self.check_neighbors(x, y, tile_index)

        # Fill any remaining empty tiles, (more like fill the collapsed tiles, but it is already did inside the loop)
        if self.collapsed():
            self.place_tile_by_posibility_list()

    def get_positions(self, position):
        x = int(position / self.tile_count)
        y = int(position % self.tile_count)
        return x, y
    
    def exists_empty_tiles(self):
        return any(self.check_if_empty(i, j) for i in range(self.tile_count) for j in range(self.tile_count))
    
    def check_if_empty(self, x, y):
        return self.map_data.tile_indices[x][y] == self.map_data.tile_rules[-1]

    def collapsed(self):
        return all(len(self.map_data.tile_possibilities[i][j]) == 1 for i in range(self.tile_count) for j in range(self.tile_count))

    def place_tile_by_posibility_list(self):
        for i in range(self.tile_count):
            for j in range(self.tile_count):
                self.place_tile_on_position(i, j, self.map_data.tile_possibilities[i][j][0])

    def place_tile_on_position(self, x, y, tile_index):
        if self.check_if_empty(x, y):
            # print(self.map_data.tile_rules[tile_index])
            try:
                self.map_data.tile_indices[x][y] = self.map_data.tile_rules[tile_index] # tile_indices may be useless?
            except:
                print(self.map_data.tile_rules[tile_index])
            # if tile_possibilities is collapsig then it will remain only one tile in each cell
            # so there can be no point of using tile_indices at all, the resulted map will be in tile_possibilities matrix already 

    def eliminate_invalid_tiles(self, x, y, valid): 
        # too many purposes, why it is placing tiles?, 
        # this initialy was only supposed to eliminate the impossible tiles from the tile_possibilities matrix on each index
        if len(self.map_data.tile_possibilities[x][y]) == 1: # if there remained only one tile then place it automatically 
            self.place_tile_on_position(x, y, self.map_data.tile_possibilities[x][y][0])
            return # is this return needed?
        self.map_data.tile_possibilities[x][y] = [value for value in self.map_data.tile_possibilities[x][y] if value in valid] # the intended code in this method, it 
        # ^^^ It eliminates from tile_possibilities matrix tiles that are not in valid, 
        # ^^^ and also it can make this tile_possibilities matrix empty which wasn't intended and shouldn't happen
        if (self.map_data.tile_possibilities[x][y] == []): # ?
            self.place_tile_on_position(x, y, valid[0])
            return # is this return needed?
        # code bellow (or not only bellow...) is used for appending new tiles to next_tiles in check_neighbors()?
        # better split this in 2 separate methods maybe
        # it is doing it absolutely random
        length = len(self.map_data.tile_possibilities[x][y]) - 1 
        if (length > 0):
            position = self.map_data.tile_possibilities[x][y][randint(0, length)]
            return [x, y, position]

    def check_neighbors(self, x, y, tile_index): 
        # Checks for valid neighboring tiles in each direction (up, right, down, left) and adds them to the next tile queue if they match the current tile's rules.
        # A neighboring tile is valid if its edge rule for the opposite side matches the current tile's edge rule for the current side.
        # Example: the 'up' rule for tile is on index 0,
        # but for face that is above us we need rule for 'bottom' side to connect it with our 'up' side -> so it is on index 2
        
        # Directions moves: up (0, -1), right (1, 0), down (0, 1), and left (-1, 0)
        # Sides 'matching' rules indexes: up (0, 2), right (1, 3), down (2, 0), and left (3, 1)
        for dx, dy, current_side_index, target_side_index in [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]:
            if 0 <= x + dx < self.tile_count and 0 <= y + dy < self.tile_count:
                
                # valid_options = []
                # for i in range(len(self.mapData.tileRules) - 1):
                #     adjacent_tile_rules = self.mapData.tileRules[i]
                #     if adjacent_tile_rules[d] == self.mapData.tileRules[Tile][s]: # So if two rules for the sides == then they can connect (maybe it need to be only when it's 1 == 1, and not 0? so it tryly 'connects')
                #         valid_options.append(i)

                valid_options = [i for i in range(len(self.map_data.tile_rules) - 1)
                                    if self.map_data.tile_rules[tile_index][current_side_index] == self.map_data.tile_rules[i][target_side_index]]
                if valid_options:
                    self.next_tiles.append(self.eliminate_invalid_tiles(x + dx, y + dy, valid_options))