import tree_sitter_python as tspython
from tree_sitter import Tree
from tree_sitter import Parser, Language
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, List, Dict
from pathlib import Path

PY_NODE_TYPES = ("function_definition", "class_definition")
JS_NODE_TYPES = ("function_declaration", "function_expression", "arrow_function", "method_definition", "class_declaration")
TS_NODE_TYPES = JS_NODE_TYPES + ("interface_declaration", "type_alias_declaration", "enum_declaration")
JAVA_NODE_TYPES = ("method_declaration", "class_declaration", "constructor_declaration", "interface_declaration")
GO_NODE_TYPES = ("function_declaration", "method_declaration", "type_declaration", "const_declaration", "var_declaration")

def chunk_python(tree: Optional[Tree], code: str, file_path: str) -> List[Dict]:
    chunks = []
    root_node = tree.root_node

    def extract_chunk(node):
        start_byte = node.start_byte
        end_byte = node.end_byte
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        chunk_text = code[start_byte:end_byte]

        return {
            "text": chunk_text,
            "file_path": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "type": node.type
        }

    def walk_and_collect(node):
        if node.type in PY_NODE_TYPES:
            chunks.append(extract_chunk(node))
        for child in node.children:
            walk_and_collect(child)

    walk_and_collect(root_node)
    return chunks

def chunk_javascript(tree: Optional[Tree], code: str, file_path: str) -> List[Dict]:
    chunks = []
    root_node = tree.root_node

    def extract_chunk(node):
        start_byte = node.start_byte
        end_byte = node.end_byte
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        chunk_text = code[start_byte:end_byte]

        return {
            "text": chunk_text,
            "file_path": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "type": node.type
        }

    def walk_and_collect(node):
        if node.type in JS_NODE_TYPES:
            chunks.append(extract_chunk(node))
        for child in node.children:
            walk_and_collect(child)

    walk_and_collect(root_node)
    return chunks

def chunk_typescript(tree: Optional[Tree], code: str, file_path: str) -> List[Dict]:
    chunks = []
    root_node = tree.root_node

    def extract_chunk(node):
        start_byte = node.start_byte
        end_byte = node.end_byte
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        chunk_text = code[start_byte:end_byte]

        return {
            "text": chunk_text,
            "file_path": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "type": node.type
        }

    def walk_and_collect(node):
        if node.type in TS_NODE_TYPES:
            chunks.append(extract_chunk(node))
        for child in node.children:
            walk_and_collect(child)

    walk_and_collect(root_node)
    return chunks

def chunk_java(tree: Optional[Tree], code: str, file_path: str) -> List[Dict]:
    chunks = []
    root_node = tree.root_node

    def extract_chunk(node):
        start_byte = node.start_byte
        end_byte = node.end_byte
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        chunk_text = code[start_byte:end_byte]

        return {
            "text": chunk_text,
            "file_path": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "type": node.type
        }

    def walk_and_collect(node):
        if node.type in JAVA_NODE_TYPES:
            chunks.append(extract_chunk(node))
        for child in node.children:
            walk_and_collect(child)

    walk_and_collect(root_node)
    return chunks

def chunk_go(tree: Optional[Tree], code: str, file_path: str) -> List[Dict]:
    chunks = []
    root_node = tree.root_node

    def extract_chunk(node):
        start_byte = node.start_byte
        end_byte = node.end_byte
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        chunk_text = code[start_byte:end_byte]

        return {
            "text": chunk_text,
            "file_path": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "type": node.type
        }

    def walk_and_collect(node):
        if node.type in GO_NODE_TYPES:
            chunks.append(extract_chunk(node))
        for child in node.children:
            walk_and_collect(child)

    walk_and_collect(root_node)
    return chunks