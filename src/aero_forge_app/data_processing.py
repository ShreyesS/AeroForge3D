import json
import re
import requests
import os
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def extract_json_from_response(response_text):
    """Extracts only the JSON block from Perplexity's response."""
    
    json_match = re.search(r"```json\n(.*?)\n```", response_text, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(1).strip()  # Extract JSON text
        try:
            return json.loads(json_str)  # Convert to dictionary
        except json.JSONDecodeError as e:
            print("❌ JSON Parsing Error:", e)
            return None
    else:
        print("❌ No JSON block found in response!")
        return None



PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

def format_text_with_perplexity(extracted_text):
    """Converts blueprint text into structured JSON."""
    
    prompt = f"""
    Convert the following aerospace blueprint text into structured JSON format with these keys:
    - component_name
    - material
    - dimensions (length, width, height, tolerance if available)
    - engineering_notes (as a list)

    ONLY return JSON. Do NOT include explanations.

    Text:
    {extracted_text}
    """

    response = requests.post(
        PERPLEXITY_API_URL,
        json={"model": "sonar", "messages": [{"role": "user", "content": prompt}]},
        headers={"Authorization": f"Bearer {PERPLEXITY_API_KEY}", "Content-Type": "application/json"}
    )

    if response.status_code == 200:
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        
        structured_data = extract_json_from_response(content)  # ✅ Use the fixed function
        return structured_data  
    else:
        print(f"❌ API Error: {response.status_code}, {response.text}")
        return None
