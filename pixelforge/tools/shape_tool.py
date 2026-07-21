from tools.base_tool import BaseTool
from engine.drawing.shapes import ShapeDrawer


class ShapeTool(BaseTool):
    def __init__(self):
        self.shapes = ShapeDrawer()

    def rectangle(self, image, start, end):
        return self.shapes.rectangle(
            image,
            start,
            end
        )