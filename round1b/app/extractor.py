import os
import json
import fitz  # PyMuPDF
from datetime import datetime

INPUT_JSON = "/app/input/persona.json"
OUTPUT_JSON = "/app/output/output.json"

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        text = doc.load_page(page_num).get_text()
        pages.append({
            "page": page_num + 1,
            "text": text
        })
    return pages

def keyword_match_score(text, keywords):
    return sum(text.lower().count(k.lower()) for k in keywords)

def get_top_sections(pdf_path, keywords, max_sections=5):
    doc = fitz.open(pdf_path)
    sections = []
    seen = set()

    for page_num, page in enumerate(doc):
        text = page.get_text()
        lines = text.split("\n")
        for i, line in enumerate(lines):
            clean_line = line.strip()
            if not clean_line or clean_line in seen:
                continue
            score = keyword_match_score(clean_line, keywords)
            if score > 0:
                sections.append({
                    "document": os.path.basename(pdf_path),
                    "page": page_num + 1,
                    "section_title": clean_line[:100],
                    "importance_rank": score
                })
                seen.add(clean_line)
    sections.sort(key=lambda x: -x["importance_rank"])
    return sections[:max_sections]

def extract_subsection_highlights(sections, pdf_lookup):
    highlights = []
    for s in sections:
        path = pdf_lookup.get(s["document"])
        if not path:
            continue
        doc = fitz.open(path)
        text = doc.load_page(s["page"] - 1).get_text()
        snippet = text.strip()[:500]
        highlights.append({
            "document": s["document"],
            "page": s["page"],
            "refined_text": snippet
        })
    return highlights

def main():
    # Load input JSON
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = data.get("documents", [])
    persona = data.get("persona", {})
    job = data.get("job_to_be_done", {})

    persona_role = persona.get("role", "")
    job_task = job.get("task", "")
    keywords = persona_role.split() + job_task.split()

    input_dir = "/app/input"
    pdf_lookup = {doc["filename"]: os.path.join(input_dir, doc["filename"]) for doc in documents}

    all_sections = []
    for doc in documents:
        pdf_path = pdf_lookup[doc["filename"]]
        top_sections = get_top_sections(pdf_path, keywords)
        all_sections.extend(top_sections)

    top_ranked = sorted(all_sections, key=lambda x: -x["importance_rank"])[:5]
    highlights = extract_subsection_highlights(top_ranked, pdf_lookup)

    output = {
        "metadata": {
            "documents": [doc["filename"] for doc in documents],
            "persona": persona_role,
            "job": job_task,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": top_ranked,
        "subsection_analysis": highlights
    }

    os.makedirs("/app/output", exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("✅ Extractor completed. Output saved to /app/output/output.json")

if __name__ == "__main__":
    main()
