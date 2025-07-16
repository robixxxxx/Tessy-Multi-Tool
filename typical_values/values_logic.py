types = {
    "int8": (-(2 ** 7), 2 ** 7 - 1, 0),
    "uint8": (0, 2 ** 8 - 1, 0),
    "int16": (-(2 ** 15), 2 ** 15 - 1, 0),
    "uint16": (0, 2 ** 16 - 1, 0),
    "int32": (-(2 ** 31), 2 ** 31 - 1, 0),
    "uint32": (0, 2 ** 32 - 1, 0),
    "float32": (-3.4028235e+30, 3.4028235e+30, 1),
    "float64": (-1.7976931348623157e+300, 1.7976931348623157e+300, 2),
}

label_order = ["Min", "Min+1", "Środek", "Max-1", "Max"]

labels = {}
name_labels = {}

def calculate(type_name):
    min_val, max_val, is_float = types[type_name]
    result = {}

    if is_float == 1:
        result["Min"] = f"{min_val:.2e}"
        result["Min+1"] = f"{min_val + 0.01e+30:.2e}"
        result["Środek"] = f"0.0"
        result["Max-1"] = f"{max_val - 0.01e+30:.2e}"
        result["Max"] = f"{max_val:.2e}"
    elif is_float == 2:
        result["Min"] = f"{min_val:.2e}"
        result["Min+1"] = f"{min_val + 0.01e+300:.2e}"
        result["Środek"] = f"0.0"
        result["Max-1"] = f"{max_val - 0.01e+300:.2e}"
        result["Max"] = f"{max_val:.2e}"
    else:
        mid = (min_val + max_val) // 2
        result["Min"] = str(min_val)
        result["Min+1"] = str(min_val + 1)
        result["Środek"] = str(mid)
        result["Max-1"] = str(max_val - 1)
        result["Max"] = str(max_val)

    return result