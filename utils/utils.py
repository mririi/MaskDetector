import base64
from google.cloud import storage
import os
import zipfile

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './auth_bucket.json'

def saveModel():
    storage_client = storage.Client()

    bucket = storage_client.bucket('mask-detector-model-bucket')

    blob = bucket.blob('model/maskDetectionModel.h5')
    blob.upload_from_filename('maskDetectionModel.h5')
    os.remove('maskDetectionModel.h5')
    print("Model uploaded successfully")
    return True

def getModel(): 
    storage_client = storage.Client()

    bucket = storage_client.bucket('mask-detector-model-bucket')

    blob = bucket.blob('model/maskDetectionModel.h5')
    blob.download_to_filename('maskDetectionModel.h5')
    print("Model downloaded successfully")
    return True

def getDataSet(): 
    storage_client = storage.Client()

    bucket = storage_client.bucket('mask-detector-model-bucket')

    blob = bucket.blob('model/dataset.zip')
    blob.download_to_filename('dataset.zip')
    
    print("Dataset downloaded successfully")

    # Unzipping the RAR file
    with zipfile.ZipFile('dataset.zip', 'r') as zf:
        zf.extractall()

    print("Dataset unzipped successfully")
    os.remove('dataset.zip')
    return True

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())