import os
import logging
from collections import Counter
from openai import OpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Incident types with specified counts
incident_types = {
    'slip': 10,
    'fire': 15,
    'safety violation': 20,
    'chemical spill': 8,
    'injury': 12,
    'near miss': 18,
    'electrical': 5,
    'ventilation': 7,
    'falling object': 9,
    'heat exhaustion': 6,
    'beehive': 3,
    'scaffolding': 7
}

# Directory to store files
output_dir = "data/input"
os.makedirs(output_dir, exist_ok=True)

# Hard-coded number of documents to generate
NUM_DOCUMENTS = 120

# Function to generate a synthetic document
def generate_synthetic_document(incident_type):
    prompt = f"Generate a 2-sentence incident report for a {incident_type} in a manufacturing plant. The first sentence should describe the incident, and the second sentence should mention potential consequences."
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates concise incident reports for manufacturing plants."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    
    return response.choices[0].message.content.strip()

# Generate documents
def generate_documents(incident_types, output_dir, num_documents):
    incident_count = Counter()
    incident_id = 1

    for incident_type, count in incident_types.items():
        for _ in range(min(count, num_documents - sum(incident_count.values()))):
            if sum(incident_count.values()) >= num_documents:
                break
            
            document_content = generate_synthetic_document(incident_type)
            
            # Save document to a TXT file
            file_name = f"incident_{incident_id}.txt"
            with open(os.path.join(output_dir, file_name), 'w') as file:
                file.write(document_content)
            
            incident_count[incident_type] += 1
            incident_id += 1
            
            # Log progress
            logging.info(f"Generated document {incident_id-1}/{num_documents}: {incident_type}")
        
        if sum(incident_count.values()) >= num_documents:
            break
    
    return incident_count

# Main function
def main():
    if not os.getenv("OPENAI_API_KEY"):
        logging.error("OPENAI_API_KEY not found in environment variables.")
        logging.error("Please make sure you have a .env file with your OpenAI API key.")
        return

    logging.info(f"Starting document generation. Target: {NUM_DOCUMENTS} documents")
    incident_count = generate_documents(incident_types, output_dir, NUM_DOCUMENTS)
    logging.info(f"Document generation complete. Total generated: {sum(incident_count.values())}")
    logging.info(f"Documents saved in: {output_dir}")
    logging.info("Incident type distribution:")
    for incident_type, count in incident_count.items():
        logging.info(f"  {incident_type}: {count}")

if __name__ == "__main__":
    main()
