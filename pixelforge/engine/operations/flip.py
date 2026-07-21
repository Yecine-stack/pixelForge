def flip(image, direction):
    if direction == "horizontal":
        return image.transpose(0)

    if direction == "vertical":
        return image.transpose(1)

    return image