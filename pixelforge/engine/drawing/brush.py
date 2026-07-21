from PIL import ImageDraw


class Brush:
    def __init__(self, size=5, color="black"):
        self.size = size
        self.color = color

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def draw(self, image, points):
        draw = ImageDraw.Draw(image)

        for point in points:
            x, y = point

            draw.ellipse(
                (
                    x - self.size,
                    y - self.size,
                    x + self.size,
                    y + self.size
                ),
                fill=self.color
            )

        return image