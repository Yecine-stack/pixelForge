class BaseCommand:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError