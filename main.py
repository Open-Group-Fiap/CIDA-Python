from fastapi import FastAPI, HTTPException, UploadFile, File
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
app = FastAPI()

account_url="cidastore.blob.core.windows.net"
credential = DefaultAzureCredential()

def get_all_blobs(container_name):
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()
    return blobs

def get_blob(container_name, blob_name):
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client

@app.get("/")
def read_root():
    blob = get_blob("upload_files", "CP4_JAVA.pdf")
    print(blob.url)
    blobs = get_all_blobs("upload_files")
    for blob in blobs:
        print(blob.name)
    return {"Hello": "World"}

if __name__ == "__main__":
    print("De preferência, use o comando abaixo para iniciar o servidor:")
    print("python -m uvicorn main:app --reload")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
