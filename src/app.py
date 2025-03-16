import chainlit as cl
from PyPDF2 import PdfReader
import io
import ollama
from docx import Document
import pandas as pd
from odf import text, teletype
from odf.opendocument import load
import markdown
from bs4 import BeautifulSoup
from pdf2image import convert_from_bytes
import pytesseract
import os

@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome to Raznet-Chat with Files Assistant! Upload a file (PDF, DOCX, XLS/XLSX, CSV, TXT, RTF, ODT, MD, JSON, HTML, PNG/JPG) to chat with it. After uploading, you can ask questions like 'What is the first line?' or 'Summarize the content.'").send()

@cl.on_message
async def on_message(message: cl.Message):
    if message.elements:
        for element in message.elements:
            if hasattr(element, 'name'):
                file_name = element.name.lower()
                extracted_text = ""

                try:
                    # Handle different file formats
                    if hasattr(element, 'path') and element.path:
                        with open(element.path, 'rb') as f:
                            content = f.read()
                    elif hasattr(element, 'content'):
                        content = await element.content.read()
                    else:
                        await cl.Message(content="Error: Unable to access file content. Please try uploading the file again.").send()
                        return

                    # PDF
                    if file_name.endswith('.pdf'):
                        images = convert_from_bytes(content)
                        for img in images:
                            page_text = pytesseract.image_to_string(img)
                            if page_text:
                                extracted_text += page_text + "\n"

                    # DOCX
                    elif file_name.endswith('.docx'):
                        doc = Document(io.BytesIO(content))
                        for para in doc.paragraphs:
                            extracted_text += para.text + "\n"

                    # XLS/XLSX
                    elif file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                        df = pd.read_excel(io.BytesIO(content))
                        extracted_text = df.to_string()

                    # CSV
                    elif file_name.endswith('.csv'):
                        df = pd.read_csv(io.BytesIO(content))
                        extracted_text = df.to_string()

                    # TXT
                    elif file_name.endswith('.txt'):
                        extracted_text = content.decode('utf-8')

                    # RTF
                    elif file_name.endswith('.rtf'):
                        #rtf_doc = pyth_doc.from_file(io.BytesIO(content))
                        extracted_text = "RTF processing skipped"

                    # ODT
                    elif file_name.endswith('.odt'):
                        doc = load(io.BytesIO(content))
                        for elem in doc.getElementsByType(text.P):
                            extracted_text += teletype.extractText(elem) + "\n"

                    # Markdown (MD)
                    elif file_name.endswith('.md'):
                        md_text = content.decode('utf-8')
                        extracted_text = markdown.markdown(md_text)

                    # JSON
                    elif file_name.endswith('.json'):
                        import json
                        data = json.loads(content.decode('utf-8'))
                        extracted_text = json.dumps(data, indent=2)

                    # HTML
                    elif file_name.endswith('.html'):
                        soup = BeautifulSoup(content, 'html.parser')
                        extracted_text = soup.get_text()

                    # Images (PNG/JPG) for OCR
                    elif file_name.endswith(('.png', '.jpg', '.jpeg')):
                        from PIL import Image
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_name.split(".")[-1]}') as temp_file:
                            temp_file.write(content)
                            img = Image.open(temp_file.name)
                            extracted_text += pytesseract.image_to_string(img) + "\n"
                        os.unlink(temp_file.name)

                    else:
                        await cl.Message(content=f"Unsupported file format: {element.name}. Please upload a file in one of these formats: PDF, DOCX, XLS/XLSX, CSV, TXT, RTF, ODT, MD, JSON, HTML, PNG/JPG.").send()
                        return

                    if not extracted_text.strip():
                        await cl.Message(content=f"Error: No text could be extracted from {element.name}. This might happen if the file is empty, image-based with unclear text, or in an unsupported format. Try uploading a different file or ensure the text is clear.").send()
                        return

                    # Store the text in the session
                    cl.user_session.set("file_text", extracted_text)
                    await cl.Message(content=f"File '{element.name}' loaded successfully! You can now ask questions like 'What is the first line?', 'Summarize the content.', or 'What is the value in cell A1?' (for spreadsheets).").send()
                except Exception as e:
                    print(f"Error processing file {element.name}: {str(e)}")
                    await cl.Message(content=f"Error processing file '{element.name}'. Please try a different file or format.").send()
                    return
    else:
        # Handle text messages (e.g., questions about the file)
        file_text = cl.user_session.get("file_text", "")
        if not file_text:
            await cl.Message(content="Please upload a file first (PDF, DOCX, XLS/XLSX, CSV, TXT, RTF, ODT, MD, JSON, HTML, PNG/JPG).").send()
            return

        # Answer questions using the file text
        prompt = f"The following is the extracted text from a document:\n\n{file_text}\n\nAnswer the following question directly based on this text, without adding assumptions or refusals: {message.content}"
        msg = cl.Message(content="")
        await msg.send()
        stream = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": "You are Raznet-Chat with Files Assistant, a helpful tool for answering questions based on the content of uploaded files. Provide direct and accurate answers based on the extracted text."},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            options={
                "temperature": 0.8
            }
        )
        for chunk in stream:
            if chunk["message"]["content"]:
                await msg.stream_token(chunk["message"]["content"])
        await msg.update()