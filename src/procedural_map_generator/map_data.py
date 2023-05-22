class MapData:
    def __init__(self, tile_count):
        self.tile_rules = { # [up, right, down, left]
            -1 : [-1, -1, -1, -1], # Empty
            0 : [0, 0, 0, 0], # Blank
            1 : [1, 1, 0, 1], # LeftUpRight
            2 : [0, 1, 1, 1], # LeftDownRight
            3 : [1, 0, 1, 1], # LeftUpDown
            4 : [1, 1, 1, 0], # RightUpDown
            5 : [0, 1, 0, 1], # Horizontal
            6 : [1, 0, 1, 0], # Vertical
            7 : [0, 0, 1, 1], # LeftDown
            8 : [1, 0, 0, 1], # LeftUp
            9 : [0, 1, 1, 0], # RightDown
            10 : [1, 1, 0, 0], # RightUp
            11 : [1, 1, 1, 1] # Intersection
        }

        self.create_tile_indices_matrix(tile_count)
        self.create_tile_possibilities_matrix(tile_count)

    def create_tile_indices_matrix(self, tile_count):
        self.tile_indices = [[self.tile_rules[-1] for _ in range(tile_count)] for _ in range(tile_count)]

    def create_tile_possibilities_matrix(self, tile_count):
        self.tile_possibilities = [[list(self.tile_rules.keys()) for _ in range(tile_count)] for _ in range(tile_count)]
