import os, hashlib
from typing import List, Dict, Any
from google.cloud import firestore
from ..common.schemas import Task

PROJECT_ID = os.getenv("GCP_PROJECT")
_db = firestore.Client(project=PROJECT_ID)

def _task_hash(t: Task) -> str:
    key = (t.title.lower() + "|" + (t.due_date.isoformat() if t.due_date else ""))
    return hashlib.sha256(key.encode()).hexdigest()

def save_tasks(patient_id: str, tasks: List[Task]) -> Dict[str, Any]:
    if not tasks: return {"saved": 0, "ids": []}
    batch = _db.batch()
    ids = []
    for t in tasks:
        if t.confidence < 0.7:  # gate low-confidence
            continue
        hid = _task_hash(t)
        doc_ref = _db.collection("patients").document(patient_id)\
                     .collection("tasks").document(hid)
        batch.set(doc_ref, {
            "title": t.title, "due_date": t.due_date.isoformat() if t.due_date else None,
            "source": t.source, "confidence": t.confidence
        }, merge=True)
        ids.append(hid)
    batch.commit()
    return {"saved": len(ids), "ids": ids}

def get_prior_metrics(patient_id: str) -> Dict[str, Any]:
    doc = _db.collection("patients").document(patient_id).collection("profile").document("metrics").get()
    return doc.to_dict() if doc.exists else {}

def save_report(patient_id: str, md: str, url: str) -> str:
    doc_ref = _db.collection("patients").document(patient_id)\
                 .collection("reports").document()
    doc_ref.set({"markdown": md, "pdf_url": url})
    return doc_ref.id
