from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from ocr_extraction import extract_text_from_pdf
from data_processing import format_text_with_perplexity
from prompt_generation import generate_sora_prompt
from image_generation import generate_luma_image
from video_generation import generate_luma_video

app = FastAPI()

# ✅ Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Load HTML templates
templates = Jinja2Templates(directory="templates")

# ✅ Store uploaded PDFs
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Home Page (Upload Form)
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Handle PDF Upload + OCR Extraction
@app.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    extracted_text = extract_text_from_pdf(file_path)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "filename": file.filename,
        "extracted_text": extracted_text,
        "structured_data": None,
        "image_url": None,
        "sora_prompt": None,
        "luma_video": None
    })

# ✅ Process Text into Structured JSON
@app.post("/process-json")
async def process_json(request: Request, filename: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    extracted_text = extract_text_from_pdf(file_path)
    structured_json = format_text_with_perplexity(extracted_text)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "filename": filename,
        "structured_data": structured_json,
        "image_url": None,
        "sora_prompt": None,
        "luma_video": None
    })

# ✅ Generate 2D Blueprint Rendering using Luma
@app.post("/generate-image")
async def generate_image(request: Request, filename: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    extracted_text = extract_text_from_pdf(file_path)
    structured_json = format_text_with_perplexity(extracted_text)

    # Generate a text prompt for the Luma AI 2D rendering
    prompt = f"""
    Generate a **high-accuracy 2D technical blueprint** of an **{structured_json['component_name']}** in **MIL-STD-31000 engineering format**.

    **Technical Requirements:**
    - **Monochrome CAD-style blueprint**, precise **engineering lines & dimensions**.
    - Display **top, front, and side views** if applicable.
    - Include key measurements: {structured_json['dimensions']}
    - Label material properties: **{structured_json['material']}**
    - Add standard aerospace blueprint gridlines & annotations.
    - **No artistic shading or color effects**—pure **technical visualization**.
    """

    image_url = generate_luma_image(prompt)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "filename": filename,
        "structured_data": structured_json,
        "image_url": image_url,
        "sora_prompt": None,
        "luma_video": None
    })

# ✅ Generate Sora Prompt
@app.post("/generate-sora")
async def generate_sora(request: Request, filename: str = Form(...), image_url: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Retrieve structured JSON data first
    structured_json = format_text_with_perplexity(file_path)

    if not structured_json:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "filename": filename,
            "error": "Failed to generate structured JSON.",
            "structured_data": None,
            "sora_prompt": None,
            "image_url": image_url,  # Keep the 2D rendering visible
            "luma_video": None
        })

    # Generate the Sora prompt from the structured JSON
    sora_prompt = generate_sora_prompt(structured_json)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "filename": filename,
        "structured_data": None,  # ✅ JSON no longer shown after Sora prompt
        "sora_prompt": sora_prompt,  # ✅ Ensure this is passed
        "image_url": image_url,  # ✅ Keep the 2D image
        "luma_video": None
    })


# ✅ Generate Luma 3D Video
@app.post("/generate-luma")
async def generate_luma(request: Request, filename: str = Form(...), sora_prompt: str = Form(...)):
    # Generate Luma Dream Machine video
    luma_video_url = generate_luma_video(sora_prompt)

    if not luma_video_url:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "filename": filename,
            "sora_prompt": sora_prompt,
            "luma_video": None,  # Ensure it's None if generation fails
            "error": "Luma video generation failed.",
        })

    return templates.TemplateResponse("results.html", {
        "request": request,
        "filename": filename,
        "sora_prompt": sora_prompt,
        "luma_video": luma_video_url,  # ✅ Pass generated video URL
    })
