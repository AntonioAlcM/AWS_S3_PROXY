# AWS_S3_PROXY
Small application to upload files and download files from AWS S3 service


## Setup
1. Clone the next repository:
    git@github.com:AntonioAlcM/AWS_S3_PROXY.git
2. Create the network:
    docker network create aws_s3_proxy_network  
3. Run docker-compose up -d in the main folder
4. Can check that the machines are up with:
    docker ps
5. Fast api has an endpoint where you can check a small documentation:
    http://localhost:8000/docs#/
 
The AWS S3 services are emulated with Minio, minion is configured by default with a bucket and user:
    bucket: s3-bucket-files
    user: alsofake
    password: alsofake
If you want to access Minio you have a website in this URL http://localhost:9001/ 

## Testing the APi
To testing the api I have used postman. Next I'm going to put some curls to test the application:

### Upload file
curl --location 'localhost:3000/upload/' \
--form 'bucket="s3-bucket-files"' \
--form 'file=@"Upload the file"' \
--form 'object_name="test_file.csv"'

### Download file
curl --location 'localhost:8000/download/s3-bucket-files/test_file.csv'