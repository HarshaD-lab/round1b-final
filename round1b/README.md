# Round 1B – Intelligent Section Extractor 🚀

## 🔹 Project Summary
You're handed a stack of PDFs and a mission from a **persona** with a **job to be done**.

This extractor reads all PDFs, understands what the user wants (from `persona.json`), and finds the most **relevant**, **insightful**, and **important** sections across all documents. It then:
- Ranks these sections by relevance 🔍
- Grabs the most meaningful snippets from the pages ✂️
- Outputs a clean, structured JSON for decision-making 📊

Perfect for AI assistants that help users make sense of large document sets intelligently.

---

## 🔹 Input
📁 `/app/input/` contains:
- `persona.json`: Describes the user's role and task (e.g., "Travel Planner", "Plan a trip of 4 days...")
- Multiple PDF files related to the challenge

---

## 🔹 Output
📁 `/app/output/` will contain:
- `output.json` with:
  - ✅ `metadata`: documents, role, task, timestamp
  - ✅ `extracted_sections`: Top 5 ranked matches from all PDFs
  - ✅ `subsection_analysis`: Refined content (snippets) from those pages

---

## 🔹 Tech Stack
- 🐍 Python 3.10
- 📚 PyMuPDF (for reading PDFs)
- 🐳 Docker (for isolated, reproducible runs)

---

## 🔹 How It Works
1. Reads all input PDFs and persona/task data
2. Extracts headings or significant lines
3. Scores each line using persona + task keywords
4. Ranks sections based on relevance
5. Pulls highlighted text from best-matching pages
6. Saves everything to `output.json`

---

## 🔹 How to Run

```bash
docker build -t pdf-outline-extractor:latest .
docker run --rm ^
  -v "%cd%/app/input":/app/input ^
  -v "%cd%/app/output":/app/output ^
  --network none pdf-outline-extractor:latest
