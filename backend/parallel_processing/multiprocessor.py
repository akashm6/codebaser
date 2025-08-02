from parallel_processing.codechunk import chunk_go, chunk_java, chunk_javascript, chunk_python, chunk_typescript
from concurrent.futures import ProcessPoolExecutor, as_completed
from tree_sitter import Parser, Language
import multiprocessing
from pathlib import Path
from typing import List
import os

LIB_PATH = './supported-languages.so'

LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go"
}

CHUNK_MAP = {
    "python": chunk_python,
    "javascript": chunk_javascript,
    "typescript": chunk_typescript,
    "java" : chunk_java,
    "go": chunk_go
}

LANGUAGE_OBJECTS = {
    lang_name: Language(LIB_PATH, lang_name)
    for lang_name in CHUNK_MAP.keys()
}

def parse_and_chunk_file(file_path: str) -> List[dict]:
    extension = os.path.splitext(file_path)[1]
    file_lang = LANG_MAP.get(extension)
    if not file_lang:
        return []

    chunk_function = CHUNK_MAP.get(file_lang)
    if not chunk_function:
        return []

    parser = Parser()
    parser.set_language(LANGUAGE_OBJECTS[file_lang]) 

    code = Path(file_path).read_text()
    tree = parser.parse(bytes(code, 'utf-8'))

    return chunk_function(tree, code, file_path)

def concurrent_parse(source_dir: str, max_workers: int = None):
    if not max_workers:
        max_workers = multiprocessing.cpu_count()
        
    file_paths = []
    for root, _, files in os.walk(source_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            if extension in LANG_MAP:
                file_paths.append(os.path.join(root, f))
                
    chunks = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_and_chunk_file, file_path) for file_path in file_paths]
        for future in as_completed(futures):
            chunks.extend(future.result())
    
    return chunks
