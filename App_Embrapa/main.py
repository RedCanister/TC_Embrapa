from fastapi import FastAPI, UploadFile, File
from utils.ocr_extractor import OCRProcessor
import os

app = FastAPI()
ocr_processor = 

@app.get("/")
async def root():
    return {"url": "http://127.0.0.1:8000/docs"}

@app.get("/extract_ocr_from_pdf")
async def extrac_ocr_from_pdf(pdf_file: UploadFile = File(...)):
    with open(pdf_file.filename, 'wb') as buffer:
        buffer.write(pdf_file.file.read())    

        ocr_text = OCRProcessor.extract_text_from_df(buffer)
        os.remove(buffer)

    return ocr_text

