# Interactive Chatbot for Document Research

This project is an interactive chatbot designed to perform intelligent research across a vast collection of documents. It can identify and extract key themes and provide detailed, cited answers to user questions.

## 🎬 **Demo**

[![Watch the Demo](https://i9.ytimg.com/vi_webp/9j3ZDTtLYZU/mq3.webp?sqp=CISJw8EG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGB4gZSguMA8=&rs=AOn4CLB31SlmQrXGPID_bPCLt0dOSqWi0w)](https://www.youtube.com/watch?v=9j3ZDTtLYZU)

*A brief demonstration of the chatbot's features, including PDF upload, querying, and receiving cited responses.*

---

## 🎯 **Objective**

The primary goal of this project is to create a robust chatbot that can:

* Conduct research across a large set of documents (minimum of 75 PDFs).
* Discern and extract multiple underlying themes from the text.
* Deliver comprehensive and accurately cited responses to user inquiries.

---

## 🧠 **Features**

* **Multi-source PDF Parsing**: Capable of processing text-based, scanned, and mixed-format PDFs.
* **Automatic Document Embedding**: Automatically embeds uploaded documents for analysis.
* **Vector-Based Search**: Utilizes FAISS for efficient and accurate similarity searches.
* **Flexible File Upload**: Supports both drag-and-drop and URL-based file uploads.
* **Web Interface**: A user-friendly web UI powered by Flask.

---

## 🗂️ **Folder Structure**
```
Sourabh-Prajapati-wasserstoff-AiInternTask/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── build_faiss.py
│   │   │   └── pdf_to_text.py
│   │   ├── models/
│   │   │   └── gemini.py
│   │   ├── services/
│   │   │   ├── embedding_monitor.py
│   │   │   ├── processor.py
│   │   │   └── vectorstore.py
│   │   ├── static/
│   │   │   └── style.css
│   │   ├── templates/
│   │   │   └── index.html
│   │   ├── main.py
│   │   └── config.py
│   ├── setup.py
│   ├── Dockerfile
│   └── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```
---

## ⚙️ **Setup and Deployment**

You can run this application either locally or using Docker.

### **Local Setup**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sourabhprajapati22/Sourabh-Prajapati-wasserstoff-AiInternTask.git](https://github.com/sourabhprajapati22/Sourabh-Prajapati-wasserstoff-AiInternTask.git)
    cd Sourabh-Prajapati-wasserstoff-AiInternTask/backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    conda create --prefix venv python=3.11 -y
    conda activate ./venv
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app/main.py
    ```

5.  **Access the application** by navigating to the following URL in your web browser:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

### **🐳 Docker Setup**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sourabhprajapati22/Sourabh-Prajapati-wasserstoff-AiInternTask.git](https://github.com/sourabhprajapati22/Sourabh-Prajapati-wasserstoff-AiInternTask.git)
    cd Sourabh-Prajapati-wasserstoff-AiInternTask/backend
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t chatbot .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run chatbot
    ```

4.  **Access the application** by navigating to the following URL in your web browser:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔧 **Key Modules**

* `pdf_to_text.py`: Extracts text from various PDF types using:
    * `fitz`: For standard text-based PDFs.
    * `pdfplumber`: For PDFs with structured layouts.
    * `paddleocr`: For scanned or image-based PDFs.

* `build_faiss.py`: Encodes the extracted text into vector embeddings and stores them in a FAISS index for efficient searching.

* `vectorstore.py`: Manages document embedding, indexing, and retrieval operations.

* `main.py`: A Flask-based web server that handles file uploads (including drag & drop) and orchestrates the automatic embedding process.

---

## 📄 **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.
