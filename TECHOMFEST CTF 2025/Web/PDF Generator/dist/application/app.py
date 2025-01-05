import os
import re
import subprocess
import fitz
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

LATEX_TEMPLATE = r"""
\documentclass{article}
\begin{document}
%s
\end{document}
"""

# I blocked everything! 
DANGEROUS_COMMANDS = [
    r'openin', r'openout', r'closein', r'closeout', r'include', r'newread', r'newwrite', 
    r'usepackage', r'write', r'write18', r'lstinputlisting', r'url', r'href', r'read', 
    r'readline', r'input', r'def', r'\^', r'catcode', r'immediate', r'csname', r'makeatletter', 
    r'lccode', r'uccode', r'if', r'else'
]

TMP_DIR = "/tmp"

def cleanup_tmp_dir():
    if os.path.exists(TMP_DIR):
        for file in os.listdir(TMP_DIR):
            os.remove(os.path.join(TMP_DIR, file))

def sanitize_input(latex_input):
    if "\n" in latex_input.strip() or any(re.search(cmd, latex_input, flags=re.IGNORECASE) for cmd in DANGEROUS_COMMANDS):
        return True
    return False

def contains_forbidden_strings(pdf_file):
    try:
        doc = fitz.open(pdf_file)
        text = ""
        
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        text = text.lower()
        
        if "tcf{" in text or "5443467b" in text:
            return True
    except Exception as e:
        print(f"Error while reading PDF: {e}")
    
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render_latex():
    try:
        latex_input = request.form.get('input', '').strip()

        if sanitize_input(latex_input):
            return "Error: Input contains forbidden strings / characters", 403

        tex_file = os.path.join(TMP_DIR, "output.tex")
        pdf_file = os.path.join(TMP_DIR, "output.pdf")

        with open(tex_file, "w") as f:
            f.write(LATEX_TEMPLATE % latex_input)

        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", TMP_DIR, tex_file], check=True)

        if contains_forbidden_strings(pdf_file):
            return "Error: PDF contains forbidden strings", 403

        if os.path.exists(pdf_file):
            return send_file(pdf_file, mimetype='application/pdf')

    except subprocess.CalledProcessError:
        return "Error: Failed to compile LaTeX.", 500
    finally:
        cleanup_tmp_dir()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=False)
