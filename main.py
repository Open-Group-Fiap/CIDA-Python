from typing import Annotated, Dict, List
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi import FastAPI
from azure.storage.blob import BlobClient, BlobServiceClient, download_blob_from_url
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel
from io import BytesIO
import os
import dotenv
from azure.ai.inference import ChatCompletionsClient 
dotenv.load_dotenv()
client = inference_client = ChatCompletionsClient(endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "", 
                                                  credential=DefaultAzureCredential(),
                                                  headers={'api-key': os.getenv("AZURE_OPENAI_API_KEY")})
app = FastAPI()

account_url="https://cidastore.blob.core.windows.net"
credential = DefaultAzureCredential()

class AnalyzeRequest(BaseModel):
    container: str
    file_names: List[str]
class AnalyzeResponse(BaseModel):
    insight: str

def process_file(file: bytes, file_name: str):
    file_data = BytesIO(file)
    text = ""
    if file_name.endswith(".pdf"):
        text = extract_text_from_pdf(file_data)
    elif file_name.endswith(".docx") or file_name.endswith(".doc"):
        text = extract_text_from_docx(file_data)
    elif file_name.endswith(".xlsx"):
        text = extract_text_from_xlsx(file_data)
    elif file_name.endswith(".csv"):
        text = extract_text_from_csv(file_data)
    else:
        raise ValueError("Unsupported file type")
    return text

def extract_text_from_pdf(file_data: BytesIO):
    from PyPDF2 import PdfReader
    pdfReader = PdfReader(file_data)
    text = ""
    for page in pdfReader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_data: BytesIO):
    from docx2txt import process
    document = process(file_data)
    return document

def extract_text_from_xlsx(file_data: BytesIO):
    from openpyxl import load_workbook
    loader = load_workbook(file_data)
    text = ""
    for sheet in loader.worksheets:
        for row in sheet.iter_rows(values_only=True):
            text += ' '.join([str(cell) for cell in row if cell]) + '\n'
    return text

def extract_text_from_csv(file_data: BytesIO):
    from csv import reader
    text = ""
    for row in reader(file_data.read().decode('utf-8').splitlines()):
        text += ' '.join(row) + '\n'
    return text


def get_blob(container_name, blob_name):
    blob_service_client = BlobServiceClient(account_url=account_url)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client

@app.get("/")
def read_root():
    return {"Hello": "World"}

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
    start_phase = "Resuma o seguinte documento e diminua seu tamanho total, mantenha a coesão, os dados e as estatisticas: "
    response = client.complete(messages=[
        SystemMessage(content=start_phase),
        UserMessage(content=text)
    ])
    text = response.choices[0].message.content
    return AnalyzeResponse(insight=text)

@app.get("/get-all-blobs/{container}")
async def get_all_blobs(container: str) -> Dict[str, str]:
    blob_service_client = BlobServiceClient(account_url=account_url)
    container_client = blob_service_client.get_container_client(container)
    blobs = container_client.list_blobs()
    blobs_dict = {}
    for blob in blobs:
        blobs_dict[blob.name] = get_blob(container, blob.name).url
    return blobs_dict



if __name__ == "__main__":
    print("De preferência, use o comando abaixo para iniciar o servidor:")
    print("python -m uvicorn main:app --reload")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
