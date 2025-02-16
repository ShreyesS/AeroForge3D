import requests
import time
import os
from dotenv import load_dotenv
load_dotenv() # we need to load env vars here

from lumaai import LumaAI

LUMA_API_KEY = os.getenv("LUMAAI_API_KEY")

# Initialize Luma Client
client = LumaAI(auth_token=LUMA_API_KEY)

def generate_luma_image(prompt, aspect_ratio="4:3", model="photon-1"):
    """Generates a high-accuracy 2D technical blueprint using Luma AI."""
    try:
        generation = client.generations.image.create(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            model=model
        )

        # Poll for completion
        while True:
            generation = client.generations.get(id=generation.id)
            if generation.state == "completed":
                break
            elif generation.state == "failed":
                raise RuntimeError(f"Generation failed: {generation.failure_reason}")
            print("🖼️ Generating 2D Image... (Please wait)")
            time.sleep(5)

        # ✅ Get the final image URL
        image_url = generation.assets.image
        print(f"✅ Image Generated: {image_url}")

        return image_url  # ✅ Return the image URL to be displayed on the frontend

    except Exception as e:
        print(f"❌ Error: {e}")
        return None
