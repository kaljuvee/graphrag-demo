import os
import json
import zipfile
import random
from faker import Faker
from collections import Counter

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

# Directory to store files
output_dir = "synthetic_incidents"
os.makedirs(output_dir, exist_ok=True)

# Sample descriptions for variation (without plant, date, or cause references)
incident_descriptions = [
    "Employee reported dizziness and nausea in the packaging area. Investigation revealed a malfunctioning {incident_type} system. The area was evacuated and maintenance was called.",
    "A {incident_type} alarm was triggered in the assembly line. Employees evacuated and emergency services responded. The issue was addressed promptly.",
    "A worker in the production area experienced a {incident_type}, resulting in minor injuries. Safety protocols have been updated.",
    "A near-miss {incident_type} incident was reported. A piece of equipment narrowly avoided colliding with a pedestrian in a blind spot.",
    "Symptoms of {incident_type} were reported by a worker. The incident prompted a review of working conditions and safety measures."
]

# Function to generate a synthetic document
def generate_synthetic_document(incident_type):
    template = random.choice(incident_descriptions)
    description = template.format(incident_type=incident_type)
    return fake.sentence() + " " + description + " " + fake.sentence()

# Generate documents
def generate_documents(incident_types, output_dir):
    incident_count = Counter()
    incident_id = 1

    for incident_type, count in incident_types.items():
        for _ in range(count):
            document_content = generate_synthetic_document(incident_type)
            
            # Save document to a text file
            file_name = f"incident_{incident_id}.txt"
            with open(os.path.join(output_dir, file_name), 'w') as file:
                file.write(document_content)
            
            incident_count[incident_type] += 1
            incident_id += 1
    
    return incident_count

def unzip_files(zip_file_name, target_dir="data/input"):
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Unzip the files to the target directory
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

def write_files(output_dir, incident_count):
    # Create a zip file of all documents
    zip_file_name = "synthetic_incidents.zip"
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)

    # Create JSON summary of incident counts
    json_file_name = "incident_summary.json"
    with open(json_file_name, 'w') as jsonfile:
        json.dump(dict(incident_count), jsonfile, indent=2)

    unzip_files(zip_file_name, target_dir="data/input")

    return zip_file_name, json_file_name

def main():
    # Generate documents and track frequencies
    incident_count = generate_documents(incident_types, output_dir)

    # Write files and get file names
    zip_file_name, json_file_name = write_files(output_dir, incident_count)

    # Output summary
    print(f"Documents generated: {sum(incident_count.values())}")
    print(f"Summary JSON: {json_file_name}")
    print(f"Zipped file: {zip_file_name}")

if __name__ == "__main__":
    main()
