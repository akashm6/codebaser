from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List
import os

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
SUMMARY_MODEL = "gpt-4.1-mini"
EMBED_MODEL = "text-embedding-3-small"

client = OpenAI(
    api_key=OPENAI_KEY,
)

summary_template = """Summarize the following function, class, or code snippet in 2-3 sentences. Be specific and cater to any specific requests or importance placed by the user."""

@retry(wait  = wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
def get_summary(code: str) -> str:

    prompt = summary_template + f" Code: {code}"
    
    response = client.responses.create(
        model=SUMMARY_MODEL,
        input=prompt,
        temperature=0.3,
    )

    return response.output_text

@retry(wait  = wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text.strip(),
    )
    return response.data[0].embedding

def embed_and_summarize_chunk(chunk: Dict) -> Dict:
    code = chunk["text"]
    summary = get_summary(code)
    embedding = get_embedding(code)

    chunk["summary"] = summary
    chunk["embedding"] = embedding
    return chunk

@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(3))
def synthesize_answer(query: str, chunks: List[Dict]) -> str:
    context_sections = []
    for c in chunks:
        snippet = f"""### Chunk from {c['file_path']} ({c['start_line']}-{c['end_line']}):
        Summary: {c['summary']}"""
        context_sections.append(snippet)

        context_block = "\n\n".join(context_sections)

        prompt = f"""You are a codebase assistant. Based on the following summaries, answer the user's question as clearly as possible.

        Question: {query}

        Relevant context:
        {context_block}

        Answer:"""

    response = client.responses.create(
        model=SUMMARY_MODEL,
        input=prompt,
        temperature=0.4,
    )

    return response.output_text.strip()

