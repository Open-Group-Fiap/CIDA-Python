from typing import Annotated, Dict, List
from fastapi import FastAPI
from azure.storage.blob import BlobClient, BlobServiceClient, download_blob_from_url
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel
from io import BytesIO
app = FastAPI()

account_url="https://cidastore.blob.core.windows.net"
credential = DefaultAzureCredential()

class AnalyzeRequest(BaseModel):
    container: str
    file_names: List[str]
class AnalyzeResponse(BaseModel):
    insight: str

def process_file(file: bytes, file_name: str):
    print(file)
    file_data = BytesIO(file)
    text = ""
    if file_name.endswith(".pdf"):
        text = extract_text_from_pdf(file_data)
    elif file_name.endswith(".docx"):
        text = extract_text_from_docx(file_data)
    elif file_name.endswith(".xlsx"):
        text = extract_text_from_xlsx(file_data)
    else:
        raise ValueError("Unsupported file type")
    return text

def extract_text_from_pdf(file_data):
    from PyPDF2 import PdfReader
    pdfReader = PdfReader(file_data)
    text = ""
    for page in pdfReader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_data):
    from docx import Document
    document = Document(file_data)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + " "
    return text

def extract_text_from_xlsx(file_data):
    from openpyxl import load_workbook
    loader = load_workbook(file_data)
    text = ""
    for sheet in loader.worksheets:
        for row in sheet.iter_rows(values_only=True):
            text += ' '.join([str(cell) for cell in row if cell]) + '\n'
    return text

def get_blob(container_name, blob_name):
    blob_service_client = BlobServiceClient(account_url=account_url)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client

@app.get("/")
def read_root():
    blob = get_blob("teste-container", "2º Ano - Challenge FIAP - 2º Semestre 2024  - Plusoft.pdf")
    print(blob.url)
    return {"Hello": "World2", "blob": blob.url}

@app.post("/analyze")
async def analyze(data: AnalyzeRequest) -> AnalyzeResponse:
    blobs: List[BlobClient] = []
    text = ""
    for file_name in data.file_names:
        blob = get_blob(data.container, file_name)
        blobs.append(blob)
    for blob in blobs:
        try:
            converted = blob.download_blob().readall()
            text += process_file(converted, blob.blob_name) + "\n"
        except Exception as e:
            print(blob.url)
            print(e)
        
    return AnalyzeResponse(insight=text)

if __name__ == "__main__":
    print("De preferência, use o comando abaixo para iniciar o servidor:")
    print("python -m uvicorn main:app --reload")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
