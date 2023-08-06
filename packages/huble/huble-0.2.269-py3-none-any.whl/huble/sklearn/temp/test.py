from boto3.session import Session

session = Session()
s3 = session.client(
    "s3",
    region_name="us-east-1",
    endpoint_url="https://s3.filebase.com",
    aws_access_key_id="709B6E02413B7282AC93",
    aws_secret_access_key="EyByFcqsBwTe4bWq6PwnoUJ9e2BqzShztJ48efVH",
)
# Upload the file to S3
s3.upload_file("tested.csv", "testsesaetsatast", "tested.csv")

# Get the response headers for the uploaded file
response = s3.head_object(Bucket="testsesaetsatast", Key="tested.csv")
headers = response.get("ResponseMetadata", {}).get("HTTPHeaders", {})

print(headers)
