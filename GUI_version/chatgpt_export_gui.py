from datetime import datetime, timezone
from pathlib import Path
import json
from docx import Document
import re

__version__ = "1.0.0"

# Define paths
input_path = "conversations.json"  # <-- Adjust if needed
output_dir = Path("chatgpt_export_reader_output")
output_dir.mkdir(exist_ok=True)

# Load the exported JSON file
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Handle both list and dict formats
conversations = data if isinstance(data, list) else data.get("conversations", [])

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

def extract_ordered_messages(mapping):
    root_id = next((k for k, v in mapping.items() if v.get("parent") is None), None)
    if not root_id:
        return []

    ordered = []
    current_id = mapping[root_id]["children"][0] if mapping[root_id]["children"] else None

    while current_id:
        node = mapping[current_id]
        message = node.get("message")
        if message:
            role = message["author"]["role"]
            parts = message["content"].get("parts", [])
            # Convert all parts to string in case of dicts
            content = "\n".join(str(p) if isinstance(p, str) else json.dumps(p, ensure_ascii=False) for p in parts).strip()
            if content:
                ordered.append((role, content))
        children = node.get("children", [])
        current_id = children[0] if children else None

    return ordered

def save_as_markdown(messages, title, created, filepath):
    output = f"# {title}\n\nCreated: {created}\n\n"
    for role, content in messages:
        output += f"**{role.upper()}**:\n{content}\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)

def save_as_docx(messages, title, created, filepath):
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(f"Created: {created}")
    doc.add_paragraph("")
    for role, content in messages:
        doc.add_paragraph(f"{role.upper()}:", style='Heading3')
        doc.add_paragraph(content)
        doc.add_paragraph("")
    doc.save(filepath)

# Process each conversation
for convo in conversations:
    raw_title = convo.get("title", "Untitled").strip()
    title = sanitize_filename(raw_title.replace(" ", "_"))[:50]
    created = datetime.fromtimestamp(convo.get("create_time", 0), timezone.utc).strftime("%Y-%m-%d")
    filename_base = f"{created}_{title}"
    messages = extract_ordered_messages(convo["mapping"])
    if not messages:
        continue

    # Save as markdown
    md_path = output_dir / f"{filename_base}.md"
    save_as_markdown(messages, raw_title, created, md_path)

    # Save as docx
    docx_path = output_dir / f"{filename_base}.docx"
    save_as_docx(messages, raw_title, created, docx_path)

print(f"✅ Extracted {len(conversations)} conversations into '{output_dir}'")
