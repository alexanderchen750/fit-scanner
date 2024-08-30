from flask import Flask, request, jsonify
import magic
import boto3
import os
from search import search_clothing_item
from botocore.exceptions import NoCredentialsError, Boto3Error

app = Flask(__name__)
mime = magic.Magic(mime=True)

# Configure AWS credentials using environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Create an S3 client
s3 = boto3.client('s3',
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file submitted'}), 400

    file = request.files['file']
    
    file_mime_type = mime.from_buffer(file.read(1024))
    file.seek(0)  # Reset file pointer after reading

    # Define allowed MIME types
    allowed_mime_types = ['image/png', 'image/jpeg']
    # Check if the MIME type is allowed
    if file_mime_type not in allowed_mime_types:
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, and JPEG files are allowed.'}), 400

    try:
        # Upload the file to S3 bucket
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename,
                          ExtraArgs={'ContentType': file.content_type})

        # Get the URL of the uploaded file
        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"

        # Call the search_clothing_item function with the file URL as a parameter
        #result = search_clothing_item(file_url)
        result = {"message": "File uploaded successfully", "file_url": file_url}

        return jsonify(result)
    except (NoCredentialsError, Boto3Error) as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
