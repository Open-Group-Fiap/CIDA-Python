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

@app.get("/")
def read_root():
    for blob in get_all_blobs("upload-files"):
        print(blob.name)
    return {"Hello": "World"}

if __name__ == "__main__":
    print("De preferência, use o comando abaixo para iniciar o servidor:")
    print("python -m uvicorn main:app --reload")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
