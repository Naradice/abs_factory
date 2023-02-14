import argparse
import ast
import copy
import os

DEFAULT_OUT_NAME = 'ABSTemplate'

def get_defined_modules(ast_object):
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
            pass
            #print(import_statements)
    return modules

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

def get_abstractmethod_definitions(node, new_class_name):
    abstractmethod_definitions = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ClassDef):
            abs_methods = exstruct_abstruct_method(child)
            if len(abs_methods) > 0:
                target_class = ast.ClassDef(name=new_class_name, bases=[ast.Name(child.name)], body=abs_methods, keywords=[], decorator_list=[])
                abstractmethod_definitions.append(target_class)
                
    return abstractmethod_definitions

def get_utilized_modules(ast_object, defined_modules):
    used_modules = []
    for node in ast.iter_child_nodes(ast_object):
        if isinstance(ast_object, ast.Name):
            id = ast_object.id
            if id in defined_modules:
                used_modules.append(defined_modules[id])
        used_modules.extend(get_utilized_modules(node, defined_modules))
    return used_modules


def create_template(in_file_path, out_file_path=None, out_class_name=DEFAULT_OUT_NAME):
    with open(in_file_path) as f:
        source = f.read()
    file_name = os.path.basename(in_file_path)
    
    if out_file_path is None:
        out_file_path = os.path.abspath(f"{os.getcwd()}/{file_name}")
        if os.path.exists(out_file_path):
            ##change file name to avoid overwriting it
            base_file_name = os.path.splitext(file_name)[0]
            file_name = f"{base_file_name}_template.py"
            out_file_path = os.path.abspath(f"{os.getcwd()}/{file_name}")
        
    ast_object = ast.parse(source, file_name)

    abstract_methods = get_abstractmethod_definitions(ast_object, out_class_name)
    defined_modules = get_defined_modules(ast_object)
    used_modules = []
    for method in abstract_methods:
        used_modules.extend(get_utilized_modules(method, defined_modules))
    used_modules = list(set(used_modules))
    template = used_modules + abstract_methods

    with open(out_file_path, "w") as fp:
        fp.write(ast.unparse(template))
    print("template file was created!")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-f","--file", required=True, help="specify file name which has abstruct class.")
    parser.add_argument("-o", "--out", help="specify file name to output.", default=None)
    parser.add_argument("-n", "--name", help="specify class name defined in output file.", default=DEFAULT_OUT_NAME)

    args = parser.parse_args()

    if os.path.exists(args.file):
        create_template(args.file, args.out, args.name)
    else:
        print("please specify existing file path.")