import fitz  # PyMuPDF
import json
import re
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# === Config ===
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON_PATH = BASE_DIR / "input" / "input.json"
INPUT_PDF_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []
    all_sizes = []

    for page_number, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    blocks.append({
                        "text": text,
                        "font_size": span["size"],
                        "font": span["font"],
                        "bbox": span["bbox"],
                        "page": page_number,
                    })
                    all_sizes.append(span["size"])
    return blocks, all_sizes

def score_block(block, min_size, max_size):
    size_score = (block["font_size"] - min_size) / (max_size - min_size + 1e-5)
    score = size_score
    if "Bold" in block["font"]:
        score += 0.5
    if block["text"].isupper():
        score += 0.3
    if block["bbox"][1] < 100:
        score += 0.3
    return score

def refine_context(top_block, all_blocks):
    page_blocks = [b for b in all_blocks if b["page"] == top_block["page"]]
    context_blocks = []

    for b in page_blocks:
        if (
            b["bbox"][1] > top_block["bbox"][1]
            and b["bbox"][1] < top_block["bbox"][1] + 250
        ):
            context_blocks.append(b["text"])

    if context_blocks:
        return top_block["text"] + " " + " ".join(context_blocks)
    return top_block["text"]

def clean_refined_text(text):
    text = text.replace("\n", " ").replace("\u2022", " ")
    # Remove any remaining non-printable/control chars:
    text = re.sub(r'[^\x20-\x7E]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_pdf(pdf_file, persona, job_task):
    blocks, sizes = extract_blocks(pdf_file)
    if not sizes:
        print(f"⚠️ Empty PDF: {pdf_file.name}")
        return []

    min_size, max_size = min(sizes), max(sizes)

    for b in blocks:
        b["structure_score"] = score_block(b, min_size, max_size)

    query = f"{persona} {job_task}"
    query_embedding = embedding_model.encode(query)
    block_embeddings = embedding_model.encode([b["text"] for b in blocks])
    similarities = util.cos_sim(query_embedding, block_embeddings)[0]

    for idx, b in enumerate(blocks):
        b["semantic_score"] = similarities[idx].item()
        b["total_score"] = b["structure_score"] + b["semantic_score"]

    top_block = sorted(blocks, key=lambda x: -x["total_score"])[0]
    refined = refine_context(top_block, blocks)
    refined_clean = clean_refined_text(refined)

    return [{
        "document": pdf_file.name,
        "section_title": top_block["text"],
        "importance_rank": 1,
        "page_number": top_block["page"],
        "refined_text": refined_clean
    }]

def main():
    if not INPUT_JSON_PATH.exists():
        print(f"❌ {INPUT_JSON_PATH} not found")
        return

    with open(INPUT_JSON_PATH) as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"]
    job_task = input_data["job_to_be_done"]["task"]

    output_data = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in input_data["documents"]],
            "persona": persona,
            "job_to_be_done": job_task,
            "processing_timestamp": datetime.now().isoformat(),
        },
        "extracted_sections": [],
        "subsection_analysis": [],
    }

    global_rank = 1

    for doc in input_data["documents"]:
        pdf_file = INPUT_PDF_DIR / doc["filename"]
        if not pdf_file.exists():
            print(f"⚠️ Missing file: {pdf_file.name}")
            continue

        best = process_pdf(pdf_file, persona, job_task)
        for s in best:
            output_data["extracted_sections"].append({
                "document": s["document"],
                "section_title": s["section_title"],
                "importance_rank": global_rank,
                "page_number": s["page_number"]
            })
            output_data["subsection_analysis"].append({
                "document": s["document"],
                "refined_text": s["refined_text"],
                "page_number": s["page_number"]
            })
            global_rank += 1

    output_file = OUTPUT_DIR / "output.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Saved: {output_file}")

if __name__ == "__main__":
    main()
