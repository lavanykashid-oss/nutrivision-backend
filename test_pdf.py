import fitz

pdf = "uploads/health_reports/sample.pdf"

doc = fitz.open(pdf)

for i, page in enumerate(doc):
    print(f"\n----- PAGE {i+1} -----\n")
    print(page.get_text())