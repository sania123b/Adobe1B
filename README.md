# 🧠 Adobe Hackathon 2025 - Round 2  
### 📚 Persona-Driven PDF Intelligence Extractor

This project is part of **Round 2 of Adobe India's Hackathon 2025**, under the theme: **“Connecting the Dots Through Docs”**.  
It builds an intelligent PDF understanding system that extracts and prioritizes key sections based on a specific **persona** and a **job-to-be-done**.

---

## 🚀 Features

- 📥 Accepts 3–10 related PDFs + Persona + Job-to-be-done.
- 🧠 Uses **Sentence Transformers** for semantic scoring.
- 🔠 Integrates **font styles, position, and size** for structural scoring.
- 🤖 Selects top-ranked sections with local **subsection context**.
- 📝 Produces a **standardized JSON output** with:
  - Metadata
  - Ranked extracted sections
  - Subsection-level summaries
- ✅ Works **offline** with **CPU-only** inference.
- 🐳 Dockerized and compatible with AMD64 platform.

---

## 📁 Input/Output Structure

### 📂 Input Directory (`input/`)
- `*.pdf` – One or more PDF documents (3–10 files).
- `persona.txt` – The role (e.g., "PhD Researcher in Biomedicine").
- `job_to_be_done.txt` – The task (e.g., "Perform literature review on X").

### 📤 Output: `output/output.json`

```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "PhD Researcher in Biomedicine",
    "job_to_be_done": "Literature review on GNNs",
    "processing_timestamp": "2025-07-28T10:32:01"
  },
  "extracted_sections": [
    {
      "document": "file1.pdf",
      "section_title": "Graph Attention Networks",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "file1.pdf",
      "refined_text": "Graph Attention Networks (GATs) allow node representation...",
      "page_number": 3
    }
  ]
}
```

---

## 🐳 Docker Instructions

### 1️⃣ Build Docker Image
```bash
docker build -t adobe1b-app .
```

### 2️⃣ Run Docker Container
```bash
docker run --rm -v "${PWD}:/app" -w /app/src adobe1b python main.py
```

---

## ⚙ How It Works

1. **Input Parsing:**  
   Reads all PDFs from `/input`, along with `persona.txt` and `job_to_be_done.txt`.  
   Auto-generates `input.json` if not provided.

2. **Block Extraction:**  
   Parses all visible text from each page using `PyMuPDF`.  
   Each block is scored structurally (font size, bold, uppercase, position).

3. **Semantic Scoring:**  
   Uses `SentenceTransformers` (MiniLM) to score semantic relevance between each block and the combined persona/task.

4. **Total Score:**  
   Combined structure + semantic score = final relevance.  
   Top-ranked block is chosen and enhanced with local context.

5. **JSON Output:**  
   - Extracted top section(s)
   - Subsection summaries
   - Metadata and page references

---

## 🛠️ Tech Stack

| Component        | Tool / Library                        |
|------------------|----------------------------------------|
| 🐍 Language       | Python 3.12                            |
| 📄 PDF Parsing    | PyMuPDF (`fitz`)                      |
| 🧠 Semantic Model | `sentence-transformers/all-MiniLM-L6-v2` |
| 📦 Embedding      | `torch`, `transformers`               |
| 🐳 Container      | Docker (AMD64)                        |

---

## ⚙ Constraints Satisfied

| Constraint           | Status              |
|----------------------|---------------------|
| ⏱ Runtime            | ✅ < 60 seconds     |
| 🧠 Model Size         | ✅ < 1 GB (170MB)   |
| 📶 Internet Required  | ✅ No               |
| 🖥 CPU Architecture   | ✅ AMD64 Compatible |
| 📤 Output Format      | ✅ Valid JSON       |

---

## 🧪 Sample Use Case

**Persona:** Investment Analyst  
**Job to be done:** "Compare R&D investments across Apple, Google, Amazon"  
**Input:** 2022–2024 annual reports of tech companies  
**Output:** Key sections highlighting R&D trends + refined analysis

---

## 📜 License

MIT License — free to use, modify, and distribute with attribution.

---

## 🙌 Authors

Built by [@Pavanid2325](https://github.com/Pavanid2325), [@sania123b](https://github.com/sania123b), [@nithya996](https://github.com/nithya996) for Adobe Hackathon 2025.

---

## ✨ Ready to Run?

```bash
docker build -t adobe1b-app .
docker run --rm -v "${PWD}:/app" -w /app/src adobe1b python main.py
```

Let your PDFs think like humans — and deliver **contextual, ranked insights** that match the reader’s intent.
