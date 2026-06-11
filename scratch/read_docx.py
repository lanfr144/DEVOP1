#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"C:\Users\lanfr144\Documents\DEVOP1\COURS\download\DEVOP1 - Project terms.docx"
output_path = r"c:\Users\lanfr144\Documents\DEVOP1\antigravity\DEVOP1\scratch\document_text.txt"

def read_docx(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
        
    try:
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Namespace for word processing ML
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = []
            for para in root.findall('.//w:p', ns):
                text_elems = para.findall('.//w:t', ns)
                if text_elems:
                    text = "".join([t.text for t in text_elems if t.text])
                    paragraphs.append(text)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for idx, para in enumerate(paragraphs):
                    f.write(f"[{idx}] {para}\n")
            print(f"Dumped {len(paragraphs)} paragraphs to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_docx(docx_path)
