from commands.base_command import BaseCommand


class DrawCommand(BaseCommand):
    def __init__(self, document, before_image, after_image):
        self.document = document
        self.before_image = before_image
        self.after_image = after_image

    def execute(self):
        self.document.update_image(
            self.after_image
        )

    def undo(self):
        self.document.update_image(
            self.before_image
        )