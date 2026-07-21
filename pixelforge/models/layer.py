from PIL import Image

class Layer:
    def __init__(self, name, image, visible=True, opacity=255):
        self.name = name
        self.image = image.copy() if image else None
        self.visible = visible
        self.opacity = opacity
        
    def copy(self):
        new_layer = Layer(
            self.name + "_copy",
            self.image.copy() if self.image else None,
            self.visible,
            self.opacity
        )
        return new_layer
    
    def set_image(self, image):
        self.image = image.copy() if image else None
        
    def is_visible(self):
        return self.visible and self.image is not None