from commands.command_manager import CommandManager
from commands.commands.draw_command import DrawCommand
from PIL import Image


class FakeDocument:
    def __init__(self, image):
        self.image = image

    def update_image(self, image):
        self.image = image


def test_undo_redo():
    image1 = Image.new("RGB", (10, 10), "white")
    image2 = Image.new("RGB", (10, 10), "black")

    document = FakeDocument(image1)

    command = DrawCommand(
        document,
        image1,
        image2
    )

    manager = CommandManager()

    manager.execute(command)

    assert document.image == image2

    manager.undo()

    assert document.image == image1

    manager.redo()

    assert document.image == image2