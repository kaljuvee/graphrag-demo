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