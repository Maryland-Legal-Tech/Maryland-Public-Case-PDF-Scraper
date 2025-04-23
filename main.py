import requests
from bs4 import BeautifulSoup
import os
import boto3
from dotenv import load_dotenv
import os

def get_b2_resource():
    

    b2 = boto3.resource(service_name='s3',
        endpoint_url=os.environ.get('bucket_endpoint_url'),     # Backblaze endpoint
        aws_access_key_id=os.environ.get('backblaze_key_id'),  # Backblaze keyID
        aws_secret_access_key=os.environ.get('backblaze_api_key'),# Backblaze applicationKey
        )
    return b2

# Rest of the code...
def getFileNamesFromBackBlazeS3():
    b2 = get_b2_resource()
    my_bucket = b2.Bucket(os.environ.get('bucket_name'))
    prefix = 'public_case_pdfs/'
    results = [object_summary.key for object_summary in my_bucket.objects.filter(Prefix=prefix)]
    # Remove the prefix from each key
    return [key.replace(prefix, '') for key in results]


def writeFileToBackBlazeS3(content, filename):
    # # Upload content from the request response to s3 so we never have to save the file locally.

    b2 = get_b2_resource()
    object = b2.Object(os.environ.get('bucket_name'), f"public_case_pdfs/{filename}")
    result = object.put(Body=content)
    if result['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error with S3: " + str(result))


# Function to download PDF files loacally if needed.
def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

def scrapeWebsiteForLinks():

    # URL of the website
    url = 'https://www.mdcourts.gov/data/case/'

    # Send a request to the website
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with ID "indexlist"
        table = soup.find('table', {'id': 'indexlist'})
        
        # Find all links in the table
        if table:
            links = table.find_all('a')
            pdf_links = [link.get('href') for link in links if link.get('href').endswith('.pdf')]
            # Folder to save the PDF files
            return pdf_links
        else:
            print("Table with ID 'indexlist' not found.")
            return None
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None


# Load environment variables from .env file
#load_dotenv()

# Get the list of filenames in the s3 bucket so we don't download them again.
s3filenames = getFileNamesFromBackBlazeS3()

#Get the new list of pdf links from the court website
pdf_links = scrapeWebsiteForLinks()

# Download each PDF file
for pdf_link in pdf_links:
    
    if(pdf_link in s3filenames):
        #Check to see if we already downloaded this file. If so then skip it.
        print(f'{pdf_link} already exists in s3 bucket.')
        continue
    #Download the PDF
    print(f'Downloading: {pdf_link}')
    full_url = f'https://www.mdcourts.gov/data/case/{pdf_link}'
    response = requests.get(full_url)
    if response.status_code == 200:
        #Write it to the s3 bucket.
        writeFileToBackBlazeS3(response.content, pdf_link)