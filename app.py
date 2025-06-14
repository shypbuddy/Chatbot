from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

# Debug logging
logger.info(f"Pinecone API Key present: {'Yes' if PINECONE_API_KEY else 'No'}")
logger.info(f"Pinecone API Env present: {'Yes' if PINECONE_API_ENV else 'No'}")
logger.info(f"OpenRouter API Key present: {'Yes' if OPENROUTER_API_KEY else 'No'}")

if not all([PINECONE_API_KEY, PINECONE_API_ENV, OPENROUTER_API_KEY]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

embeddings = download_hugging_face_embeddings()

# Initializing Pinecone
try:
    pinecone.init(api_key=PINECONE_API_KEY,
                  environment=PINECONE_API_ENV)
    logger.info("Successfully initialized Pinecone")
except Exception as e:
    logger.error(f"Failed to initialize Pinecone: {str(e)}")
    raise

index_name = "medical-bot"

# Loading the index
try:
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    logger.info("Successfully loaded Pinecone index")
except Exception as e:
    logger.error(f"Failed to load Pinecone index: {str(e)}")
    raise

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def get_openrouter_response(prompt):
    """Get response from OpenRouter API"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "moonshot-v1-8k",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
    except Exception as e:
        logger.error(f"Error calling OpenRouter API: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        input_text = msg
        
        # Get relevant context from Pinecone
        docs = docsearch.similarity_search(input_text, k=2)
        context = "\n".join([doc.page_content for doc in docs])
        
        # Format prompt with context
        prompt = PROMPT.format(context=context, question=input_text)
        
        # Get response from OpenRouter
        response = get_openrouter_response(prompt)
        return response
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)


