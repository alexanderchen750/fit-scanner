import streamlit as st
from search_function import search_clothing_item  # Assuming this is your custom function
import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

# Configure AWS credentials using environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not S3_BUCKET_NAME:
    st.error("AWS credentials or S3 bucket name are missing.")
else:
    # Create an S3 client
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Upload an image
    st.title("Clothing Scanner Demo")


    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        try:
            filename = uploaded_image.name  

            s3.upload_fileobj(uploaded_image, S3_BUCKET_NAME, filename,
                              ExtraArgs={'ContentType': uploaded_image.type})

            file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
            results = search_clothing_item(file_url)

            cols = st.columns(2)

            for index, result in enumerate(results.values()):
                if all(key in result for key in ['title', 'link', 'thumbnail', 'extracted_price']):
                    # Place content in alternating columns
                    with cols[index % 2]:
                        st.image(result['thumbnail'], width=350)
                        st.markdown(f"[{result['title']}]({result['link']})")
                        st.write(f"Extracted Price: ${result['extracted_price']}")
                    


        except (NoCredentialsError, ClientError) as e:
            st.error(f"Error uploading file to S3: {e}")
