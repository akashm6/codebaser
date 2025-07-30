from tree_sitter import Language

parser_paths = [
    'parsers/tree-sitter-go',
    'parsers/tree-sitter-java',
    'parsers/tree-sitter-javascript',
    'parsers/tree-sitter-python',
    'parsers/tree-sitter-typescript/typescript',
    'parsers/tree-sitter-typescript/tsx',
    
]

Language.build_library(
    output_path='./supported-languages.so',
    repo_paths=parser_paths
)