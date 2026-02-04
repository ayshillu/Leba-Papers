
import sys
import PyPDF2

def extract_text(pdf_path, output_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(text)
        print(f"Successfully wrote content to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_path = r"c:\Users\ijasa\OneDrive\Desktop\archivebox\LEBA_Papers_Content_Reference_for_Antigravity.pdf"
    output_path = r"c:\Users\ijasa\OneDrive\Desktop\archivebox\pdf_content.txt"
    extract_text(pdf_path, output_path)
