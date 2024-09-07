import logging

from config import load_secrets

from fastapi import FastAPI, UploadFile, HTTPException, Form, File, status
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from botocore.exceptions import ClientError

from libs.aws_s3 import AwsS3


app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")

@app.post("/upload", status_code=status.HTTP_200_OK)
def upload_file(bucket: str = Form(...), file: UploadFile = File(...), object_name: str = Form(...)):
    response = {"status": False, "message": "Failed to upload the file"}
    config = load_secrets()
    aws_s3 = AwsS3()
    try:
        aws_s3.connect(aws_access_key_id=config['aws_access_key_id'],
                          aws_secret_access_key=config['aws_secret_access_key'], endpoint_url=config['endpoint_minio'])
            
        aws_s3.upload_file(bucket, file.file, object_name)
        
        response = {"status": True, "message": "File uploaded successfully"}
        return JSONResponse(response)
    
    except ClientError as err:
        logging.error(f"Something was wrong with the download {object_name} on {bucket}")
        logging.error(f"Error code: {err}")
        raise HTTPException(status_code=err.response['ResponseMetadata']['HTTPStatusCode'])

@app.get("/download/{bucket}/{object_name}", status_code=status.HTTP_200_OK)
def download_file(bucket: str, object_name: str):
    config = load_secrets()
    aws_s3 = AwsS3()
    try:
        aws_s3.connect(aws_access_key_id=config['aws_access_key_id'],
                          aws_secret_access_key=config['aws_secret_access_key'], endpoint_url=config['endpoint_minio'])
        
        file = aws_s3.download_file(bucket, object_name)
        if file:
            return StreamingResponse(file, media_type="application/octet-stream",
                                        headers={"Content-Disposition": f"attachment; filename={object_name}"})
            
    except ClientError as err:
        logging.error(f"Something was wrong with the download {object_name} on {bucket}")
        logging.error(f"Error code: {err}")
        raise HTTPException(status_code=err.response['ResponseMetadata']['HTTPStatusCode'])
    
