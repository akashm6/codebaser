# Codebaser

**Codebaser** is an AI-powered developer productivity tool that helps engineers quickly **understand, navigate, and query unfamiliar codebases**. It combines **static analysis** (via [Tree-sitter](https://tree-sitter.github.io/)), **semantic embeddings** (via [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)), and **vector search** ([ChromaDB](https://www.trychroma.com/)) to provide **semantic code search and Q&A** on large repositories.

**Demo Video:** [Watch here](https://www.youtube.com/watch?v=6Zqd6JGbLik&ab_channel=AkashMohan)  
**Live App:** [codebaser.app](https://codebaser.vercel.app/)


## Features

- **Codebase Uploads**: Upload a `.zip` file of any repository, or fetch directly via GitHub URL.
- **Syntax-Aware Parsing**: Uses Tree-sitter to parse multiple programming languages into functions, classes, and modules.
- **Chunk Summaries**: Generates concise summaries of each chunk using GPT-4.1-mini.
- **Semantic Search**: Stores embeddings in ChromaDB for efficient semantic retrieval.
- **Natural Language Q&A**: Ask questions about the codebase and get context-aware answers with both summaries and the original code.
- **Metadata Storage**: Chunk metadata is indexed in PostgreSQL for fast filtering and retrieval.
- **Clean Frontend**: Next.js + shadcn/ui + Framer Motion + Shiki for a modern, minimal developer UI.
- **GitHub OAuth**: Authenticate with GitHub to isolate user workspaces and support private repos.

## Tech Stack

- **Backend**: FastAPI, PostgreSQL, ChromaDB, Redis, AWS S3  
- **Frontend**: Next.js, Tailwind CSS, Shiki (syntax highlighting), Framer Motion, shadcn/ui
- **AI/Parsing**: Tree-sitter, OpenAI GPT-4.1-mini, OpenAI embeddings  

## 🏗️ Architecture
### Backend
```
codebaser
│   README.md
└───backend
    │   .gitignore
    │   Dockerfile
    │   app.py
    │   build_shared_lib.py
    │   requirements.txt
    │   routes.py
    │   s3_utils.py
    │   supported-languages.so
    └───db
    |    chroma_store.py
    |    models.py        
    |    postgres_store.py
    └───embedding
    │    summarize.py
    └───parallel_processing
    │   codechunk.py
    |   multiprocessor.py
    └───parsers
    |   tree-sitter-go
    |   tree-sitter-java
    |   tree-sitter-javascript
    |   tree-sitter-python
    |   tree-sitter-typescript 
```  
---

## Demo

### [Watch a short demo](https://www.youtube.com/watch?v=6Zqd6JGbLik&ab_channel=AkashMohan) to see Codebaser in action.  

## Roadmap
- Expand support for additional programming languages (Rust, C++, etc.)  
- Inline annotations inside code files  
- Query analytics and developer insights  
