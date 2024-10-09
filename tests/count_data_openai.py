import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_documents(input_folder):
    documents = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(input_folder, filename), 'r') as file:
                content = file.read().strip()
                documents.append(content)
    return documents

def analyze_incidents(documents):
    incidents_text = "\n\n".join([f"Incident {i+1}: {doc}" for i, doc in enumerate(documents)])
    prompt = f"""Analyze the following incident reports:

{incidents_text}

1. Identify all unique types of incidents mentioned in these reports.
2. For each identified incident type, provide response in this format:
   - incident type: incident count
3. If an incident could be classified under multiple types, explain your decision process.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant specialized in analyzing incident reports."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def main():
    input_folder = 'data/input'
    documents = read_documents(input_folder)
    
    if not documents:
        print("No documents found in the input folder.")
        return

    # Analyze incidents using GPT-4
    analysis = analyze_incidents(documents)
    print("\nIncident Analysis:")
    print(analysis)

if __name__ == "__main__":
    main()