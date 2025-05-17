import json
from tree_sitter import Language, Parser
from typing import Dict, List, Optional, Union, Any, Set
import os
from collections import defaultdict, Counter

class LLMFriendlyASTCompressor:
    """
    优化版Java AST压缩工具类，使用键名映射表辅助LLM理解，
    完全忽略位置信息，平衡信息完整性与大小
    """
    
    # 键名映射表 - 用于减小JSON大小同时保持LLM可理解性
    KEY_MAPPING = {
        # 基本结构
        "type": "t",
        "name": "n",
        "file_info": "fi",
        "structure": "s",
        "classes": "cs",
        "methods": "ms",
        "fields": "fs",
        "parameters": "ps",
        
        # 类型和修饰符
        "modifiers": "mod",
        "return_type": "rt",
        
        # 流程信息
        "control_flow": "cf", 
        "data_flow": "df",
        "flow_elements": "fe",
        "condition": "cond",
        
        # 变量信息
        "variables": "vars",
        "usage_summary": "us",
        "declarations": "decl",
        "reads": "rd",
        "writes": "wr",
        
        # 分析信息
        "method_analysis": "ma",
        "complexity": "cx",
        "max_nesting": "mn",
        "intent": "in",
        "complexity_rating": "cr",
        
        # 注释信息
        "key_comments": "kc",
        "text": "txt",
        
        # 其他常见属性
        "package": "pkg",
        "imports": "imp",
        "total_lines": "tl",
        "has_value": "hv",
        "exception_type": "et",
        "call_count": "cc"
    }
    
    # 反向映射 - 用于恢复原始键名(主要用于调试)
    REVERSE_MAPPING = {v: k for k, v in KEY_MAPPING.items()}
    
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
    
    # 控制流节点，需要完整保留结构
    CONTROL_FLOW_NODES = {
        'if_statement', 'for_statement', 'while_statement', 'do_statement',
        'switch_statement', 'try_statement', 'return_statement', 'throw_statement',
        'synchronized_statement', 'break_statement', 'continue_statement'
    }
    
    # 注释节点类型
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
    
    # 忽略的节点类型
    IGNORED_NODE_TYPES = {
        'semicolon', 'comma', 'dimensions', 
        'empty_statement', '.', ';', '{', '}', '(', ')', '[', ']'
    }
    
    # 表示状态变更的节点类型
    STATE_CHANGE_NODES = {
        'assignment_expression', 'update_expression'
    }
    
    def __init__(self, 
                 preserve_comments: bool = True,
                 track_control_flow: bool = True,
                 track_data_flow: bool = True,
                 include_method_intent: bool = True,
                 aggregation_level: str = "medium",
                 use_key_mapping: bool = True):
        """
        初始化优化版AST压缩器
        
        Args:
            preserve_comments: 是否保留关键注释信息
            track_control_flow: 是否跟踪控制流
            track_data_flow: 是否跟踪数据流
            include_method_intent: 是否包含方法意图分析
            aggregation_level: 聚合级别 ("low", "medium", "high")
            use_key_mapping: 是否使用键名映射表减小输出大小
        """
        self.preserve_comments = preserve_comments
        self.track_control_flow = track_control_flow
        self.track_data_flow = track_data_flow
        self.include_method_intent = include_method_intent
        self.aggregation_level = aggregation_level
        self.use_key_mapping = use_key_mapping
        
        # 用于跟踪已收集的注释
        self.important_comments = []
        
        # 用于收集变量使用信息
        self.variable_usages = {}
        
        # 用于收集方法调用关系
        self.method_calls = {}
        
        # 控制流信息
        self.control_flow = {}
        
        # 方法总体复杂度
        self.method_complexity = {}
        
        # 字段信息
        self.fields_info = {}
        
        # 当前上下文
        self.current_class = None
        self.current_method = None
        
    def compress(self, root_node, source_code: Optional[str] = None) -> Dict[str, Any]:
        """压缩整个AST，优化输出大小同时保留语义关系"""
        # 重置状态
        self.important_comments = []
        self.variable_usages = {}
        self.method_calls = {}
        self.control_flow = {}
        self.method_complexity = {}
        self.fields_info = {}
        self.current_class = None
        self.current_method = None
        
        # 第一遍：收集基本信息
        self._analyze_and_collect(root_node, source_code)
        
        # 构建优化后的AST
        result = {}
        
        # 添加基本文件信息
        result["file_info"] = self._extract_file_info(root_node, source_code)
        
        # 添加类和方法结构信息
        result["structure"] = self._extract_structural_info(root_node)
        
        # 按需添加控制流信息
        if self.track_control_flow:
            result["control_flow"] = self.control_flow
        
        # 按需添加数据流信息
        if self.track_data_flow:
            result["data_flow"] = self._extract_data_flow_info()
        
        # 添加方法意图和复杂度
        if self.include_method_intent:
            result["method_analysis"] = self._extract_method_analysis()
        
        # 添加重要注释（聚合后）
        if self.preserve_comments and self.important_comments:
            result["key_comments"] = self._extract_key_comments()
        
        # 应用键名映射以减小大小
        if self.use_key_mapping:
            # 创建包含映射表的最终结果
            final_result = {
                "key_mapping": self.KEY_MAPPING,
                "data": self._apply_key_mapping(result)
            }
            return final_result
        
        return result
    
    def _apply_key_mapping(self, obj: Any) -> Any:
        """递归应用键名映射以减小输出大小"""
        if isinstance(obj, dict):
            return {
                self.KEY_MAPPING.get(k, k): self._apply_key_mapping(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [self._apply_key_mapping(item) for item in obj]
        elif isinstance(obj, set):
            return list(obj)  # 将集合转换为列表
        else:
            return obj
    
    def _analyze_and_collect(self, root_node, source_code: Optional[str]) -> None:
        """第一遍遍历：收集基本信息"""
        # 提取文件注释
        if self.preserve_comments and source_code:
            self._extract_comments(source_code)
        
        # 分析结构并收集控制流、数据流信息
        self._analyze_node(root_node, 0)
    
    def _extract_comments(self, source_code: str) -> None:
        """从源代码提取重要注释"""
        lines = source_code.split('\n')
        
        # 寻找文件头和类文档注释
        in_doc_comment = False
        current_comment = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 处理文档注释块
            if "/**" in line:
                in_doc_comment = True
                current_comment = [line]
            elif in_doc_comment and "*/" in line:
                current_comment.append(line)
                comment_text = "\n".join(current_comment)
                self.important_comments.append({
                    "type": "doc_comment",
                    "text": comment_text
                })
                in_doc_comment = False
                current_comment = []
            elif in_doc_comment:
                current_comment.append(line)
            
            # 处理单行注释（只保留看起来重要的）
            elif line.startswith("//") and any(keyword in line.lower() for keyword in [
                "todo", "fixme", "note", "important", "bug", "warning", "hack", 
                "功能", "注意", "关键", "实现", "处理"
            ]):
                self.important_comments.append({
                    "type": "line_comment",
                    "text": line
                })
        
        # 如果聚合级别高，只保留最重要的注释
        if self.aggregation_level == "high":
            # 按照关键词重要性排序，只保留前5条
            self.important_comments = sorted(
                self.important_comments, 
                key=lambda c: self._comment_importance(c["text"]),
                reverse=True
            )[:5]
    
    def _comment_importance(self, comment_text: str) -> int:
        """评估注释的重要性分数"""
        score = 0
        keywords = ["功能", "注意", "关键", "实现", "处理", "todo", "fixme", "important"]
        for keyword in keywords:
            if keyword.lower() in comment_text.lower():
                score += 1
        
        # 文档注释通常更重要
        if comment_text.strip().startswith("/**"):
            score += 3
        
        # 较长的注释可能包含更多信息
        score += min(len(comment_text) // 100, 3)
        
        return score
    
    def _analyze_node(self, node, depth: int) -> None:
        """分析节点并收集信息"""
        if node is None:
            return
        
        # 更新当前类和方法上下文
        self._update_context(node)
        
        # 收集控制流信息
        if self.track_control_flow and node.type in self.CONTROL_FLOW_NODES:
            self._collect_control_flow(node)
        
        # 收集数据流信息（变量使用和状态变更）
        if self.track_data_flow:
            if node.type == 'variable_declarator':
                self._collect_variable_declaration(node)
            elif node.type == 'identifier' and not self._is_type_or_method_name(node):
                self._collect_variable_usage(node)
            elif node.type in self.STATE_CHANGE_NODES:
                self._collect_state_change(node)
        
        # 收集方法调用信息
        if node.type == 'method_invocation':
            self._collect_method_call(node)
        
        # 收集字段信息
        if node.type == 'field_declaration':
            self._collect_field_info(node)
        
        # 计算方法复杂度
        if self.include_method_intent and node.type == 'method_declaration':
            self._calculate_method_complexity(node)
        
        # 递归处理子节点
        if hasattr(node, 'children'):
            for child in node.children:
                self._analyze_node(child, depth + 1)
    
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
                
                # 初始化方法的控制流和复杂度信息
                if self.current_method not in self.control_flow:
                    self.control_flow[self.current_method] = {"flow_elements": []}
                
                if self.include_method_intent and self.current_method not in self.method_complexity:
                    self.method_complexity[self.current_method] = {
                        "complexity": 1,  # 基础复杂度为1
                        "max_nesting": 0
                    }
        
        # 方法结束时重置当前方法
        elif node.type == 'block' and self._is_method_body(node) and self.current_method:
            self.current_method = None
    
    def _is_method_body(self, node) -> bool:
        """检查节点是否为方法体"""
        parent = self._get_parent(node)
        return parent and parent.type == 'method_declaration'
    
    def _get_parent(self, node):
        """获取节点的父节点（树形结构中不直接支持，近似实现）"""
        # 这是一个占位符实现，实际情况中需要在遍历过程中构建父子关系
        return None
    
    def _collect_control_flow(self, node) -> None:
        """收集控制流信息"""
        if not self.current_method:
            return
        
        # 提取控制流元素
        flow_element = {"type": node.type}
        
        # 提取条件信息
        if node.type in {'if_statement', 'while_statement', 'for_statement'}:
            condition = self._extract_condition(node)
            if condition:
                flow_element["condition"] = condition
        
        # 提取异常处理信息
        elif node.type == 'try_statement':
            catches = self._extract_catch_info(node)
            if catches:
                flow_element["catches"] = catches
        
        # 提取返回信息
        elif node.type == 'return_statement':
            has_value = self._has_return_value(node)
            flow_element["has_value"] = has_value
        
        # 增加复杂度计数
        if node.type in {'if_statement', 'switch_statement', 'for_statement', 'while_statement', 'do_statement'}:
            self.method_complexity[self.current_method]["complexity"] += 1
        
        # 添加到当前方法的控制流
        self.control_flow[self.current_method]["flow_elements"].append(flow_element)
    
    def _extract_condition(self, node) -> Optional[str]:
        """提取条件表达式的摘要"""
        condition_node = self._find_condition_expression(node)
        if condition_node:
            # 只返回条件的简洁摘要
            return self._summarize_expression(condition_node)
        return None
    
    def _extract_catch_info(self, node) -> List[Dict[str, Any]]:
        """提取try-catch语句的异常处理信息"""
        catches = []
        
        for child in node.children:
            if child.type == 'catch_clause':
                catch_info = {"type": "catch"}
                
                # 提取异常类型
                param_node = self._find_child_by_type(child, 'catch_formal_parameter')
                if param_node:
                    type_node = self._find_child_by_type(param_node, 'type_identifier')
                    if type_node and hasattr(type_node, 'text'):
                        catch_info["exception_type"] = type_node.text.decode('utf-8')
                
                catches.append(catch_info)
        
        return catches
    
    def _has_return_value(self, node) -> bool:
        """检查return语句是否返回值"""
        for child in node.children:
            if child.type != 'return':
                return True
        return False
    
    def _collect_variable_declaration(self, node) -> None:
        """收集变量声明信息"""
        if not self.current_method:
            return
        
        # 获取变量名
        name_node = self._find_child_by_type(node, 'identifier')
        if not name_node or not hasattr(name_node, 'text'):
            return
            
        var_name = name_node.text.decode('utf-8')
        
        # 获取变量类型（从父节点找）
        var_type = "unknown"
        parent = self._get_parent(node)
        if parent:
            type_node = self._find_child_by_type(parent, 'type_identifier')
            if type_node and hasattr(type_node, 'text'):
                var_type = type_node.text.decode('utf-8')
        
        # 初始化变量使用记录
        if var_name not in self.variable_usages:
            self.variable_usages[var_name] = {
                "type": var_type,
                "methods": {}
            }
        
        # 记录在当前方法中的声明
        if self.current_method not in self.variable_usages[var_name]["methods"]:
            self.variable_usages[var_name]["methods"][self.current_method] = {
                "declarations": 0,
                "reads": 0,
                "writes": 0
            }
        
        self.variable_usages[var_name]["methods"][self.current_method]["declarations"] += 1
    
    def _collect_variable_usage(self, node) -> None:
        """收集变量使用信息"""
        if not self.current_method or not hasattr(node, 'text'):
            return
            
        var_name = node.text.decode('utf-8')
        
        # 如果变量还未记录，初始化
        if var_name not in self.variable_usages:
            self.variable_usages[var_name] = {
                "type": "unknown",
                "methods": {}
            }
        
        # 如果当前方法还未记录，初始化
        if self.current_method not in self.variable_usages[var_name]["methods"]:
            self.variable_usages[var_name]["methods"][self.current_method] = {
                "declarations": 0,
                "reads": 0,
                "writes": 0
            }
        
        # 确定是读取还是写入
        is_write = self._is_assignment_target(node)
        
        # 更新使用计数
        if is_write:
            self.variable_usages[var_name]["methods"][self.current_method]["writes"] += 1
        else:
            self.variable_usages[var_name]["methods"][self.current_method]["reads"] += 1
    
    def _is_assignment_target(self, node) -> bool:
        """检查标识符是否为赋值目标"""
        parent = self._get_parent(node)
        if parent and parent.type == 'assignment_expression':
            # 如果是赋值表达式的第一个子节点，那么它是目标
            if hasattr(parent, 'children') and len(parent.children) > 0:
                return parent.children[0] is node
        return False
    
    def _collect_state_change(self, node) -> None:
        """收集状态变更信息"""
        if not self.current_method:
            return
        
        # 提取赋值目标
        target = None
        if node.type == 'assignment_expression' and hasattr(node, 'children') and len(node.children) > 0:
            target_node = node.children[0]
            if hasattr(target_node, 'text'):
                target = target_node.text.decode('utf-8')
        
        if not target:
            return
        
        # 如果聚合级别高，只关注字段变更
        if self.aggregation_level == "high" and target not in self.fields_info:
            return
            
        # 更新变量的写入记录
        if target in self.variable_usages:
            method_info = self.variable_usages[target]["methods"].get(self.current_method)
            if method_info:
                method_info["writes"] += 1
    
    def _collect_method_call(self, node) -> None:
        """收集方法调用信息"""
        if not self.current_method:
            return
            
        # 提取方法名
        method_name = self._get_method_name(node)
        if not method_name:
            return
        
        # 提取调用者
        caller = self._get_caller(node)
        
        # 初始化方法调用记录
        if method_name not in self.method_calls:
            self.method_calls[method_name] = {
                "callers": set(),
                "called_from": set(),
                "call_count": 0
            }
        
        # 更新记录
        if caller:
            self.method_calls[method_name]["callers"].add(caller)
        self.method_calls[method_name]["called_from"].add(self.current_method)
        self.method_calls[method_name]["call_count"] += 1
    
    def _get_method_name(self, node) -> Optional[str]:
        """从方法调用中提取方法名"""
        for child in node.children:
            # 方法名通常是第二个或最后一个标识符
            if child.type == 'identifier' and hasattr(child, 'text'):
                return child.text.decode('utf-8')
        return None
    
    def _get_caller(self, node) -> Optional[str]:
        """从方法调用中提取调用者"""
        if hasattr(node, 'children') and len(node.children) > 0:
            first_child = node.children[0]
            if first_child.type == 'identifier' and hasattr(first_child, 'text'):
                return first_child.text.decode('utf-8')
        return None
    
    def _collect_field_info(self, node) -> None:
        """收集字段信息"""
        # 提取字段类型
        type_node = self._find_child_by_type(node, 'type_identifier')
        if not type_node or not hasattr(type_node, 'text'):
            return
        
        field_type = type_node.text.decode('utf-8')
        
        # 提取字段名
        var_declarator = self._find_child_by_type(node, 'variable_declarator')
        if not var_declarator:
            return
            
        name_node = self._find_child_by_type(var_declarator, 'identifier')
        if not name_node or not hasattr(name_node, 'text'):
            return
            
        field_name = name_node.text.decode('utf-8')
        
        # 提取修饰符
        modifiers = []
        modifiers_node = self._find_child_by_type(node, 'modifiers')
        if modifiers_node:
            for mod in modifiers_node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final'}:
                    modifiers.append(mod.type)
        
        # 记录字段信息
        self.fields_info[field_name] = {
            "type": field_type,
            "modifiers": modifiers
        }
    
    def _calculate_method_complexity(self, node) -> None:
        """计算方法复杂度"""
        if not self.current_method:
            return
        
        # 嵌套深度计算
        max_nesting = self._calculate_max_nesting(node)
        self.method_complexity[self.current_method]["max_nesting"] = max_nesting
        
        # 判断方法类型（根据名称）
        method_type = self._determine_method_type(self.current_method)
        if method_type:
            self.method_complexity[self.current_method]["intent"] = method_type
    
    def _calculate_max_nesting(self, node, current_depth: int = 0) -> int:
        """计算最大嵌套深度"""
        if not hasattr(node, 'children'):
            return current_depth
        
        # 检查是否是嵌套控制结构
        is_control_structure = node.type in self.CONTROL_FLOW_NODES
        next_depth = current_depth + (1 if is_control_structure else 0)
        
        # 递归计算子节点的嵌套深度
        max_depth = next_depth
        for child in node.children:
            child_depth = self._calculate_max_nesting(child, next_depth)
            max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _determine_method_type(self, method_name: str) -> Optional[str]:
        """根据方法名判断方法类型"""
        method_name_lower = method_name.lower()
        
        if method_name_lower.startswith(('get', 'is', 'has', 'find')):
            return "accessor"
        elif method_name_lower.startswith(('set', 'add', 'remove', 'delete', 'update')):
            return "mutator"
        elif method_name_lower.startswith(('create', 'build', 'make', 'generate')):
            return "factory"
        elif method_name_lower.startswith(('process', 'handle', 'execute', 'run')):
            return "processor"
        elif method_name_lower.startswith(('validate', 'check', 'verify')):
            return "validator"
        elif method_name_lower.startswith(('convert', 'transform', 'parse')):
            return "transformer"
        elif method_name_lower == 'main':
            return "entry_point"
        
        return None
    
    def _is_type_or_method_name(self, node) -> bool:
        """检查标识符是否为类型名或方法名"""
        parent = self._get_parent(node)
        if not parent:
            return False
            
        # 类型相关
        if parent.type in {'type_identifier', 'class_declaration', 'interface_declaration'}:
            return True
            
        # 方法声明
        if parent.type == 'method_declaration' and hasattr(parent, 'children'):
            for i, child in enumerate(parent.children):
                if child is node and i < 3:  # 方法名通常在前几个子节点
                    return True
        
        return False
    
    def _extract_file_info(self, root_node, source_code: Optional[str]) -> Dict[str, Any]:
        """提取文件基本信息"""
        file_info = {"type": "Java source file"}
        
        # 提取包名
        package_node = self._find_child_by_type(root_node, 'package_declaration')
        if package_node:
            package_name = self._extract_package_name(package_node)
            if package_name:
                file_info["package"] = package_name
        
        # 提取导入
        imports = []
        for child in root_node.children:
            if child.type == 'import_declaration':
                import_name = self._extract_import_name(child)
                if import_name:
                    imports.append(import_name)
        
        # 根据聚合级别决定如何处理导入信息
        if imports:
            if self.aggregation_level == "high":
                # 只记录导入包的数量
                file_info["imports_count"] = len(imports)
                
                # 分类导入
                std_lib_count = sum(1 for imp in imports if imp.startswith("java."))
                if std_lib_count > 0:
                    file_info["java_stdlib_imports"] = std_lib_count
            else:
                # 保留完整导入列表
                file_info["imports"] = imports
        
        # 添加文件统计信息
        if source_code:
            lines = source_code.split('\n')
            file_info["total_lines"] = len(lines)
        
        return file_info
    
    def _extract_package_name(self, package_node) -> Optional[str]:
        """从包声明中提取包名"""
        for child in package_node.children:
            if child.type == 'scoped_identifier' and hasattr(child, 'text'):
                return child.text.decode('utf-8')
            
            # 递归搜索
            if hasattr(child, 'children'):
                for grandchild in child.children:
                    if grandchild.type == 'scoped_identifier' and hasattr(grandchild, 'text'):
                        return grandchild.text.decode('utf-8')
        
        return None
    
    def _extract_import_name(self, import_node) -> Optional[str]:
        """从导入声明中提取导入名"""
        for child in import_node.children:
            if child.type == 'scoped_identifier' and hasattr(child, 'text'):
                return child.text.decode('utf-8')
            
            # 递归搜索
            if hasattr(child, 'children'):
                for grandchild in child.children:
                    if grandchild.type == 'scoped_identifier' and hasattr(grandchild, 'text'):
                        return grandchild.text.decode('utf-8')
        
        return None
    
    def _extract_structural_info(self, root_node) -> Dict[str, Any]:
        """提取代码结构信息"""
        structure = {"classes": []}
        
        # 查找所有类声明
        for child in root_node.children:
            if child.type == 'class_declaration':
                class_info = self._extract_class_info(child)
                if class_info:
                    structure["classes"].append(class_info)
        
        return structure
    
    def _extract_class_info(self, class_node) -> Dict[str, Any]:
        """提取类信息"""
        class_info = {"type": "class"}
        
        # 提取类名
        name_node = self._find_child_by_type(class_node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            class_info["name"] = name_node.text.decode('utf-8')
        
        # 提取修饰符
        modifiers = []
        modifiers_node = self._find_child_by_type(class_node, 'modifiers')
        if modifiers_node:
            for mod in modifiers_node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final', 'abstract'}:
                    modifiers.append(mod.type)
        
        if modifiers:
            class_info["modifiers"] = modifiers
        
        # 提取继承信息
        extends_node = self._find_child_by_field(class_node, 'superclass')
        if extends_node and hasattr(extends_node, 'text'):
            class_info["extends"] = extends_node.text.decode('utf-8')
        
        # 提取字段信息（按聚合级别）
        if self.fields_info:
            if self.aggregation_level == "high":
                # 只记录字段数量
                class_fields = [name for name in self.fields_info.keys() 
                               if self.aggregation_level != "high" or self._is_important_field(name)]
                if class_fields:
                    class_info["fields_count"] = len(class_fields)
            else:
                # 记录重要字段详情
                fields = []
                for name, info in self.fields_info.items():
                    if self.aggregation_level != "medium" or self._is_important_field(name):
                        fields.append({
                            "name": name,
                            "type": info["type"],
                            "modifiers": info["modifiers"]
                        })
                
                if fields:
                    class_info["fields"] = fields
        
        # 提取方法信息
        methods = []
        class_body = self._find_child_by_type(class_node, 'class_body')
        if class_body:
            for child in class_body.children:
                if child.type == 'method_declaration':
                    method_info = self._extract_method_info(child)
                    if method_info:
                        methods.append(method_info)
        
        if methods:
            class_info["methods"] = methods
        
        return class_info
    
    def _extract_method_info(self, method_node) -> Dict[str, Any]:
        """提取方法信息"""
        method_info = {"type": "method"}
        
        # 提取方法名
        name_node = self._find_child_by_type(method_node, 'identifier')
        if name_node and hasattr(name_node, 'text'):
            method_name = name_node.text.decode('utf-8')
            method_info["name"] = method_name
        else:
            return None  # 无法识别的方法
        
        # 提取修饰符
        modifiers = []
        modifiers_node = self._find_child_by_type(method_node, 'modifiers')
        if modifiers_node:
            for mod in modifiers_node.children:
                if mod.type in {'public', 'private', 'protected', 'static', 'final', 'abstract', 'synchronized'}:
                    modifiers.append(mod.type)
        
        if modifiers:
            method_info["modifiers"] = modifiers
        
        # 提取返回类型
        return_type = self._find_child_by_type(method_node, 'type_identifier')
        if return_type and hasattr(return_type, 'text'):
            method_info["return_type"] = return_type.text.decode('utf-8')
        else:
            # 检查是否返回void
            void_type = self._find_child_by_type(method_node, 'void_type')
            if void_type:
                method_info["return_type"] = "void"
        
        # 提取参数信息
        params = []
        params_node = self._find_child_by_type(method_node, 'formal_parameters')
        if params_node:
            for child in params_node.children:
                if child.type == 'formal_parameter':
                    param_info = {}
                    
                    # 参数类型
                    type_node = self._find_child_by_type(child, 'type_identifier')
                    if type_node and hasattr(type_node, 'text'):
                        param_info["type"] = type_node.text.decode('utf-8')
                    
                    # 参数名称
                    name_node = self._find_child_by_type(child, 'identifier')
                    if name_node and hasattr(name_node, 'text'):
                        param_info["name"] = name_node.text.decode('utf-8')
                    
                    if param_info:
                        params.append(param_info)
        
        if params:
            method_info["parameters"] = params
        
        return method_info
    
    def _extract_data_flow_info(self) -> Dict[str, Any]:
        """提取数据流信息"""
        data_flow = {}
        
        # 根据聚合级别处理变量使用信息
        if self.aggregation_level == "high":
            # 高聚合：只关注重要变量和字段
            important_vars = {}
            for var_name, var_info in self.variable_usages.items():
                if self._is_important_variable(var_name, var_info):
                    important_vars[var_name] = {
                        "type": var_info["type"],
                        "usage_summary": self._summarize_variable_usage(var_info["methods"])
                    }
            
            if important_vars:
                data_flow["key_variables"] = important_vars
        else:
            # 中/低聚合：包含更多变量信息
            variables = {}
            for var_name, var_info in self.variable_usages.items():
                if self.aggregation_level == "low" or self._is_important_variable(var_name, var_info):
                    # 中聚合：包含方法级别的使用汇总
                    if self.aggregation_level == "medium":
                        variables[var_name] = {
                            "type": var_info["type"],
                            "usage_by_method": {
                                method: self._summarize_usage_counts(usage)
                                for method, usage in var_info["methods"].items()
                            }
                        }
                    # 低聚合：包含完整使用细节
                    else:
                        variables[var_name] = var_info
            
            if variables:
                data_flow["variables"] = variables
        
        return data_flow
    
    def _is_important_variable(self, var_name: str, var_info: Dict[str, Any]) -> bool:
        """判断变量是否重要"""
        # 字段通常更重要
        if var_name in self.fields_info:
            return True
        
        # 查看使用情况
        total_usages = sum(
            usage["declarations"] + usage["reads"] + usage["writes"]
            for usage in var_info["methods"].values()
        )
        
        # 使用频繁的变量更重要
        if total_usages >= 5:
            return True
        
        # 特定类型的变量可能更重要
        important_types = {'String', 'List', 'Map', 'Set', 'File', 'Exception'}
        if var_info["type"] in important_types:
            return True
        
        return False
    
    def _is_important_field(self, field_name: str) -> bool:
        """判断字段是否重要"""
        # 具有特定修饰符的字段通常更重要
        field_info = self.fields_info.get(field_name, {})
        modifiers = field_info.get("modifiers", [])
        
        if "public" in modifiers or "static" in modifiers or "final" in modifiers:
            return True
        
        # 常量名（全大写）通常是重要配置
        if field_name.isupper():
            return True
        
        return False
    
    def _summarize_variable_usage(self, method_usages: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        """汇总变量在所有方法中的使用情况"""
        total_decl = 0
        total_reads = 0
        total_writes = 0
        
        for usage in method_usages.values():
            total_decl += usage["declarations"]
            total_reads += usage["reads"]
            total_writes += usage["writes"]
        
        return {
            "declarations": total_decl,
            "reads": total_reads, 
            "writes": total_writes
        }
    
    def _summarize_usage_counts(self, usage: Dict[str, int]) -> str:
        """将使用计数转换为简洁描述"""
        parts = []
        
        if usage["declarations"] > 0:
            parts.append(f"{usage['declarations']}次声明")
        if usage["reads"] > 0:
            parts.append(f"{usage['reads']}次读")
        if usage["writes"] > 0:
            parts.append(f"{usage['writes']}次写")
        
        return "、".join(parts)
    
    def _extract_method_analysis(self) -> Dict[str, Any]:
        """提取方法分析信息"""
        method_analysis = {}
        
        # 处理方法复杂度
        for method_name, complexity in self.method_complexity.items():
            method_analysis[method_name] = {
                "complexity": complexity["complexity"],
                "max_nesting": complexity["max_nesting"]
            }
            
            # 添加方法类型
            if "intent" in complexity:
                method_analysis[method_name]["intent"] = complexity["intent"]
            
            # 添加方法调用信息（如果有）
            if method_name in self.method_calls:
                caller_count = len(self.method_calls[method_name]["callers"])
                if caller_count > 0:
                    method_analysis[method_name]["called_by"] = caller_count
            
            # 提供复杂度评级
            cyclomatic = complexity["complexity"]
            if cyclomatic <= 3:
                method_analysis[method_name]["complexity_rating"] = "低"
            elif cyclomatic <= 7:
                method_analysis[method_name]["complexity_rating"] = "中"
            else:
                method_analysis[method_name]["complexity_rating"] = "高"
        
        return method_analysis
    
    def _extract_key_comments(self) -> List[Dict[str, Any]]:
        """提取关键注释"""
        # 如果聚合级别高，进一步减少注释数量
        if self.aggregation_level == "high":
            # 只保留文档注释和关键功能说明
            return [comment for comment in self.important_comments 
                   if comment["type"] == "doc_comment" or "功能" in comment["text"]]
        
        return self.important_comments
    
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
    
    def _find_condition_expression(self, node):
        """查找条件表达式"""
        if hasattr(node, 'children'):
            for child in node.children:
                if child.type == 'parenthesized_expression':
                    if hasattr(child, 'children'):
                        for paren_child in child.children:
                            if paren_child.type not in {'(', ')'}:
                                return paren_child
        return None
    
    def _summarize_expression(self, node) -> str:
        """简化表达式为文本摘要"""
        if not node:
            return "unknown"
        
        if hasattr(node, 'text'):
            text = node.text.decode('utf-8')
            # 如果文本太长，截断它
            if len(text) > 30:
                return text[:27] + "..."
            return text
        
        if node.type == 'binary_expression':
            if hasattr(node, 'children') and len(node.children) >= 3:
                left = self._summarize_expression(node.children[0])
                op = "?"
                if hasattr(node.children[1], 'type'):
                    op = node.children[1].type
                right = self._summarize_expression(node.children[2])
                
                summary = f"{left} {op} {right}"
                if len(summary) > 30:
                    return summary[:27] + "..."
                return summary
        
        return node.type


def compress_java_ast(java_code: str, 
                       lang_path: str = None,
                       preserve_comments: bool = True, 
                       track_control_flow: bool = True,
                       track_data_flow: bool = True,
                       include_method_intent: bool = True,
                       aggregation_level: str = "medium",
                       use_key_mapping: bool = True) -> Dict[str, Any]:
    """
    解析并优化压缩Java代码的AST，使用键名映射表减小大小并保持LLM可理解性
    
    Args:
        java_code: Java源代码字符串
        lang_path: tree-sitter语言库路径
        preserve_comments: 是否保留关键注释信息
        track_control_flow: 是否跟踪控制流
        track_data_flow: 是否跟踪数据流
        include_method_intent: 是否包含方法意图分析
        aggregation_level: 聚合级别 ("low", "medium", "high")
        use_key_mapping: 是否使用键名映射表减小输出大小
    
    Returns:
        优化压缩后的AST字典
    """
    # 加载tree-sitter Java语言支持
    try:
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
    
    # 设置解析器
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    
    # 解析代码
    tree = parser.parse(bytes(java_code, 'utf8'))
    
    # 创建压缩器
    compressor = LLMFriendlyASTCompressor(
        preserve_comments=preserve_comments,
        track_control_flow=track_control_flow,
        track_data_flow=track_data_flow,
        include_method_intent=include_method_intent,
        aggregation_level=aggregation_level,
        use_key_mapping=use_key_mapping
    )
    
    # 压缩AST
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


# 压缩JSON输出的辅助函数
def get_compressed_json(data: Any) -> str:
    """获取紧凑格式的JSON字符串"""
    import gzip
    import base64
    
    # 先将数据转换为JSON字符串
    json_str = json.dumps(data, ensure_ascii=False)
    
    # 使用gzip压缩
    compressed = gzip.compress(json_str.encode('utf-8'))
    
    # 转换为base64编码的字符串
    base64_str = base64.b64encode(compressed).decode('ascii')
    
    return base64_str


def load_compressed_json(base64_str: str) -> Any:
    """从压缩的JSON字符串中加载数据"""
    import gzip
    import base64
    
    # 解码base64
    compressed = base64.b64decode(base64_str)
    
    # 解压gzip
    json_str = gzip.decompress(compressed).decode('utf-8')
    
    # 解析JSON
    return json.loads(json_str)


# 使用示例
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='LLM友好的Java AST压缩工具')
    parser.add_argument('input', help='Java源代码文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径', default=None)
    parser.add_argument('--lang-path', '-l', help='tree-sitter语言库路径', default=None)
    parser.add_argument('--no-comments', action='store_true', help='不保留注释')
    parser.add_argument('--no-control-flow', action='store_true', help='不跟踪控制流')
    parser.add_argument('--no-data-flow', action='store_true', help='不跟踪数据流')
    parser.add_argument('--no-method-intent', action='store_true', help='不包含方法意图分析')
    parser.add_argument('--no-key-mapping', action='store_true', help='不使用键名映射表')
    parser.add_argument('--aggregation', '-a', choices=['low', 'medium', 'high'], 
                        default='medium', help='聚合级别')
    parser.add_argument('--no-indent', action='store_true', help='输出不缩进的JSON')
    parser.add_argument('--compress-output', action='store_true', help='压缩输出的JSON')
    
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
        output_file = f"{base_name}_llm_friendly_ast.json"
    
    # 压缩AST
    print(f"正在优化分析 {args.input}...")
    compressed_ast = compress_java_ast(
        java_code,
        lang_path=args.lang_path,
        preserve_comments=not args.no_comments,
        track_control_flow=not args.no_control_flow,
        track_data_flow=not args.no_data_flow,
        include_method_intent=not args.no_method_intent,
        aggregation_level=args.aggregation,
        use_key_mapping=not args.no_key_mapping
    )
    
    # 保存AST
    indent = None if args.no_indent else 2
    if args.compress_output:
        # 压缩JSON输出
        base64_str = get_compressed_json(compressed_ast)
        with open(output_file + '.b64', 'w') as f:
            f.write(base64_str)
        print(f"压缩的AST已保存到: {output_file}.b64")
    else:
        save_compressed_ast(compressed_ast, output_file, indent=indent)
    
    # 输出统计信息
    print("\n优化AST统计信息:")
    
    # 估算大小减少
    original_json = json.dumps(compressed_ast)
    original_size = len(original_json)
    
    # 如果使用了键名映射表，计算节省的空间
    if not args.no_key_mapping:
        # 假设没有使用键名映射
        data = compressed_ast.get("data", {})
        unwrapped_json = json.dumps(data)
        unwrapped_size = len(unwrapped_json)
        
        saved_bytes = unwrapped_size - original_size + len(json.dumps(compressed_ast["key_mapping"]))
        save_percent = (saved_bytes / unwrapped_size) * 100 if unwrapped_size > 0 else 0
        
        print(f"- 键名映射节省空间: {saved_bytes / 1024:.2f} KB ({save_percent:.1f}%)")
    
    # 基本输出大小统计
    print(f"- AST压缩后大小: {original_size / 1024:.2f} KB")
    
    # 显示键名映射表
    if not args.no_key_mapping:
        key_count = len(compressed_ast["key_mapping"])
        print(f"- 使用了 {key_count} 个键名映射")
    
    # 输出类和方法信息
    data = compressed_ast.get("data", compressed_ast)
    structure = data.get("s" if not args.no_key_mapping else "structure", {})
    classes = structure.get("cs" if not args.no_key_mapping else "classes", [])
    
    if classes:
        class_key = "n" if not args.no_key_mapping else "name"
        method_key = "ms" if not args.no_key_mapping else "methods"
        
        print(f"\n找到 {len(classes)} 个类:")
        
        for cls in classes:
            print(f"- 类: {cls.get(class_key, 'Unknown')}")
            
            methods = cls.get(method_key, [])
            if methods:
                print(f"  包含 {len(methods)} 个方法")
    
    print(f"\n分析完成，结果已保存到: {output_file}")
