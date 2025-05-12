from tree_sitter_language_pack import get_language, get_parser

# 加载 Java 语法
java_language = get_language('java')
java_parser = get_parser('java')

# 示例 Java 代码
source_code = b"""
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""

# 解析 Java 代码
tree = java_parser.parse(source_code)

# 打印语法树的根节点信息
print("Root node type:", tree.root_node.type)
print("Root node start byte:", tree.root_node.start_byte)
print("Root node end byte:", tree.root_node.end_byte)

# 遍历语法树的函数
def traverse_tree(node, level=0):
    indent = "  " * level
    print(f"{indent}- {node.type} [{node.start_byte}:{node.end_byte}]")
    
    # 打印文本内容（如果是叶子节点）
    if node.child_count == 0 and node.start_byte < node.end_byte:
        text = source_code[node.start_byte:node.end_byte].decode('utf-8')
        print(f"{indent}  Text: '{text}'")
    
    # 递归遍历子节点
    for child in node.children:
        traverse_tree(child, level + 1)

# 遍历并打印整个语法树
print("\nFull syntax tree:")
traverse_tree(tree.root_node)
