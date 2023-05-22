from image_handling.map_image_handler import save_map_as_image, get_map_as_image
from procedural_map_generator.map_generator import MapGenerator

if __name__ == '__main__':
    tile_count = 10
    Map = MapGenerator(tile_count)
    Map.generate()
    # print(Map.mapData.tilePosibility) # when there is an error, it can be observed that either an array is empty or an array has too many possibilities
    save_map_as_image(Map)