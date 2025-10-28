import fitz # PyMuPDF
import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from openai import OpenAI


load_dotenv()


OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY']= OPENAI_API_KEY


client=OpenAI(api_key= OPENAI_API_KEY)


def extracted_text_from_pdf(uploaded_file):
    """ 
    Extracts text from a PDF file.
    Args :
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text 

    """
    
    doc= fitz.open(stream=uploaded_file.read(), filetype= "pdf")

    text=""
    for page in doc:
        text+= page.get_text()
    return text


def ask_openai(prompt, model='gpt-3.5-turbo', temperature= 0.7):
    """
    Sends a prompt to the openAI API and return the response.

    Args:
        prompt(str): The prompt to send to the OpenAI API.
        model(str): The model to use for the Request
        temperature (float): The temperature for the response critivity language

    Returns:
        str: The response from the OpenAI API.

    """
    

    response= client.chat.complettions.create(
        model='gpt-4o',
        messages= [{
            'role':'user', 
            'content': prompt
        }],
        temperature= 0.5,max_tokens= max_tokens
    )

    return response.choices[0].message.content
