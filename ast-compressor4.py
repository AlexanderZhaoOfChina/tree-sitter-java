import json
from tree_sitter import Language, Parser
from typing import Dict, List, Optional, Union, Any, Set, Tuple
import os
import gzip
from collections import defaultdict, Counter

class EnhancedASTCompressor:
    """增强版Java AST压缩工具类，针对LLM代码理解的特殊优化"""
    
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
        'modifiers', 'type_parameters',
        'bracket_expression',
    }
    
    # 完全忽略的节点类型（不再忽略注释！）
    IGNORED_NODE_TYPES = {
        'semicolon', 'comma', 'dimensions', 
        'empty_statement', '.', ';', '{', '}', '(', ')', '[', ']'
    }
    
    # 注释节点类型，需要特殊处理
    COMMENT_NODE_TYPES = {
        'comment', 'line_comment', 'block_comment',
    }
    
    # 对文本内容进行保留的节点类型
    TEXT_NODES = {
        'identifier', 'string_literal', 'number_literal', 'character_literal',
        'decimal_integer_literal', 'hex_integer_literal', 'octal_integer_literal',
        'binary_integer_literal', 'decimal_floating_point_literal', 'true', 
        'false', 'null_literal', 'type_identifier'
    }
    
    # 控制流节点，需要完整保留结构
    CONTROL_FLOW_NODES = {
        'if_statement', 'for_statement', 'while_statement', 'do_statement',
        'switch_statement', 'try_statement', 'return_statement', 'throw_statement',
        'synchronized_statement', 'break_statement', 'continue_statement'
    }
    
    # 表示状态变更的节点类型
    STATE_CHANGE_NODES = {
        'assignment_expression', 'update_expression', 'method_invocation'
    }
    
    def __init__(self, max_depth: int = 20, include_position: bool = False, 
                 preserve_comments: bool = True, extract_control_flow: bool = True,
                 track_variable_usage: bool = True, analyze_method_calls: bool = True,
                 identify_state_changes: bool = True, semantic_grouping: bool = True,
                 calculate_complexity: bool = True, max_method_body_depth: int = 8):
        """
        初始化增强版AST压缩器
        
        Args:
            max_depth: 递归处理的最大深度
            include_position: 是否包含位置信息
            preserve_comments: 是否保留注释信息
            extract_control_flow: 是否提取控制流结构
            track_variable_usage: 是否跟踪变量使用情况
            analyze_method_calls: 是否分析方法调用关系
            identify_state_changes: 是否识别状态变更点
            semantic_grouping: 是否进行方法的语义分组
            calculate_complexity: 是否计算复杂度指标
            max_method_body_depth: 方法体最大递归深度
        """
        self.max_depth = max_depth
        self.include_position = include_position
        self.preserve_comments = preserve_comments
        self.extract_control_flow = extract_control_flow
        self.track_variable_usage = track_variable_usage
        self.analyze_method_calls = analyze_method_calls
        self.identify_state_changes = identify_state_changes
        self.semantic_grouping = semantic_grouping
        self.calculate_complexity = calculate_complexity
        self.max_method_body_depth = max_method_body_depth
        
        # 用于跟踪已收集的注释
        self.comments = []
        
        # 用于收集变量使用信息
        self.variable_usages = defaultdict(list)
        
        # 用于收集方法调用关系
        self.method_calls = defaultdict(list)
        
        # 用于收集状态变更点
        self.state_changes = []
        
        # 用于方法语义分组
        self.method_groups = {}
        
        # 用于计算方法复杂度
        self.method_complexity = {}
        
        # 当前处理的类和方法上下文
        self.current_class = None
        self.current_method = None
    
    def compress(self, root_node, source_code: Optional[str] = None) -> Dict[str, Any]:
        """压缩整个AST，并添加增强的语义分析信息
        
        Args:
            root_node: AST根节点
            source_code: 原始源代码文本，用于提取注释和上下文
        
        Returns:
            增强压缩后的AST
        """
        # 重置状态
        self.comments = []
        self.variable_usages = defaultdict(list)
        self.method_calls = defaultdict(list)
        self.state_changes = []
        self.method_groups = {}
        self.method_complexity = {}
        self.current_class = None
        self.current_method = None
        
        # 第一遍：收集注释和基本信息
        if self.preserve_comments or self.track_variable_usage:
            self._analyze_and_collect(root_node, 0, source_code)
        
        # 第二遍：实际压缩AST
        result = self._compress_node(root_node, 0)
        
        # 添加代码上下文信息
        if source_code:
            result["code_context"] = self._extract_code_context(root_node, source_code)
        
        # 添加收集的注释（如果启用）
        if self.preserve_comments and self.comments:
            result["comments"] = self.comments
        
        # 添加变量使用信息（如果启用）
        if self.track_variable_usage and self.variable_usages:
            result["variable_usages"] = dict(self.variable_usages)
        
        # 添加方法调用关系（如果启用）
        if self.analyze_method_calls and self.method_calls:
            result["method_calls"] = dict(self.method_calls)
        
        # 添加状态变更点（如果启用）
        if self.identify_state_changes and self.state_changes:
            result["state_changes"] = self.state_changes
        
        # 添加方法语义分组（如果启用）
        if self.semantic_grouping and self.method_groups:
            result["method_groups"] = self.method_groups
        
        # 添加方法复杂度指标（如果启用）
        if self.calculate_complexity and self.method_complexity:
            result["method_complexity"] = self.method_complexity
        
        # 生成代码摘要
        result["summary"] = self._generate_code_summary(result)
        
        return result
    
    def _analyze_and_collect(self, node, depth: int, source_code: Optional[str] = None) -> None:
        """第一遍遍历：收集注释、变量使用和方法调用信息"""
        if node is None or depth > self.max_depth:
            return
        
        # 更新当前处理的类和方法上下文
        self._update_context(node)
        
        # 收集注释节点
        if self.preserve_comments and node.type in self.COMMENT_NODE_TYPES and hasattr(node, 'text'):
            comment_text = node.text.decode('utf-8').strip()
            if comment_text:
                # 为注释添加位置信息
                comment_info = {
                    "text": comment_text,
                    "type": node.type
                }
                
                if hasattr(node, 'start_point') and hasattr(node, 'end_point'):
                    comment_info["line"] = node.start_point[0] + 1
                    
                    # 尝试关联注释到类或方法
                    if self.current_class:
                        comment_info["associated_class"] = self.current_class
                    if self.current_method:
                        comment_info["associated_method"] = self.current_method
                
                self.comments.append(comment_info)
        
        # 收集变量使用信息
        if self.track_variable_usage:
            self._collect_variable_usage(node)
        
        # 收集方法调用信息
        if self.analyze_method_calls and node.type == 'method_invocation':
            self._collect_method_call(node)
        
        # 收集状态变更点
        if self.identify_state_changes and node.type in self.STATE_CHANGE_NODES:
            self._collect_state_change(node)
        
        # 递归处理子节点
        if hasattr(node, 'children'):
            for child in node.children:
                self._analyze_and_collect(child, depth + 1, source_code)
    
    def _update_context(self, node) -> None:
        """更新当前处理的类和方法上下文"""
        if node.type == 'class_declaration':
            name_node = self._find_child_by_type(node, 'identifier')
            if name_node and hasattr(name_node, 'text'):
                self.current_class = name_node.text.decode('utf-8')
        
        elif node.type == 'method_declaration':
            name_node = self._find_child_by_type(node, 'identifier')
            if name_node and hasattr(name_node, 'text'):
                self.current_method = name_node.text.decode('utf-8')
    
    def _collect_variable_usage(self, node) -> None:
        """收集变量使用信息"""
        # 变量声明
        if node.type == 'variable_declarator':
            name_node = self._find_child_by_type(node, 'identifier')
            if name_node and hasattr(name_node, 'text'):
                var_name = name_node.text.decode('utf-8')
                
                # 检查是否有初始化表达式
                initializer = None
                for child in node.children:
                    if child.type not in {'identifier', '='}:
                        initializer = child.type
                        break
                
                usage = {
                    "type": "declaration",
                    "location": {
                        "line": node.start_point[0] + 1 if hasattr(node, 'start_point') else -1
                    }
                }
                
                if initializer:
                    usage["initializer"] = initializer
                
                if self.current_method:
                    usage["in_method"] = self.current_method
                
                self.variable_usages[var_name].append(usage)
        
        # 变量引用
        elif node.type == 'identifier' and not self._is_method_name(node) and not self._is_type_name(node):
            var_name = node.text.decode('utf-8') if hasattr(node, 'text') else "unknown"
            
            # 确定使用类型（读取、修改）
            usage_type = "read"
            parent = self._get_parent(node)
            
            if parent and parent.type == 'assignment_expression':
                if node is parent.children[0]:  # 左侧 = 赋值目标
                    usage_type = "write"
            
            usage = {
                "type": usage_type,
                "location": {
                    "line": node.start_point[0] + 1 if hasattr(node, 'start_point') else -1
                }
            }
            
            if self.current_method:
                usage["in_method"] = self.current_method
            
            self.variable_usages[var_name].append(usage)
    
    def _is_method_name(self, node) -> bool:
        """检查标识符是否为方法名"""
        parent = self._get_parent(node)
        if parent and parent.type in {'method_declaration', 'method_invocation'}:
            children = parent.children if hasattr(parent, 'children') else []
            if node in children:
                index = children.index(node)
                # 方法声明中的标识符通常是第一个子节点
                # 方法调用中的标识符通常是第二个子节点（第一个通常是调用对象）
                return index == 0 or index == 1
        return False
    
    def _is_type_name(self, node) -> bool:
        """检查标识符是否为类型名"""
        parent = self._get_parent(node)
        if parent and parent.type in {'type_identifier', 'class_declaration', 'interface_declaration'}:
            return True
        return False
    
    def _get_parent(self, node):
        """获取节点的父节点（注意：tree-sitter不直接支持，这是一个近似方法）"""
        # 实际实现可能需要在遍历过程中构建父子关系
        # 这里只是一个占位实现
        return None
    
    def _collect_method_call(self, node) -> None:
        """收集方法调用信息"""
        method_name = self._get_method_call_name(node)
        if not method_name:
            return
            
        caller = self._find_method_caller(node)
        args_count = self._count_call_arguments(node)
        
        call_info = {
            "caller": caller,
            "args_count": args_count,
            "location": {
                "line": node.start_point[0] + 1 if hasattr(node, 'start_point') else -1
            }
        }
        
        # 记录调用上下文
        if self.current_method:
            call_info["called_from"] = self.current_method
        
        # 尝试分析调用意图
        call_intent = self._analyze_call_intent(node, method_name)
        if call_intent:
            call_info["intent"] = call_intent
        
        self.method_calls[method_name].append(call_info)
    
    def _analyze_call_intent(self, node, method_name: str) -> Optional[str]:
        """分析方法调用的意图"""
        # 基于方法名前缀推断意图
        if method_name.startswith("get") or method_name.startswith("find") or method_name.startswith("read"):
            return "accessor"
        elif method_name.startswith("set") or method_name.startswith("update") or method_name.startswith("write"):
            return "mutator"
        elif method_name.startswith("is") or method_name.startswith("has") or method_name.startswith("can"):
            return "predicate"
        elif method_name.startswith("create") or method_name.startswith("build") or method_name.startswith("make"):
            return "factory"
        elif method_name.startswith("parse") or method_name.startswith("convert") or method_name.startswith("transform"):
            return "transformer"
        elif method_name.startswith("validate") or method_name.startswith("check") or method_name.startswith("ensure"):
            return "validator"
        
        # 基于调用上下文推断意图
        parent = self._get_parent(node)
        if parent:
            if parent.type in {'if_statement', 'while_statement', 'for_statement'}:
                # 在条件中使用，可能是谓词或验证
                return "condition"
            elif parent.type == 'return_statement':
                # 在返回语句中，可能是提供值
                return "provider"
        
        return None
    
    def _collect_state_change(self, node) -> None:
        """收集状态变更点"""
        if node.type == 'assignment_expression':
            # 提取赋值目标
            if hasattr(node, 'children') and len(node.children) >= 3:
                target = node.children[0]
                if hasattr(target, 'text'):
                    target_name = target.text.decode('utf-8')
                    
                    change_info = {
                        "type": "assignment",
                        "target": target_name,
                        "location": {
                            "line": node.start_point[0] + 1 if hasattr(node, 'start_point') else -1
                        }
                    }
                    
                    if self.current_method:
                        change_info["in_method"] = self.current_method
                    
                    self.state_changes.append(change_info)
        
        elif node.type == 'method_invocation':
            method_name = self._get_method_call_name(node)
            
            # 基于名称判断是否可能更改状态
            if method_name and (method_name.startswith("set") or 
                                method_name.startswith("update") or 
                                method_name.startswith("add") or 
                                method_name.startswith("remove") or
                                method_name.startswith("delete")):
                
                change_info = {
                    "type": "method_invocation",
                    "method": method_name,
                    "location": {
                        "line": node.start_point[0] + 1 if hasattr(node, 'start_point') else -1
                    }
                }
                
                if self.current_method:
                    change_info["in_method"] = self.current_method
                
                self.state_changes.append(change_info)
    
    def _get_method_call_name(self, node) -> Optional[str]:
        """获取方法调用的名称"""
        # 查找方法名节点
        if hasattr(node, 'children'):
            for i, child in enumerate(node.children):
                if i > 0 and child.type == 'identifier' and hasattr(child, 'text'):
                    return child.text.decode('utf-8')
        
        return None
    
    def _find_method_caller(self, node) -> Optional[str]:
        """查找方法调用的调用者"""
        if hasattr(node, 'children') and len(node.children) > 0:
            first_child = node.children[0]
            if first_child.type == 'identifier' and hasattr(first_child, 'text'):
                return first_child.text.decode('utf-8')
        
        return None
    
    def _count_call_arguments(self, node) -> int:
        """统计方法调用的参数数量"""
        args_count = 0
        if hasattr(node, 'children'):
            for child in node.children:
                if child.type == 'argument_list' and hasattr(child, 'children'):
                    for arg in child.children:
                        if arg.type not in {',', '(', ')'}:
                            args_count += 1
        return args_count
    
    def _extract_code_context(self, root_node, source_code: str) -> Dict[str, Any]:
        """提取代码上下文信息"""
        context = {
            "declared_classes": [],
            "imported_packages": [],
            "package_name": None,
            "statistics": {
                "total_lines": source_code.count('\n') + 1,
                "code_lines": 0,
                "comment_lines": 0,
                "blank_lines": 0
            }
        }
        
        # 统计代码行、空行和注释行
        for line in source_code.split('\n'):
            line = line.strip()
            if not line:
                context["statistics"]["blank_lines"] += 1
            elif line.startswith('//') or line.startswith('/*') or line.startswith('*'):
                context["statistics"]["comment_lines"] += 1
            else:
                context["statistics"]["code_lines"] += 1
        
        # 提取包名
        package_node = self._find_child_by_type(root_node, 'package_declaration')
        if package_node:
            # 从包声明中提取完整路径
            package_name = self._extract_package_name(package_node)
            if package_name:
                context["package_name"] = package_name
        
        # 提取导入和类
        if hasattr(root_node, 'children'):
            for child in root_node.children:
                if child.type == 'import_declaration':
                    import_name = self._extract_import_name(child)
                    if import_name:
                        context["imported_packages"].append(import_name)
                
                elif child.type in {'class_declaration', 'interface_declaration', 'enum_declaration'}:
                    class_name = self._get_node_name(child)
                    if class_name:
                        context["declared_classes"].append(class_name)
        
        return context
    
    def _extract_package_name(self, package_node) -> Optional[str]:
        """从包声明节点提取包名"""
        if hasattr(package_node, 'children'):
            for child in package_node.children:
                if child.type == 'scoped_identifier' and hasattr(child, 'text'):
                    return child.text.decode('utf-8')
                
                # 递归检查嵌套结构
                name = self._extract_package_name(child)
                if name:
                    return name
        
        return None
    
    def _extract_import_name(self, import_node) -> Optional[str]:
        """从导入声明节点提取导入名"""
        if hasattr(import_node, 'children'):
            for child in import_node.children:
                if child.type == 'scoped_identifier' and hasattr(child, 'text'):
                    return child.text.decode('utf-8')
                
                # 递归检查嵌套结构
                name = self._extract_import_name(child)
                if name:
                    return name
        
        return None
    
    def _get_node_name(self, node) -> Optional[str]:
        """获取节点的名称（通常是标识符）"""
        name_node = self._find_child_by_type(node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            return name_node.text.decode('utf-8')
        return None
    
    def _generate_code_summary(self, compressed_ast: Dict[str, Any]) -> Dict[str, Any]:
        """生成代码摘要信息"""
        summary = {
            "file_type": "Java source file"
        }
        
        # 提取包名
        if "code_context" in compressed_ast and "package_name" in compressed_ast["code_context"]:
            summary["package"] = compressed_ast["code_context"]["package_name"]
        
        # 提取类信息
        classes = []
        for node in compressed_ast.get("children", []):
            if node.get("type") == "class_declaration":
                class_info = self._generate_class_summary(node)
                if class_info:
                    classes.append(class_info)
        
        if classes:
            summary["classes"] = classes
        
        # 提取统计信息
        if "code_context" in compressed_ast and "statistics" in compressed_ast["code_context"]:
            summary["statistics"] = compressed_ast["code_context"]["statistics"]
        
        # 添加复杂度信息
        if "method_complexity" in compressed_ast:
            complexity_summary = {}
            for method, complexity in compressed_ast["method_complexity"].items():
                complexity_summary[method] = {
                    "cyclomatic_complexity": complexity.get("cyclomatic", 1),
                    "nesting_depth": complexity.get("max_nesting", 0)
                }
            
            if complexity_summary:
                summary["complexity"] = complexity_summary
        
        # 添加方法分组信息
        if "method_groups" in compressed_ast:
            summary["method_groups"] = compressed_ast["method_groups"]
        
        return summary
    
    def _generate_class_summary(self, class_node: Dict[str, Any]) -> Dict[str, Any]:
        """生成类的摘要信息"""
        class_info = {
            "name": class_node.get("name", "Unknown"),
            "modifiers": class_node.get("modifiers", [])
        }
        
        # 添加继承信息
        if "extends" in class_node:
            class_info["extends"] = class_node["extends"]
        
        # 添加实现接口信息
        if "implements" in class_node:
            class_info["implements"] = class_node["implements"]
        
        # 统计成员信息
        if "members" in class_node:
            members = class_node["members"]
            
            # 统计字段
            if "fields" in members:
                fields = []
                for field in members["fields"]:
                    field_info = self._extract_field_info(field)
                    if field_info:
                        fields.append(field_info)
                
                if fields:
                    class_info["fields"] = fields
            
            # 统计方法
            if "methods" in members:
                methods = []
                for method in members["methods"]:
                    method_info = self._extract_method_info(method)
                    if method_info:
                        methods.append(method_info)
                
                if methods:
                    class_info["methods"] = methods
        
        return class_info
    
    def _extract_field_info(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """提取字段信息"""
        field_info = {}
        
        # 查找变量声明器
        for child in field.get("children", []):
            if child.get("type") == "variable_declarator":
                name_node = None
                for var_child in child.get("children", []):
                    if var_child.get("type") == "identifier":
                        name_node = var_child
                        break
                
                if name_node and "text" in name_node:
                    field_info["name"] = name_node["text"]
        
        # 提取字段类型
        for child in field.get("children", []):
            if child.get("type") == "type_identifier":
                field_info["type"] = child.get("text", "unknown")
                break
        
        # 提取修饰符
        modifiers = []
        for child in field.get("children", []):
            if child.get("type") == "modifiers":
                for mod in child.get("children", []):
                    if mod.get("type") in {"public", "private", "protected", "static", "final"}:
                        modifiers.append(mod.get("type"))
        
        if modifiers:
            field_info["modifiers"] = modifiers
        
        return field_info
    
    def _extract_method_info(self, method: Dict[str, Any]) -> Dict[str, Any]:
        """提取方法信息"""
        method_info = {
            "name": method.get("name", "unknown"),
            "modifiers": method.get("modifiers", []),
            "return_type": method.get("return_type", "void")
        }
        
        # 添加参数信息
        if "parameters" in method:
            params = []
            for param in method["parameters"]:
                param_info = {}
                if "type" in param:
                    param_info["type"] = param["type"]
                if "name" in param:
                    param_info["name"] = param["name"]
                
                if param_info:
                    params.append(param_info)
            
            if params:
                method_info["parameters"] = params
        
        # 添加控制流信息
        if "control_flow" in method:
            flow_summary = self._summarize_control_flow(method["control_flow"])
            if flow_summary:
                method_info["flow_summary"] = flow_summary
        
        # 添加功能分类
        intent = self._classify_method_intent(method)
        if intent:
            method_info["intent"] = intent
        
        return method_info
    
    def _summarize_control_flow(self, control_flow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """总结控制流信息"""
        summary = {
            "if_count": 0,
            "loop_count": 0,
            "try_catch_count": 0,
            "return_points": 0,
            "throw_points": 0
        }
        
        for node in control_flow:
            node_type = node.get("type", "")
            
            if node_type == "if_statement":
                summary["if_count"] += 1
            elif node_type in {"for_statement", "while_statement", "do_statement"}:
                summary["loop_count"] += 1
            elif node_type == "try_statement":
                summary["try_catch_count"] += 1
            elif node_type == "return_statement":
                summary["return_points"] += 1
            elif node_type == "throw_statement":
                summary["throw_points"] += 1
        
        return summary
    
    def _classify_method_intent(self, method: Dict[str, Any]) -> Optional[str]:
        """分类方法意图"""
        method_name = method.get("name", "")
        
        # 基于名称前缀分类
        if method_name.startswith("get") or method_name.startswith("find") or method_name.startswith("read"):
            return "accessor"
        elif method_name.startswith("set") or method_name.startswith("update") or method_name.startswith("write"):
            return "mutator"
        elif method_name.startswith("is") or method_name.startswith("has") or method_name.startswith("can"):
            return "predicate"
        elif method_name.startswith("create") or method_name.startswith("build") or method_name.startswith("make"):
            return "factory"
        elif method_name.startswith("parse") or method_name.startswith("convert") or method_name.startswith("transform"):
            return "transformer"
        elif method_name.startswith("validate") or method_name.startswith("check") or method_name.startswith("ensure"):
            return "validator"
        elif method_name.startswith("process") or method_name.startswith("handle") or method_name.startswith("execute"):
            return "processor"
        
        # 基于返回类型分类
        return_type = method.get("return_type", "void")
        if return_type == "void":
            # 无返回值的方法通常是动作执行器或修改器
            if "state_changes" in method:
                return "mutator"
            else:
                return "action"
        elif return_type == "boolean":
            return "predicate"
        
        # 基于控制流分类
        if "flow_summary" in method:
            flow = method["flow_summary"]
            if flow.get("try_catch_count", 0) > 0:
                return "protected_action"
            if flow.get("return_points", 0) > 1:
                return "multi_condition"
        
        return None
    
    def _compress_node(self, node, depth: int) -> Optional[Dict[str, Any]]:
        """递归压缩单个节点及其子节点"""
        if node is None or depth > self.max_depth:
            return None
        
        node_type = node.type
        
        # 检查是否为忽略的节点类型
        if node_type in self.IGNORED_NODE_TYPES:
            return None
        
        # 特殊处理注释节点
        if self.preserve_comments and node_type in self.COMMENT_NODE_TYPES:
            comment_text = node.text.decode('utf-8') if hasattr(node, 'text') and node.text else None
            if comment_text:
                return {
                    "type": node_type,
                    "text": comment_text
                }
            return None
        
        # 获取节点文本
        node_text = None
        if hasattr(node, 'text'):
            node_text = node.text.decode('utf-8') if node.text else None
        
        # 创建基本节点信息
        result = {"type": node_type}
        
        # 添加文本内容（对于标识符和字面量很重要）
        if node_text and (node_type in self.TEXT_NODES):
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
        elif node_type == 'block':
            # 增强版块处理，保留控制流结构
            result = self._process_block(node, depth, result)
        elif node_type in self.CONTROL_FLOW_NODES:
            # 增强版控制流节点处理
            result = self._process_control_flow_node(node, depth, result)
        elif node_type == 'method_invocation':
            # 增强版方法调用处理
            result = self._process_method_invocation(node, depth, result)
        elif node_type == 'assignment_expression':
            # 增强版赋值表达式处理
            result = self._process_assignment(node, depth, result)
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
        """增强版方法声明处理，提取丰富的方法特征"""
        # 保存当前处理的方法名
        method_name = None
        
        # 查找方法名
        name_node = self._find_child_by_type(node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            method_name = name_node.text.decode('utf-8')
            result["name"] = method_name
            self.current_method = method_name
        
        # 处理修饰符
        modifiers = []
        modifiers_node = self._find_child_by_type(node, 'modifiers')
        if modifiers_node:
            for mod in modifiers_node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final', 'abstract', 'synchronized'}:
                    modifiers.append(mod.type)
        if modifiers:
            result["modifiers"] = modifiers
        
        # 查找返回类型
        return_type = self._find_child_by_type(node, 'type_identifier')
        if return_type and hasattr(return_type, 'text'):
            result["return_type"] = return_type.text.decode('utf-8')
        else:
            # 检查是否有void类型
            void_type = self._find_child_by_type(node, 'void_type')
            if void_type:
                result["return_type"] = "void"
        
        # 处理参数
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
                        param_info["name"] = param_name.text.decode('utf-8')
                    
                    if param_info:
                        params.append(param_info)
            
            if params:
                result["parameters"] = params
        
        # 处理方法体
        body_node = self._find_child_by_type(node, 'block')
        if body_node and depth < self.max_method_body_depth:
            if self.extract_control_flow:
                # 提取控制流
                control_flow = self._extract_control_flow(body_node)
                if control_flow:
                    result["control_flow"] = control_flow
                
                # 计算圈复杂度
                if self.calculate_complexity and method_name:
                    cyclomatic = self._calculate_cyclomatic_complexity(control_flow)
                    max_nesting = self._calculate_max_nesting(body_node)
                    
                    self.method_complexity[method_name] = {
                        "cyclomatic": cyclomatic,
                        "max_nesting": max_nesting
                    }
            else:
                # 只统计语句类型
                stmt_counts = self._count_statement_types(body_node)
                if stmt_counts:
                    result["body_summary"] = stmt_counts
        
        # 方法语义分析
        if method_name and self.semantic_grouping:
            intent = self._analyze_method_intent(node, method_name, result)
            if intent:
                # 将方法按意图分组
                if intent not in self.method_groups:
                    self.method_groups[intent] = []
                self.method_groups[intent].append(method_name)
                
                result["intent"] = intent
        
        # 重置当前方法
        self.current_method = None
        
        return result
    
    def _analyze_method_intent(self, node, method_name: str, method_info: Dict[str, Any]) -> str:
        """分析方法的功能意图"""
        # 基于命名约定的分析
        name_lower = method_name.lower()
        
        # 访问器方法
        if name_lower.startswith("get") or name_lower.startswith("find") or name_lower.startswith("retrieve"):
            return "accessor"
        
        # 修改器方法
        if name_lower.startswith("set") or name_lower.startswith("update") or name_lower.startswith("modify"):
            return "mutator"
        
        # 谓词方法
        if name_lower.startswith("is") or name_lower.startswith("has") or name_lower.startswith("can") or name_lower.startswith("should"):
            return "predicate"
        
        # 创建方法
        if name_lower.startswith("create") or name_lower.startswith("new") or name_lower.startswith("build") or name_lower.startswith("generate"):
            return "factory"
        
        # 转换方法
        if name_lower.startswith("convert") or name_lower.startswith("transform") or name_lower.startswith("parse"):
            return "transformer"
        
        # 验证方法
        if name_lower.startswith("validate") or name_lower.startswith("check") or name_lower.startswith("verify"):
            return "validator"
        
        # 处理方法
        if name_lower.startswith("process") or name_lower.startswith("handle") or name_lower.startswith("execute"):
            return "processor"
        
        # 计算方法
        if name_lower.startswith("calculate") or name_lower.startswith("compute") or name_lower.startswith("count"):
            return "calculator"
        
        # 基于返回类型的分析
        return_type = method_info.get("return_type")
        if return_type == "void":
            # 无返回值的方法可能是动作或处理器
            return "action"
        if return_type == "boolean":
            return "predicate"
        
        # 基于参数和修饰符的分析
        params = method_info.get("parameters", [])
        modifiers = method_info.get("modifiers", [])
        
        if not params and "static" in modifiers:
            return "utility"
        
        if "main" in name_lower:
            return "entry_point"
        
        # 如果上面都不匹配，尝试基于方法体内容推断
        # 这需要访问方法体内容，在这里我们可以使用已经提取的控制流
        if "control_flow" in method_info:
            # 检查是否包含大量的条件分支
            if_count = sum(1 for node in method_info["control_flow"] if node.get("type") == "if_statement")
            try_count = sum(1 for node in method_info["control_flow"] if node.get("type") == "try_statement")
            
            if if_count > 3:
                return "decision_maker"
            if try_count > 0:
                return "protected_action"
        
        # 默认分类
        return "general"
    
    def _extract_control_flow(self, node) -> List[Dict[str, Any]]:
        """提取控制流结构"""
        result = []
        
        if not hasattr(node, 'children'):
            return result
        
        # 提取当前节点的控制流结构
        if node.type in self.CONTROL_FLOW_NODES:
            flow_node = {"type": node.type}
            
            # 对特定控制流节点类型进行特殊处理
            if node.type == 'if_statement':
                # 提取条件表达式
                condition = self._find_condition_expression(node)
                if condition:
                    flow_node["condition"] = self._summarize_expression(condition)
                
                # 提取then分支
                then_block = self._find_then_block(node)
                if then_block:
                    then_flow = self._extract_control_flow(then_block)
                    if then_flow:
                        flow_node["then"] = then_flow
                
                # 提取else分支
                else_block = self._find_else_block(node)
                if else_block:
                    else_flow = self._extract_control_flow(else_block)
                    if else_flow:
                        flow_node["else"] = else_flow
            
            elif node.type in {'for_statement', 'while_statement', 'do_statement'}:
                # 提取循环条件
                condition = self._find_condition_expression(node)
                if condition:
                    flow_node["condition"] = self._summarize_expression(condition)
                
                # 提取循环体
                body = self._find_loop_body(node)
                if body:
                    body_flow = self._extract_control_flow(body)
                    if body_flow:
                        flow_node["body"] = body_flow
            
            elif node.type == 'try_statement':
                # 提取try块
                try_block = self._find_try_block(node)
                if try_block:
                    try_flow = self._extract_control_flow(try_block)
                    if try_flow:
                        flow_node["try"] = try_flow
                
                # 提取catch块
                catch_blocks = []
                for catch in self._find_catch_clauses(node):
                    catch_info = {"type": "catch_clause"}
                    
                    # 提取异常类型
                    exception_type = self._find_catch_exception_type(catch)
                    if exception_type:
                        catch_info["exception_type"] = exception_type
                    
                    # 提取catch块内容
                    catch_block = self._find_catch_block(catch)
                    if catch_block:
                        catch_flow = self._extract_control_flow(catch_block)
                        if catch_flow:
                            catch_info["body"] = catch_flow
                    
                    catch_blocks.append(catch_info)
                
                if catch_blocks:
                    flow_node["catch"] = catch_blocks
                
                # 提取finally块
                finally_block = self._find_finally_block(node)
                if finally_block:
                    finally_flow = self._extract_control_flow(finally_block)
                    if finally_flow:
                        flow_node["finally"] = finally_flow
            
            elif node.type == 'return_statement':
                # 提取返回表达式
                expr = self._find_return_expression(node)
                if expr:
                    flow_node["expression"] = self._summarize_expression(expr)
                    flow_node["expression_type"] = self._infer_expression_type(expr)
            
            elif node.type == 'throw_statement':
                # 提取抛出表达式
                expr = self._find_throw_expression(node)
                if expr:
                    flow_node["expression"] = self._summarize_expression(expr)
                    flow_node["expression_type"] = self._infer_expression_type(expr)
            
            elif node.type == 'switch_statement':
                # 提取switch表达式
                expr = self._find_switch_expression(node)
                if expr:
                    flow_node["expression"] = self._summarize_expression(expr)
                
                # 提取case块
                cases = self._extract_switch_cases(node)
                if cases:
                    flow_node["cases"] = cases
            
            result.append(flow_node)
        
        elif node.type == 'block':
            # 对于代码块，递归处理所有子语句
            for child in node.children:
                if child.type not in {'{', '}'}:
                    child_flow = self._extract_control_flow(child)
                    result.extend(child_flow)
        
        elif node.type == 'expression_statement':
            # 处理表达式语句
            expr = self._extract_expression(node)
            if expr:
                result.append(expr)
        
        return result
    
    def _extract_expression(self, node) -> Optional[Dict[str, Any]]:
        """从表达式语句中提取表达式"""
        if not hasattr(node, 'children') or not node.children:
            return None
        
        # 查找第一个非分隔符子节点
        for child in node.children:
            if child.type not in {';'}:
                # 特殊处理方法调用
                if child.type == 'method_invocation':
                    return self._extract_method_invocation(child)
                
                # 特殊处理赋值表达式
                elif child.type == 'assignment_expression':
                    return self._extract_assignment(child)
                
                # 默认处理
                return {
                    "type": "expression",
                    "expression_type": child.type
                }
        
        return None
    
    def _extract_method_invocation(self, node) -> Dict[str, Any]:
        """提取方法调用信息"""
        result = {"type": "method_invocation"}
        
        # 提取方法名
        method_name = self._get_method_call_name(node)
        if method_name:
            result["method"] = method_name
        
        # 提取调用者
        caller = self._find_method_caller(node)
        if caller:
            result["caller"] = caller
        
        # 提取参数数量
        result["args_count"] = self._count_call_arguments(node)
        
        return result
    
    def _extract_assignment(self, node) -> Dict[str, Any]:
        """提取赋值表达式信息"""
        result = {"type": "assignment"}
        
        # 提取左侧（赋值目标）
        left = self._find_assignment_left(node)
        if left and hasattr(left, 'text'):
            result["target"] = left.text.decode('utf-8')
        
        # 提取右侧（赋值来源）
        right = self._find_assignment_right(node)
        if right:
            result["source_type"] = right.type
            
            # 如果右侧是方法调用，提取更多信息
            if right.type == 'method_invocation':
                method_info = self._extract_method_invocation(right)
                if method_info:
                    result["source"] = method_info
        
        return result
    
    def _find_condition_expression(self, node):
        """查找条件表达式"""
        if hasattr(node, 'children'):
            for child in node.children:
                if child.type == 'parenthesized_expression':
                    # 条件通常在括号内
                    if hasattr(child, 'children'):
                        for paren_child in child.children:
                            if paren_child.type not in {'(', ')'}:
                                return paren_child
        return None
    
    def _find_then_block(self, if_node):
        """查找if语句的then块"""
        if hasattr(if_node, 'children'):
            # 找到条件后的第一个块或语句
            found_condition = False
            for child in if_node.children:
                if found_condition and child.type not in {'else'}:
                    return child
                if child.type == 'parenthesized_expression':
                    found_condition = True
        return None
    
    def _find_else_block(self, if_node):
        """查找if语句的else块"""
        if hasattr(if_node, 'children'):
            # 找到else关键字之后的块或语句
            found_else = False
            for child in if_node.children:
                if found_else:
                    return child
                if child.type == 'else':
                    found_else = True
        return None
    
    def _find_loop_body(self, loop_node):
        """查找循环体"""
        if hasattr(loop_node, 'children'):
            # 找到条件后的块或语句
            found_condition = False
            for child in loop_node.children:
                if found_condition:
                    return child
                if child.type == 'parenthesized_expression':
                    found_condition = True
        return None
    
    def _find_try_block(self, try_node):
        """查找try块"""
        if hasattr(try_node, 'children'):
            for child in try_node.children:
                if child.type == 'block':
                    return child
        return None
    
    def _find_catch_clauses(self, try_node):
        """查找所有catch子句"""
        catch_clauses = []
        if hasattr(try_node, 'children'):
            for child in try_node.children:
                if child.type == 'catch_clause':
                    catch_clauses.append(child)
        return catch_clauses
    
    def _find_catch_exception_type(self, catch_clause):
        """查找catch子句的异常类型"""
        if hasattr(catch_clause, 'children'):
            for child in catch_clause.children:
                if child.type == 'catch_formal_parameter':
                    type_node = self._find_child_by_type(child, 'type_identifier')
                    if type_node and hasattr(type_node, 'text'):
                        return type_node.text.decode('utf-8')
        return None
    
    def _find_catch_block(self, catch_clause):
        """查找catch块"""
        if hasattr(catch_clause, 'children'):
            for child in catch_clause.children:
                if child.type == 'block':
                    return child
        return None
    
    def _find_finally_block(self, try_node):
        """查找finally块"""
        if hasattr(try_node, 'children'):
            found_finally = False
            for child in try_node.children:
                if found_finally and child.type == 'block':
                    return child
                if child.type == 'finally':
                    found_finally = True
        return None
    
    def _find_return_expression(self, return_node):
        """查找return语句中的表达式"""
        if hasattr(return_node, 'children'):
            for child in return_node.children:
                if child.type != 'return':
                    return child
        return None
    
    def _find_throw_expression(self, throw_node):
        """查找throw语句中的表达式"""
        if hasattr(throw_node, 'children'):
            for child in throw_node.children:
                if child.type != 'throw':
                    return child
        return None
    
    def _find_switch_expression(self, switch_node):
        """查找switch语句的表达式"""
        if hasattr(switch_node, 'children'):
            for child in switch_node.children:
                if child.type == 'parenthesized_expression':
                    if hasattr(child, 'children'):
                        for paren_child in child.children:
                            if paren_child.type not in {'(', ')'}:
                                return paren_child
        return None
    
    def _extract_switch_cases(self, switch_node):
        """提取switch语句的case块"""
        cases = []
        
        if hasattr(switch_node, 'children'):
            # 找到switch块
            switch_block = None
            for child in switch_node.children:
                if child.type == 'switch_block':
                    switch_block = child
                    break
            
            if switch_block and hasattr(switch_block, 'children'):
                current_case = None
                
                for child in switch_block.children:
                    if child.type == 'case_statement':
                        # 开始新的case
                        case_value = None
                        for case_child in child.children:
                            if case_child.type not in {'case', ':'}:
                                case_value = self._summarize_expression(case_child)
                                break
                        
                        current_case = {
                            "value": case_value,
                            "statements": []
                        }
                        cases.append(current_case)
                    
                    elif child.type == 'default_statement':
                        # 默认case
                        current_case = {
                            "value": "default",
                            "statements": []
                        }
                        cases.append(current_case)
                    
                    elif current_case is not None and child.type not in {'{', '}'}:
                        # 添加语句到当前case
                        stmt_flow = self._extract_control_flow(child)
                        if stmt_flow:
                            current_case["statements"].extend(stmt_flow)
        
        return cases
    
    def _find_assignment_left(self, assignment_node):
        """查找赋值表达式的左侧"""
        if hasattr(assignment_node, 'children') and len(assignment_node.children) >= 1:
            return assignment_node.children[0]
        return None
    
    def _find_assignment_right(self, assignment_node):
        """查找赋值表达式的右侧"""
        if hasattr(assignment_node, 'children') and len(assignment_node.children) >= 3:
            return assignment_node.children[2]
        return None
    
    def _summarize_expression(self, expr_node) -> str:
        """简化表达式为文本摘要"""
        if not expr_node:
            return "unknown"
        
        if hasattr(expr_node, 'text'):
            text = expr_node.text.decode('utf-8')
            # 如果文本太长，截断它
            if len(text) > 50:
                return text[:47] + "..."
            return text
        
        expr_type = expr_node.type
        
        if expr_type == 'binary_expression':
            # 尝试格式化二元表达式
            if hasattr(expr_node, 'children') and len(expr_node.children) >= 3:
                left = self._summarize_expression(expr_node.children[0])
                operator = expr_node.children[1].type if hasattr(expr_node.children[1], 'type') else "?"
                right = self._summarize_expression(expr_node.children[2])
                
                # 限制长度
                if len(left) + len(operator) + len(right) > 50:
                    return f"{left[:20]}...{operator}...{right[-20:]}"
                return f"{left} {operator} {right}"
        
        elif expr_type == 'method_invocation':
            method_name = self._get_method_call_name(expr_node)
            if method_name:
                args_count = self._count_call_arguments(expr_node)
                return f"{method_name}(...{args_count} args)"
        
        # 默认返回类型名
        return expr_type
    
    def _infer_expression_type(self, expr_node) -> str:
        """推断表达式的类型"""
        if not expr_node:
            return "unknown"
        
        expr_type = expr_node.type
        
        if expr_type == 'string_literal':
            return "String"
        elif expr_type in {'decimal_integer_literal', 'hex_integer_literal', 'octal_integer_literal', 'binary_integer_literal'}:
            return "int"
        elif expr_type == 'decimal_floating_point_literal':
            return "double"
        elif expr_type in {'true', 'false'}:
            return "boolean"
        elif expr_type == 'null_literal':
            return "null"
        elif expr_type == 'character_literal':
            return "char"
        elif expr_type == 'identifier':
            # 尝试从变量使用信息查找类型
            if hasattr(expr_node, 'text'):
                var_name = expr_node.text.decode('utf-8')
                for usage in self.variable_usages.get(var_name, []):
                    if usage.get("type") == "declaration" and "var_type" in usage:
                        return usage["var_type"]
        
        # 默认返回未知
        return "unknown"
    
    def _process_class_declaration(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """增强版类声明处理，提取更多语义信息"""
        # 更新当前处理的类名
        name_node = self._find_child_by_type(node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            class_name = name_node.text.decode('utf-8')
            result["name"] = class_name
            self.current_class = class_name
        
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
        
        # 处理实现的接口
        implements_node = self._find_child_by_field(node, 'interfaces')
        if implements_node:
            implements_list = []
            for interface in self._get_comma_separated_children(implements_node):
                if hasattr(interface, 'text'):
                    implements_list.append(interface.text.decode('utf-8'))
            
            if implements_list:
                result["implements"] = implements_list
        
        # 处理类成员
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
        
        # 如果启用了语义分组，分析类的职责
        if self.semantic_grouping and class_name:
            class_responsibility = self._analyze_class_responsibility(result)
            if class_responsibility:
                result["responsibility"] = class_responsibility
        
        # 重置当前类
        self.current_class = None
        
        return result
    
    def _get_comma_separated_children(self, node) -> List:
        """获取逗号分隔的子节点"""
        result = []
        if hasattr(node, 'children'):
            for child in node.children:
                if child.type != ',':
                    result.append(child)
        return result
    
    def _analyze_class_responsibility(self, class_info: Dict[str, Any]) -> str:
        """分析类的主要职责"""
        class_name = class_info.get("name", "").lower()
        
        # 基于类名后缀的分析
        if class_name.endswith("controller"):
            return "controller"
        elif class_name.endswith("service"):
            return "service"
        elif class_name.endswith("repository") or class_name.endswith("dao"):
            return "data_access"
        elif class_name.endswith("factory"):
            return "factory"
        elif class_name.endswith("builder"):
            return "builder"
        elif class_name.endswith("adapter"):
            return "adapter"
        elif class_name.endswith("listener") or class_name.endswith("observer"):
            return "event_handler"
        elif class_name.endswith("exception"):
            return "exception"
        elif class_name.endswith("util") or class_name.endswith("utils"):
            return "utility"
        elif class_name.endswith("dto") or class_name.endswith("bean") or class_name.endswith("entity"):
            return "data_container"
        
        # 基于模式匹配的分析
        if "daemon" in class_name or "service" in class_name:
            return "service"
        if "watcher" in class_name or "monitor" in class_name:
            return "monitor"
        if "parser" in class_name or "reader" in class_name:
            return "parser"
        
        # 基于类成员的分析
        members = class_info.get("members", {})
        methods = members.get("methods", [])
        fields = members.get("fields", [])
        
        # 检查是否主要是数据类
        if len(fields) > len(methods) * 2:
            return "data_container"
        
        # 检查是否主要是工具类
        static_methods = sum(1 for m in methods if "static" in m.get("modifiers", []))
        if static_methods > len(methods) / 2:
            return "utility"
        
        # 检查是否主要是服务类
        process_methods = sum(1 for m in methods if 
                             any(keyword in m.get("name", "").lower() 
                                for keyword in ["process", "handle", "execute", "perform"]))
        if process_methods >= 2:
            return "service"
        
        # 默认分类
        return "general"
    
    def _process_block(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """处理代码块"""
        # 如果是深层次代码块，或者不需要控制流分析，则简化处理
        if depth > self.max_method_body_depth or not self.extract_control_flow:
            stmt_count = sum(1 for child in node.children if child.type not in {'{', '}'})
            result["stmt_count"] = stmt_count
            return result
        
        # 提取控制流
        control_flow = self._extract_control_flow(node)
        if control_flow:
            result["statements"] = control_flow
        
        return result
    
    def _process_control_flow_node(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """专门处理控制流节点"""
        # 使用控制流提取逻辑来处理
        flow = self._extract_control_flow(node)
        if flow and len(flow) == 1:
            # 合并单个控制流节点的结果
            for key, value in flow[0].items():
                if key != "type":  # 避免覆盖原始类型
                    result[key] = value
        
        return result
    
    def _process_method_invocation(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """处理方法调用节点"""
        # 提取方法名
        method_name = self._get_method_call_name(node)
        if method_name:
            result["method"] = method_name
        
        # 提取调用者
        caller = self._find_method_caller(node)
        if caller:
            result["caller"] = caller
        
        # 提取参数信息
        args_node = self._find_child_by_type(node, 'argument_list')
        if args_node:
            args = []
            for arg in args_node.children:
                if arg.type not in {',', '(', ')'}:
                    arg_info = {
                        "type": self._infer_expression_type(arg)
                    }
                    
                    # 尝试获取参数值描述
                    if hasattr(arg, 'text'):
                        arg_info["value"] = arg.text.decode('utf-8')
                    else:
                        arg_info["value_type"] = arg.type
                    
                    args.append(arg_info)
            
            if args:
                result["arguments"] = args
                result["args_count"] = len(args)
        
        return result
    
    def _process_assignment(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """处理赋值表达式"""
        # 提取左侧（赋值目标）
        left = self._find_assignment_left(node)
        if left:
            if hasattr(left, 'text'):
                result["target"] = left.text.decode('utf-8')
            else:
                result["target_type"] = left.type
        
        # 提取操作符
        if hasattr(node, 'children') and len(node.children) >= 2:
            op = node.children[1]
            if hasattr(op, 'type'):
                result["operator"] = op.type
        
        # 提取右侧（赋值来源）
        right = self._find_assignment_right(node)
        if right:
            result["source_type"] = right.type
            
            # 如果右侧是字面量，提取值
            if hasattr(right, 'text') and right.type in self.TEXT_NODES:
                result["source_value"] = right.text.decode('utf-8')
            
            # 如果右侧是方法调用，提取更多信息
            elif right.type == 'method_invocation':
                method_name = self._get_method_call_name(right)
                if method_name:
                    result["source_method"] = method_name
                    result["args_count"] = self._count_call_arguments(right)
        
        # 标记为状态变更
        if self.identify_state_changes:
            if left and hasattr(left, 'text'):
                target_name = left.text.decode('utf-8')
                
                change_info = {
                    "type": "assignment",
                    "target": target_name,
                    "location": {
                        "line": node.start_point[0] + 1 if hasattr(node, 'start_point') else -1
                    }
                }
                
                if self.current_method:
                    change_info["in_method"] = self.current_method
                
                self.state_changes.append(change_info)
        
        return result
    
    def _process_simplified_node(self, node, depth: int, result: Dict[str, Any]) -> Dict[str, Any]:
        """简化处理某些节点类型"""
        if hasattr(node, 'text'):
            node_text = node.text.decode('utf-8')
            if len(node_text) > 100:  # 对于长文本，只保留长度
                result["text_length"] = len(node_text)
            else:
                result["text"] = node_text
        
        # 简化处理子节点
        if node.type == 'modifiers' and hasattr(node, 'children'):
            modifiers = []
            for mod in node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final', 'abstract', 'synchronized'}:
                    modifiers.append(mod.type)
            
            if modifiers:
                result["modifiers"] = modifiers
        
        elif node.type == 'formal_parameters':
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
    
    def _calculate_cyclomatic_complexity(self, control_flow: List[Dict[str, Any]]) -> int:
        """计算圈复杂度（McCabe复杂度）"""
        # 基础复杂度为1
        complexity = 1
        
        def traverse_flow(flow_list):
            nonlocal complexity
            for node in flow_list:
                node_type = node.get("type", "")
                
                # 条件分支增加复杂度
                if node_type in {"if_statement", "switch_statement", "case_statement", 
                              "for_statement", "while_statement", "do_statement", 
                              "catch_clause"}:
                    complexity += 1
                
                # &&和||操作符也会增加复杂度
                if node_type == "binary_expression":
                    if "condition" in node and ("&&" in node["condition"] or "||" in node["condition"]):
                        complexity += node["condition"].count("&&") + node["condition"].count("||")
                
                # 递归处理嵌套结构
                if node_type == "if_statement":
                    if "then" in node:
                        traverse_flow(node["then"] if isinstance(node["then"], list) else [node["then"]])
                    if "else" in node:
                        traverse_flow(node["else"] if isinstance(node["else"], list) else [node["else"]])
                
                elif node_type in {"for_statement", "while_statement", "do_statement"}:
                    if "body" in node:
                        traverse_flow(node["body"] if isinstance(node["body"], list) else [node["body"]])
                
                elif node_type == "switch_statement" and "cases" in node:
                    for case in node["cases"]:
                        if "statements" in case:
                            traverse_flow(case["statements"])
                
                elif node_type == "try_statement":
                    if "try" in node:
                        traverse_flow(node["try"] if isinstance(node["try"], list) else [node["try"]])
                    if "catch" in node:
                        for catch in node["catch"]:
                            if "body" in catch:
                                traverse_flow(catch["body"] if isinstance(catch["body"], list) else [catch["body"]])
                    if "finally" in node:
                        traverse_flow(node["finally"] if isinstance(node["finally"], list) else [node["finally"]])
        
        traverse_flow(control_flow)
        return complexity
    
    def _calculate_max_nesting(self, node, current_depth: int = 0) -> int:
        """计算最大嵌套深度"""
        if not hasattr(node, 'children'):
            return current_depth
        
        max_depth = current_depth
        
        # 检查是否是增加嵌套深度的节点
        if node.type in {'if_statement', 'for_statement', 'while_statement', 'do_statement', 
                          'switch_statement', 'try_statement'}:
            current_depth += 1
            max_depth = current_depth
        
        # 递归检查子节点
        for child in node.children:
            child_depth = self._calculate_max_nesting(child, current_depth)
            max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _count_statement_types(self, node) -> Dict[str, int]:
        """统计代码块中各类语句的数量"""
        counts = Counter()
        
        def traverse(node):
            if not hasattr(node, 'children'):
                return
            
            # 统计语句类型
            if node.type.endswith('_statement'):
                counts[node.type] += 1
            
            # 特殊处理方法调用
            elif node.type == 'method_invocation':
                counts['method_invocation'] += 1
            
            # 递归处理子节点
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return dict(counts)


def compress_java_ast(java_code: str, lang_path: str = None, 
                      preserve_comments: bool = True, 
                      extract_control_flow: bool = True,
                      track_variable_usage: bool = True, 
                      analyze_method_calls: bool = True,
                      identify_state_changes: bool = True,
                      max_depth: int = 20) -> Dict[str, Any]:
    """
    解析并增强压缩Java代码的AST
    
    Args:
        java_code: Java源代码字符串
        lang_path: tree-sitter语言库路径
        preserve_comments: 是否保留注释
        extract_control_flow: 是否提取控制流结构
        track_variable_usage: 是否跟踪变量使用
        analyze_method_calls: 是否分析方法调用
        identify_state_changes: 是否识别状态变更点
        max_depth: 最大递归深度
    
    Returns:
        增强压缩后的AST字典
    """
    try:
        # 尝试加载已构建的库
        if lang_path:
            JAVA_LANGUAGE = Language(lang_path, 'java')
        else:
            # 尝试常见路径
            candidates = [
                'build/languages.dll',
                'build/languages.so',
                './languages.dll',
                './languages.so'
            ]
            
            for candidate in candidates:
                try:
                    JAVA_LANGUAGE = Language(candidate, 'java')
                    break
                except:
                    continue
            else:
                raise RuntimeError("无法找到Java语言支持库，请指定lang_path参数")
    except Exception as e:
        print(f"无法加载Java语言支持: {e}")
        raise
    
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    
    tree = parser.parse(bytes(java_code, 'utf8'))
    compressor = EnhancedASTCompressor(
        max_depth=max_depth,
        preserve_comments=preserve_comments,
        extract_control_flow=extract_control_flow,
        track_variable_usage=track_variable_usage,
        analyze_method_calls=analyze_method_calls,
        identify_state_changes=identify_state_changes
    )
    
    return compressor.compress(tree.root_node, java_code)


def save_compressed_ast(compressed_ast: Dict[str, Any], output_file: str, indent: int = 2) -> None:
    """
    将压缩后的AST保存到文件
    
    Args:
        compressed_ast: 压缩后的AST字典
        output_file: 输出文件路径
        indent: JSON缩进级别，None表示不缩进
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compressed_ast, f, ensure_ascii=False, indent=indent)
    
    print(f"AST已保存到: {output_file}")


# 使用示例
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='增强版Java AST分析与压缩工具')
    parser.add_argument('input', help='Java源代码文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径', default=None)
    parser.add_argument('--lang-path', '-l', help='tree-sitter语言库路径', default=None)
    parser.add_argument('--no-comments', action='store_true', help='不保留注释')
    parser.add_argument('--no-control-flow', action='store_true', help='不提取控制流结构')
    parser.add_argument('--no-variable-tracking', action='store_true', help='不跟踪变量使用')
    parser.add_argument('--no-method-calls', action='store_true', help='不分析方法调用')
    parser.add_argument('--no-state-changes', action='store_true', help='不识别状态变更点')
    parser.add_argument('--depth', '-d', type=int, default=20, help='最大递归深度')
    parser.add_argument('--no-indent', action='store_true', help='输出不缩进的JSON')
    
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
        output_file = f"{base_name}_enhanced_ast.json"
    
    # 压缩AST
    print(f"正在分析 {args.input}...")
    compressed_ast = compress_java_ast(
        java_code,
        lang_path=args.lang_path,
        preserve_comments=not args.no_comments,
        extract_control_flow=not args.no_control_flow,
        track_variable_usage=not args.no_variable_tracking,
        analyze_method_calls=not args.no_method_calls,
        identify_state_changes=not args.no_state_changes,
        max_depth=args.depth
    )
    
    # 保存AST
    indent = None if args.no_indent else 2
    save_compressed_ast(compressed_ast, output_file, indent=indent)
    
    # 输出统计信息
    if "summary" in compressed_ast and "classes" in compressed_ast["summary"]:
        print(f"\n分析结果摘要:")
        for cls in compressed_ast["summary"]["classes"]:
            print(f"- 类: {cls.get('name', 'Unknown')}")
            
            if "methods" in cls:
                method_count = len(cls["methods"])
                print(f"  - 方法数量: {method_count}")
                
                # 输出部分方法信息
                if method_count > 0:
                    print(f"  - 方法列表:")
                    for method in cls["methods"][:5]:  # 只显示前5个方法
                        method_name = method.get("name", "unnamed")
                        method_type = method.get("intent", "general")
                        print(f"    * {method_name} ({method_type})")
                    
                    if method_count > 5:
                        print(f"    * ... 及其他 {method_count - 5} 个方法")
    
    # 输出复杂度信息
    if "method_complexity" in compressed_ast:
        high_complexity = {name: info for name, info in compressed_ast["method_complexity"].items() 
                          if info.get("cyclomatic", 1) > 5}
        
        if high_complexity:
            print("\n较高复杂度的方法:")
            for name, info in high_complexity.items():
                print(f"- {name}: 圈复杂度={info.get('cyclomatic', '?')}, 嵌套深度={info.get('max_nesting', '?')}")
    
    print(f"\n分析完成，结果已保存到: {output_file}")
