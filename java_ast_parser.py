from tree_sitter import Language, Parser
import tree_sitter_languages
import os

def write_node(file, node, source_code, level=0):
    """递归写入AST节点信息到文件"""
    indent = "  " * level
    node_text = source_code[node.start_byte:node.end_byte].decode('utf8')
    file.write(f"{indent}{node.type}: '{node_text}'\n")
    
    # 递归写入所有子节点
    for child in node.children:
        write_node(file, child, source_code, level + 1)

def parse_java_file(java_file_path, output_file_path):
    """解析Java文件并将AST信息写入到输出文件"""
    # 获取Java语言支持
    java_language = tree_sitter_languages.get_language('java')
    
    # 创建解析器
    parser = Parser()
    parser.set_language(java_language)
    
    # 读取Java文件
    with open(java_file_path, 'rb') as f:
        source_code = f.read()
    
    # 解析代码
    tree = parser.parse(source_code)
    
    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # 写入AST到文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(f"Java文件AST分析结果: {java_file_path}\n")
        f.write("=" * 80 + "\n\n")
        write_node(f, tree.root_node, source_code)

if __name__ == "__main__":
    # 输入Java文件路径
    java_file = "D:/8/src/main/java/com/asiainfo/cvd/daemon/CNVDDirectoryWatcherDaemon.java"
    
    # 输出文件路径
    output_file = "D:/8/src/main/java/com/asiainfo/cvd/daemon/CNVDDirectoryWatcherDaemon_ast_output.txt"
    
    try:
        parse_java_file(java_file, output_file)
        print(f"AST分析完成，结果已写入到文件: {output_file}")
    except Exception as e:
        print(f"解析出错: {str(e)}") 