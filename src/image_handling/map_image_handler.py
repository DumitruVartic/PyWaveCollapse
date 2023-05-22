from PIL import Image, ImageOps
from datetime import datetime
from os.path import dirname, join, abspath

def get_map_as_image(Map):
    return create_png(Map)

def save_map_as_image(Map, image=None): # if an image is already created it will be just saved with filename
    if image is None:
        image = create_png(Map)
    filename = "map_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".png"
    image.save(filename, optimize=True)

def create_png(Map):
    images = load_images()
    _, tile_size = images[0].size
    width = height = tile_size * Map.tile_count
    
    tiles_image = create_tiles_image(Map, images, tile_size, width, height)
    
    # resizing, because otherwise it will be (tile_size * tile_number) pixels width/height
    new_size = (1280, 1280) # how to to scale tile_size/images initialy, in order not to do this?
    image = ImageOps.fit(tiles_image, new_size, Image.ANTIALIAS)
    
    return image

def load_images(): # Loads the tile images required for creating the map image.
    # Images must be square
    # Match the names order with the tile rules order from the map_data
    image_names = ["Blank.png", "LeftUpRight.png", "LeftDownRight.png",
                    "LeftUpDown.png", "RightUpDown.png","Horizontal.png",
                    "Vertical.png", "LeftDown.png", "LeftUp.png", 
                    "RightDown.png", "RightUp.png", "Intersection.png"]
    images = {} # a dictionary containing the loaded images, indexed by their corresponding tile rule.
    current_path = dirname(abspath(__file__))
    for i,name in enumerate(image_names):
        path = join(current_path, "images", name)
        images[i] = Image.open(path) 
    return images

def create_tiles_image(Map, images, tile_size, width, height):
    # Create a new image by combining the tiles defined in Map with the given images
    image = Image.new(mode="RGB", size=(height, width))

    # Invert the tileRules dictionary, for easier finding of the image index
    # (tuple because list is unhashable and cannot be used as key)
    inverted_rules_dict = {tuple(v): k for k, v in Map.map_data.tile_rules.items()}

    # Loop over each tile in the map, find corresponding image by it's index and paste it.
    for row in range(Map.tile_count):
        for column in range(Map.tile_count):

            key = inverted_rules_dict.get(tuple(Map.map_data.tile_indices[row][column]))
            tileImage = images[key]
            image.paste(tileImage, (row * tile_size, column * tile_size))

    return image
