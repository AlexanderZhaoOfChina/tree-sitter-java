import os
import sys
import time  # 添加time模块用于计时
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

def get_line_number(node):
    """获取节点的起始行号"""
    return node.start_point[0] + 1  # 行号从0开始，转为1开始

def get_class_info(class_node, package_name, imports, file_path):
    """提取类信息及其方法和变量"""
    class_info = {
        'name': '',
        'full_path': '',
        'methods': [],
        'fields': [],
        'line': get_line_number(class_node),
        'file_path': file_path
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
        'local_variables': [],
        'line': get_line_number(method_node)
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

def extract_type_full_info(node, imports, package_name):
    """提取类型的完整信息，包括集合类型和数组类型"""
    # 处理基本类型和普通类型
    if node.type == "primitive_type":
        return node.text.decode('utf-8'), node.text.decode('utf-8')
    elif node.type == "type_identifier":
        var_type = node.text.decode('utf-8')
        # 尝试解析全路径
        if var_type in imports:
            var_type_full_path = imports[var_type]
        else:
            # 假设与当前类在同一包下
            var_type_full_path = f"{package_name}.{var_type}" if package_name else var_type
        return var_type, var_type_full_path
    # 处理泛型类型
    elif node.type == "generic_type":
        base_type = None
        type_args = []
        
        for child in node.children:
            if child.type == "type_identifier":
                base_type = child.text.decode('utf-8')
            elif child.type in ["type_arguments", "type_argument"]:
                for arg_child in child.children:
                    if arg_child.type in ["type_identifier", "primitive_type"]:
                        type_args.append(arg_child.text.decode('utf-8'))
        
        if base_type and type_args:
            var_type = f"{base_type}<{', '.join(type_args)}>"
            # 尝试解析全路径
            if base_type in imports:
                base_type_full_path = imports[base_type]
                var_type_full_path = f"{base_type_full_path}<{', '.join(type_args)}>"
            else:
                # 假设与当前类在同一包下
                base_type_full_path = f"{package_name}.{base_type}" if package_name else base_type
                var_type_full_path = f"{base_type_full_path}<{', '.join(type_args)}>"
            return var_type, var_type_full_path
    # 处理数组类型
    elif node.type == "array_type":
        element_type = None
        for child in node.children:
            if child.type in ["type_identifier", "primitive_type"]:
                element_type_name, element_type_full_path = extract_type_full_info(child, imports, package_name)
                var_type = f"{element_type_name}[]"
                var_type_full_path = f"{element_type_full_path}[]"
                return var_type, var_type_full_path
    
    # 如果无法识别类型，返回空字符串
    return "", ""

def guess_type_from_name(var_name):
    """根据变量名猜测可能的类型"""
    # 常见的命名模式与对应的类型
    if var_name in ['i', 'j', 'k', 'n', 'index', 'count', 'size', 'length']:
        return 'int', 'int'
    elif 'time' in var_name.lower() and ('start' in var_name.lower() or 'end' in var_name.lower() or 'stamp' in var_name.lower()):
        return 'long', 'long'
    elif var_name.lower() in ['found', 'has', 'is', 'exists', 'contains']:
        return 'boolean', 'boolean'
    elif var_name == 'rowNum' or var_name.endswith('Num') or var_name.endswith('Count') or var_name.startswith('num'):
        return 'int', 'int'
    
    # 变量类型猜测：根据后缀约定
    if var_name.endswith('Id') or var_name.endswith('ID'):
        return 'Long', 'Long'
    
    # 对于无法猜测的变量，返回空字符串
    return '', ''

def extract_local_variables(block_node, local_vars, imports, package_name):
    """从方法体中提取局部变量"""
    
    def traverse_node(node):
        if node.type == "local_variable_declaration":
            var_type = ""
            var_type_full_path = ""
            var_declarations = []
            
            # 查找类型声明和变量声明
            for child in node.children:
                # 处理基本类型和普通类型
                if child.type in ["primitive_type", "type_identifier", "generic_type", "array_type"]:
                    var_type, var_type_full_path = extract_type_full_info(child, imports, package_name)
                # 处理变量声明
                elif child.type == "variable_declarator":
                    for grandchild in child.children:
                        if grandchild.type == "identifier":
                            var_name = grandchild.text.decode('utf-8')
                            
                            # 如果无法从声明中获取类型，尝试根据变量名猜测
                            if not var_type:
                                var_type, var_type_full_path = guess_type_from_name(var_name)
                            
                            var_declarations.append({
                                'name': var_name,
                                'type': var_type,
                                'type_full_path': var_type_full_path,
                                'line': get_line_number(child)  # 记录变量声明的行号
                            })
            
            # 添加所有变量声明到列表
            local_vars.extend(var_declarations)
        
        # 递归遍历子节点
        for child in node.children:
            traverse_node(child)
    
    traverse_node(block_node)

def extract_field_info(field_node, imports, package_name):
    """提取字段/变量信息"""
    field_infos = []
    
    # 查找类型声明
    type_node = None
    for child in field_node.children:
        if child.type in ["primitive_type", "type_identifier", "generic_type", "array_type"]:
            type_node = child
            break
    
    # 如果找到类型节点，提取类型信息
    if type_node:
        var_type, var_type_full_path = extract_type_full_info(type_node, imports, package_name)
        
        # 查找所有变量声明
        for child in field_node.children:
            if child.type == "variable_declarator":
                for grandchild in child.children:
                    if grandchild.type == "identifier":
                        field_name = grandchild.text.decode('utf-8')
                        
                        # 如果无法从声明中获取类型，尝试根据变量名猜测
                        if not var_type:
                            var_type, var_type_full_path = guess_type_from_name(field_name)
                            
                        field_infos.append({
                            'name': field_name,
                            'type': var_type,
                            'type_full_path': var_type_full_path,
                            'line': get_line_number(child)  # 记录字段声明的行号
                        })
    
    return field_infos

def process_java_file(file_path, parser):
    """处理单个Java文件"""
    with open(file_path, 'rb') as f:
        source_code = f.read()
    
    # 计算文件行数
    line_count = len(source_code.splitlines())
    
    tree = parser.parse(source_code)
    root_node = tree.root_node
    
    package_name = get_package_name(root_node)
    imports = get_imports(root_node)
    
    classes = []
    
    # 提取所有类声明
    for node in root_node.children:
        if node.type == "class_declaration":
            class_info = get_class_info(node, package_name, imports, file_path)
            classes.append(class_info)
    
    return classes, line_count

def process_directory(directory_path, parser):
    """递归处理目录中的所有Java文件"""
    all_classes = []
    total_lines = 0
    total_files = 0
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                try:
                    classes, line_count = process_java_file(file_path, parser)
                    all_classes.extend(classes)
                    total_lines += line_count
                    total_files += 1
                    if total_files % 100 == 0:
                        print(f"已处理 {total_files} 个文件, {total_lines} 行代码...")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
    
    return all_classes, total_lines, total_files

def generate_markdown_header():
    """生成Markdown文件的头部内容"""
    return "# Java项目结构分析\n\n" + \
           "| 类 | 方法 | 变量名 | 变量类型 | 变量位置 | 源文件位置 |\n" + \
           "|---|------|-------|--------|--------|----------|\n"

def generate_markdown_files(classes, output_dir):
    """生成多个Markdown文件，每个不超过2MB"""
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 定义每个文件的最大大小为2MB
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    
    file_index = 1
    current_file_path = os.path.join(output_dir, f"java_structure_{file_index}.md")
    
    # 创建并写入第一个文件的头部
    with open(current_file_path, 'w', encoding='utf-8') as f:
        f.write(generate_markdown_header())
    
    current_file_size = len(generate_markdown_header().encode('utf-8'))
    
    # 处理所有类
    for class_info in classes:
        class_name = class_info['full_path']
        class_file = class_info['file_path']
        class_line = class_info['line']
        
        # 为当前类生成内容
        class_content = ""
        
        # 如果类没有方法和字段，添加一个空行
        if not class_info['methods'] and not class_info['fields']:
            class_content += f"| {class_name} | | | | | {class_file}:{class_line} |\n"
        else:
            # 处理每个方法
            for i, method in enumerate(class_info['methods']):
                method_name = method['name']
                method_line = method['line']
                
                # 第一个方法显示类名，其余方法不显示
                if i == 0:
                    class_content += f"| {class_name} | {method_name} | | | | {class_file}:{class_line} / 方法:{method_line} |\n"
                else:
                    class_content += f"| | {method_name} | | | | {class_file}:方法:{method_line} |\n"
                
                # 处理方法内部的局部变量
                for var in method['local_variables']:
                    var_name = var['name']
                    var_type = var['type_full_path']
                    var_line = var.get('line', '')
                    class_content += f"| | | {var_name} | {var_type} | 局部变量 | 行:{var_line} |\n"
            
            # 处理每个字段
            for i, field in enumerate(class_info['fields']):
                field_name = field['name']
                field_type = field['type_full_path']
                field_line = field.get('line', '')
                
                # 如果没有方法但有字段，第一个字段显示类名
                if not class_info['methods'] and i == 0:
                    class_content += f"| {class_name} | | {field_name} | {field_type} | 类字段 | {class_file}:{class_line} / 字段:{field_line} |\n"
                else:
                    class_content += f"| | | {field_name} | {field_type} | 类字段 | 行:{field_line} |\n"
        
        # 检查添加这个类的内容是否会使当前文件超过大小限制
        content_size = len(class_content.encode('utf-8'))
        
        if current_file_size + content_size > MAX_FILE_SIZE:
            # 如果会超过，创建新文件
            file_index += 1
            current_file_path = os.path.join(output_dir, f"java_structure_{file_index}.md")
            
            with open(current_file_path, 'w', encoding='utf-8') as f:
                f.write(generate_markdown_header())
            
            current_file_size = len(generate_markdown_header().encode('utf-8'))
        
        # 将类内容添加到当前文件
        with open(current_file_path, 'a', encoding='utf-8') as f:
            f.write(class_content)
        
        current_file_size += content_size
    
    return file_index  # 返回生成的文件数量

def main():
    if len(sys.argv) < 2:
        print("用法: python java-analysis.py <Java项目路径> [输出目录]")
        sys.exit(1)
    
    java_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "java_structure_docs"
    
    # 记录开始时间
    start_time = time.time()
    print(f"开始分析Java项目: {java_path}")
    
    parser = setup_tree_sitter()
    
    total_lines = 0
    total_files = 0
    
    if os.path.isfile(java_path) and java_path.endswith('.java'):
        classes, line_count = process_java_file(java_path, parser)
        total_lines = line_count
        total_files = 1
    elif os.path.isdir(java_path):
        classes, total_lines, total_files = process_directory(java_path, parser)
    else:
        print(f"错误: 文件路径 {java_path} 不是有效的Java文件或目录")
        sys.exit(1)
    
    # 生成Markdown文件
    file_count = generate_markdown_files(classes, output_dir)
    
    # 计算总耗时
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 打印统计信息
    print(f"分析完成! 结果已保存到 {output_dir} 目录中的 {file_count} 个文件")
    print(f"总计扫描了 {total_files} 个Java文件, {total_lines} 行代码")
    print(f"总耗时: {execution_time:.2f} 秒")
    
    # 将统计信息也写入到summary.txt文件中
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"Java项目分析统计信息\n")
        f.write(f"====================\n\n")
        f.write(f"分析的项目路径: {os.path.abspath(java_path)}\n")
        f.write(f"总计扫描文件数: {total_files} 个Java文件\n")
        f.write(f"总计代码行数: {total_lines} 行\n")
        f.write(f"总计耗时: {execution_time:.2f} 秒\n")
        f.write(f"生成的Markdown文件数: {file_count} 个\n")
        f.write(f"\n分析时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    main()