from tools.base_tool import BaseTool
from engine.drawing.eraser import Eraser


class EraserTool(BaseTool):
    def __init__(self):
        self.eraser = Eraser()

    def set_size(self, size):
        self.eraser.size = size

    def apply(self, image, points):
        return self.eraser.erase(image, points)