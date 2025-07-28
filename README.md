# 📘 Adobe Hackathon Round 2 – Persona-Driven Document Intelligence

## 🚀 Challenge Overview

In Round 2 of Adobe’s “Connecting the Dots” Hackathon, the goal is to build an intelligent document analyst that **extracts and prioritizes the most relevant sections from a collection of PDFs**, based on a given **persona** and a **job-to-be-done**.

This round builds on top of Round 1 by introducing **semantic understanding**, **section ranking**, and **contextual refinement**.

---

## 💡 What This Project Does

Given:
- A set of PDFs (`/input/*.pdf`)
- A persona file (`persona.txt`)
- A task file (`job_to_be_done.txt`)

The system:
1. Extracts blocks of text using PyMuPDF
2. Scores blocks using a combination of:
   - Font size and position (structure-based)
   - Semantic similarity to persona/task (transformer-based)
3. Selects the **most relevant section** from each document
4. Gathers nearby context and refines it
5. Outputs a JSON file with:
   - Extracted Sections (title, page, rank)
   - Refined Subsections (text, page, document)

---

## 🧠 Model and Libraries Used

| Component             | Description                                      |
|----------------------|--------------------------------------------------|
| `fitz` (PyMuPDF)      | PDF parsing and layout extraction               |
| `sentence-transformers` | Semantic similarity scoring (MiniLM-L6-v2)     |
| `langdetect` (optional) | For language-aware extensions (if needed)     |
| `re`, `datetime`, `json` | Standard preprocessing and formatting         |

Transformer Model Used: `all-MiniLM-L6-v2` (approx. 90MB) ✅

---

## 🏗 Directory Structure

```
.
├── input/
│   ├── file1.pdf
│   ├── file2.pdf
│   ├── persona.txt
│   ├── job_to_be_done.txt
│   └── input.json (auto-generated if missing)
├── output/
│   └── output.json (final result)
├── src/
│   └── main.py (this script)
├── Dockerfile
└── README.md
```

---

## 📦 How to Build and Run (Dockerized)

### 🔨 Build Docker Image

```bash
docker build --platform linux/amd64 -t adobe-pdf-agent .
```

### ▶️ Run Container

```bash
docker run --rm   -v $(pwd)/input:/app/input   -v $(pwd)/output:/app/output   --network none   adobe-pdf-agent
```

⏱ **Processing Time:** < 10 seconds for 3–5 PDFs

---

## 🧾 Output Format (output/output.json)

```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "Research Analyst",
    "job_to_be_done": "Analyze R&D investment trends",
    "processing_timestamp": "2025-07-27T15:44:32"
  },
  "extracted_sections": [
    {
      "document": "file1.pdf",
      "section_title": "R&D Investment Overview",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "file1.pdf",
      "refined_text": "R&D spending has increased by 23%...",
      "page_number": 3
    }
  ]
}
```

---

## 🧪 Example Scenario

**Persona:** PhD Scholar in Environmental Science  
**Task:** Summarize key findings related to climate change in 3 UN reports.

→ The model ranks and extracts top headings like _"Climate Impact Summary"_ and refines paragraphs following the heading for context. Final JSON is ready for visualization or embedding in a reading experience.

---

## 📌 Constraints Followed

| Constraint              | ✅ Status           |
|-------------------------|--------------------|
| CPU-only (AMD64)        | ✅ Fully compatible |
| Max model size < 1GB    | ✅ Model = ~90MB    |
| No Internet Calls       | ✅ Offline mode     |
| Execution < 60s         | ✅ Runs < 10s       |

---

## 📎 Notes

- The entire logic is implemented in a single `main.py` script for simplicity.
- Works on any domain of documents: research, education, finance, etc.
- You can manually edit `persona.txt` and `job_to_be_done.txt` in the `input/` folder to test custom cases.

---

## 📍 License

MIT License. Built as part of Adobe India Hackathon 2025 (Round 2).
