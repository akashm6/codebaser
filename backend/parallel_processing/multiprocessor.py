from parallel_processing.codechunk import chunk_go, chunk_java, chunk_javascript, chunk_python, chunk_typescript
from concurrent.futures import ProcessPoolExecutor, as_completed
from tree_sitter import Parser, Language
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

def parse_and_chunk_file(file_path: str) -> List[dict]:
    extension = os.path.splitext(file_path)[1]
    file_lang = LANG_MAP.get(extension, None)
    if not file_lang:
        return []
    
    chunk_function = CHUNK_MAP.get(file_lang, None)
    if not chunk_function:
        return []

    parser = Parser()
    language = Language(LIB_PATH, file_lang)
    parser.set_language(language)
    code = Path(file_path).read_text()
    tree = parser.parse(bytes(code, 'utf-8'))

    chunks = chunk_function(tree, code, file_path)
    return chunks

def concurrent_parse(source_dir: str, max_workers: int = 8):
    file_paths = []
    for root, _, files in os.walk(source_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            if extension in LANG_MAP:
                file_paths.append(os.path.join(root, f))

    #print(f"discovered {len(file_paths)} code files")
    chunks = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_and_chunk_file, file_path) for file_path in file_paths]
        for future in as_completed(futures):
            chunks.extend(future.result())
    # logging
    '''
    count = 1
    for c in chunks:
        print(f"CHUNK #{count}")
        print("=" * 40)
        print(c)
        count += 1
    '''
    return chunks
