from PIL import ImageDraw


class ShapeDrawer:
    def rectangle(self, image, start, end, color="black"):
        draw = ImageDraw.Draw(image)

        draw.rectangle(
            (
                start[0],
                start[1],
                end[0],
                end[1]
            ),
            outline=color
        )

        return image

    def line(self, image, start, end, color="black"):
        draw = ImageDraw.Draw(image)

        draw.line(
            (
                start[0],
                start[1],
                end[0],
                end[1]
            ),
            fill=color
        )

        return image