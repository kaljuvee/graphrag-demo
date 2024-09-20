import os
import random
import csv
import zipfile
from faker import Faker
from collections import defaultdict

# Initialize Faker
fake = Faker()

# Incident types and causes
incident_types = [
    'slip', 'fire', 'safety violation', 'chemical spill', 'injury', 'near-miss', 
    'electrical', 'ventilation', 'falling object', 'heat exhaustion', 'other'
]
incident_causes = ['Human error', 'Equipment', 'Environment']
plants = ['Plant A', 'Plant B', 'Plant C']

# Set number of documents to generate
num_documents = 1000

# Directory to store files
output_dir = "synthetic_incidents"
os.makedirs(output_dir, exist_ok=True)

# Keep track of the frequency of incidents by type, cause, and plant
incident_summary = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

# Sample descriptions for variation (without incident type and cause tags)
incident_descriptions = [
    "Employee reported dizziness and nausea in {plant}'s packaging area on {date}. Investigation revealed a malfunctioning ventilation system. The area was evacuated and maintenance was called.",
    "A fire alarm was triggered in {plant}'s assembly line on {date}. Employees evacuated and the fire department responded. The cause was determined to be a faulty wiring system.",
    "On {date}, a worker in {plant}'s production area tripped over an unmarked hazard, resulting in minor injuries. Safety protocols have been updated.",
    "A near-miss incident was reported on {date} at {plant}. A forklift narrowly avoided colliding with a pedestrian in a blind spot.",
    "Symptoms of heat exhaustion were reported by a worker in {plant} on {date}. The incident prompted a review of working conditions for outdoor tasks."
]

# Function to generate a synthetic document
def generate_synthetic_document(incident_id, plant):
    date = fake.date_this_year()
    description_template = random.choice(incident_descriptions)
    description = description_template.format(plant=plant, date=date)
    incident_report = f"Incident ID: {incident_id}\n{description}\n"
    return incident_report

# Generate documents and track frequencies
def generate_documents(num_documents, output_dir):
    incident_summary = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for i in range(1, num_documents + 1):
        incident_type = random.choice(incident_types)
        cause = random.choice(incident_causes)
        plant = random.choice(plants)
        
        # Update summary table
        incident_summary[plant][incident_type][cause] += 1
        
        # Generate the document
        document_content = generate_synthetic_document(i, plant)
        
        # Save document to a text file
        file_name = f"incident_{i}.txt"
        with open(os.path.join(output_dir, file_name), 'w') as file:
            file.write(document_content)
    
    return incident_summary

def write_files(output_dir, incident_summary):
    # Create a zip file of all documents
    zip_file_name = "synthetic_incidents.zip"
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)

    # Create CSV summary of incident counts by Plant, Type, and Cause
    csv_file_name = "incident_summary.csv"
    with open(csv_file_name, 'w', newline='') as csvfile:
        fieldnames = ['Plant', 'Incident Type', 'Cause', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for plant, incident_types in incident_summary.items():
            for incident_type, causes in incident_types.items():
                for cause, count in causes.items():
                    writer.writerow({'Plant': plant, 'Incident Type': incident_type, 'Cause': cause, 'Count': count})

    return zip_file_name, csv_file_name

def main():
    # Set number of documents to generate
    num_documents = 100

    # Directory to store files
    output_dir = "synthetic_incidents"
    os.makedirs(output_dir, exist_ok=True)

    # Generate documents and track frequencies
    incident_summary = generate_documents(num_documents, output_dir)

    # Write files and get file names
    zip_file_name, csv_file_name = write_files(output_dir, incident_summary)

    # Output summary
    print(f"Documents generated: {num_documents}")
    print(f"Summary CSV: {csv_file_name}")
    print(f"Zipped file: {zip_file_name}")

if __name__ == "__main__":
    main()
