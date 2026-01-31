# resume optimizer

Resume-as-code.

## What’s in here
- `docs/resume.md` — **Edit this file** to update your resume (Markdown format, easy to edit/diff)
- `docs/resume.dox` — Auto-generated from `resume.md` (used for HTML generation, do not edit manually)
- `scripts/` — build scripts for HTML (Doxygen), DOCX, and PDF

## Updating Your Resume

**Only edit `docs/resume.md`** — this is your single source of truth. The `resume.dox` file is automatically generated from the markdown file when you run the build scripts.

1. Edit `docs/resume.md` with your changes
2. Run `./scripts/build_all.sh` to regenerate all outputs (HTML, DOCX, PDF)

The build process will automatically:
- Convert `resume.md` → `resume.dox` (for HTML generation)
- Generate HTML from the Doxygen file
- Generate DOCX and PDF from the markdown file

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
- `build/{name}_Resume.docx` (name configured in `config/resume_config.yaml`)

### Build PDF
```bash
./scripts/build_pdf.sh
```

Output:
- `build/{name}_Resume.pdf` (name configured in `config/resume_config.yaml`)

### Build everything
```bash
./scripts/build_all.sh
```

## AI-Powered Resume Optimization

Optimize your resume for specific job postings using AI. The tool analyzes job descriptions and tailors your resume to maximize impact with recruiters and ATS systems.

### FREE AI Providers Available

The tool supports multiple AI providers, including several **FREE options**:

1. **Ollama** (100% FREE, runs locally) ⭐ Recommended
   - Install: https://ollama.ai
   - No API key needed
   - Runs completely offline
   - Models: llama3.2, mistral, etc.

2. **Google Gemini** (FREE tier)
   - Get API key: https://makersuite.google.com/app/apikey
   - Generous free tier
   - **Rate limit:** The script retries up to 3 times with backoff. If you still hit limits, switch to Ollama or Groq.

3. **Groq** (FREE tier, very fast)
   - Get API key: https://console.groq.com/keys
   - Extremely fast responses
   - Install: `pip install groq`

4. **Hugging Face** (FREE tier)
   - Get API key: https://huggingface.co/settings/tokens
   - Open source models

5. **OpenAI** (Paid, but high quality)
   - Get API key: https://platform.openai.com/api-keys
   - Best quality, but requires payment
   - Install: `pip install openai`

### Setup

1. Install dependencies (required before first use):
```bash
pip install -r requirements.txt
```

   Or if you prefer using a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

2. Configure your AI provider:

   **Option A: Use Ollama (FREE, recommended)**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.2
   
   # Edit config/resume_config.yaml and set:
   # provider: "ollama"
   ```

   **Option B: Use a free API provider**
   ```bash
   cp config/secrets.yaml.example config/secrets.yaml
   # Edit config/secrets.yaml and add your API key (gemini_api_key, groq_api_key, etc.)
   # Edit config/resume_config.yaml and set provider to: "gemini", "groq", or "huggingface"
   ```
   
   The `config/secrets.yaml` file is gitignored for security, so your API keys won't be committed.

### Rate limit (e.g. "GEMINI API Rate Limit Exceeded")

- **Automatic retries:** Gemini requests are retried up to 3 times with 30s, 60s, 120s delays.
- **Switch provider:** In `config/resume_config.yaml` set `provider: "ollama"` (no limits) or `provider: "groq"` (higher free limits).
- **Ollama:** No rate limits; runs locally. Install from https://ollama.ai and run `ollama pull llama3.2`.

3. Customize configuration (optional):
   - Edit `config/resume_config.yaml` to adjust:
     - Your name (for file naming)
     - Output file patterns
     - AI prompts and model settings

### Usage

```bash
./scripts/optimize_resume.sh <job_description_url> [--company COMPANY]
```

Examples:
```bash
# Basic usage
./scripts/optimize_resume.sh https://example.com/jobs/software-engineer

