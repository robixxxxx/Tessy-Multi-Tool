import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import pyperclip
from stub_generator.utils import parse_function_signature
from stub_generator.generator import gen_declarations, gen_definitions, gen_prolog, gen_stub

selected_func_index = None

class TessyGUI:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.stored_functions = []
        self.selected_index = None
        self._build_widgets()

    def _build_widgets(self):
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(4, weight=3)
        for i in range(7):                       
            self.frame.grid_columnconfigure(i, weight=1)

        tk.Label(self.frame, text="📥 Liczba wywołań (CALLS):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.call_entry = tk.Entry(self.frame)
        self.call_entry.insert(0, "2")
        self.call_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)

        buttons = [
            ("➕ Dodaj", self.add_function),
            ("🏷 Generuj", self.generate_output),
            ("💾 Zapisz", self.save_to_file),
            ("🔁 Aktualizuj", self.update_selected),
            ("🗑 Usuń", self.delete_selected),
            ("🧹 Wyczyść", self.clear_all)
        ]
        for i, (txt, cmd) in enumerate(buttons, start=2):
            tk.Button(self.frame, text=txt, command=cmd).grid(row=0, column=i, sticky="we", padx=2, pady=5)

        tk.Label(self.frame, text="📜 Zapisane funkcje:").grid(row=1, column=0, columnspan=7, sticky="w", padx=5, pady=(10, 0))
        self.func_listbox = tk.Listbox(self.frame)
        self.func_listbox.grid(row=2, column=0, columnspan=7, sticky="nsew", padx=5, pady=5)

        tk.Label(self.frame, text="📂 Podgląd wyniku:").grid(row=3, column=0, columnspan=7, sticky="w", padx=5, pady=(10, 0))
        self.output_text = scrolledtext.ScrolledText(self.frame)
        self.output_text.grid(row=4, column=0, columnspan=7, sticky="nsew", padx=5, pady=5)

    def show_argument_selector_popup(self, master, arguments, on_confirm_callback):
        popup = tk.Toplevel(master)
        popup.title("Wybierz argumenty")
        popup.transient(master)       # Ustaw jako popup
        popup.grab_set()              # Modalne okno

        check_vars = []

        for arg in arguments:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(popup, text=f"{arg.type} {arg.name}", variable=var)
            cb.pack(anchor="w", padx=10)
            check_vars.append(var)

        def on_submit():
            selected_args = [arg for arg, var in zip(arguments, check_vars) if var.get()]
            popup.grab_release()
            popup.destroy()
            on_confirm_callback(selected_args)

        tk.Button(popup, text="Zatwierdź", command=on_submit).pack(pady=10)

    def add_function(self):
        sig = pyperclip.paste().strip()
        if not sig:
            messagebox.showwarning("Brak danych", "Schowek jest pusty!")
            return
        parsed = parse_function_signature(sig)
        
        def on_arguments_selected(selected_args):
                parsed["arguments"] = selected_args           

        if not parsed:
            messagebox.showerror("Błąd", "Nie udało się sparsować funkcji.")
            return
        try:
            cnt = int(self.call_entry.get())
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną liczbę wywołań.")
            return
        parsed['n_calls'] = cnt
        self.stored_functions.append(parsed)
        self.func_listbox.insert(tk.END, f"{parsed['name']} (calls: {cnt})")
        self.show_argument_selector_popup(self.root, parsed["arguments"], on_arguments_selected)

    def generate_output(self):
        self.output_text.delete('1.0', tk.END)
        if not self.stored_functions:
            return
        
        declarations = ["//// ===================== DECLARATIONS ====================="]
        definitions = ["//// ===================== DEFINITIONS ====================="]
        prologs = ["//// ===================== PROLOGS ====================="]
        stubs = ["//// ===================== STUBS ====================="]

        for func in self.stored_functions:
            name = func["name"]
            args = func["arguments"]
            ret = func["ret_type"]
            n_calls = func["n_calls"]

            declarations.append(f"/// --- Function: {name} ---\n{gen_declarations(name, args, ret, n_calls)}")
            definitions.append(f"/// --- Function: {name} ---\n{gen_definitions(name, args, ret)}")
            prologs.append(f"/// --- Function: {name} ---\n{gen_prolog(name, args, ret, n_calls)}")
            stubs.append(f"/// --- Function: {name} ---\n{gen_stub(name, args, ret)}")

        text = "\n\n".join(declarations + definitions + prologs + stubs)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def save_to_file(self):
        data = self.output_text.get('1.0', tk.END)
        if not data.strip():
            messagebox.showwarning("Brak danych", "Brak danych do zapisania.")
            return
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files','*.txt')])
        if not path: return
        try:
            with open(path,'w',encoding='utf-8') as f: f.write(data)
            messagebox.showinfo("Zapisane", f"Zapisano dane do: {path}")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", str(e))

    def on_select(self, event):
        sel = event.widget.curselection()
        self.selected_index = sel[0] if sel else None
        if self.selected_index is not None:
            cnt = self.stored_functions[self.selected_index]['n_calls']
            self.call_entry.delete(0, tk.END)
            self.call_entry.insert(0, str(cnt))

    def update_selected(self):
        global selected_func_index

        sel = self.func_listbox.curselection()
        if not sel:
            messagebox.showwarning("Brak wyboru", "Nie wybrano funkcji do edycji.")
            return
        idx = sel[0]  # zachowujemy zaznaczenie nawet po edycji pola
        try:
            new_calls = int(self.call_entry.get())
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną liczbę wywołań.")
            return
        # Aktualizacja wewnętrznej listy
        self.stored_functions[idx]['n_calls'] = new_calls
        func_name = self.stored_functions[idx]['name']
        # Odświeżenie listboxa
        self.func_listbox.delete(idx)
        self.func_listbox.insert(idx, f"{func_name} (calls: {new_calls})")
        self.func_listbox.select_set(idx)
        self.func_listbox.activate(idx)
        self.func_listbox.see(idx)
        messagebox.showinfo("Zaktualizowano", f"Liczba wywołań dla '{func_name}' została zmieniona.")


    def delete_selected(self):
        global selected_func_index
        sel = self.func_listbox.curselection()
        if not sel:
            messagebox.showwarning("Brak wyboru", "Nie wybrano funkcji do usunięcia.")
            return
        idx = sel[0]
        name = self.stored_functions[idx]['name']
        if not messagebox.askyesno("Potwierdź", f"Usuń funkcję '{name}'?" ):
            return
        del self.stored_functions[idx]
        self.func_listbox.delete(idx)
        self.selected_index = None

    def clear_all(self):
        self.stored_functions.clear()
        self.func_listbox.delete(0, tk.END)
        self.output_text.delete('1.0', tk.END)

    