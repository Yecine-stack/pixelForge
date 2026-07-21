from engine.operations.resize import resize
from engine.operations.crop import crop
from engine.operations.rotate import rotate
from engine.operations.flip import flip
from engine.operations.brightness import adjust_brightness
from engine.operations.contrast import adjust_contrast
from engine.operations.filters import grayscale


class ImageProcessor:
    def resize(self, image, width, height):
        return resize(image, width, height)

    def crop(self, image, box):
        return crop(image, box)

    def rotate(self, image, angle):
        return rotate(image, angle)

    def flip(self, image, direction):
        return flip(image, direction)

    def brightness(self, image, factor):
        return adjust_brightness(image, factor)

    def contrast(self, image, factor):
        return adjust_contrast(image, factor)

    def grayscale(self, image):
        return grayscale(image)