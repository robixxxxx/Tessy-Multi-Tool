# utils.py
import re
from collections import namedtuple
import tkinter as tk

Argument = namedtuple("Argument", ["type", "name"])

def parse_function_signature(signature):
    match = re.match(r"\s*([\w\s\*\&]+?)\s+(\w+)\s*\((.*)\)", signature)
    if not match:
        return None
    ret_type = match.group(1).strip()
    name = match.group(2).strip()
    args_str = match.group(3).strip()
    arguments = []
    if args_str and args_str.lower() != 'void':
        for arg in args_str.split(','):
            arg = arg.strip()
            arg_match = re.match(r'([\w\s\*\&]+?)\s+(\w+)$', arg)
            if arg_match:
                arguments.append(Argument(type=arg_match.group(1).strip(), name=arg_match.group(2).strip()))
    return {"name": name, "ret_type": ret_type, "arguments": arguments}


def extract_base_type(type_str):
    return type_str.replace('*','').replace('&','').strip()


def map_type_to_macro(base_type):
    t = base_type.strip().lower().replace('const ', '').replace('  ', ' ')
    
    synonyms = {
        'char': ['char', 's8', 'int8_t', 's08', 's08_T', 'int8', 'int8_T'],
        'unsigned char': ['unsigned char', 'u8', 'u08_T', 'uchar', 'uint8', 'uint8_t', 'u08', 'uint8_T'],
        'short': ['short', 'short int', 'int16_t', 'int16', 's16', 's16_T', 'int16_T'],
        'unsigned short': ['unsigned short', 'unsigned short int', 'uint16','uint16_t', 'u16', 'u16_T', 'ushort'],
        'long': ['long', 'long int', 'int32', 'int32_t', 's32', 's32_T', 'int32_T'],
        'unsigned long': ['unsigned long', 'unsigned long int', 'uint32', 'uint32_t', 'u32', 'u32_T', 'ulong'],
        'long long': ['long long', 'int64', 'int64_t', 's64', 's64_T', 'long long int'],
        'unsigned long long': ['unsigned long long', 'uint64', 'uint64_t', 'u64', 'u64_T', 'unsigned long long int'],
        'float': ['float', 'float32', 'f32', 'f32_T'],
        'double': ['double', 'float64', 'f64', 'f64_T'],
        'long double': ['long double', 'float128', 'f128', 'f128_T']
    }
    
    macro_map = {
        'char': 'TESSY_EVAL_S8',
        'unsigned char': 'TESSY_EVAL_U8',
        'short': 'TESSY_EVAL_S16',
        'unsigned short': 'TESSY_EVAL_U16',
        'long': 'TESSY_EVAL_S32',
        'unsigned long': 'TESSY_EVAL_U32',
        'long long': 'TESSY_EVAL_S64',
        'unsigned long long': 'TESSY_EVAL_U64',
        'float': 'TESSY_EVAL_FLT',
        'double': 'TESSY_EVAL_DBL',
        'long double': 'TESSY_EVAL_LONGDOUBLE',
    }

    for canonical, alias_list in synonyms.items():
        if t in alias_list:
            return macro_map[canonical]
    return ask_eval_macro(base_type)
    
def map_macro_to_type(macro):
    macro_map = {
        'TESSY_EVAL_S8': 'char',
        'TESSY_EVAL_U8': 'unsigned char',
        'TESSY_EVAL_S16': 'short',
        'TESSY_EVAL_U16': 'unsigned short',
        'TESSY_EVAL_S32': 'long',
        'TESSY_EVAL_U32': 'unsigned long',
        'TESSY_EVAL_S64': 'long long',
        'TESSY_EVAL_U64': 'unsigned long long',
        'TESSY_EVAL_FLT': 'float',
        'TESSY_EVAL_DBL': 'double',
        'TESSY_EVAL_LONGDOUBLE': 'long double',
    }
    return macro_map[macro]

def ask_eval_macro(type_str):
    def on_select(value):
        nonlocal selected
        selected = value
        popup.destroy()

    popup = tk.Toplevel()
    popup.title(f"Wybierz TESSY_EVAL_* dla typu '{type_str}'")
    popup.geometry("300x400")
    tk.Label(popup, text=f"Nieznany typ: '{type_str}'\nWybierz odpowiednie makro:").pack(pady=10)

    macros = [
        "TESSY_EVAL_S8", "TESSY_EVAL_U8",
        "TESSY_EVAL_S16", "TESSY_EVAL_U16",
        "TESSY_EVAL_S32", "TESSY_EVAL_U32",
        "TESSY_EVAL_S64", "TESSY_EVAL_U64",
        "TESSY_EVAL_FLT", "TESSY_EVAL_DBL",
        "TESSY_EVAL_LONGDOUBLE"
    ]

    selected = None
    for macro in macros:
        btn = tk.Button(popup, text=macro, command=lambda m=macro: on_select(m))
        btn.pack(pady=2)

    popup.grab_set()
    popup.wait_window()
    return selected or "TESSY_EVAL_S32"
