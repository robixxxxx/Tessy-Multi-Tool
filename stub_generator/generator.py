from stub_generator.utils import extract_base_type, map_type_to_macro, map_macro_to_type


def gen_declarations(funName, arguments, retType, nOfCalls):
    dec = f"#define TS_{funName}_CALL_COUNT_MAX ({nOfCalls} + 1)\n"
    for arg in arguments:
        base = extract_base_type(arg.type)
        dec += f"extern {base} TS_{funName}_{arg.name}[TS_{funName}_CALL_COUNT_MAX];\n"
        if '*' in arg.type or '&' in arg.type:
            dec += f"extern {base} TS_{funName}_{arg.name}_NewValue[TS_{funName}_CALL_COUNT_MAX];\n"
    if retType and retType != 'void':
        dec += f"extern {extract_base_type(retType)} TS_{funName}_retval[TS_{funName}_CALL_COUNT_MAX];\n"
    return dec


def gen_definitions(funName, arguments, retType):
    defn = ''
    for arg in arguments:
        base = extract_base_type(arg.type)
        defn += f"{base} TS_{funName}_{arg.name}[TS_{funName}_CALL_COUNT_MAX] = {{0}};\n"
        if '*' in arg.type or '&' in arg.type:
            defn += f"{base} TS_{funName}_{arg.name}_NewValue[TS_{funName}_CALL_COUNT_MAX] = {{0}};\n"
    if retType and retType != 'void':
        defn += f"{extract_base_type(retType)} TS_{funName}_retval[TS_{funName}_CALL_COUNT_MAX] = {{0}};\n"
    return defn


def gen_prolog(funName, arguments, retType, nOfCalls):
    pro = ''
    for i in range(nOfCalls):
        idx = i + 1
        for arg in arguments:
            pro += f"TS_{funName}_{arg.name}[{idx}] = 0;\n"
            if '*' in arg.type or '&' in arg.type:
                pro += f"TS_{funName}_{arg.name}_NewValue[{idx}] = 0;\n"
        if retType and retType != 'void':
            pro += f"TS_{funName}_retval[{idx}] = 0;\n"
    return pro


def gen_stub(funName, arguments, retType):
    stub = f"if (TS_CALL_COUNT < TS_{funName}_CALL_COUNT_MAX) {{\n"
    for arg in arguments:
        base = extract_base_type(arg.type)
        macro = map_type_to_macro(base)
        if '*' in arg.type:
            if('void' in arg.type or 'void*' in arg.type):
                cast_type = map_macro_to_type(macro)
                stub += f"    {macro}(\"Function {funName}(), Parameter *{arg.name}\", *(({cast_type} *){arg.name}), ==, TS_{funName}_{arg.name}[TS_CALL_COUNT]);\n"
                stub += f"    if({arg.name} != 0){{\n"
                stub += f"    \t*(({cast_type} *){arg.name}) = TS_{funName}_{arg.name}_NewValue[TS_CALL_COUNT];\n"
            else:
                stub += f"    {macro}(\"Function {funName}(), Parameter *{arg.name}\", *{arg.name}, ==, TS_{funName}_{arg.name}[TS_CALL_COUNT]);\n"
                stub += f"    if({arg.name} != 0){{\n"
                stub += f"    \t*{arg.name} = TS_{funName}_{arg.name}_NewValue[TS_CALL_COUNT];\n"
            
            stub += f"    }}\n"
        elif '&' in arg.type:
            stub += f"    {macro}(\"Function {funName}(), Parameter {arg.name}\", {arg.name}, ==, TS_{funName}_{arg.name}[TS_CALL_COUNT]);\n"
            stub += f"    {arg.name} = TS_{funName}_{arg.name}_NewValue[TS_CALL_COUNT];\n"
        else:
            stub += f"    {macro}(\"Function {funName}(), Parameter {arg.name}\", {arg.name}, ==, TS_{funName}_{arg.name}[TS_CALL_COUNT]);\n"
    if retType and retType != 'void':
        if '*' in retType or '&' in retType:
            stub += f"    return &TS_{funName}_retval[TS_CALL_COUNT];\n"
        else:
            stub += f"    return TS_{funName}_retval[TS_CALL_COUNT];\n"
    stub += "} \nelse {\n"
    stub += f"    TESSY_EVAL_U8(\"Function {funName}(), OVERCALL\", 1, ==, 0);\n"
    if retType and retType != 'void':
        stub += "    return 0;\n"
    stub += "}\n"
    return stub