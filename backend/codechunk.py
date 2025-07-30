import tree_sitter_python as tspython
from tree_sitter import Tree
from tree_sitter import Parser, Language
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional
from pathlib import Path

def chunk_python(tree: Optional[Tree], code: str, file_path: str):
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
        if node.type in ("function_definition", "class_definition"):
            chunks.append(extract_chunk(node))
        for child in node.children:
            walk_and_collect(child)

    walk_and_collect(root_node)
    return chunks