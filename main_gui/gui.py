import tkinter as tk
from tkinter import ttk, messagebox
from stub_generator.stub_gui import *
from typical_values.values_gui import *

HELP_TEXT = (
    "Tessy Generator GUI - Instrukcja obsługi:\n"
    "1. Ustaw liczbę wywołań (CALLS).\n"
    "2. '➕ Dodaj' - skopiuj deklaracje funkcji do schowka, kliknij przycisk, aby dodać do listy.\n"
    "3. '🏷 Generuj' - wygeneruj kod i wyświetl w polu poniżej.\n"
    "4. '💾 Zapisz' - zapisz zawartość pola do pliku .txt.\n"
    "5. '🔁 Aktualizuj' - zmień liczbę wywołań zaznaczonej funkcji.\n"
    "6. '🗑 Usuń' - usuń zaznaczoną funkcję z listy.\n"
    "7. '🧹 Wyczyść' - usuń wszystkie funkcje i wyczyść pole.\n"
    "8. Menu 'Pomoc' - wyświetla tę instrukcję.\n"
    )

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tessy Combo Tool")
        self.always_on_top_var = tk.BooleanVar(value=False)
        self._build_menu()
        self._build_tabs()
        self._build_widgets()
        self.root.mainloop()

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Instrukcja", command=self._show_help)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(label="Zawsze na widoku", variable=self.always_on_top_var, command=self._toggle_always_on_top )
        # view_menu.add_command(label="Zawsze na widoku", command=self._toggle_always_on_top )
        menubar.add_cascade(label="Widok", menu=view_menu)
        menubar.add_cascade(label="Pomoc", menu=help_menu)
        self.root.config(menu=menubar)

    def _build_tabs(self):
        tab_view = ttk.Notebook(self.root)
        tab_view.pack(fill="both", expand=True)

        # --- KARTA 1: PIERWSZA APLIKACJA ---
        self.typical_value_tab = tk.Frame(tab_view)
        tab_view.add(self.typical_value_tab, text="Typowe wartości")

        # --- KARTA 2: DRUGA APLIKACJA ---
        self.stub_generator_tab = tk.Frame(tab_view)
        tab_view.add(self.stub_generator_tab, text="Generator Stubów")

        tab_view.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _build_widgets(self):
        tessy_stub_generator = TessyGUI(self.root, self.stub_generator_tab)
        tessy_typical_values = TypicalValuesGUI(self.root, self.typical_value_tab)

    def _show_help(self):
        messagebox.showinfo("Pomoc - Tessy Generator GUI", HELP_TEXT)

    def _toggle_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())

    def _on_tab_change(self, event):
        selected_index = event.widget.index("current")

        if selected_index == 0:  # "Typowe wartości" — dynamiczne dopasowanie
            self.root.bind("<ButtonPress-1>", self._start_move)
            self.root.bind("<B1-Motion>", self._do_move)
            self.root.geometry("220x300")
        elif selected_index == 1:  # "Generator Stubów" — stały rozmiar
            self.root.unbind("<ButtonPress-1>")
            self.root.unbind("<B1-Motion>")
            self.root.geometry("1000x650")

    def _start_move(self, event):
        self.root.x = event.x_root
        self.root.y = event.y_root

    def _do_move(self, event):
        dx = event.x_root - self.root.x
        dy = event.y_root - self.root.y
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")
        self.root.x = event.x_root
        self.root.y = event.y_root