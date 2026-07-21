from PIL import Image

from engine.processor import ImageProcessor


def create_test_image():
    return Image.new("RGB", (100, 100), "red")


def test_resize():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.resize(image, 50, 50)

    assert result.size == (50, 50)


def test_crop():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.crop(image, (0, 0, 50, 50))

    assert result.size == (50, 50)


def test_rotate():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.rotate(image, 90)

    assert result.size == (100, 100)


def test_flip():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.flip(image, "horizontal")

    assert result.size == image.size


def test_brightness():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.brightness(image, 2)

    assert result.size == image.size


def test_contrast():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.contrast(image, 2)

    assert result.size == image.size


def test_grayscale():
    processor = ImageProcessor()
    image = create_test_image()

    result = processor.grayscale(image)

    assert result.mode == "L"


if __name__ == "__main__":
    test_resize()
    test_crop()
    test_rotate()
    test_flip()
    test_brightness()
    test_contrast()
    test_grayscale()

    print("All image processing tests passed")