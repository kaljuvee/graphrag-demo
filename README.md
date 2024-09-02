# graphrag-demo

# Overview

- Test implementation of MMG in Flask

## Project Structure

```
TBC

```

## Virtual Environment and Dependencies

```
    python -m venv .venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate` or conda activate .conda
    pip install -r requirements.txt
```

## Running Indexer

```
    mkdir -p ./ragtest/input
    curl https://www.gutenberg.org/cache/epub/24022/pg24022.txt > ./ragtest/input/book.txt
```


## Set Workspace Variables

```
    python -m graphrag.index --init --root ./ragtest
```

## Running the Indexing pipeline

```
    python -m graphrag.index --root ./ragtest
```

## Running the Query Engine

```
    python -m graphrag.query \
    --root ./ragtest \
    --method global \
    "What are the top themes in this story?"
```

```
    python -m graphrag.query \
    --root ./ragtest \
    --method local \
    "Who is Scrooge, and what are his main relationships?"
```