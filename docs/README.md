nano docs/README.md

Replace the content with:
markdown
# Raznet-Chat with Files Assistant

A Chainlit-based app that allows you to upload and chat with various file formats, including PDF, DOCX, XLSX/CSV, TXT, ODT, MD, JSON, HTML, and PNG/JPG. The app extracts text from files (using OCR for images and PDFs) and answers questions based on the content using the Ollama language model.

## Project Folder Structure
The project is organized as follows:

Raznet-CHAT-with-FILES/
├── docs/                 # Documentation
│   └── README.md         # Project documentation
├── frontend/             # React frontend files (if applicable)
│   ├── src/              # React source code
│   ├── public/           # Public assets (e.g., index.html)
│   ├── index.js          # Main JavaScript entry point
│   └── package.json      # Node.js dependencies
├── src/                  # Source code for the backend
│   ├── app.py            # Main application logic
│   └── utils/            # Optional: Utility scripts (e.g., for file processing)
├── tests/                # Test files and data
│   ├── data/             # Test files (PDFs, images, etc.)
│   │   ├── test.pdf      # Test PDF
│   │   └── output-1.png  # Test image
│   └── scripts/          # Test scripts (if any)
├── requirements.txt      # Python dependencies
├── venv/                 # Virtual environment
└── .gitignore            # Git ignore file to exclude temporary files
text

## Features
- Supports multiple file formats: PDF, DOCX, XLS/XLSX, CSV, TXT, ODT, MD, JSON, HTML, PNG/JPG
- Extracts text using OCR for PDFs and images (via Tesseract)
- Answers questions about file content using Ollama (`llama3.2:1b` by default)
- User-friendly prompts and error messages

## Setup Instructions
1. **Clone the Repository** (if deploying locally):
   ```bash
   git clone <repository-url>
   cd Raznet-CHAT-with-FILES

    Install Dependencies:
        Install Python dependencies:
        bash

pip install -r requirements.txt
Install Tesseract for OCR:
bash
sudo apt install tesseract-ocr tesseract-ocr-eng -y
Download eng.traineddata if not present:
bash
sudo wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata -P /usr/local/share/tessdata
Set the TESSDATA_PREFIX environment variable:
bash

    export TESSDATA_PREFIX=/usr/local/share/tessdata
    echo 'export TESSDATA_PREFIX=/usr/local/share/tessdata' >> ~/.bashrc
    source ~/.bashrc

Run Ollama:

    Start the Ollama server:
    bash

ollama serve
Ensure the desired model is available (e.g., llama3.2:1b or llama3.2:3b):
bash

    ollama pull llama3.2:1b

Start the App:
bash

    chainlit run src/app.py --host 0.0.0.0 --port 8002
        Access the app at http://127.0.0.1:8002.

Usage

    Upload a file in one of the supported formats.
    Ask questions about the file content, such as:
        "What is the first line?"
        "Summarize the content."
        "What is the value in cell A1?" (for spreadsheets)# Project Documentation
