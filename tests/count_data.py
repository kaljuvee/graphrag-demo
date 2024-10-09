import os
import json
import random
from faker import Faker
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize Faker
fake = Faker()

# Incident types with specified counts
incident_types = {
    'slip': 10,
    'fire': 15,
    'safety violation': 20,
    'chemical spill': 8,
    'injury': 12,
    'near-miss': 18,
    'electrical': 5,
    'ventilation': 7,
    'falling object': 9,
    'heat exhaustion': 6,
    'beehive': 3,
    'scaffolding': 7
}

# Sample descriptions for variation
incident_descriptions = [
    "Employee reported dizziness and nausea in the packaging area. Investigation revealed a malfunctioning {incident_type} system. The area was evacuated and maintenance was called.",
    "A {incident_type} alarm was triggered in the assembly line. Employees evacuated and emergency services responded. The issue was addressed promptly.",
    "A worker in the production area experienced a {incident_type}, resulting in minor injuries. Safety protocols have been updated.",
    "A near-miss {incident_type} incident was reported. A piece of equipment narrowly avoided colliding with a pedestrian in a blind spot.",
    "Symptoms of {incident_type} were reported by a worker. The incident prompted a review of working conditions and safety measures."
]

def generate_synthetic_document(incident_type):
    template = random.choice(incident_descriptions)
    description = template.format(incident_type=incident_type)
    return fake.sentence() + " " + description + " " + fake.sentence()

def generate_documents(incident_types):
    documents = []
    labels = []
    for incident_type, count in incident_types.items():
        for _ in range(count):
            document_content = generate_synthetic_document(incident_type)
            documents.append(document_content)
            labels.append(incident_type)
    return documents, labels

# Generate documents and labels
documents, labels = generate_documents(incident_types)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed the documents
embeddings = model.encode(documents)

# Create a FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))

def query_index(query, k=5):
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector.astype('float32'), k)
    return indices[0]

def count_incidents(query):
    indices = query_index(query, k=len(documents))
    incident_counts = {incident_type: 0 for incident_type in incident_types}
    for idx in indices:
        incident_type = labels[idx]
        incident_counts[incident_type] += 1
    return incident_counts

# Example usage
query = "fire incident"
result = count_incidents(query)
print(f"Incident counts for query '{query}':")
print(json.dumps(result, indent=2))

# Verify total counts
total_counts = {incident_type: 0 for incident_type in incident_types}
for label in labels:
    total_counts[label] += 1

print("\nTotal incident counts:")
print(json.dumps(total_counts, indent=2))

# Compare with ground truth
print("\nGround truth:")
print(json.dumps(incident_types, indent=2))
