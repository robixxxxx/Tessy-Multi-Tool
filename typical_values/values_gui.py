import tkinter as tk
from tkinter import ttk
from typical_values.values_logic import *


class TypicalValuesGUI:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self._build_widgets()

    def _build_widgets(self):
        self.selected_type = tk.StringVar(value="int8")
        type_menu = ttk.Combobox(self.frame, textvariable=self.selected_type, values=list(types.keys()), state="readonly")
        type_menu.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        type_menu.bind("<<ComboboxSelected>>", self.update_labels)

        for i, key in enumerate(label_order):
            name_lbl = tk.Label(self.frame, text=f"{key}:", font=("Consolas", 14), anchor="w")
            name_lbl.grid(row=i+1, column=0, padx=(5, 2), pady=5, sticky="e")
            name_labels[key] = name_lbl

            value_lbl = tk.Label(self.frame, text="", font=("Consolas", 14), cursor="hand2", anchor="w")
            value_lbl.grid(row=i+1, column=1, padx=(2, 5), pady=5, sticky="w")
            value_lbl.bind("<Button-1>", self.copy_to_clipboard)
            labels[key] = value_lbl

        self.status_label = tk.Label(self.frame, text="", font=("Arial", 10), fg="green")
        self.status_label.grid(row=len(label_order)+1, column=0, columnspan=2, pady=5)
        self.update_labels()


    def update_labels(self, *args):
        type_name = self.selected_type.get()
        result = calculate(type_name)

        for key in label_order:
            value = result.get(key, "")
            if value == "":
                labels[key].config(state="disabled", text="")
            else:
                labels[key].config(state="normal", text=value)
        self.frame.update_idletasks()

    def copy_to_clipboard(self, event):
        widget = event.widget
        value = widget.cget("text")
        if value == "":
            return

        type_name = self.selected_type.get()
        result = calculate(type_name)

        reverse_lookup = {v: k for k, v in result.items() if v}
        label_type = reverse_lookup.get(value, None)

        if label_type == "Środek":
            clipboard_content = value
        elif label_type:
            clipboard_content = f"/* {value} */\n*{label_type}*"
            clipboard_content = clipboard_content.casefold()
        else:
            clipboard_content = value

        self.frame.clipboard_clear()
        self.frame.clipboard_append(clipboard_content)
        self.status_label.config(text=f"Skopiowano: {clipboard_content}")