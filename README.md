# ChatGPT Export Reader

🧠 A simple, powerful Python script to convert your exported ChatGPT chat history into clean, readable `.md` and `.docx` files — perfect for writers, researchers, and anyone who wants to preserve or reuse conversations.

---

## ✅ Features

- Parses your `conversations.json` file from a ChatGPT data export
- Reconstructs each chat in proper message order
- Outputs both:
  - 📄 Markdown files (`.md`) — great for Obsidian or version control
  - 📝 Word documents (`.docx`) — open in Google Docs or MS Word
- Cleans up filenames automatically (no OS errors)
- Handles large JSON exports from OpenAI

---

## 📦 Requirements

- Python 3.8+
- Install dependencies with:

```bash
pip install python-docx
```

---

## 🚀 How to Use

1. Download your data from https://chat.openai.com/settings > **Export Data**
2. Extract the ZIP file and locate `conversations.json`
3. Place it in the same folder as this script
4. Run the script:

```bash
python chatgpt_export_reader.py
```

5. Output files will be in the `chatgpt_export_reader_output/` folder.

---

## 🔒 Safe by Default

Your `conversations.json` and output folder are `.gitignore`d automatically so you don't accidentally commit personal data.

---

## 🛠 Roadmap

- [ ] Add GUI (Tkinter)
- [ ] Summarize each chat
- [ ] Export as PDF
- [ ] Make a custom GPT that uses this data

---

## 🧠 Made by [Matt Collman](https://github.com/Matt-Collman)

