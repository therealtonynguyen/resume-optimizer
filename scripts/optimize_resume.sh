#!/bin/bash
# Optimize resume for a specific job posting
#
# Usage:
#   ./scripts/optimize_resume.sh <job_description_url> [--company COMPANY] [--verbose]
#
# Options:
#   --company, -c    Company name (for file naming)
#   --verbose, -v    Show detailed error information when errors occur
#
# API Key Configuration:
#   Set your OpenAI API key in config/secrets.yaml:
#   1. Copy the example: cp config/secrets.yaml.example config/secrets.yaml
#   2. Edit config/secrets.yaml and add your API key

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <job_description_url> [--company COMPANY]"
    exit 1
fi

JOB_URL="$1"
shift  # Remove first argument

# Check for API key (script will check config files and env var)
# The Python script will provide a helpful error message if key is missing

# Run the Python script with remaining arguments
python3 "$(dirname "$0")/optimize_resume.py" "$JOB_URL" "$@"
