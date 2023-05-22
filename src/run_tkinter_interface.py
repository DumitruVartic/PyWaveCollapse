from tkinter import *
from PIL import Image, ImageTk
from image_handling.map_image_handler import save_map_as_image, get_map_as_image
from procedural_map_generator.map_generator import MapGenerator

class ImageViewer:
    def __init__(self):
        self.setup()

    def setup(self):
        self.root = Tk()
        self.root.title("Image Viewer")
        self.root.resizable(False, False)

        # Create a background default image
        self.size = (800, 800)
        background_color = "#264653"
        new_image = Image.new("RGB", self.size, background_color)
        self.default_image = ImageTk.PhotoImage(new_image)

        self.label = Label(image=self.default_image, anchor='center')
        self.label.pack(fill=BOTH, expand=True)

        # Entry field for tile number
        self.tile_number_entry = Entry(self.root)
        self.tile_number_entry.pack(side=LEFT, padx=10, pady=10)
        self.tile_number_entry.insert(0, "Enter number of tiles")

        self.create_button = Button(text="Create", command=self.create_image)
        self.create_button.pack(side=LEFT, padx=10, pady=10)

        self.reset_button = Button(text="Reset", command=self.reset_image)
        self.reset_button.pack(side=LEFT, padx=10, pady=10)

        self.save_button = Button(text="Save", command=self.save_image)
        self.save_button.pack(side=LEFT, padx=10, pady=10)

        # Event handler to remove the hint text when user clicks on the entry field
        self.tile_number_entry.bind("<FocusIn>", self.on_entry_click)

    def on_entry_click(self, event):
        """remove the hint text when user clicks on the entry field"""
        if self.tile_number_entry.get() == "Enter number of tiles":
            self.tile_number_entry.delete(0, END)

    def create_image(self):
        try: # if it is empty
            tile_number = int(self.tile_number_entry.get())  # Get tile number from entry field
        except:
            return
        
        self.Map = MapGenerator(tile_number)
        self.Map.run_wave_function_collapse()

        self.image = get_map_as_image(self.Map)
        self.image_original_size = self.image.size

        self.image = self.image.resize(self.size)
        self.new_image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.new_image)
        
    def reset_image(self):
        self.label.configure(image=self.default_image)
        self.image = None
        try:
            self.Map.reset()
        except:
            return

    def save_image(self):
        try: # if it wasn't created
            if self.image is not None:
                save_map_as_image(self.Map, self.image.resize(self.image_original_size))
        except:
            return
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    viewer = ImageViewer()
    viewer.run()
