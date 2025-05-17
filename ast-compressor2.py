import json
from tree_sitter import Language, Parser
from typing import Dict, List, Optional, Union, Any, Set
import os
import gzip
from collections import defaultdict

class ASTCompressor:
    """用于压缩Java AST的工具类，增强版"""
    
    # 重要的节点类型，这些将被保留
    IMPORTANT_NODE_TYPES = {
        'program', 'package_declaration', 'import_declaration', 'class_declaration', 
        'interface_declaration', 'enum_declaration', 'method_declaration', 
        'constructor_declaration', 'field_declaration', 'variable_declarator',
        'if_statement', 'for_statement', 'while_statement', 'do_statement', 
        'switch_statement', 'case_statement', 'try_statement', 'catch_clause',
        'method_invocation', 'class_instance_creation', 'return_statement',
        'throw_statement', 'assignment_expression', 'binary_expression',
        'object_creation_expression', 'lambda_expression',
    }
    
    # 可以被简化的节点类型（只保留关键信息）
    SIMPLIFIED_NODE_TYPES = {
        'modifiers', 'formal_parameters', 'type_parameters',
        'block', 'argument_list', 'type_arguments'
    }
    
    # 完全忽略的节点类型
    IGNORED_NODE_TYPES = {
        'comment', 'line_comment', 'block_comment', 'semicolon', 'comma', 
        'dimensions', 'parenthesized_expression', 'bracket_expression',
        'empty_statement', '.', ';', '{', '}', '(', ')', '[', ']'
    }
    
    # 对文本内容进行保留的节点类型
    TEXT_NODES = {
        'identifier', 'string_literal', 'number_literal', 'character_literal',
        'decimal_integer_literal', 'hex_integer_literal', 'octal_integer_literal',
        'binary_integer_literal', 'decimal_floating_point_literal', 'true', 
        'false', 'null_literal', 'type_identifier'
    }
    
    def __init__(self, max_depth: int = 15, include_position: bool = False, 
                 use_symbol_table: bool = True, deduplicate: bool = True,
                 prune_empty_nodes: bool = True, compress_output: bool = False):
        """
        初始化AST压缩器
        
        Args:
            max_depth: 递归处理的最大深度
            include_position: 是否包含位置信息
            use_symbol_table: 是否使用符号表进行字符串去重
            deduplicate: 是否去重结构相同的子树
            prune_empty_nodes: 是否剪枝空节点
            compress_output: 是否对最终输出进行gzip压缩
        """
        self.max_depth = max_depth
        self.include_position = include_position
        self.use_symbol_table = use_symbol_table
        self.deduplicate = deduplicate
        self.prune_empty_nodes = prune_empty_nodes
        self.compress_output = compress_output
        
        # 符号表用于文本去重
        self.symbol_table = {}
        self.symbol_reverse = []
        
        # 子树缓存用于去重
        self.subtree_cache = {}
        self.subtree_refs = defaultdict(int)
        
    def compress(self, root_node) -> Dict[str, Any]:
        """压缩整个AST"""
        # 第一遍：构建符号表和子树缓存
        if self.use_symbol_table or self.deduplicate:
            self._build_tables(root_node, 0)
        
        # 第二遍：实际压缩AST
        result = self._compress_node(root_node, 0)
        
        # 添加符号表（如果使用）
        if self.use_symbol_table and self.symbol_reverse:
            result["_symbol_table"] = self.symbol_reverse
        
        return result
    
    def _build_tables(self, node, depth: int) -> None:
        """构建符号表和子树缓存的预处理遍历"""
        if node is None or depth > self.max_depth:
            return
        
        # 文本节点添加到符号表
        if self.use_symbol_table and hasattr(node, 'text'):
            text = node.text.decode('utf-8')
            if text and len(text) > 3 and text not in self.symbol_table:
                self.symbol_table[text] = len(self.symbol_reverse)
                self.symbol_reverse.append(text)
        
        # 递归处理子节点
        if hasattr(node, 'children'):
            for child in node.children:
                self._build_tables(child, depth + 1)
    
    def _get_node_hash(self, node) -> int:
        """计算节点的哈希值用于去重"""
        if not hasattr(node, 'text'):
            return hash(node.type)
        
        return hash((node.type, node.text))
    
    def _compress_node(self, node, depth: int) -> Optional[Dict[str, Any]]:
        """递归压缩单个节点及其子节点"""
        if node is None or depth > self.max_depth:
            return None
        
        node_type = node.type
        
        # 检查是否为忽略的节点类型
        if node_type in self.IGNORED_NODE_TYPES:
            return None
            
        # 使用缓存的子树（去重优化）
        if self.deduplicate:
            node_hash = self._get_node_hash(node)
            if node_hash in self.subtree_cache and depth > 2:  # 避免顶层节点复用
                self.subtree_refs[node_hash] += 1
                ref_id = f"_ref_{node_hash}"
                return {"_ref": ref_id}
        
        # 获取节点文本
        node_text = None
        if hasattr(node, 'text'):
            node_text = node.text.decode('utf-8') if node.text else None
        
        # 创建基本节点信息
        result = {"type": node_type}
        
        # 添加文本内容（对于标识符和字面量很重要）
        if node_text and (node_type in self.TEXT_NODES):
            if self.use_symbol_table and node_text in self.symbol_table and len(node_text) > 3:
                # 使用符号表引用
                result["text_ref"] = self.symbol_table[node_text]
            else:
                result["text"] = node_text
            
        # 添加位置信息（如果需要）
        if self.include_position:
            result["pos"] = [node.start_point[0], node.start_point[1], 
                             node.end_point[0], node.end_point[1]]
        
        # 基于节点类型进行特殊处理
        if node_type == 'method_declaration':
            result = self._process_method_declaration(node, depth, result)
        elif node_type == 'class_declaration':
            result = self._process_class_declaration(node, depth, result)
        elif node_type in self.SIMPLIFIED_NODE_TYPES:
            result = self._process_simplified_node(node, depth, result)
        elif node_type in self.IMPORTANT_NODE_TYPES:
            # 处理重要节点类型的子节点
            children = self._compress_children(node, depth)
            if children:
                result["children"] = children
        else:
            # 默认处理方式：递归处理子节点
            if depth < self.max_depth - 1:
                children = self._compress_children(node, depth)
                if children:
                    result["children"] = children
        
        # 存储子树缓存（用于去重）
        if self.deduplicate and node_type not in {'identifier', 'string_literal'}:
            node_hash = self._get_node_hash(node)
            self.subtree_cache[node_hash] = result
            ref_id = f"_ref_{node_hash}"
            self.subtree_refs[node_hash] = 1
        
        # 剪枝空节点
        if self.prune_empty_nodes:
            if len(result) == 1 and "type" in result:  # 只有类型字段的节点
                return None
        
        return result
    
    def _compress_children(self, node, depth: int) -> List[Dict[str, Any]]:
        """压缩所有子节点"""
        result = []
        if hasattr(node, 'children'):
            for child in node.children:
                compressed_child = self._compress_node(child, depth + 1)
                if compressed_child:
                    result.append(compressed_child)
        return result
    
    def _process_method_declaration(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """处理方法声明，提取关键信息"""
        # 查找方法名
        name_node = self._find_child_by_type(node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            if self.use_symbol_table and name_node.text.decode('utf-8') in self.symbol_table:
                result["name_ref"] = self.symbol_table[name_node.text.decode('utf-8')]
            else:
                result["name"] = name_node.text.decode('utf-8')
        
        # 处理修饰符
        modifiers = []
        modifiers_node = self._find_child_by_type(node, 'modifiers')
        if modifiers_node:
            for mod in modifiers_node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final', 'abstract'}:
                    modifiers.append(mod.type)
        if modifiers:
            result["modifiers"] = modifiers
        
        # 查找返回类型
        return_type = self._find_child_by_type(node, 'type_identifier')
        if return_type and hasattr(return_type, 'text'):
            result["return_type"] = return_type.text.decode('utf-8')
        
        # 处理参数的优化版本
        params_node = self._find_child_by_type(node, 'formal_parameters')
        if params_node:
            params = []
            for param in params_node.children:
                if param.type == 'formal_parameter':
                    param_info = {}
                    param_type = self._find_child_by_type(param, 'type_identifier')
                    param_name = self._find_child_by_type(param, 'identifier')
                    
                    if param_type and hasattr(param_type, 'text'):
                        param_info["type"] = param_type.text.decode('utf-8')
                    if param_name and hasattr(param_name, 'text'):
                        name_text = param_name.text.decode('utf-8')
                        if self.use_symbol_table and name_text in self.symbol_table:
                            param_info["name_ref"] = self.symbol_table[name_text]
                        else:
                            param_info["name"] = name_text
                    
                    if param_info:
                        params.append(param_info)
            
            if params:
                result["parameters"] = params
        
        # 处理方法体
        if depth < self.max_depth - 2:  # 减少深度以节省空间
            body_node = self._find_child_by_type(node, 'block')
            if body_node:
                # 只记录方法体的主要语句类型和数量
                if not self.include_position:  # 如果不需要具体实现细节，简化方法体
                    stmt_counts = defaultdict(int)
                    for stmt in body_node.children:
                        if stmt.type not in {'{', '}'}:
                            stmt_counts[stmt.type] += 1
                    
                    if stmt_counts:
                        result["body_summary"] = dict(stmt_counts)
                else:
                    # 包含完整实现
                    body_content = self._compress_children(body_node, depth + 1)
                    if body_content:
                        result["body"] = body_content
        
        return result
    
    def _process_class_declaration(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """处理类声明，提取关键信息"""
        # 查找类名
        name_node = self._find_child_by_type(node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            name_text = name_node.text.decode('utf-8')
            if self.use_symbol_table and name_text in self.symbol_table:
                result["name_ref"] = self.symbol_table[name_text]
            else:
                result["name"] = name_text
        
        # 处理修饰符
        modifiers = []
        modifiers_node = self._find_child_by_type(node, 'modifiers')
        if modifiers_node:
            for mod in modifiers_node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final', 'abstract'}:
                    modifiers.append(mod.type)
        if modifiers:
            result["modifiers"] = modifiers
        
        # 处理继承
        extends_node = self._find_child_by_field(node, 'superclass')
        if extends_node and hasattr(extends_node, 'text'):
            result["extends"] = extends_node.text.decode('utf-8')
        
        # 处理类成员（优化版本）
        if depth < self.max_depth - 1:
            class_body = self._find_child_by_type(node, 'class_body')
            if class_body:
                # 组织成员节点
                members = {}
                field_count = method_count = constructor_count = inner_class_count = 0
                
                # 只保存每种类型的计数而不是完整内容
                if not self.include_position and depth > 2:  # 对于深层次类，只保留摘要
                    for child in class_body.children:
                        if child.type == 'field_declaration':
                            field_count += 1
                        elif child.type == 'method_declaration':
                            method_count += 1
                        elif child.type == 'constructor_declaration':
                            constructor_count += 1
                        elif child.type in {'class_declaration', 'interface_declaration', 'enum_declaration'}:
                            inner_class_count += 1
                    
                    members_summary = {}
                    if field_count > 0:
                        members_summary["fields_count"] = field_count
                    if method_count > 0:
                        members_summary["methods_count"] = method_count
                    if constructor_count > 0:
                        members_summary["constructors_count"] = constructor_count
                    if inner_class_count > 0:
                        members_summary["inner_classes_count"] = inner_class_count
                    
                    if members_summary:
                        result["members_summary"] = members_summary
                else:
                    # 为顶层类保留完整的成员
                    members = {
                        "fields": [],
                        "methods": [],
                        "constructors": [],
                        "inner_classes": []
                    }
                    
                    for child in class_body.children:
                        if child.type == 'field_declaration':
                            field = self._compress_node(child, depth + 1)
                            if field:
                                members["fields"].append(field)
                        elif child.type == 'method_declaration':
                            method = self._compress_node(child, depth + 1)
                            if method:
                                members["methods"].append(method)
                        elif child.type == 'constructor_declaration':
                            constructor = self._compress_node(child, depth + 1)
                            if constructor:
                                members["constructors"].append(constructor)
                        elif child.type in {'class_declaration', 'interface_declaration', 'enum_declaration'}:
                            inner_class = self._compress_node(child, depth + 1)
                            if inner_class:
                                members["inner_classes"].append(inner_class)
                    
                    # 移除空列表
                    for key in list(members.keys()):
                        if not members[key]:
                            del members[key]
                    
                    if members:
                        result["members"] = members
        
        return result
    
    def _process_simplified_node(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """简化处理某些节点类型，只保留关键信息"""
        if hasattr(node, 'text'):
            node_text = node.text.decode('utf-8')
            if len(node_text) > 100:  # 对于长文本，只保留长度
                result["text_length"] = len(node_text)
            else:
                result["text"] = node_text
        
        # 对于某些特定节点，简化表示
        if node.type == 'formal_parameters':
            params_count = sum(1 for child in node.children if child.type == 'formal_parameter')
            result["params_count"] = params_count
        elif node.type == 'block':
            stmt_count = sum(1 for child in node.children 
                            if child.type not in {'{', '}'} and child.type.endswith('_statement'))
            if stmt_count > 0:
                result["stmt_count"] = stmt_count
        
        return result
    
    def _find_child_by_type(self, node, type_name: str):
        """查找特定类型的子节点"""
        if hasattr(node, 'children'):
            for child in node.children:
                if child.type == type_name:
                    return child
        return None
    
    def _find_child_by_field(self, node, field_name: str):
        """查找特定字段名的子节点"""
        if hasattr(node, 'children'):
            for child in node.children:
                if hasattr(child, 'field_name') and child.field_name == field_name:
                    return child
        return None


def compress_java_ast(java_code: str, max_depth: int = 15, include_position: bool = False,
                      use_symbol_table: bool = True, compress_output: bool = False) -> Dict[str, Any]:
    """
    解析并压缩Java代码的AST
    
    Args:
        java_code: Java源代码字符串
        max_depth: 最大递归深度
        include_position: 是否包含位置信息
        use_symbol_table: 是否使用符号表进行字符串去重
        compress_output: 是否对最终输出进行gzip压缩
    
    Returns:
        压缩后的AST字典
    """
    try:
        # 尝试加载已构建的库
        JAVA_LANGUAGE = Language('build/languages.dll', 'java')
    except:
        try:
            # 失败则尝试构建库
            Language.build_library(
                'build/languages.dll',
                [os.path.join(os.path.dirname(__file__), 'tree-sitter-java')]
            )
            JAVA_LANGUAGE = Language('build/languages.dll', 'java')
        except Exception as e:
            print(f"无法加载或构建Java语言支持: {e}")
            # 如果平台是Linux，尝试使用so扩展名
            try:
                JAVA_LANGUAGE = Language('build/languages.so', 'java')
            except:
                print("尝试查找替代库...")
                # 查找当前目录下的任何相关库
                lib_candidates = [f for f in os.listdir('.') if f.endswith('.dll') or f.endswith('.so')]
                for lib in lib_candidates:
                    try:
                        JAVA_LANGUAGE = Language(lib, 'java')
                        print(f"找到并使用库: {lib}")
                        break
                    except:
                        continue
                else:
                    raise RuntimeError("无法找到或加载任何Java语言支持库")
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    
    tree = parser.parse(bytes(java_code, 'utf8'))
    compressor = ASTCompressor(
        max_depth=max_depth,
        include_position=include_position,
        use_symbol_table=use_symbol_table,
        deduplicate=True,
        prune_empty_nodes=True,
        compress_output=compress_output
    )
    
    return compressor.compress(tree.root_node)


def save_compressed_ast(compressed_ast: Dict[str, Any], output_file: str, 
                         use_gzip: bool = False, indent: int = 2) -> None:
    """
    将压缩后的AST保存到文件
    
    Args:
        compressed_ast: 压缩后的AST字典
        output_file: 输出文件路径
        use_gzip: 是否使用gzip压缩
        indent: JSON缩进级别，None表示不缩进
    """
    if use_gzip:
        with gzip.open(output_file + '.gz', 'wt', encoding='utf-8') as f:
            json.dump(compressed_ast, f, ensure_ascii=False, indent=indent)
        print(f"压缩AST已保存到: {output_file}.gz")
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(compressed_ast, f, ensure_ascii=False, indent=indent)
        print(f"AST已保存到: {output_file}")

def count_nodes(ast_node):
    """计算AST中的节点数量"""
    if not isinstance(ast_node, dict):
        return 0
    
    count = 1  # 当前节点
    
    # 递归计算子节点
    if "children" in ast_node:
        for child in ast_node["children"]:
            count += count_nodes(child)
    
    # 计算特殊字段中的节点
    for field in ["members", "body", "parameters"]:
        if field in ast_node:
            if isinstance(ast_node[field], list):
                for item in ast_node[field]:
                    count += count_nodes(item)
            else:
                count += count_nodes(ast_node[field])
    
    return count

def estimate_file_size_reduction(original_file: str, compressed_file: str) -> float:
    """估算文件大小减少的百分比"""
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    return (1 - compressed_size / original_size) * 100


# 使用示例
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Java AST压缩工具')
    parser.add_argument('input', help='Java源代码文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径', default=None)
    parser.add_argument('--depth', '-d', type=int, default=15, help='最大递归深度')
    parser.add_argument('--no-symbols', action='store_true', help='禁用符号表优化')
    parser.add_argument('--gzip', '-g', action='store_true', help='使用gzip压缩输出')
    parser.add_argument('--no-indent', action='store_true', help='输出不缩进的JSON')
    parser.add_argument('--positions', '-p', action='store_true', help='包含位置信息')
    
    args = parser.parse_args()
    
    # 读取指定的Java文件
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            java_code = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        exit(1)
    
    # 生成输出文件名
    if args.output:
        output_file = args.output
    else:
        filename = os.path.basename(args.input)
        base_name = os.path.splitext(filename)[0]
        output_file = f"{base_name}_ast_compressed.json"
    
    # 压缩AST
    print(f"正在压缩 {args.input}...")
    compressed_ast = compress_java_ast(
        java_code,
        max_depth=args.depth,
        include_position=args.positions,
        use_symbol_table=not args.no_symbols,
        compress_output=args.gzip
    )
    
    # 保存AST
    indent = None if args.no_indent else 2
    save_compressed_ast(
        compressed_ast,
        output_file,
        use_gzip=args.gzip,
        indent=indent
    )
    
    # 打印压缩前后的大小比较
    print(f"原始代码行数: {len(java_code.splitlines())}")
    print(f"压缩后AST节点数: {count_nodes(compressed_ast)}")
    
    # 如果保存了文件，计算压缩率
    try:
        input_size = os.path.getsize(args.input)
        output_size = os.path.getsize(output_file)
        if args.gzip:
            output_size = os.path.getsize(output_file + '.gz')
        compression_ratio = (1 - output_size / input_size) * 100
        print(f"压缩率: {compression_ratio:.2f}% (原始: {input_size/1024:.2f}KB, 压缩后: {output_size/1024:.2f}KB)")
    except:
        pass