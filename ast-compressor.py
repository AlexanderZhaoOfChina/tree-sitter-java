import json
from tree_sitter import Language, Parser
from typing import Dict, List, Optional, Union, Any
import os

class ASTCompressor:
    """用于压缩Java AST的工具类"""
    
    # 重要的节点类型，这些将被保留
    IMPORTANT_NODE_TYPES = {
        'program', 
        'package_declaration', 
        'import_declaration',
        'class_declaration', 
        'interface_declaration', 
        'enum_declaration',
        'method_declaration', 
        'constructor_declaration',
        'field_declaration', 
        'variable_declarator',
        'if_statement', 
        'for_statement', 
        'while_statement', 
        'do_statement',
        'switch_statement', 
        'case_statement',
        'try_statement', 
        'catch_clause',
        'method_invocation', 
        'class_instance_creation',
        'return_statement',
        'throw_statement',
        'assignment_expression',
        'binary_expression',
        'object_creation_expression',
        'lambda_expression',
        # 可以根据需要添加更多类型
    }
    
    # 可以被简化的节点类型（只保留关键信息）
    SIMPLIFIED_NODE_TYPES = {
        'modifiers', 
        'formal_parameters', 
        'type_parameters',
        'block', 
        'argument_list',
        'type_arguments'
    }
    
    # 可以被忽略的节点类型
    IGNORED_NODE_TYPES = {
        'comment', 
        'line_comment', 
        'block_comment',
        'semicolon', 
        'comma', 
        'dimensions',
        'parenthesized_expression',  # 除非需要保留括号语义
        'bracket_expression',
        'empty_statement',
        # 可以根据需要添加更多
    }
    
    def __init__(self, max_depth: int = 10, include_position: bool = False):
        """
        初始化AST压缩器
        
        Args:
            max_depth: 递归处理的最大深度
            include_position: 是否包含位置信息，默认为False
        """
        self.max_depth = max_depth
        self.include_position = include_position
        
    def compress(self, root_node) -> Dict[str, Any]:
        """
        压缩整个AST
        
        Args:
            root_node: tree-sitter的根节点
            
        Returns:
            压缩后的AST字典
        """
        return self._compress_node(root_node, 0)
    
    def _compress_node(self, node, depth: int) -> Optional[Dict[str, Any]]:
        """递归压缩单个节点及其子节点"""
        if node is None or depth > self.max_depth:
            return None
        
        node_type = node.type
        
        # 检查是否为忽略的节点类型
        if node_type in self.IGNORED_NODE_TYPES:
            return None
            
        # 获取节点文本（用于标识符、字面量等）
        node_text = node.text.decode('utf-8') if hasattr(node, 'text') else None
        
        # 创建基本节点信息
        result = {
            "type": node_type,
        }
        
        # 添加文本内容（对于标识符和字面量很重要）
        if node_text and (node_type in {'identifier', 'string_literal', 'number_literal', 
                                        'true', 'false', 'null_literal'}):
            result["text"] = node_text
            
        # 添加位置信息（如果需要）
        if self.include_position:
            result["start_point"] = {"row": node.start_point[0], "column": node.start_point[1]}
            result["end_point"] = {"row": node.end_point[0], "column": node.end_point[1]}
        
        # 基于节点类型进行特殊处理
        if node_type == 'method_declaration':
            # 方法声明的特殊处理
            result = self._process_method_declaration(node, depth, result)
        elif node_type == 'class_declaration':
            # 类声明的特殊处理
            result = self._process_class_declaration(node, depth, result)
        elif node_type in self.SIMPLIFIED_NODE_TYPES:
            # 简化处理某些节点类型
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
        if name_node:
            result["name"] = name_node.text.decode('utf-8')
        
        # 查找返回类型
        return_type = self._find_child_by_type(node, 'type_identifier')
        if return_type:
            result["return_type"] = return_type.text.decode('utf-8')
        
        # 处理参数
        params_node = self._find_child_by_type(node, 'formal_parameters')
        if params_node:
            params = []
            for param in params_node.children:
                if param.type == 'formal_parameter':
                    param_info = {}
                    param_type = self._find_child_by_type(param, 'type_identifier')
                    param_name = self._find_child_by_type(param, 'identifier')
                    
                    if param_type:
                        param_info["type"] = param_type.text.decode('utf-8')
                    if param_name:
                        param_info["name"] = param_name.text.decode('utf-8')
                    
                    if param_info:
                        params.append(param_info)
            
            if params:
                result["parameters"] = params
        
        # 处理方法体
        if depth < self.max_depth - 1:
            body_node = self._find_child_by_type(node, 'block')
            if body_node:
                body_content = self._compress_children(body_node, depth + 1)
                if body_content:
                    result["body"] = body_content
        
        return result
    
    def _process_class_declaration(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """处理类声明，提取关键信息"""
        # 查找类名
        name_node = self._find_child_by_type(node, 'identifier')
        if name_node:
            result["name"] = name_node.text.decode('utf-8')
        
        # 处理继承
        extends_node = self._find_child_by_field(node, 'superclass')
        if extends_node:
            result["extends"] = extends_node.text.decode('utf-8')
        
        # 处理接口实现
        implements_node = self._find_child_by_field(node, 'interfaces')
        if implements_node:
            interfaces = []
            for child in implements_node.children:
                if child.type == 'type_identifier':
                    interfaces.append(child.text.decode('utf-8'))
            if interfaces:
                result["implements"] = interfaces
        
        # 处理类成员
        if depth < self.max_depth - 1:
            class_body = self._find_child_by_type(node, 'class_body')
            if class_body:
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
        result["text"] = node.text.decode('utf-8') if hasattr(node, 'text') else None
        
        # 对于某些特定节点，我们可能希望保留部分子节点
        if node.type == 'formal_parameters':
            # 参数列表，可能需要简化表示
            params_count = sum(1 for child in node.children if child.type == 'formal_parameter')
            result["params_count"] = params_count
        
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


def compress_java_ast(java_code: str, max_depth: int = 10) -> Dict[str, Any]:
    """
    解析并压缩Java代码的AST
    
    Args:
        java_code: Java源代码字符串
        max_depth: 最大递归深度
    
    Returns:
        压缩后的AST字典
    """
    # 构建Java语言库
    try:
        Language.build_library(
            # Windows上使用.dll扩展名
            'build/languages.dll',
            [os.path.join(os.path.dirname(__file__), 'tree-sitter-java')]
        )
        JAVA_LANGUAGE = Language('build/languages.dll', 'java')
    except:
        # 如果构建失败，尝试直接加载已存在的库
        JAVA_LANGUAGE = Language('build/languages.dll', 'java')
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    
    tree = parser.parse(bytes(java_code, 'utf8'))
    compressor = ASTCompressor(max_depth=max_depth)
    
    return compressor.compress(tree.root_node)


def save_compressed_ast(compressed_ast: Dict[str, Any], output_file: str) -> None:
    """
    将压缩后的AST保存到文件
    
    Args:
        compressed_ast: 压缩后的AST字典
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compressed_ast, f, ensure_ascii=False, indent=2)

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

# 使用示例
if __name__ == "__main__":
    # 读取指定的Java文件
    java_file_path = "8/src/main/java/com/asiainfo/cvd/daemon/CNVDDirectoryWatcherDaemon.java"
    try:
        with open(java_file_path, 'r', encoding='utf-8') as f:
            java_code = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        exit(1)
    
    # 生成输出文件名
    output_file = "CNVDDirectoryWatcherDaemon_ast_output2.json"
    
    # 注意：确保已正确设置tree-sitter和Java语言支持
    compressed_ast = compress_java_ast(java_code)
    save_compressed_ast(compressed_ast, output_file)
    
    # 打印压缩前后的大小比较
    print(f"原始代码行数: {len(java_code.splitlines())}")
    print(f"压缩后AST节点数: {count_nodes(compressed_ast)}")
    print(f"AST已保存到: {output_file}")


