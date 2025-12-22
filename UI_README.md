# Paper Abstract Manager - Web UI

This is a simple web application for managing academic papers. You can add paper URLs, extract titles and abstracts, and export them to markdown files for review.

## Features

- 🔗 Add papers by pasting URLs (supports arXiv, Nature, and other academic sources)
- 📝 Automatically extracts titles and abstracts
- 💾 Persists paper collection across sessions
- 📤 Export all papers to a markdown file
- 🗑️ Remove papers you're not interested in
- 🎨 Clean, modern UI

## Setup

1. Install dependencies:
```bash
uv sync
```

## Running the Application

1. Start the Flask server:
```bash
uv run python app.py
```

   This command starts the Flask server in **debug mode**, which is intended for local development only. Do **not** use this mode in production; for a production deployment, run the app with debug disabled and behind a production-ready WSGI server.
2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Add a Paper**: Paste a paper URL in the input field and click "Add Paper" or press Enter
   - Examples:
     - `https://arxiv.org/pdf/2408.09869`
     - `https://www.nature.com/articles/s41746-025-02022-1`

2. **View Papers**: All added papers will appear in the list below with their title and abstract

3. **Remove Papers**: Click the "Remove" button on any paper you want to delete

4. **Export to Markdown**: Click "Export All to Markdown" to create a markdown file with all papers
   - The file will be created in the project root with a timestamp
   - Format: `papers_export_YYYYMMDD_HHMMSS.md`

## Data Storage

- Papers are stored in `papers_data.json` in the project root
- The data persists between sessions
- You can manually edit or backup this file if needed

## Project Structure

```
docparse/
├── app.py                      # Flask web application
├── src/
│   ├── abstract_extractor.py  # Abstract extraction logic
│   └── paper_manager.py        # Paper management and storage
├── templates/
│   └── index.html             # Web UI
├── papers_data.json           # Persistent storage (created on first run)
└── papers_export_*.md         # Exported markdown files
```

## Supported Paper Sources

The application uses the Docling library which supports:
- arXiv papers
- Nature articles
- Many other academic publishers
- Direct PDF links

If a source doesn't work, check that the URL points to a valid document that Docling can process.
