#!/usr/bin/env python3
"""
Generate a clean PDF from docs/resume.md (headings + bullets + paragraphs).
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "resume.md"
OUTDIR = ROOT / "build"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUT = OUTDIR / "Tony_Nguyen_Resume.pdf"

LEFT = 0.75 * inch
RIGHT = 0.75 * inch
TOP = 0.75 * inch
BOTTOM = 0.75 * inch

H1, H2, H3, BODY = 16, 12, 11, 10
LEADING = 13

def wrap_draw(c, text, x, y, maxw, font, size):
    c.setFont(font, size)
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, font, size) <= maxw:
            line = test
        else:
            c.drawString(x, y, line)
            y -= LEADING
            line = w
    if line:
        c.drawString(x, y, line)
        y -= LEADING
    return y

def main():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    c = canvas.Canvas(str(OUT), pagesize=letter)
    width, height = letter
    maxw = width - LEFT - RIGHT
    y = height - TOP

    for raw in lines:
        line = raw.rstrip()
        if not line:
            y -= 6
            continue
        if y < BOTTOM + 2*LEADING:
            c.showPage()
            y = height - TOP

        if line.startswith("# "):
            y = wrap_draw(c, line[2:].strip(), LEFT, y, maxw, "Helvetica-Bold", H1)
            y -= 4
            continue
        if line.startswith("## "):
            y = wrap_draw(c, line[3:].strip(), LEFT, y, maxw, "Helvetica-Bold", H2)
            y -= 2
            continue
        if line.startswith("### ") or line.startswith("#### "):
            txt = line.split(" ",1)[1].strip()
            y = wrap_draw(c, txt, LEFT, y, maxw, "Helvetica-Bold", H3)
            continue

        if line.lstrip().startswith("- "):
            txt = line.strip()[2:].strip()
            c.setFont("Helvetica", BODY)
            c.drawString(LEFT, y, u"\u2022")
            y = wrap_draw(c, txt, LEFT + 12, y, maxw - 12, "Helvetica", BODY)
            continue

        y = wrap_draw(c, line, LEFT, y, maxw, "Helvetica", BODY)

    c.save()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
