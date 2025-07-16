#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies required by PyMuPDF (fitz) and Pytesseract
apt-get update && apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev

# Install Python dependencies
pip install -r requirements.txt