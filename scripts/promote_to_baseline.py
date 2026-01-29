#!/usr/bin/env python3
"""
Promote an optimized resume to be the new baseline resume.

This script:
1. Backs up the current baseline resume
2. Replaces it with the optimized version
3. Updates the changelog with promotion information
4. Regenerates all baseline outputs (DOCX, PDF, DOX)

Usage:
    python scripts/promote_to_baseline.py <optimized_resume.md> [--reason REASON]
    
Example:
    python scripts/promote_to_baseline.py build/optimized/resume_optimized_20250128_120000.md --reason "Incorporated feedback from Google application"
"""
import sys
import argparse
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from datetime import datetime
from config_loader import get_path

def promote_to_baseline(optimized_resume_path, reason=None):
    """
    Promote an optimized resume to be the new baseline.
    
    Args:
        optimized_resume_path: Path to the optimized resume markdown file
        reason: Optional reason for the promotion (for changelog)
    """
    optimized_resume_path = Path(optimized_resume_path).resolve()
    if not optimized_resume_path.exists():
        raise FileNotFoundError(f"Optimized resume file not found: {optimized_resume_path}")
    
    baseline_resume = get_path('resume_source')
    changelog_file = get_path('changelog')
    
    # Create backup directory
    backup_dir = get_path('build_dir') / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f"resume_backup_{timestamp}.md"
    
    try:
        # Backup current baseline
        if baseline_resume.exists():
            print(f"📦 Backing up current baseline to: {backup_file}")
            backup_file.write_text(baseline_resume.read_text(encoding='utf-8'), encoding='utf-8')
        
        # Read optimized resume
        print(f"📄 Reading optimized resume: {optimized_resume_path}")
        optimized_content = optimized_resume_path.read_text(encoding='utf-8')
        
        # Replace baseline with optimized version
        print(f"✨ Promoting optimized resume to baseline: {baseline_resume}")
        baseline_resume.write_text(optimized_content, encoding='utf-8')
        
        # Update changelog
        date_str = datetime.now().strftime("%Y-%m-%d")
        reason_text = f"\n**Reason:** {reason}" if reason else ""
        
        changelog_entry = f"""
## {date_str} - Promoted Optimized Resume to Baseline

**Source:** {optimized_resume_path.name}
**Backup:** {backup_file.name}{reason_text}

The optimized resume has been promoted to be the new baseline resume.
All future optimizations will be based on this version.

---
"""
        
        if changelog_file.exists():
            current_content = changelog_file.read_text(encoding='utf-8')
        else:
            current_content = "# Resume Optimization Changelog\n\n"
        
        changelog_file.write_text(current_content + changelog_entry, encoding='utf-8')
        print(f"✓ Updated changelog: {changelog_file}")
        
        # Regenerate all baseline outputs
        print("\n🔄 Regenerating baseline outputs...")
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
        
        print("\n✅ Promotion complete!")
        print(f"   Baseline resume: {baseline_resume}")
        print(f"   Backup saved: {backup_file}")
        
    except Exception as e:
        # Restore backup if something went wrong
        if backup_file.exists() and baseline_resume.exists():
            print(f"\n⚠️  Error occurred, restoring backup...", file=sys.stderr)
            baseline_resume.write_text(backup_file.read_text(encoding='utf-8'), encoding='utf-8')
        raise

def main():
    parser = argparse.ArgumentParser(
        description='Promote an optimized resume to be the new baseline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Promote with a reason
  python scripts/promote_to_baseline.py build/optimized/resume_optimized_20250128_120000.md --reason "Incorporated Google feedback"
  
  # Promote without reason
  python scripts/promote_to_baseline.py build/optimized/resume_optimized_20250128_120000.md
        """
    )
    parser.add_argument('optimized_resume', help='Path to optimized resume markdown file')
    parser.add_argument('--reason', '-r', help='Reason for promotion (for changelog)', default=None)
    
    args = parser.parse_args()
    
    try:
        promote_to_baseline(args.optimized_resume, args.reason)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
