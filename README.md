# Overview

- A demonstration how to use [Microsoft GraphRAG](https://github.com/microsoft/graphrag) for incident analysis.

## Project Structure

```
data/input
```
contains the *.txt files as inputs.

## Virtual Environment and Dependencies

```
    python -m venv .venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate` or conda activate .conda
    pip install -r requirements.txt
```

## Initialise Workspace Variables

```
    python -m graphrag.index --init --root ./data
```

## Running the Indexing pipeline

```
    python -m graphrag.index --root ./data
```

## Running the Query Engine

```
    python -m graphrag.query \
    --root ./data \
    --method global \
    "How many heat related accidents were there?"
```

```
    python -m graphrag.query \
    --root ./data \
    --method local \
    "Which events included fire?"
```

## References
- [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/pdf/2404.16130) - by Microsoft Research
- [Microsoft GraphRAG and Ollama: Code Your Way to Smarter Question Answering](https://blog.gopenai.com/microsoft-graphrag-and-ollama-code-your-way-to-smarter-question-answering-45a57cc5c38b)
