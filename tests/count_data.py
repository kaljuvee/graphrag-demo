import os
from collections import Counter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def read_documents(input_folder):
    documents = []
    labels = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(input_folder, filename), 'r') as file:
                content = file.read().strip()
                documents.append(content)
                incident_type = content.split()[0].lower()
                labels.append(incident_type)
    return documents, labels

def create_index(documents):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(documents)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    return index, model

def query_index(index, model, query, k=5):
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector.astype('float32'), k)
    return indices[0]

def count_incidents(index, model, labels, query):
    indices = query_index(index, model, query, k=len(labels))
    return Counter(labels[i] for i in indices)

def main():
    input_folder = 'data/input'
    documents, labels = read_documents(input_folder)
    
    if not documents:
        print("No documents found in the input folder.")
        return

    index, model = create_index(documents)

    # Get and print total counts
    total_counts = Counter(labels)
    print("Total incident counts:")
    for incident_type, count in total_counts.items():
        print(f"{incident_type}: {count}")

    # Example query
    query = "fire incident"
    result = count_incidents(index, model, labels, query)
    print(f"\nIncident counts for query '{query}':")
    for incident_type, count in result.items():
        print(f"{incident_type}: {count}")

    # Interactive query loop
    while True:
        user_query = input("\nEnter a query (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        query_result = count_incidents(index, model, labels, user_query)
        print(f"Incident counts for query '{user_query}':")
        for incident_type, count in query_result.items():
            print(f"{incident_type}: {count}")

if __name__ == "__main__":
    main()
