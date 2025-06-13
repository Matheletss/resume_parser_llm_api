from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from utils.pdf_extractor import extract_text_from_pdf
from utils.preprocessor import structure_for_llm
from utils.logger import save_training_example
from utils.openai_parser import call_openai_parser 
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume Parser API", description="Extracts structured JSON from resume PDFs using OpenAI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_location)
    structured_prompt = structure_for_llm(resume_text)
    os.remove(file_location)

    parsed_resume = call_openai_parser(structured_prompt)
    save_training_example(structured_prompt, parsed_resume)

    return JSONResponse(content={
        "prompt_input": structured_prompt,
        "parsed_resume": parsed_resume
    })