# With company name (for better file organization)
./scripts/optimize_resume.sh https://example.com/jobs/software-engineer --company "Google"
```

### Outputs

The script generates:
- **Optimized Resume** (`build/optimized/resume_optimized_YYYYMMDD_HHMMSS.md`) - Tailored resume for the job posting
- **Cover Letter** (`build/optimized/cover_letter_YYYYMMDD_HHMMSS.md`) - 2-3 paragraph cover letter
- **Changelog** (`CHANGELOG.md`) - List of changes made to the resume

### Building Optimized Resume Outputs

After generating an optimized resume, you can build DOCX, PDF, and HTML outputs:

```bash
python scripts/build_optimized.py <optimized_resume.md> [--company COMPANY]
```

Example:
```bash
python scripts/build_optimized.py build/optimized/resume_optimized_20250128_120000.md --company "Google"
```

This generates:
- `build/{name}_Resume_{company}_{timestamp}.docx`
- `build/{name}_Resume_{company}_{timestamp}.pdf`
- `docs/resume.dox` (updated for HTML generation)

**Note:** The `build_all.sh` script builds outputs from the **baseline** resume (`docs/resume.md`), not optimized versions. Use `build_optimized.py` for optimized resumes.

### Promoting Optimized Resume to Baseline

If you want to make an optimized resume your new baseline (e.g., after incorporating feedback):

```bash
python scripts/promote_to_baseline.py <optimized_resume.md> [--reason REASON]
```

Example:
```bash
python scripts/promote_to_baseline.py build/optimized/resume_optimized_20250128_120000.md --reason "Incorporated feedback from Google application"
```

This will:
1. Back up the current baseline to `build/backups/resume_backup_{timestamp}.md`
2. Replace `docs/resume.md` with the optimized version
3. Update `CHANGELOG.md` with promotion details
4. Regenerate all baseline outputs (DOCX, PDF, DOX)

### Configuration

Edit `config/resume_config.yaml` to customize:
- **Name**: Used in output file names
- **Output Patterns**: File naming conventions for baseline and optimized resumes
- **AI Prompts**: Optimization strategy, cover letter style, changelog format
- **Model Settings**: AI model selection, temperature, token limits

### File Organization

```
resume/
├── docs/
│   ├── resume.md          # Baseline resume (source of truth)
│   └── resume.dox          # Generated Doxygen file
├── build/
│   ├── {name}_Resume.docx  # Baseline DOCX
│   ├── {name}_Resume.pdf   # Baseline PDF
│   ├── optimized/          # AI-optimized resumes
│   │   ├── resume_optimized_*.md
│   │   └── cover_letter_*.md
│   └── backups/            # Backups when promoting to baseline
├── config/
│   └── resume_config.yaml  # Configuration file
└── CHANGELOG.md            # Optimization history
```

### GitHub Workflow Recommendations

**Saving AI-Generated Versions:**

Yes, you should save optimized resumes! They're valuable for:
- Tracking what optimizations worked
- Comparing different versions
- Building a portfolio of tailored resumes

**Git Branching Strategy:**

Consider creating branches for each company/application:

```bash
# Create a branch for a specific company
git checkout -b optimize/google-swe-2025

# After optimization
git add build/optimized/ CHANGELOG.md
git commit -m "Optimize resume for Google SWE position"

# Tag the branch for easy reference
git tag -a google-swe-2025 -m "Resume optimized for Google SWE application"

# Push branch and tag
git push origin optimize/google-swe-2025
git push origin google-swe-2025
```

**Alternative: Keep optimized versions local**

If you prefer not to commit optimized versions:
- Add `build/optimized/` to `.gitignore`
- Only commit when promoting to baseline
- Use tags on main/master branch for baseline versions

The `build/optimized/` directory is already in `.gitignore` via the `build/` pattern, so optimized resumes won't be committed unless you explicitly add them.
