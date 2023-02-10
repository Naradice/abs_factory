import ast
import copy


FILE_NAME = "client.py"

with open(f"../personal/finance_client/finance_client/csv/{FILE_NAME}") as f:
    source = f.read()

ast_object = ast.parse(source, FILE_NAME)

modules = {}

for import_statements in ast_object.body:
    if isinstance(import_statements, ast.Import):
        for module in import_statements.names:
            if module.asname is None:
                modules[module.name] = ast.Import(names=[ast.alias(name=module.name)])
            else:
                modules[module.asname] = ast.Import(names=[ast.alias(name=module.name, asname=module.asname)])
    elif isinstance(import_statements, ast.ImportFrom):
        module_name = import_statements.module
        for module in import_statements.names:
            if module.asname is None:
                modules[module.name] = ast.ImportFrom(module=module_name, names=[ast.alias(name=module.name)])
            else:
                modules[module.name] = ast.ImportFrom(module=module_name, names=[ast.alias(name=module.name, asname=module.asname)])
    else:
        print(import_statements)

def is_abstruct_method(node):
    if isinstance(node, ast.FunctionDef):
        if len(node.decorator_list) > 0:
            if any(isinstance(item, ast.Name) and item.id == "abstractmethod" for item in node.decorator_list):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def exstruct_abstruct_method(class_node):
    methods = []
    if isinstance(class_node, ast.ClassDef):
        for child in ast.iter_child_nodes(class_node):
            if is_abstruct_method(child):
                method  = copy.copy(child)
                method.decorator_list = []
                methods.append(method)
    return methods

def get_abstractmethod_definitions(node):
    abstractmethod_definitions = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ClassDef):
            abs_methods = exstruct_abstruct_method(child)
            if len(abs_methods) > 0:
                target_class = copy.copy(child)
                target_class.body = abs_methods
                abstractmethod_definitions.append(target_class)
                
    return abstractmethod_definitions

abstract_methods = get_abstractmethod_definitions(ast_object)

with open(FILE_NAME, "w") as fp:
    fp.write(ast.unparse(abstract_methods))


item = abstract_methods[0].body[0]

required_modules = []

def get_used_modules(arg):
    used_modules = []
    if isinstance(arg, ast.arg):
        if isinstance(arg.annotation, ast.Name):
            if arg.annotation.id in modules:
                used_modules.append(modules[arg.annotation.id])
    return used_modules

for arg in item.args.args:
    required_modules.extend(get_used_modules(arg))

for arg in item.args.kwonlyargs:
    required_modules.extend(get_used_modules(arg))