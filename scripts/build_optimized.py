#!/usr/bin/env python3
"""
Build optimized resume outputs (DOCX, PDF, DOX) from an optimized markdown file.

Usage:
    python scripts/build_optimized.py <optimized_resume.md> [--company COMPANY]
    
Example:
    python scripts/build_optimized.py build/optimized/resume_optimized_20250128_120000.md --company "Google"
"""
import sys
import argparse
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from datetime import datetime
from config_loader import get_path, get_output_filename

def build_from_markdown(source_md, company=None):
    """
    Build DOCX, PDF, and DOX from a markdown resume file.
    
    Args:
        source_md: Path to the markdown resume file
        company: Optional company name for output file naming
    """
    source_md = Path(source_md).resolve()
    if not source_md.exists():
        raise FileNotFoundError(f"Resume file not found: {source_md}")
    
    # Temporarily replace the source resume
    original_resume = get_path('resume_source')
    backup_resume = original_resume.with_suffix('.md.backup')
    
    try:
        # Backup original and use optimized version
        if original_resume.exists():
            backup_resume.write_text(original_resume.read_text(encoding='utf-8'), encoding='utf-8')
        
        # Copy optimized resume to source location temporarily
        optimized_content = source_md.read_text(encoding='utf-8')
        original_resume.write_text(optimized_content, encoding='utf-8')
        
        # Build outputs using subprocess to run build scripts
        print(f"📄 Building outputs from: {source_md}")
        
        scripts_dir = Path(__file__).parent
        
        # Build DOX
        print("  → Generating DOX...")
        subprocess.run([sys.executable, str(scripts_dir / "md_to_dox.py")], check=True)
        
        # Build DOCX
        print("  → Generating DOCX...")
        subprocess.run([sys.executable, str(scripts_dir / "build_docx.py")], check=True)
        
        # Build PDF
        print("  → Generating PDF...")
        subprocess.run([sys.executable, str(scripts_dir / "build_pdf.py")], check=True)
        
        # Rename outputs based on whether company is provided
        build_dir = get_path('build_dir')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Rename DOCX
        baseline_docx = build_dir / get_output_filename('baseline_docx')
        if baseline_docx.exists():
            if company:
                optimized_docx = build_dir / get_output_filename('optimized_docx', company=company, timestamp=timestamp)
            else:
                optimized_docx = build_dir / get_output_filename('optimized_docx_fallback', timestamp=timestamp)
            baseline_docx.rename(optimized_docx)
            print(f"  ✓ DOCX: {optimized_docx}")
        
        # Rename PDF
        baseline_pdf = build_dir / get_output_filename('baseline_pdf')
        if baseline_pdf.exists():
            if company:
                optimized_pdf = build_dir / get_output_filename('optimized_pdf', company=company, timestamp=timestamp)
            else:
                optimized_pdf = build_dir / get_output_filename('optimized_pdf_fallback', timestamp=timestamp)
            baseline_pdf.rename(optimized_pdf)
            print(f"  ✓ PDF: {optimized_pdf}")
        
    finally:
        # Restore original resume
        if backup_resume.exists():
            original_resume.write_text(backup_resume.read_text(encoding='utf-8'), encoding='utf-8')
            backup_resume.unlink()

def main():
    parser = argparse.ArgumentParser(description='Build optimized resume outputs')
    parser.add_argument('resume_md', help='Path to optimized resume markdown file')
    parser.add_argument('--company', '-c', help='Company name (for output file naming)', default=None)
    
    args = parser.parse_args()
    
    try:
        build_from_markdown(args.resume_md, args.company)
        print("\n✅ Build complete!")
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
