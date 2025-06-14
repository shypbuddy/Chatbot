# Logistics Support Assistant

A smart logistics support chatbot that helps customers with shipping, delivery tracking, and order status inquiries.

## Features
- Order status tracking via PostgreSQL database
- Shipping and delivery information
- Logistics FAQs and support
- Package tracking assistance
- Professional and friendly responses

## How to run?

### STEPS:

Clone the repository

```bash
Project repo: https://github.com/
```

### STEP 01- Create a conda environment after opening the repository

```bash
https://repo.anaconda.com/miniconda/Miniconda3-py310_25.3.1-1-Windows-x86_64.exe
```
```bash
conda create -n BuddyAI python=3.10 -y
```

```bash
conda activate BuddyAI
```

### STEP 02- Install the requirements
```bash
pip install -r requirements.txt
```

### STEP 03- Set up environment variables
Create a `.env` file in the root directory and add your credentials:

```ini
# Pinecone credentials
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_API_ENV = "your-pinecone-environment"

# OpenRouter API key
OPENROUTER_API_KEY = "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"

# PostgreSQL credentials
DB_HOST = "your-db-host"
DB_NAME = "your-db-name"
DB_USER = "your-db-user"
DB_PASSWORD = "your-db-password"
```

### STEP 04- Set up PostgreSQL database
Create the required table in your PostgreSQL database:

```sql
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    status VARCHAR(50),
    delivery_estimate TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### STEP 05- Download the model
Download the quantized model and place it in the model directory:

```ini
## Download the Llama 2 Model:
llama-2-7b-chat.ggmlv3.q4_0.bin

## From the following link:
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
```

### STEP 06- Initialize the vector store
```bash
python store_index.py
```

### STEP 07- Run the application
```bash
python app.py
```

Now, open your browser and navigate to:
```bash
http://localhost:8080
```

## Techstack Used:
- Python
- LangChain
- Flask
- Meta Llama2
- Pinecone
- PostgreSQL
- OpenRouter API


