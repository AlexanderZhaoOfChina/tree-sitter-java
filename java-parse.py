import os
import sys
from tree_sitter import Language, Parser
import re
from pathlib import Path
from collections import defaultdict

def setup_tree_sitter():
    """设置tree-sitter-java解析器"""
    # 确保tree-sitter-java存在
    tree_sitter_path = Path("./tree-sitter-java")
    if not tree_sitter_path.exists():
        print("正在克隆tree-sitter-java...")
        os.system("git clone https://github.com/tree-sitter/tree-sitter-java")
    
    # 构建tree-sitter-java
    Language.build_library(
        "build/my-languages.so",
        [str(tree_sitter_path)]
    )
    
    # 加载Java语言
    JAVA_LANGUAGE = Language("build/my-languages.so", "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    
    return parser

def get_package_name(root_node):
    """从语法树中提取包名"""
    package_node = next((node for node in root_node.children 
                         if node.type == "package_declaration"), None)
    if package_node:
        for child in package_node.children:
            if child.type == "scoped_identifier":
                return child.text.decode('utf-8')
    return ""

def get_imports(root_node):
    """提取所有导入语句，用于解析全路径类型"""
    imports = {}
    import_nodes = [node for node in root_node.children 
                   if node.type == "import_declaration"]
    
    for import_node in import_nodes:
        for child in import_node.children:
            if child.type == "scoped_identifier":
                import_text = child.text.decode('utf-8')
                class_name = import_text.split('.')[-1]
                if class_name != "*":  # 忽略通配符导入
                    imports[class_name] = import_text
    
    return imports

def get_class_info(class_node, package_name, imports):
    """提取类信息及其方法和变量"""
    class_info = {
        'name': '',
        'full_path': '',
        'methods': [],
        'fields': []
    }
    
    # 提取类名
    for child in class_node.children:
        if child.type == "identifier":
            class_name = child.text.decode('utf-8')
            class_info['name'] = class_name
            if package_name:
                class_info['full_path'] = f"{package_name}.{class_name}"
            else:
                class_info['full_path'] = class_name
    
    # 提取类声明体
    class_body = next((child for child in class_node.children 
                      if child.type == "class_body"), None)
    
    if class_body:
        # 提取方法
        for child in class_body.children:
            if child.type == "method_declaration":
                method_info = extract_method_info(child, imports, package_name)
                if method_info:
                    class_info['methods'].append(method_info)
            
            # 提取字段/变量
            elif child.type == "field_declaration":
                field_infos = extract_field_info(child, imports, package_name)
                class_info['fields'].extend(field_infos)
    
    return class_info

def extract_method_info(method_node, imports, package_name):
    """提取方法信息及其内部局部变量"""
    method_info = {
        'name': '',
        'return_type': '',
        'local_variables': []
    }
    
    # 提取方法名和返回类型
    for child in method_node.children:
        if child.type == "identifier":
            method_info['name'] = child.text.decode('utf-8')
        elif child.type == "primitive_type" or child.type == "type_identifier":
            method_info['return_type'] = child.text.decode('utf-8')
        elif child.type == "void_type":
            method_info['return_type'] = "void"
        
        # 提取方法体
        elif child.type == "block":
            # 遍历方法体寻找局部变量声明
            extract_local_variables(child, method_info['local_variables'], imports, package_name)
    
    return method_info

def extract_local_variables(block_node, local_vars, imports, package_name):
    """从方法体中提取局部变量"""
    
    def traverse_node(node):
        if node.type == "local_variable_declaration":
            # 提取局部变量类型
            type_node = None
            var_type = ""
            var_type_full_path = ""
            
            for child in node.children:
                if child.type == "type_identifier":
                    type_node = child
                    var_type = child.text.decode('utf-8')
                    
                    # 尝试解析全路径
                    if var_type in imports:
                        var_type_full_path = imports[var_type]
                    else:
                        # 假设与当前类在同一包下
                        var_type_full_path = f"{package_name}.{var_type}" if package_name else var_type
                        
                elif child.type == "primitive_type":
                    type_node = child
                    var_type = child.text.decode('utf-8')
                    var_type_full_path = var_type
                
                # 提取变量名
                elif child.type == "variable_declarator":
                    for grandchild in child.children:
                        if grandchild.type == "identifier":
                            var_name = grandchild.text.decode('utf-8')
                            local_vars.append({
                                'name': var_name,
                                'type': var_type,
                                'type_full_path': var_type_full_path
                            })
        
        # 递归遍历子节点
        for child in node.children:
            traverse_node(child)
    
    traverse_node(block_node)

def extract_field_info(field_node, imports, package_name):
    """提取字段/变量信息"""
    field_infos = []
    
    # 提取字段类型
    field_type = ""
    field_type_full_path = ""
    
    for child in field_node.children:
        if child.type == "type_identifier":
            field_type = child.text.decode('utf-8')
            # 尝试解析全路径
            if field_type in imports:
                field_type_full_path = imports[field_type]
            else:
                # 假设与当前类在同一包下
                field_type_full_path = f"{package_name}.{field_type}" if package_name else field_type
        
        elif child.type == "primitive_type":
            field_type = child.text.decode('utf-8')  # 原始类型不需要全路径
            field_type_full_path = field_type
        
        # 提取字段名
        elif child.type == "variable_declarator":
            for grandchild in child.children:
                if grandchild.type == "identifier":
                    field_name = grandchild.text.decode('utf-8')
                    field_infos.append({
                        'name': field_name,
                        'type': field_type,
                        'type_full_path': field_type_full_path
                    })
    
    return field_infos

def process_java_file(file_path, parser):
    """处理单个Java文件"""
    with open(file_path, 'rb') as f:
        source_code = f.read()
    
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    package_name = get_package_name(root_node)
    imports = get_imports(root_node)
    
    classes = []
    
    # 提取所有类声明
    for node in root_node.children:
        if node.type == "class_declaration":
            class_info = get_class_info(node, package_name, imports)
            classes.append(class_info)
    
    return classes

def process_directory(directory_path, parser):
    """递归处理目录中的所有Java文件"""
    all_classes = []
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                try:
                    classes = process_java_file(file_path, parser)
                    all_classes.extend(classes)
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
    
    return all_classes

def generate_markdown(classes, output_file):
    """生成Markdown输出"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Java项目结构分析\n\n")
        f.write("| 类 | 方法 | 变量名 | 变量类型 | 变量位置 |\n")
        f.write("|---|------|-------|--------|--------|\n")
        
        for class_info in classes:
            class_name = class_info['full_path']
            
            # 如果类没有方法和字段，添加一个空行
            if not class_info['methods'] and not class_info['fields']:
                f.write(f"| {class_name} | | | | |\n")
                continue
            
            # 处理每个方法
            for i, method in enumerate(class_info['methods']):
                method_name = method['name']
                method_return = method['return_type']
                
                # 第一个方法显示类名，其余方法不显示
                if i == 0:
                    f.write(f"| {class_name} | {method_name} | | | |\n")
                else:
                    f.write(f"| | {method_name} | | | |\n")
                
                # 处理方法内部的局部变量
                for var in method['local_variables']:
                    var_name = var['name']
                    var_type = var['type_full_path']
                    f.write(f"| | | {var_name} | {var_type} | 局部变量 |\n")
            
            # 处理每个字段
            for i, field in enumerate(class_info['fields']):
                field_name = field['name']
                field_type = field['type_full_path']
                
                # 如果没有方法但有字段，第一个字段显示类名
                if not class_info['methods'] and i == 0:
                    f.write(f"| {class_name} | | {field_name} | {field_type} | 类字段 |\n")
                else:
                    f.write(f"| | | {field_name} | {field_type} | 类字段 |\n")

def main():
    if len(sys.argv) < 2:
        print("用法: python java_parser.py <Java项目路径> [输出文件]")
        sys.exit(1)
    
    java_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "java_structure.md"
    
    parser = setup_tree_sitter()
    
    if os.path.isfile(java_path) and java_path.endswith('.java'):
        classes = process_java_file(java_path, parser)
    elif os.path.isdir(java_path):
        classes = process_directory(java_path, parser)
    else:
        print(f"错误: 文件路径 {java_path} 不是有效的Java文件或目录")
        sys.exit(1)
    
    generate_markdown(classes, output_file)
    print(f"分析完成! 结果已保存到 {output_file}")

if __name__ == "__main__":
    main()