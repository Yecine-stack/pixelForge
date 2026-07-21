import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import ImageTk

from storage.image_loader import ImageLoader
from storage.image_exporter import ImageExporter
from models.document import Document
from models.layer import Layer
from engine.processor import ImageProcessor
from ui.toolbar import Toolbar
from ui.widgets.brush_selector import BrushSelector
from ui.widgets.color_picker import ColorPicker
from ui.layer_panel import LayerPanel
from commands.commands.draw_command import DrawCommand

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PixelForge")

        self.document = Document()
        self.loader = ImageLoader()
        self.exporter = ImageExporter()
        self.processor = ImageProcessor()
        self.original_image = None

        from commands.command_manager import CommandManager
        self.command_manager = CommandManager()

        from engine.drawing.brush import Brush
        from engine.drawing.eraser import Eraser

        self.brush = Brush()
        self.eraser = Eraser()

        self.drawing = False
        self.brush_active = False
        self.eraser_active = False
        self.last_point = None
        self.stroke_before_image = None

        self.canvas = tk.Canvas(
            self.root,
            width=800,
            height=600
        )

        self.canvas.bind(
            "<ButtonPress-1>",
            self.start_draw
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.draw
        )
        
        self.canvas.bind(
            "<ButtonRelease-1>",
            self.end_draw
        )
        
        self.canvas.pack(side=tk.LEFT, padx=5, pady=5)

        self.tk_image = None

        self.toolbar = Toolbar(
            self.root,
            {
                "brush": self.activate_brush,
                "eraser": self.activate_eraser,
                "grayscale": self.apply_grayscale,
                "rotate": self.apply_rotate,
                "flip_horizontal": self.apply_flip_horizontal,
                "flip_vertical": self.apply_flip_vertical,
                "resize": self.apply_resize,
                "undo": self.undo,
                "redo": self.redo
            }
        )
        self.toolbar.show()

        self.brush_selector = BrushSelector(
            self.root,
            self.change_brush_size
        )

        self.brush_selector.show()

        self.color_picker = ColorPicker(
            self.root,
            self.change_brush_color
        )

        self.color_picker.show()

        self.layer_panel = LayerPanel(
            self.root,
            self.document,
            {
                'on_layer_select': self.on_layer_selected,
                'on_add_layer': self.add_layer,
                'on_delete_layer': self.delete_layer,
                'on_visibility_change': self.on_visibility_changed,
                'on_layer_move': self.on_layer_moved
            }
        )
        self.layer_panel.show()

        self.create_menu()
        
        self.create_empty_document()

    def create_empty_document(self):
        from PIL import Image
        width, height = 800, 600
        self.document.width = width
        self.document.height = height
        
        empty_image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
        base_layer = Layer("Background", empty_image)
        self.document.add_layer(base_layer, 0)
        self.document.active_layer_index = 0
        self.document.composite()
        self.display_image()

    def create_menu(self):
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(
            label="Open",
            command=self.open_image
        )
        file_menu.add_command(
            label="Export",
            command=self.export_image
        )

        menu.add_cascade(
            label="File",
            menu=file_menu
        )

        self.root.config(menu=menu)

    def open_image(self):
        path = filedialog.askopenfilename()

        if path:
            image = self.loader.load(path)
            self.original_image = image.copy()
            self.document.set_image(image, path)
            self.layer_panel.update_layer_list()
            self.display_image()

    def display_image(self):
        if self.document.composited_image:
            self.tk_image = ImageTk.PhotoImage(
                self.document.composited_image
            )

            self.canvas.delete("all")

            self.canvas.create_image(
                400,
                300,
                image=self.tk_image
            )

    def activate_brush(self):
        self.brush_active = not self.brush_active
        self.eraser_active = False

    def activate_eraser(self):
        self.eraser_active = not self.eraser_active
        self.brush_active = False

    def change_brush_size(self, size):
        self.brush.set_size(size)
        self.eraser.size = size

    def change_brush_color(self, color):
        self.brush.set_color(color)

    def start_draw(self, event):
        if (self.brush_active or self.eraser_active) and self.document.get_active_layer_image():
            layer_image = self.document.get_active_layer_image()
            self.stroke_before_image = layer_image.copy()
            
            image_width, image_height = layer_image.size

            canvas_x = event.x - (400 - image_width / 2)
            canvas_y = event.y - (300 - image_height / 2)

            self.last_point = (
                canvas_x,
                canvas_y
            )

    def draw(self, event):
        if (self.brush_active or self.eraser_active) and self.document.get_active_layer_image() and self.last_point and self.stroke_before_image is not None:

            active_image = self.document.get_active_layer_image()
            image_width, image_height = active_image.size

            canvas_x = event.x - (400 - image_width / 2)
            canvas_y = event.y - (300 - image_height / 2)

            temp_image = active_image.copy()

            if self.brush_active:
                image = self.brush.draw(
                    temp_image,
                    [
                        self.last_point,
                        (canvas_x, canvas_y)
                    ]
                )

            elif self.eraser_active:
                image = self.eraser.erase(
                    temp_image,
                    self.original_image,
                    [
                        self.last_point,
                        (canvas_x, canvas_y)
                    ]
                )

            self.document.set_active_layer_image(image)

            self.last_point = (
                canvas_x,
                canvas_y
            )

            self.display_image()

    def end_draw(self, event):
        if (
            self.stroke_before_image is not None
            and self.document.get_active_layer_image() is not None
            and self.stroke_before_image != self.document.get_active_layer_image()
        ):
            command = DrawCommand(
                self.document,
                self.stroke_before_image,
                self.document.get_active_layer_image().copy()
            )
            
            self.command_manager.execute(command)

        self.stroke_before_image = None
        self.last_point = None

    def apply_grayscale(self):
        if self.document.get_active_layer_image():
            image = self.processor.grayscale(
                self.document.get_active_layer_image()
            )
            self.document.set_active_layer_image(image)
            self.display_image()

    def apply_rotate(self):
        if self.document.get_active_layer_image():
            image = self.processor.rotate(
                self.document.get_active_layer_image(),
                90
            )
            self.document.set_active_layer_image(image)
            self.display_image()

    def apply_flip_horizontal(self):
        if self.document.get_active_layer_image():
            image = self.processor.flip(
                self.document.get_active_layer_image(),
                "horizontal"
            )
            self.document.set_active_layer_image(image)
            self.display_image()

    def apply_flip_vertical(self):
        if self.document.get_active_layer_image():
            image = self.processor.flip(
                self.document.get_active_layer_image(),
                "vertical"
            )
            self.document.set_active_layer_image(image)
            self.display_image()

    def apply_resize(self):
        if self.document.get_active_layer_image():
            dialog = tk.Toplevel(self.root)
            dialog.title("Resize")

            tk.Label(dialog, text="Width:").pack()
            width_entry = tk.Entry(dialog)
            width_entry.pack()

            tk.Label(dialog, text="Height:").pack()
            height_entry = tk.Entry(dialog)
            height_entry.pack()

            def apply_resize():
                width = int(width_entry.get())
                height = int(height_entry.get())

                image = self.processor.resize(
                    self.document.get_active_layer_image(),
                    width,
                    height
                )

                self.document.set_active_layer_image(image)
                self.display_image()
                dialog.destroy()

            tk.Button(
                dialog,
                text="Apply",
                command=apply_resize
            ).pack()

    def undo(self):
        self.command_manager.undo()
        self.layer_panel.update_layer_list()
        self.display_image()

    def redo(self):
        self.command_manager.redo()
        self.layer_panel.update_layer_list()
        self.display_image()

    def export_image(self):
        if self.document.composited_image:
            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg")
                ]
            )

            if path:
                self.exporter.export(
                    self.document.composited_image,
                    path
                )

    def on_layer_selected(self):
        self.display_image()

    def add_layer(self):
        self.document.create_empty_layer(f"Layer {self.document.get_layer_count()}")
        self.layer_panel.update_layer_list()
        self.display_image()

    def delete_layer(self, index):
        if self.document.remove_layer(index):
            self.layer_panel.update_layer_list()
            self.display_image()

    def on_visibility_changed(self):
        self.display_image()

    def on_layer_moved(self):
        self.display_image()

    def show(self):
        self.root.mainloop()