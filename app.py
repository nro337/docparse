"""Flask web application for managing academic papers."""

from flask import Flask, jsonify, render_template, request

from src.paper_manager import PaperManager

app = Flask(__name__)
paper_manager = PaperManager()


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/api/papers", methods=["GET"])
def get_papers():
    """Get all papers."""
    return jsonify(paper_manager.get_all_papers())


@app.route("/api/papers", methods=["POST"])
def add_paper():
    """Add a new paper by URL."""
    data = request.json
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        paper = paper_manager.add_paper(url)
        return jsonify(paper), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/papers/<int:paper_id>", methods=["DELETE"])
def delete_paper(paper_id):
    """Delete a paper by ID."""
    if paper_manager.remove_paper(paper_id):
        return jsonify({"success": True})
    return jsonify({"error": "Paper not found"}), 404


@app.route("/api/export", methods=["POST"])
def export_papers():
    """Export all papers to markdown."""
    try:
        filename = paper_manager.export_to_markdown()
        return jsonify({"success": True, "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
