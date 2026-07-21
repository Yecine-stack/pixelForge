from PIL import ImageDraw


class Eraser:
    def __init__(self, size=10):
        self.size = size

    def erase(self, image, original_image, points):
        draw = ImageDraw.Draw(image)

        original_pixels = original_image.load()

        for point in points:
            x, y = point

            for i in range(
                int(x - self.size),
                int(x + self.size)
            ):
                for j in range(
                    int(y - self.size),
                    int(y + self.size)
                ):
                    if (
                        0 <= i < image.width
                        and 0 <= j < image.height
                    ):
                        image.putpixel(
                            (i, j),
                            original_pixels[i, j]
                        )

        return image