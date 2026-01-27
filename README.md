# resume

Resume-as-code for Tony Nguyen.

## What’s in here
- `docs/resume.dox` — Doxygen source (generates a nice HTML resume page)
- `docs/resume.md` — Markdown source (easy to edit / diff)
- `scripts/` — build scripts for HTML (Doxygen), DOCX, and PDF

## Quick start

### Build HTML (Doxygen)
```bash
./scripts/build_html.sh
```

Output:
- `build/doxygen/html/index.html`

### Build DOCX
```bash
./scripts/build_docx.sh
```

Output:
- `build/Tony_Nguyen_Resume.docx`

### Build PDF
```bash
./scripts/build_pdf.sh
```

Output:
- `build/Tony_Nguyen_Resume.pdf`

### Build everything
```bash
./scripts/build_all.sh
```
