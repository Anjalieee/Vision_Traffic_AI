def extract_resume_text(file_path):
    import os
    from docx import Document
    import PyPDF2

    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"

        elif ext == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        print(f"⚠️ Could not read {file_path}: {e}")

    return text
