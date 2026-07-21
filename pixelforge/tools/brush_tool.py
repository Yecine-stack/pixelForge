from tools.base_tool import BaseTool
from engine.drawing.brush import Brush


class BrushTool(BaseTool):
    def __init__(self):
        self.brush = Brush()

    def apply(self, image, points):
        return self.brush.draw(image, points)