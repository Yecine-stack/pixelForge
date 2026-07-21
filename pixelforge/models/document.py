from PIL import Image
from models.layer import Layer

class Document:
    def __init__(self):
        self.layers = []
        self.active_layer_index = -1
        self.composited_image = None
        self.file_path = None
        self.modified = False
        self.width = 800
        self.height = 600
        
    def add_layer(self, layer, index=None):
        if index is None:
            index = len(self.layers)
        self.layers.insert(index, layer)
        self.active_layer_index = index
        self.modified = True
        self.composite()
        
    def remove_layer(self, index):
        if 0 <= index < len(self.layers):
            if len(self.layers) == 1:
                return False
                
            del self.layers[index]
            
            if self.active_layer_index >= len(self.layers):
                self.active_layer_index = len(self.layers) - 1
            elif self.active_layer_index == index:
                self.active_layer_index = max(0, index - 1)
                
            self.modified = True
            self.composite()
            return True
        return False
        
    def get_active_layer(self):
        if 0 <= self.active_layer_index < len(self.layers):
            return self.layers[self.active_layer_index]
        return None
        
    def set_active_layer(self, index):
        if 0 <= index < len(self.layers):
            self.active_layer_index = index
            
    def set_active_layer_image(self, image):
        layer = self.get_active_layer()
        if layer:
            layer.set_image(image)
            self.modified = True
            self.composite()
            
    def get_active_layer_image(self):
        layer = self.get_active_layer()
        return layer.image if layer else None
        
    def composite(self):
        if not self.layers:
            self.composited_image = None
            return
            
        composite = None
        for layer in self.layers:
            if layer.is_visible():
                if composite is None:
                    composite = layer.image.copy()
                else:
                    composite = Image.alpha_composite(
                        composite.convert('RGBA'),
                        layer.image.convert('RGBA')
                    )
                    
        self.composited_image = composite
        
    def set_image(self, image, file_path=None):
        self.layers = []
        self.file_path = file_path
        self.width, self.height = image.size
        
        base_layer = Layer("Background", image.copy())
        self.add_layer(base_layer, 0)
        self.active_layer_index = 0
        self.modified = False
        self.composite()
        
    def update_image(self, image):
        self.set_active_layer_image(image)
        
    def create_empty_layer(self, name="Layer"):
        if self.composited_image:
            size = self.composited_image.size
        else:
            size = (self.width, self.height)
            
        empty_image = Image.new('RGBA', size, (0, 0, 0, 0))
        layer = Layer(name, empty_image)
        self.add_layer(layer)
        return layer
        
    def get_layer_count(self):
        return len(self.layers)
        
    def get_layer_names(self):
        return [layer.name for layer in self.layers]
        
    def get_visible_layers_count(self):
        return sum(1 for layer in self.layers if layer.is_visible())
        
    def toggle_layer_visibility(self, index):
        if 0 <= index < len(self.layers):
            self.layers[index].visible = not self.layers[index].visible
            self.modified = True
            self.composite()
            
    def move_layer_up(self, index):
        if 0 <= index < len(self.layers) - 1:
            self.layers[index], self.layers[index + 1] = self.layers[index + 1], self.layers[index]
            if self.active_layer_index == index:
                self.active_layer_index = index + 1
            elif self.active_layer_index == index + 1:
                self.active_layer_index = index
            self.modified = True
            self.composite()
            
    def move_layer_down(self, index):
        if 0 < index < len(self.layers):
            self.layers[index], self.layers[index - 1] = self.layers[index - 1], self.layers[index]
            if self.active_layer_index == index:
                self.active_layer_index = index - 1
            elif self.active_layer_index == index - 1:
                self.active_layer_index = index
            self.modified = True
            self.composite()