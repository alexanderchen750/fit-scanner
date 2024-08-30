from flask import Flask, jsonify
import boto3
import os
from PIL import Image
from search import search_clothing_item
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
load_dotenv()
# Configure AWS credentials using environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')  # Add your region here


# Create an S3 client with region
s3 = boto3.client('s3',
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                   region_name=AWS_REGION)  # Specify the region

def upload_photo(file_path):
    """
    Uploads a local file to the S3 bucket and returns the result.
    """
    try:
        # Open the file using PIL
        with Image.open(file_path) as img:
            # Check if the file is a JPEG or PNG
            if img.format not in ['JPEG', 'PNG']:
                return {"error": "Invalid file type"}

            # Upload the file to the S3 bucket
            with open(file_path, 'rb') as file:
                s3.upload_fileobj(file, S3_BUCKET_NAME, os.path.basename(file_path),
                                  ExtraArgs={'ContentType': f'image/{img.format.lower()}'})

            # Get the URL of the uploaded file
            file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{os.path.basename(file_path)}"

            # Optionally call the search_clothing_item function with the file URL
            result = search_clothing_item(file_url)
            
            return result

    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": "Credentials error: " + str(e)}

    except ClientError as e:
        return {"error": "AWS Client error: " + str(e)}

    except IOError:
        return {"error": "Could not open or read the file"}

if __name__ == '__main__':
    file_path = 'hoodie1.jpg'
    result = upload_photo(file_path)
    print(result)
