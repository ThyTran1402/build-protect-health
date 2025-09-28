import os, io
from typing import Optional
from google.cloud import storage
import markdown as md

BUCKET = os.getenv("BUCKET")
_storage = storage.Client()

def render_pdf_from_markdown(markdown_text: str, object_name: str) -> str:
    # Simple HTML export (swap with real PDF renderer in prod)
    html = md.markdown(markdown_text, extensions=["tables", "fenced_code"])
    html_bytes = html.encode("utf-8")

    bucket = _storage.bucket(BUCKET)
    blob = bucket.blob(object_name)
    blob.upload_from_file(io.BytesIO(html_bytes), content_type="text/html")
    blob.make_public()  # for demo; use signed URLs in prod
    return blob.public_url
