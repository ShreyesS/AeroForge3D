import requests
import time
import os
from lumaai import LumaAI
from dotenv import load_dotenv
load_dotenv() # we need to load env vars here

LUMA_API_KEY = os.getenv("LUMAAI_API_KEY")

# Initialize Luma Client
client = LumaAI(auth_token=LUMA_API_KEY)

def generate_luma_video(prompt, aspect_ratio="16:9", model="ray-2", loop=True):
    """Generates a cinematic aerospace 3D rendering with Luma AI"""
    try:
        generation = client.generations.video.create(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            model=model,
            loop=loop
        )

        # Polling for completion
        while True:
            generation = client.generations.get(id=generation.id)
            if generation.state == "completed":
                break
            elif generation.state == "failed":
                raise RuntimeError(f"Generation failed: {generation.failure_reason}")
            print("🎥 Generating Video... (Please wait)")
            time.sleep(5)

        # ✅ Debug the full response
        print(f"🔍 Debugging: generation.assets = {generation.assets}")

        # ✅ Correct video URL extraction
        if hasattr(generation.assets, "video"):  # Ensure attribute exists
            video_url = generation.assets.video
        else:
            raise ValueError("No video URL found in response.")

        print(f"✅ Video Generated: {video_url}")

        # ✅ Save video to local directory
        video_filename = f'generated_videos/{generation.id}.mp4'
        os.makedirs("generated_videos", exist_ok=True)  

        response = requests.get(video_url, stream=True)
        with open(video_filename, 'wb') as file:
            file.write(response.content)

        print(f"📂 Video saved as {video_filename}")
        return video_url  

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ✅ Example Usage (Only runs when this file is executed directly)
if __name__ == "__main__":
    prompt_text = "Generate a high-fidelity 3D render of a Titanium Alloy Compressor Blade, aerospace-grade."
    video_file = generate_luma_video(prompt_text)
