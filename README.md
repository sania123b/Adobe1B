# 🧠 Adobe 1B - Persona-Driven Document Intelligence

This solution automatically analyzes PDF documents and extracts the most relevant sections and sub-sections based on a user persona and their job-to-be-done. It combines structural and semantic analysis using lightweight NLP models.

---

## 📁 Folder Structure

ADOBE1B/
├── input/
│ ├── *.pdf # Collection of related documents
│ ├── Persona.txt # Persona description
│ ├── job_to_be_done.txt # Task to be done
│ └── input.json # (Auto-generated) structured config
│
├── output/
│ └── output.json # Final extracted and ranked output
│
├── src/
│ └── main.py # Core processing script
│
├── requirements.txt # Python dependencies
├── dockerfile # Docker configuration
├── .dockerignore
└── README.md # You're here!


Build an intelligent document analyst that extracts and ranks the most **relevant sections** based on:
- 👤 A **Persona** (e.g., student, researcher, analyst)
- 🎯 A **Job to be Done** (task the persona must accomplish)
- 📚 A set of **PDF documents**

---

## ⚙️ Dependencies

Listed in `requirements.txt`:
```txt
transformers==4.40.1
sentence-transformers==2.2.2
scikit-learn
PyMuPDF==1.23.22



⛔ Constraints
✅ CPU-only

✅ Model < 1GB (MiniLM)

✅ Runtime < 60 seconds for 3–5 PDFs

❌ No internet access inside container




Total Size Summary (Model & Runtime)

| Component               | Approx Size |
| ----------------------- | ----------- |
| MiniLM-L6-v2 Model      | 85 MB       |
| Scikit-learn Classifier | \~2 MB      |
| OCR (Tesseract + data)  | \~50 MB     |
| PyTorch Runtime         | \~300 MB    |
| **Total**               | \~437 MB    |

RUN:
1)docker build -t adobe-b .
2)docker run --rm -v "${PWD}:/app" -w /app/src adobe1b python main.py

