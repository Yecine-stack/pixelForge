import tkinter as tk
from tkinter import ttk

class LayerPanel:
    def __init__(self, parent, document, callbacks):
        self.parent = parent
        self.document = document
        self.callbacks = callbacks
        
        self.frame = tk.Frame(parent, relief=tk.RAISED, bd=1)
        
        title_label = tk.Label(self.frame, text="Layers", font=('Arial', 10, 'bold'))
        title_label.pack(pady=5)
        
        self.layer_listbox = tk.Listbox(
            self.frame,
            height=10,
            width=20,
            selectmode=tk.SINGLE
        )
        self.layer_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.layer_listbox.bind('<<ListboxSelect>>', self.on_layer_select)
        
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=5)
        
        add_btn = tk.Button(
            button_frame,
            text="Add",
            width=6,
            command=self.add_layer
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = tk.Button(
            button_frame,
            text="Delete",
            width=6,
            command=self.delete_layer
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        visibility_btn = tk.Button(
            button_frame,
            text="Hide/Show",
            width=8,
            command=self.toggle_visibility
        )
        visibility_btn.pack(side=tk.LEFT, padx=2)
        
        move_up_btn = tk.Button(
            button_frame,
            text="▲",
            width=3,
            command=self.move_up
        )
        move_up_btn.pack(side=tk.LEFT, padx=2)
        
        move_down_btn = tk.Button(
            button_frame,
            text="▼",
            width=3,
            command=self.move_down
        )
        move_down_btn.pack(side=tk.LEFT, padx=2)
        
        self.update_layer_list()
        
    def update_layer_list(self):
        self.layer_listbox.delete(0, tk.END)
        
        for layer in self.document.layers:
            visibility = "👁" if layer.visible else "○"
            name = layer.name[:15]
            display_text = f"{visibility} {name}"
            self.layer_listbox.insert(tk.END, display_text)
        
        if self.document.active_layer_index >= 0:
            self.layer_listbox.selection_set(self.document.active_layer_index)
                
    def on_layer_select(self, event):
        selection = self.layer_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.document.layers):
                self.document.set_active_layer(index)
                if 'on_layer_select' in self.callbacks:
                    self.callbacks['on_layer_select']()
                self.update_layer_list()
                    
    def add_layer(self):
        if 'on_add_layer' in self.callbacks:
            self.callbacks['on_add_layer']()
        self.update_layer_list()
        self.layer_listbox.selection_set(self.document.active_layer_index)
        
    def delete_layer(self):
        selection = self.layer_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.document.layers):
                if 'on_delete_layer' in self.callbacks:
                    self.callbacks['on_delete_layer'](index)
                self.update_layer_list()
                if self.document.active_layer_index < len(self.document.layers):
                    self.layer_listbox.selection_set(self.document.active_layer_index)
            
    def toggle_visibility(self):
        selection = self.layer_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.document.layers):
                self.document.toggle_layer_visibility(index)
                self.update_layer_list()
                self.layer_listbox.selection_set(index)
                if 'on_visibility_change' in self.callbacks:
                    self.callbacks['on_visibility_change']()
                
    def move_up(self):
        selection = self.layer_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 < index < len(self.document.layers):
                self.document.move_layer_up(index)
                self.update_layer_list()
                self.layer_listbox.selection_set(index - 1)
                if 'on_layer_move' in self.callbacks:
                    self.callbacks['on_layer_move']()
                
    def move_down(self):
        selection = self.layer_listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.document.layers) - 1:
                self.document.move_layer_down(index)
                self.update_layer_list()
                self.layer_listbox.selection_set(index + 1)
                if 'on_layer_move' in self.callbacks:
                    self.callbacks['on_layer_move']()
                
    def show(self):
        self.frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
    def hide(self):
        self.frame.pack_forget()