import openai
import json
import os
from dotenv import load_dotenv
load_dotenv() # we need to load env vars here

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_sora_prompt(blueprint_json):
    """Generates a MIL-STD-31000-compliant Sora prompt with precise dimensions, materials, and tolerances"""

    component_name = blueprint_json.get("component_name", "Aerospace Component")
    material = blueprint_json.get("material", "Unknown Material")
    dimensions = blueprint_json.get("dimensions", {})
    
    length = dimensions.get("length", "Unknown")
    width = dimensions.get("width", "Unknown")
    height = dimensions.get("height", "Unknown")
    tolerance = dimensions.get("tolerance", "Unknown")

    engineering_notes = blueprint_json.get("engineering_notes", [])
    formatted_notes = "\n".join(f"- {note}" for note in engineering_notes) if engineering_notes else "No specific engineering notes provided."

    user_prompt = f"""
    Generate a MIL-STD-31000-compliant 3D engineering visualization of a {component_name}, optimized for defense and aerospace applications.

    **Rendering Style & Compliance Standards:**
    - **MIL-STD-31000 TDP format**: Use **orthographic projection** with precise **CAD labeling, metadata tags, and GD&T notations**.
    - **Blueprint Presentation**:
      - **Monochrome CAD layout** with **white background, black outlines, and labeled dimensions**.
      - No shading, cinematic effects, or artistic renderings—strictly **technical accuracy**.

    **Technical Specifications:**
    - **Component**: {component_name}
    - **Material**: {material}
    - **Dimensions**:
      - **Length**: {length}
      - **Width**: {width}
      - **Height**: {height}
      - **Tolerance**: {tolerance}

    **Additional Engineering Notes:**
    {formatted_notes}

    **Animation & Camera:**
    - Center the {component_name} in the frame.
    - Perform a **360-degree isometric rotation** to display all features.
    - Include an **exploded view animation** showcasing internal structures.

    **Strict Constraints:**
    - No photorealism—strictly **engineering CAD visualization**.
    - No artistic interpretation—adhere strictly to **Technical Data Package standards**.
    - No cinematic effects—this should resemble official aerospace documentation.

    Ensure the visualization maintains accurate proportions and follows MIL-STD-31000 specifications.
    """

    # ✅ Use the OpenAI client correctly
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an aerospace engineering expert specializing in MIL-STD-31000-compliant visualizations."},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content  # ✅ Correct way to access response
