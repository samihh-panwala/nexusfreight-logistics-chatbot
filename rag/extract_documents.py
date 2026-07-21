import os
import fitz

DOCUMENT_FOLDER = "documents"

pdf_files = [f for f in os.listdir(DOCUMENT_FOLDER) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("No PDF files found.")
    exit()

for file in pdf_files:

    pdf_path = os.path.join(DOCUMENT_FOLDER, file)

    try:

        pdf = fitz.open(pdf_path)

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        txt_filename = os.path.splitext(file)[0] + ".txt"
        txt_path = os.path.join(DOCUMENT_FOLDER, txt_filename)

        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        print(f"✓ Converted: {file}")

    except Exception as e:
        print(f"✗ Failed: {file}")
        print(e)

print("\nAll PDF conversion completed.")