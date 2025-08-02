FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git gcc g++ make cmake curl

WORKDIR /app

COPY . .

RUN mkdir -p parsers && \
    git clone https://github.com/tree-sitter/tree-sitter-go.git parsers/tree-sitter-go && \
    git clone https://github.com/tree-sitter/tree-sitter-java.git parsers/tree-sitter-java && \
    git clone https://github.com/tree-sitter/tree-sitter-javascript.git parsers/tree-sitter-javascript && \
    git clone https://github.com/tree-sitter/tree-sitter-python.git parsers/tree-sitter-python && \
    git clone https://github.com/tree-sitter/tree-sitter-typescript.git parsers/tree-sitter-typescript && \
    git clone https://github.com/tree-sitter/tree-sitter-tsx.git parsers/tree-sitter-tsx

RUN python3 build_shared_lib.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
