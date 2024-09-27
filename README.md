# Project Overview:

Clothing Scanner scans an image of clothing and returns shopping links to similar items. It uses the Google Lens API from SerpAPI to support the scan. It's meant to be a backend funciton, but it can also be demoed using streamlit.

# Setup:

**Clone the repository**


```bash
git clone https://github.com/alexanderchen750/fit-scanner.git
```

**Setup .env file:**

Create a .env in your repository. You will need a SERPAPI_KEY, and a link to images that are uploaded, I'm using a s3 bucket. Make sure to replace with you keys.
```bash
SERPAPI_KEY=key
AWS_ACCESS_KEY_ID=id
AWS_SECRET_ACCESS_KEY=key
S3_BUCKET_NAME=key
AWS_REGION=region
```

**Python Venv**

Create a virtual enviroment in Python
```bash
python3 -m venv venv
```
Activate enviroment
```bash
source venv/bin/activate
```

**Install dependencies**

```Bash
pip install streamlit boto3 python-dotenv serpapi
```

# Running:
Make sure your in the folder `function` in command line, then to run the demo, use
```bash
streamlit run demo.py
```



