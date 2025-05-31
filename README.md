# Garibaldi Wine List – Auto HTML Generator

This repository automatically generates an elegant wine list (HTML) from the shared Google Sheet.

## ✅ Workflow Summary
- Python script: `generate_html.py`
- Trigger: Manual or scheduled GitHub Action
- Source: [Google Sheet - Sommelier_Selection_Garibaldi_Optimized](https://docs.google.com/spreadsheets/d/1Wg0mpJLpSKohr9nTUY8RfHR9DF05PYKC5Wp63R2ECsw)
- Output: `index.html`

## 🔐 Secrets
- `GOOGLE_CREDENTIALS_JSON` must be configured in GitHub Secrets

## 🚀 To Update the Wine List
1. Update the Google Sheet
2. Run the GitHub Action "Generate HTML from Google Sheet"

## 🧹 Optional Cleanup
You can delete the `.xlsx` and unused assets from the repo.

---

Maintained by: **Antonio Valentini**
